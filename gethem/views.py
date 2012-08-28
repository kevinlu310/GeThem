from __future__ import with_statement
from flask import Flask
from flask import g
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import redirect
from flask import abort
from flask import flash
from flask import send_from_directory
from flask import Blueprint
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from werkzeug import secure_filename
from contextlib import closing
from database import Connection
from hashlib import md5
from datetime import datetime
from gethem import app
from gethem import ALLOWED_EXTENSIONS
import time
import os
import config

# connect database
def connect_db():
	return Connection(config.DB_HOST,
					  config.DB_NAME,
					  config.DB_USER,
					  config.DB_PASSWD)

def get_user_id(username):
	rv = g.db.get('select * from user where username = %s',
				   username)
	return rv.id if rv else None

def format_datetime(timestamp):
	"""Format a timestamp for display."""
	return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.before_request
def before_request():
	g.db = connect_db()
	g.user = None
	if 'user_id' in session:
		g.user = g.db.get('select * from user where user_id = %s',
						 session['user_id'])

@app.after_request
def close_connection(response):
	if hasattr(g, 'db'):
		g.db.close()
	return response

#Show uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Upload file
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
	  <p><input type=file name=file>
		 <input type=submit value=Upload>
	</form>
	'''
	
@app.route('/')
def home():
	"""Displays home"""
	profile_user = g.user
	if g.user:
		needs=g.db.iter('''select need.*, user.* from need, user where
					user.user_id = need.need_author_id and user.user_id = %s
					order by need.need_pub_date''',
					profile_user['user_id'])
		provides=g.db.iter('''select provide.*, user.* from provide, user where
					user.user_id = provide.provide_author_id and user.user_id = %s
					order by provide.provide_pub_date''',
					profile_user['user_id'])
	
		return render_template('home.html', needs=needs, provides=provides)
	else:
		return redirect(url_for('login'))

@app.route('/all')
def public_home():
	"""Displays needs and provides of all users."""
	needs=g.db.iter('''select need.*, user.* from need, user
					where need.need_author_id = user.user_id
					order by need.need_pub_date''')
	provides=g.db.iter('''select provide.*, user.* from provide, user
					where provide.provide_author_id = user.user_id
					order by provide.provide_pub_date''')
	return render_template('home.html', needs=needs, provides=provides)

@app.route('/need/<needid>')
def need_view(needid):
	#need view
	need=g.db.get('select need.*,user.* from need,user where user.user_id=need.need_author_id and need.need_id=%s',needid)
	if need is None:
		abort(404)
	return render_template('needview.html',need=need)

@app.route('/provide/<provideid>')
def provide_view(provideid):
	#provide view
	provide=g.db.get('select provide.*,user.* from provide,user where user.user_id=provide.provide_author_id and provide.provide_id=%s',provideid)
	if provide is None:
		abort(404)
	return render_template('provideview.html',provide=provide)

@app.route('/<username>')
def user_home(username):
	"""Displays a user's needs and provides."""
	profile_user = g.db.get('select * from user where username = %s',
							username)
	if profile_user is None:
		abort(404)
	followed = False
	if g.user:
		followed = g.db.get('''select * from follower where
			follower.who_id = %s and follower.whom_id = %s''',
			session['user_id'], profile_user['user_id']) \
			is not None
		needs=g.db.iter('''select need.*, user.* from need, user where
			user.user_id = need.need_author_id and user.user_id = %s
			order by need.need_pub_date''',
			profile_user['user_id'])
		provides=g.db.iter('''select provide.*, user.* from provide, user where
			user.user_id = provide.provide_author_id and user.user_id = %s
			order by provide.provide_pub_date''',
			profile_user['user_id'])
	
	return render_template('home.html', needs=needs, provides=provides,
						   followed=followed, profile_user=profile_user)

@app.route('/<username>/follow')
def follow_user(username):
	"""Adds the current user as follower of the given user."""
	if not g.user:
		abort(401)
	whom_id = get_user_id(username)
	if whom_id is None:
		abort(404)
	g.db.execute('insert into follower (who_id, whom_id) values(%s, %s)',
				 session['user_id'], whom_id)
	flash('You are now following "%s"' % username)
	return render_template('ineed.html')

@app.route('/<username>/unfollow')
def unfollow_user(username):
	"""Removes the current user as follower of the given user."""
	if not g.user:
		abort(401)
	whom_id = get_user_id(username)
	if whom_id is None:
		abort(404)
	g.db.execute('delete from follower where who_id=%s and whom_id=%s',
				 session['user_id'], whom_id)
	flash('You are no longer following "%s"' % username)
	return render_template('ineed.html')

@app.route('/<username>/like')
def like_post(username):
	return render_template('ineed.html')

@app.route('/<username>/unlike')
def unlike_post(username):
	return render_template('ineed.html')

@app.route('/ineed')
def ineed():
	"""Displays a user's needs and matching provides."""
	profile_user = g.user
	if profile_user is None:
		abort(404)
	if g.user:
		needs=g.db.iter('''select need.*, user.* from need, user where
			user.user_id = need.need_author_id and user.user_id = %s
			order by need.need_pub_date''',
			profile_user['user_id'])
	
	return render_template('ineed.html', needs=needs)

@app.route('/iprovide')
def iprovide():
	"""Displays a user's needs and matching provides."""
	profile_user = g.user
	if profile_user is None:
		abort(404)
	if g.user:
		provides=g.db.iter('''select provide.*, user.* from provide, user where
			user.user_id = provide.provide_author_id and user.user_id = %s
			order by provide.provide_pub_date''',
			profile_user['user_id'])

	return render_template('iprovide.html', provides=provides)

@app.route('/add_need', methods=['POST'])
def add_need():
	"""Registers a new need post for the user."""
	if 'user_id' not in session:
		abort(401)
	if request.form['need_title']:
		g.db.execute('''insert into need (need_author_id, need_title, need_content, need_pub_date)
			values (%s, %s, %s, %s)''', session['user_id'], request.form['need_title'], request.form['need_content'],
			  int(time.time()))
		flash('Your need was posted.')
	return render_template('ineed.html')

@app.route('/add_provide', methods=['POST'])
def add_provide():
	"""Registers a new provide post for the user."""
	if 'user_id' not in session:
		abort(401)
	if request.form['provide_title']:
		g.db.execute('''insert into provide (provide_author_id, provide_title, provide_content, provide_pub_date)
			values (%s, %s, %s, %s)''', session['user_id'], request.form['provide_title'], request.form['provide_content'],
			  int(time.time()))
		flash('Your provide was posted.')
	return render_template('iprovide.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		######## for testing
		flash(g.user.username)	
		return redirect(url_for('home'))
	error = None
	if request.method== 'POST':
		user = g.db.get('''select * from user where
			username = %s''', request.form['username'])
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user['pw_hash'],
									 request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = user['user_id']
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Register a user."""
	if g.user:
		return redirect(url_for('ineed'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['email'] or \
				 '@' not in request.form['email']:
			error = 'You have to enter a valid email address'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			g.db.execute('''insert into user ( \
				username, email, pw_hash) values(%s, %s, %s)''', \
				request.form['username'], request.form['email'], \
				generate_password_hash(request.form['password']))
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)

@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out.')
	session.pop('user_id', None)
	return redirect(url_for('login'))

# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime

#if __name__ == '__main__':
#	app.debug = True
#	app.run(host='127.0.0.1')
