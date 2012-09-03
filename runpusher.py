from __future__ import with_statement
from flask import Response
from flask import Flask
from redis import StrictRedis
from gethem import red
import time

app = Flask(__name__)

def event_push():
	pubsub = red.pubsub()
	pubsub.subscribe('push')
	print pubsub.channels
	for msg in pubsub.listen():
		print msg
		yield 'data: %s\n\n' % msg['data']

@app.route('/push')
def push():
	print "reach here!"
	return Response(event_push(), mimetype='text/event-stream')

if __name__ == '__main__':
	app.debug = True
	app.threaded = True
	app.run(host='localhost', port=8001)
