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

if __name__ == "__main__":
	
	# app server.
	m = WSGIContainer(gethem.app)
	app_main = Application([(r".*", FallbackHandler, {'fallback':m})])
	app_main.listen(8000)
	IOLoop.instance().start()
	
