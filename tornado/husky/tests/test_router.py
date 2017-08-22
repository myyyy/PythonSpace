import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys
sys.path.append("..")
from husky import route
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

@route('/')
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
