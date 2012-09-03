from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler
from tornado.web import RequestHandler
from tornado.web import Application
import gethem

m = WSGIContainer(gethem.app)

application_main = Application([
	(r".*", FallbackHandler, {'fallback':m})
  ])

if __name__ == "__main__":
	application_main.listen(8000)
	IOLoop.instance().start()
