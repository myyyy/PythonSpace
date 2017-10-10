# -*- coding:utf-8 -*-
"""
    passport action
"""
import base64, time
from kpages import url, service_async, get_context, service_async, ContextHandler
from logic import passport
from bson import ObjectId
from tornado.web import RequestHandler
import uuid

import tornado.web
import hashlib
from bson import ObjectId
from mongo_util import MongoIns
import oauth2 as oauth

EXPIRES_IN = 86400


class BaseHandler(tornado.web.RequestHandler):
    def verfiy_token(self):
        oauth_request = oauth.Request.from_request('GET',self.request.uri)
        access_token = oauth_request.parameters.get('access_token')
        access_token = oauth.RsaEncryption().decrypt(refresh_str)
        owner = refresh_token.split(',')[0]
        pwd = refresh_token.split(',')[-1]
        user = MongoIns().m_find_one('passport', dbname='cas', _id = ObjectId(owner))
        if pwd == user.get('pwd'):
            return True,owner,'access_token验证通过'
        else:
            return False,None,'access_token验证失败'



@url(r"/oauth2/appinfo")
class AppInfoHandler(BaseHandler):
    """
    获取该应用的
    :APPID
    :APPSECRET
    """
    def get(self):
        self.render('oauth2/regapp.html')

    def post(self):
        url = self.get_argument('url')
        client_id=ObjectId()
        secret = oauth.RsaEncryption().encrypt(str(client_id))
        import pdb;pdb.set_trace()
        MongoIns().m_insert("oauth2_app", **{'url':url,'_id':client_id,'secret':secret})

        self.write(dict(client_id=str(client_id),secret=secret))

@url(r"/oauth2/auth")
class RequestTokenHandler(BaseHandler):
    def get(self):
        # code 753ff4c4c3f779f08ee12ef905e5887c7565e1362047f7e7eb3767215f3aa96aaaeaf1c59779db8c79f3789b595e9b068a3c251a5f3a661c80b4bad496579d0685d28fb2a5a1aeea70218cc3032302559cc9e3b41c8e4d05af807728bd99eaf019cacc68e5ec214ba4995f978c895eca163e6c0761b2eb5514278b0af80e873d
        # http://127.0.0.1:8887/oauth2/auth?client_id=59dc294535f9a85e465d75b1&redirect_uri=http://baidu.com&response_type=code&state=sina7d3521db1a403d39cee2815ff42289ce
        uri = self.request.uri
        oauth_request = oauth.Request.from_request('GET',self.request.uri)
        self.render('oauth2/index.html',uri = uri,oauth_request=oauth_request)
    def post(self):
        username = self.get_argument('name')
        pwd = self.get_argument('pwd')
        oauth_request = oauth.Request.from_request('GET',self.request.uri)
        user = MongoIns().m_find_one('passport', dbname='cas', username = username)
        redirect_uri = oauth_request.parameters.get('redirect_uri')
        client_id = oauth_request.parameters.get('client_id')
        app = MongoIns().m_find_one("oauth2_app", dbname='cas',url=redirect_uri)
        if hashlib.md5(pwd).hexdigest() == user.get('pwd') and app:
            code = oauth.Code().set(client_id,user.get('_id'))
            oauth_request = oauth.Request.from_request('GET',self.request.uri)
            redirect_uri= redirect_uri+'?code=' +code+'&state='+oauth_request.parameters.get('state','')
            self.redirect(redirect_uri)
            return
        else:
            self.write(dict(status=False,msg='用户授权失败，请检查用户名(密码)'))

@url(r"/oauth2/access_token")
class AccessTokenHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.Request.from_request('GET',self.request.uri)
        # 验证appid＆secret
        # http://127.0.0.1:8887/oauth2/access_token?client_id=59dc294535f9a85e465d75b1&secret=926e1cc30543aa8c78a16fa74e5119ccb0f135ed9f2ac891ab7e5fff0adafe6ce2e8e279c325f25ecafbda50740b0e88b402667dce2e865ef456286b2f0ff6e1c5d96d9b25fdd0638d82ed47ab89cf043d182af294ca018499206acc61e109dea66e2565b6a0c4af322e57d6eb6032a080ef4bd3e50072faa78063a666cc4e05&code=1df913dac4a47da3488f1211805af23cfa8f0611565ea88761827409c5036d3dd0abcd28de4c33872792a893e81b63c05a4d2666a326203d1fa86386a182ba42a59fec14b537e1a85ef084e4675d71a89504eec6d03a038000df3e0a1712535d3f3d48227fcf87cb4dbca5fea7eaf80b3873a316546bb26220fdde53ca2149d5&state=sina7d3521db1a403d39cee2815ff42289ce
        client_id = oauth_request.parameters.get('client_id')
        secret = oauth_request.parameters.get('secret')
        app = MongoIns().m_find_one('oauth2_app', dbname='cas', _id = ObjectId(client_id))
        if app.get('secret') == secret:
            code = oauth_request.parameters.get('code')
            owner = oauth.Code().get(code)
            user = MongoIns().m_find_one('passport', dbname='cas', _id = ObjectId(owner))
            access_str = owner + ',' + user.get('pwd')
            access_token = oauth.RsaEncryption().encrypt(access_str)
            refresh_str = owner + ',' + str(EXPIRES_IN)
            refresh_token = oauth.RsaEncryption().encrypt(refresh_str)

            MongoIns().m_insert('oauth2_user', dbname='cas', owner = owner,EXPIRES_IN=EXPIRES_IN,start=time.time())
            self.write(dict(status=True,access_token=access_token,refresh_token=refresh_token,expires_in=EXPIRES_IN))
        else:
            self.write(dict(status=False,msg='app验证失败'))

@url(r"/oauth2/refresh")
class RefreshTokenHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.Request.from_request('GET',self.request.uri)
        refresh_token = oauth_request.parameters.get('refresh_token')
        refresh_token = oauth.RsaEncryption().decrypt(refresh_str)
        owner = refresh_token.split(',')[0]
        user = MongoIns().m_update('oauth2_user',{'owner':owner}, dbname='cas', start = time.time())
        self.wfile(dict(status=True,msg='access_token刷新成功'))


@url(r"/oauth2/get_token_info")
class GetTokenInfoHandler(BaseHandler):
    def get(self):
        status,owner,msg = self.verfiy_token()
        ouser = MongoIns().m_find_one('oauth2_user', dbname='cas', owner = owner)
        self.wfile(dict(status=True,ouser=ouser))

@url(r"/oauth2/reoauth")
class Reoauth(BaseHandler):
    def get(self):
        oauth_request = oauth.Request.from_request('GET',self.request.uri)
        access_token = oauth_request.parameters.get('access_token')
        access_token = oauth.RsaEncryption().decrypt(refresh_str)
        owner = refresh_token.split(',')[0]
        user = MongoIns().m_del('oauth2_user', owner = owner,dbname='cas')
        self.wfile(dict(status=True,msg='取消授权成功'))

#权限列表todo
@url(r"/oauth2/resource")
class ResourceHandler(BaseHandler):
    def get(self):
        status,owner,msg = self.verfiy_token()

