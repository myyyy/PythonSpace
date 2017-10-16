# -*- coding:utf-8 -*-

from bson import ObjectId
import tornado.web
from kpages import url, get_members
from mongo_util import MongoIns
import oauth2 as oauth

#Oauth权限BaseHandler
class OauthRoleHandler(tornado.web.RequestHandler):
    access = property(lambda self: self.get_access())
    token = property(lambda self: self.get_argument('token', None))
    owner = property(lambda self: self.get_owner())
    payload = property(lambda self: self.get_payload())
    header = property(lambda self: self.get_header())

    def get_payload(self):
        payload,header= oauth.AppToken().serialization(self.token)
        return payload
    def get_header(self):
        atpayload,header= oauth.AppToken().serialization(self.token)
        return header
    def get_owner(self):
        return self.payload.get('owner')

    def get_access(self):
        app = MongoIns().m_find_one("oauth2_app", dbname='cas',dbhost = __conf__.CAS_DB_HOST,_id=ObjectId(self.payload.get('client_id','')))
        return app.get('access','')

    def prepare(self):
        urlname = '{0}.{1}'.format(self.__module__, self.__class__.__name__)
        import pdb;pdb.set_trace()
        if urlname not in self.access:
            self.send_error(403)

def oauth2restful(**kwargs):
    def wrapper(handler):
        handler.__oauth2restful__ = kwargs
        return handler

    return wrapper

def get_handlers():
    member_filter = lambda m: isinstance(m, type) and hasattr(m, '__oauth2restful__')
    return get_members('oauth2', member_filter)

@oauth2restful()
@url(r"/oauth2/resource")
class ResourceHandler(OauthRoleHandler):
    def get(self):
        pass