from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler
from tornado.web import RequestHandler
from tornado.web import Application
from gethem import app

tr = WSGIContainer(app)
print app

application = Application([
  (r".*", FallbackHandler, dict(fallback=tr)),
  ])

if __name__ == "__main__":
  application.listen(8000)
  IOLoop.instance().start()
