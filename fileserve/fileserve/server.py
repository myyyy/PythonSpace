# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""
import tornado.ioloop
import tornado.web
import json
from pymongo import MongoClient
import gridfs
import os
import logging


import tornado.options
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r"/", IndexHandler),
            (r"\/*.*", IndexHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass
class IndexHandler(BaseHandler):
    def get(self):
        # import pdb;pdb.set_trace()
        uri =self.request.uri 
        path = os.getcwd()
        file_path = path+uri
        if os.path.isfile(file_path):
            file_name = uri.split('/')[-1]
            self.set_header ('Content-Type', 'application/octet-stream')
            self.set_header ('Content-Disposition', 'attachment; filename{}'.format(file_name))

            with open(file_path, 'rb') as f:
                data = f.read()
                self.write(data)

        if os.path.isdir(file_path):

            files = [item for item in os.listdir(file_path)]
            print files
            self.render('index.html',files=files)
    def post(self):
        # TODO 上传文件
        pass




class ErrorHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.redirect('/')


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info('Serving HTTP on 0.0.0.0 port %d ...' % options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()


