#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import json
from pymongo import MongoClient
import gridfs
import os
import logging

import tornado.options
from tornado.options import define, options
import oauth2 as oauth


define("port", default=8999, help="run on the given port", type=int)

USER={'suyf':'111'}
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r"/", IndexHandler),
            (r"/request_token", RequestTokenHandler),
            (r"/access_token", AccessTokenHandler),
            (r"/authorize", AuthorizeHandler),
            (r"/resource", ResourceHandler),
        ]
        settings = dict(
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass

class RequestTokenHandler(BaseHandler):
    def get(self):
        # https://api.weibo.com/oauth2/authorize?client_id=1473879058&redirect_uri=xxx&response_type=code&state=sina7d3521db1a403d39cee2815ff42289ce
        uri=self.request.uri
        print uri
        import pdb;pdb.set_trace()
        oauth_request = oauth.Request.from_request('GET',uri)
        token = oauth.Token(self.key, self.secret)

        self.render('index.html',token=token)
    def post(self):
        name = self.get_argument('name')
        pwd = self.get_argument('pwd')
        import pdb;pdb.set_trace()
        if USER.get(name) == pwd:
            oauth_request = oauth.Request.from_request('POST',
                self.path, headers=self.headers, query_string=None)
        token = self.oauth_server.fetch_request_token(oauth_request)

class AuthorizeHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.OAuthRequest.from_request('GET',self.path)
        token = self.oauth_server.fetch_request_token(oauth_request)
        self.send_response(200, 'OK')
        self.end_headers()
        # return the token
        self.wfile.write(token.to_string())

class AccessTokenHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.OAuthRequest.from_request('GET',self.path)
        token = self.oauth_server.fetch_request_token(oauth_request)
        self.send_response(200, 'OK')
        self.end_headers()
        # return the token
        self.wfile.write(token.to_string())


class ResourceHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.OAuthRequest.from_request('GET',self.path)
        token = self.oauth_server.fetch_request_token(oauth_request)
        self.send_response(200, 'OK')
        self.end_headers()
        # return the token
        self.wfile.write(token.to_string())


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


