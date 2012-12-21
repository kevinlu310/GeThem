'''
The SockJS based push notification system.
The message exchange pool is redis pub/sub channel.

The push server URL is: http://www.gethem.com:5000/notification

In case of multi-user issue, tornado server is required for
the deployment.
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
		#TODO: more work needs to be done here.
		# filter user channels.
		for c in cls.clients:
			c.send(msg.body)
			print msg.body



if __name__ == "__main__":
	red = tornadoredis.Client()
	red.connect()
	red.subscribe('notification', lambda s: red.listen(NotificationConnection.pubsub))
	NotificationRouter = SockJSRouter(NotificationConnection, '/notification')
	app_notification = Application(NotificationRouter.urls)
	app_notification.listen(5000)
	IOLoop.instance().start()


