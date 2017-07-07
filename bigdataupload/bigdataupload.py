#!/usr/bin/env python

"""Usage: python file_receiver.py
Demonstrates a server that receives a multipart-form-encoded set of files in an
HTTP POST, or streams in the raw data of a single file in an HTTP PUT.
See file_uploader.py in this directory for code that uploads files in this format.
"""

import logging

try:
    from urllib.parse import unquote
except ImportError:
    # Python 2.
    from urllib import unquote

import tornado.ioloop
import tornado.web
from tornado import options
MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB
MAX_STREAMED_SIZE = 1000*MB

class POSTHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write(dict(hello='helloword'))
    def post(self):
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info['filename'], info['content_type']
                body = info['body']
                logging.info('POST "%s" "%s" %d bytes',
                             filename, content_type, len(body))

        self.write('OK')


@tornado.web.stream_request_body
class PUTHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)
    def initialize(self):
        self.bytes_read = 0
        self.body = ""

    def data_received(self, chunk):
        # print chunk
        # self.body += chunk
        self.bytes_read += len(chunk)
        # import pdb;pdb.set_trace()
        print self.bytes_read

    def post(self, filename):
        filename = unquote(filename)
        mtype = self.request.headers.get('Content-Type')
        # import pdb;pdb.set_trace()
        print '############', filename, mtype, self.bytes_read, len(self.body)
        self.write('OK')


def make_app():
    return tornado.web.Application([
        (r"/post", POSTHandler),
        (r"/(.*)", PUTHandler),
    ])


if __name__ == "__main__":
    # Tornado configures logging.
    options.parse_command_line()
    app = make_app()
    app.listen(1994)
    tornado.ioloop.IOLoop.current().start()