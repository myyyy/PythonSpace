# -*- coding:utf-8 -*-
import tornado
from bson import ObjectId

import tor_access
from tor_access import needcheck, ACL

from kpages import ContextHandler, get_modules, app_path
from mongo_util import MongoIns
from kpages import url

class BaseHandler(ContextHandler, tornado.web.RequestHandler):
    subdomain = property(lambda self: self.get_subdomain())
    admin_id = property(lambda self: self.get_secure_cookie('_ADMIN_ID'))
    user_name = property(lambda self: self.get_secure_cookie('_USER_NAME'))

    def prepare(self):
        if self.request.uri.startswith("/evaluate/exec/api") or self.request.uri.startswith("/evaluate/exec/score/api") or self.request.uri.startswith("/evaluate/exec/alarm"):
            return
        if not self.admin_id:
            template_name = "{0}.html".format(403)
            self.render(template_name)
