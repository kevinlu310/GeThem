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
from flask import send_file
from flask import Blueprint
from flask import Response
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from werkzeug import secure_filename
from contextlib import closing
from database import Connection
from hashlib import md5
from datetime import datetime
from gethem import app
from gethem import ALLOWED_EXTENSIONS
from gethem import red
from pprint import pprint
import json
import time
import os
import config
import simplejson
import hashlib

# connect database
def connect_db():
	return Connection(config.DB_HOST,
					  config.DB_NAME,
					  config.DB_USER,
					  config.DB_PASSWD)

def get_user_id(username):
	rv = g.db.get('''select * from user where username = %s''', username)
	return rv.id if rv else None

def get_username(user_id):
	rv = g.db.get('''select * from user where user_id = %s''', user_id)
	return rv.username if rv else None

def get_post_id(userid, title, content, mark):
	if mark == 'need':
		rv = g.db.get('''select * from need where need_author_id = %s 
			and need_title = %s and need_content = %s''', userid, title, content)
		return rv.need_id if rv else None
	else:
		rv = g.db.get('''select * from provide where provide_author_id = %s
			and provide_title = %s and provide_content = %s''', userid, title, content)
		return rv.provide_id if rv else None

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
	g.user = None
	return response

@app.route('/images/<image_id>', methods=['GET', 'POST'])
def show_images(image_id):
	if not session['user_id']:
		abort(400)
	ext = image_id.split('.')[1]
	return send_file('../uploads/' + image_id, mimetype='image/'+ext)

@app.route('/')
def index():
	if g.user:
		return redirect(url_for('home', userid=session['user_id']))
	else:
		return redirect(url_for('login'))

@app.route('/u/<userid>')
def home(userid):
	"""Displays home"""
	profile_user = g.db.get('select * from user where user_id = %s',
					userid)
	if profile_user is None:
		abort(404)
	if session['user_id'] == profile_user['user_id']:
		needs_iter = g.db.iter('''select need.*, user.* from need, user where
					user.user_id = need.need_author_id and user.user_id = %s
					order by need.need_pub_date desc limit 1000''', userid)
		needs = []
		for item in needs_iter:
			postid = item['need_id']
			db2 = connect_db()
			img_iter = db2.iter('''select need_img.* from need_img where
			need_img.need_post_id = %s''', postid)
			imgs = []
			for img in img_iter:
				imgs.append(img['uri'])
			if len(imgs) == 0:
				imgs = ['default.png']
			item['images'] = imgs
			needs.append(item)
			
		provides_iter = g.db.iter('''select provide.*, user.* from provide, user where
					user.user_id = provide.provide_author_id and user.user_id = %s
					order by provide.provide_pub_date desc limit 1000''', userid)
		provides = []
		for item in provides_iter:
			postid = item['provide_id']
			db2 = connect_db()
			img_iter = db2.iter('''select provide_img.* from provide_img where
			provide_img.provide_post_id = %s''', postid)
			imgs = []
			for img in img_iter:
				imgs.append(img['uri'])
			if len(imgs) == 0:
				imgs = ['default.png']
			item['images'] = imgs
			provides.append(item)
			
		return render_template('home.html', needs=needs, provides=provides)
	else:
		# TODO bug here, behavior not expected
		return redirect(url_for('login'))

@app.route('/all')
def public():
	"""Displays needs and provides of all users."""
	needs_iter = g.db.iter('''select need.*, user.* from need, user
					where need.need_author_id = user.user_id
					order by need.need_pub_date desc limit 1000''')
	needs = []
	for item in needs_iter:
		postid = item['need_id']
		db2 = connect_db()
		img_iter = db2.iter('''select need_img.* from need_img where
												need_img.need_post_id = %s''', postid)
		imgs = []
		for img in img_iter:
			imgs.append(img['uri'])
		if len(imgs) == 0:
			imgs = ['default.png']
		item['images'] = imgs
		needs.append(item)
	
	provides_iter = g.db.iter('''select provide.*, user.* from provide, user
					where provide.provide_author_id = user.user_id
					order by provide.provide_pub_date desc limit 1000''')
	provides = []
	for item in provides_iter:
		postid = item['provide_id']
		db2 = connect_db()
		img_iter = db2.iter('''select provide_img.* from provide_img where
												provide_img.provide_post_id = %s''', postid)
		imgs = []
		for img in img_iter:
			imgs.append(img['uri'])
		if len(imgs) == 0:
			imgs = ['default.png']
		item['images'] = imgs
		provides.append(item)
	
	return render_template('public.html', needs=needs, provides=provides)

