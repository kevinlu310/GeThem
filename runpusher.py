from __future__ import with_statement
from flask import Response
from flask import Flask
from flask import g
from redis import StrictRedis
import json
import time

app = Flask(__name__)
red = StrictRedis()

#@app.before_request
#def before_request():
#	g.red = StrictRedis()
#	g.pubsub = g.red.pubsub()

#@app.after_request
#def close_connection(response):
#	if hasattr(g, 'red'):
#		g.red = None
#	if hasattr(g, 'pubsub'):
#		g.pubsub = None
#	return response

def event_notification():
#	if not g.pubsub:
#		abort(404)
#	g.pubsub.subscribe('notification')
	ps = red.pubsub()
	ps.subscribe('notification')
	for msg in ps.listen():
		print 'data: %s\n\n' % msg['data']
		yield 'data: %s\n\n' % msg['data']
		time.sleep(3)

@app.route('/notification', methods=['GET', 'POST'])
def notification():
	print "reach here!"
	return Response(event_notification(), mimetype='text/event-stream')

if __name__ == '__main__':
	app.debug = True
	#app.threaded = True
	app.run()
