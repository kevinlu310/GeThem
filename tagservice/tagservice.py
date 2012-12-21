'''
The tag service system.

The service is built on Flask as an independent service,
rather than bundle to the main app service. Becuase more
work will be added to the tag service and its potential
integration with the core background match engine.

The tag service URL is: http://www.gethem.com:8001/tags/<tag>
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
import tagservice

if __name__ == "__main__":
	# app server.
	m = WSGIContainer(gethem.app)
	app_main = Application([(r".*", FallbackHandler, {'fallback':m})])
	app_main.listen(8001)
	IOLoop.instance().start()
	