@app.route('/u/<username>/')
def user_page(username):
	"""Displays a user's needs and provides."""
	target_user = g.db.get('select * from user where username = %s',
							username)
	if target_user is None:
		abort(404)
	
	if target_user['user_id'] == session['user_id']:
		return redirect(url_for('home', userid=session['user_id']))
	
	followed = False
	if g.user:
		followed = g.db.get('''select * from follower where
			follower.who_id = %s and follower.whom_id = %s''',
			session['user_id'], target_user['user_id']) is not None
			
		needs_iter = g.db.iter('''select need.*, user.* from need, user where
														user.user_id = need.need_author_id and user.user_id = %s
														order by need.need_pub_date desc limit 1000''',
														target_user['user_id'])
		needs = []
		for item in needs_iter:
			postid = item['need_id']
			db2 = connect_db()
			img_iter = db2.iter('''select need_img.* from need_img where
													need_img.need_post_id = %s''', postid)
			imgs = []
			for img in img_iter:
				imgs.append(img['uri'])
			if len(imgs) == 0:
				imgs = ['default.png']
			item['images'] = imgs
			needs.append(item)
		
		provides_iter = g.db.iter('''select provide.*, user.* from provide, user where
			user.user_id = provide.provide_author_id and user.user_id = %s
			order by provide.provide_pub_date desc limit 1000''',
			target_user['user_id'])
		provides = []
		for item in provides_iter:
			postid = item['provide_id']
			db2 = connect_db()
			img_iter = db2.iter('''select provide_img.* from provide_img where
													provide_img.provide_post_id = %s''', postid)
			imgs = []
			for img in img_iter:
				imgs.append(img['uri'])
			if len(imgs) == 0:
				imgs = ['default.png']
			item['images'] = imgs
			provides.append(item)
		
	return render_template('user_page.html', needs=needs, provides=provides,
						   followed=followed, target_user=target_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('home', userid=session['user_id']))
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
			return redirect(url_for('home', userid=session['user_id']))
	return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Register a user."""
	if g.user:
		return redirect(url_for('home', userid=session['user_id']))
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
	return redirect(url_for('index'))

@app.route('/needs/<needid>')
def need_view(needid):
	#need view
	need=g.db.get('select need.*,user.* from need,user where user.user_id=need.need_author_id and need.need_id=%s',needid)
	if need is None:
		abort(404)
	return render_template('needview.html',need=need)

@app.route('/provides/<provideid>')
def provide_view(provideid):
	#provide view
	provide=g.db.get('select provide.*,user.* from provide,user where user.user_id=provide.provide_author_id and provide.provide_id=%s',provideid)
	if provide is None:
		abort(404)
	return render_template('provideview.html',provide=provide)

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
		my_needs_iter=g.db.iter('''select need.*, user.* from need, user where
			user.user_id = need.need_author_id and user.user_id = %s
			order by need.need_pub_date desc limit 1000''',
			profile_user['user_id'])
		my_needs = []
		for item in my_needs_iter:
			my_needs.append(item)
		
		# TODO: bring matchdb's data here! Currently, only test UI.
		#they_provides = g.db.iter('''select provide.*, user.* from provide, user limit 1000''')
		they_provides_iter=g.db.iter('''select provide.*, user.* from provide, user
						where provide.provide_author_id = user.user_id
						order by provide.provide_pub_date desc limit 1000''')
		they_provides = []
		for item in they_provides_iter:
			if item.user_id == profile_user['user_id']: continue
			postid = item['provide_id']
			db2 = connect_db()
			img_iter = db2.iter('''select provide_img.* from provide_img where
			provide_img.provide_post_id = %s''', postid)
			imgs = []
			for img in img_iter:
				imgs.append(img['uri'])
			if len(imgs) == 0:
				imgs = ['default.png']
			item['images'] = imgs
			they_provides.append(item)
	
	return render_template('ineed.html', needs=my_needs, provides=they_provides)

@app.route('/iprovide')
def iprovide():
	"""Displays a user's needs and matching provides."""
	profile_user = g.user
	if profile_user is None:
		abort(404)
	if g.user:
		my_provides_iter=g.db.iter('''select provide.*, user.* from provide, user where
			user.user_id = provide.provide_author_id and user.user_id = %s
			order by provide.provide_pub_date desc limit 1000''',
			profile_user['user_id'])
		my_provides = []
		for item in my_provides_iter:
			my_provides.append(item)
		
		# TODO: bring matchdb's data here! Currently, only test UI.
		#they_needs = g.db.iter('''select need.*, user.* from need, user limit 1000''')
		they_needs_iter=g.db.iter('''select need.*, user.* from need, user
						where need.need_author_id = user.user_id
						order by need.need_pub_date desc limit 1000''')
		they_needs = []
		for item in they_needs_iter:
			if item.user_id == profile_user['user_id']: continue
			db2 = connect_db()
			img_iter = db2.iter('''select need_img.* from need_img where
			need_img.need_post_id = %s''', item['need_id'])
			imgs = []
			for img in img_iter:
				imgs.append(img['uri'])
			if len(imgs) == 0:
				imgs = ['default.png']
			item['images'] = imgs
			they_needs.append(item)

	return render_template('iprovide.html', provides=my_provides, needs=they_needs)

