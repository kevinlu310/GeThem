'''
	Both app instance and pusher instance are
	handled under this script.
'''


from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler
from tornado.web import RequestHandler
from tornado.web import Application
from sockjs.tornado import SockJSConnection
from sockjs.tornado import SockJSRouter
import tornadoredis
import argparse
import sys
import gethem

class NotificationConnection(SockJSConnection):
	clients = set()

	def on_open(self, info):
		self.clients.add(self)
	
	def on_message(self, message):
		pass
	
	def on_close(self):
		self.clients.remove(self)
	
	@classmethod
	def pubsub(cls, msg):
		for c in cls.clients:
			c.send(msg.body)
			print msg.body



if __name__ == "__main__":
	
	tp = None
	for arg in sys.argv:
		if arg == 'app': tp = 'app'
		if arg == 'pusher': tp = 'pusher'
	
	if tp == 'app':
		# app server.
		m = WSGIContainer(gethem.app)
		app_main = Application([(r".*", FallbackHandler, {'fallback':m})])
		app_main.listen(8000)
		IOLoop.instance().start()
	
	else:
	# notification server.
		red = tornadoredis.Client()
		red.connect()
		red.subscribe('notification', lambda s: red.listen(NotificationConnection.pubsub))
		NotificationRouter = SockJSRouter(NotificationConnection, '/notification')
		app_notification = Application(NotificationRouter.urls)
		app_notification.listen(5000)
		IOLoop.instance().start()


