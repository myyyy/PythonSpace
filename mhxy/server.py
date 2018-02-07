#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import json
from pymongo import MongoClient
import gridfs
import os
import logging
import sqlite3
import tornado.options
from tornado.options import define, options
from supickle import pickledb

import file_util as fu

define("port", default=8999, help="run on the given port", type=int)



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
        self.db = pickledb('json.db', True) 

class BaseHandler(tornado.web.RequestHandler):
    def db(self):
        return self.application.db
class IndexHandler(BaseHandler):
    def get(self):
        db = pickledb('json.db', True)
        data = db.get('travel')
        self.render('index.html',data=data)
    def post(self):
        # TODO 上传文件
        quhao = self.get_argument('quhao')
        email = self.get_argument('email')
        toquhao = self.get_argument('toquhao')
        db = pickledb('json.db', True)
        if not db.lgetall('send'):
            db.lcreate('send')
            db.ladd('send',(quhao,toquhao,email))
        else:
            db.ladd('send',(quhao,toquhao,email))
        self.write(dict(status=True,msg='添加成功'))

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