@app.route('/add_need', methods=['POST'])
def add_need():
	"""Registers a new need post for the user."""
	if 'user_id' not in session:
		abort(401)
	if request.form['need_title']:
		# insert post.
		ts = time.time()
		g.db.execute('''insert into need (need_author_id, need_title, need_content, need_pub_date)
			values (%s, %s, %s, %s)''', session['user_id'], request.form['need_title'], request.form['need_content'],
			  int(ts))
			  
		postid = g.db.get('''select * from need where need_author_id=%s and need_pub_date=%s''',
										session['user_id'], int(ts))['need_id']
		# insert image.
		for f in request.files.getlist('need_imgs'):
			if f and allowed_file(f.filename):
				ext = '.' + f.filename.split('.')[1]
				fname = hashlib.sha224(str(session['user_id']) + str(request.form['need_title']) \
				+ str(request.form['need_content']) + f.filename + str(int(ts))).hexdigest() + ext
				f.save('uploads/'+fname)
				g.db.execute('''insert into need_img (need_post_id, uri) values (%s, %s)''', \
										int(postid), fname)
		
		# pass msg to redis. Later push to clients.
		title = request.form['need_title']
		content = request.form['need_content']
		post = {'type':'need', 
				'user':get_username(session['user_id']), 
				'title':title, 
				'pid':get_post_id(session['user_id'], title, content, 'need'),
				'ts':str(format_datetime(ts))}
		print red.publish('notification', json.dumps(post))
		#print red.publish('notification', u'[Need @ %s] %s, %s' % (ts, title, content))

		if g.user:
			my_needs=g.db.iter('''select need.*, user.* from need, user where
				user.user_id = need.need_author_id and user.user_id = %s
				order by need.need_pub_date desc limit 1000''',	g.user.user_id)
			they_provides = g.db.iter('''select * from provide''')

		flash('Your need was posted.')
	return redirect(url_for('ineed'))

@app.route('/add_provide', methods=['POST'])
def add_provide():
	"""Registers a new provide post for the user."""
	if 'user_id' not in session:
		abort(401)
	if request.form['provide_title']:
		ts = time.time()
		g.db.execute('''insert into provide (provide_author_id, provide_title, provide_content, provide_pub_date)
			values (%s, %s, %s, %s)''', session['user_id'], request.form['provide_title'], request.form['provide_content'],
			  int(ts))

		postid = g.db.get('''select * from provide where provide_author_id=%s and provide_pub_date=%s''',
										session['user_id'], int(ts))['provide_id']	
		# insert image.
		print request.files
		print request.files.getlist('provide_imgs')
		for f in request.files.getlist('provide_imgs'):
			if f and allowed_file(f.filename):
				ext = '.' + f.filename.split('.')[1]
				fname = hashlib.sha224(str(session['user_id']) + str(request.form['provide_title']) \
				+ str(request.form['provide_content']) + f.filename + str(int(ts))).hexdigest() + ext
				f.save('uploads/'+fname)
				g.db.execute('''insert into provide_img (provide_post_id, uri) values (%s, %s)''', \
										int(postid), fname)
										
		# pass msg to redis. Later push to clients.
		title = request.form['provide_title']
		content = request.form['provide_content']
		post = {'type':'provide', 
				'user':get_username(session['user_id']), 
				'title':title, 
				'pid':get_post_id(session['user_id'], title, content, 'provide'),
				'ts':str(format_datetime(ts))}
		print red.publish('notification', json.dumps(post))
		#print red.publish('notification', u'provide,%s,%s,%s,%s' % (ts, title, content))

		if g.user:
			my_provides=g.db.iter('''select provide.*, user.* from provide, user where
				user.user_id = provide.provide_author_id and user.user_id = %s
				order by provide.provide_pub_date desc limit 1000''', g.user.user_id)
			they_needs = g.db.iter('''select * from need''')
			
		flash('Your provide was posted.')

	return redirect(url_for('iprovide'))


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime

#if __name__ == '__main__':
#	app.debug = True
#	app.run(host='127.0.0.1')
