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

import tornado.options
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/gfsmedia", GetGfsMedia),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class IndexHandler(BaseHandler):
    def get(self):
        data={"results":[{"gender":"female","name":{"title":"miss","first":"inmaculada","last":"herrero"},"location":{"street":"7936 calle de la democracia","city":"vigo","state":"comunidad valenciana","postcode":89386},"email":"inmaculada.herrero@example.com","login":{"username":"beautifulmouse810","password":"steven","salt":"o7gnbpWG","md5":"be12c9ae1ffa2c4546d87d871ac56575","sha1":"0ff587f11d86ed376c3f19cab4b987519ff99bbb","sha256":"adf4f1c7e619a7a08da6ca593913c000f67df296f0d82d98d58a7bcaf0203bd7"},"dob":"1969-05-11 20:21:33","registered":"2013-05-19 09:38:20","phone":"901-869-091","cell":"666-950-554","id":{"name":"DNI","value":"31648111-I"},"picture":{"large":"https://randomuser.me/api/portraits/women/76.jpg","medium":"https://randomuser.me/api/portraits/med/women/76.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/76.jpg"},"nat":"ES"}],"info":{"seed":"4258edb756a16134","results":1,"page":1,"version":"1.1"}}
        self.write(json.dumps(data))
        self.render('index.html')

class GetGfsMedia(BaseHandler):
    def get(self):
        my_db = MongoClient().test
        fs = gridfs.GridFSBucket(my_db)
        grid_out = fs.open_download_stream_by_name("FNSHX104.mp4")
        contents = grid_out.read()
        print contents
        import pdb;pdb.set_trace()
        self.set_header("Content-Type", grid_out.content_type )
        self.write(contents)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()


