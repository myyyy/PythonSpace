# -*- coding:utf-8 -*-
"""
    passport action
"""
import base64, time
from kpages import url, service_async, get_context, service_async, ContextHandler
from bson import ObjectId
from tornado.web import RequestHandler
import uuid

import tornado.web
import hashlib
from bson import ObjectId
from mongo_util import MongoIns
import oauth2 as oauth
from reportapi import get_handlers

EXPIRES_IN = 86400


class BaseHandler(tornado.web.RequestHandler):
    pass


@url(r"/oauth2/appinfo")
class AppInfoHandler(BaseHandler):
    """
    获取该应用的
    :APPID
    :APPSECRET
    """
    def get(self):
        allh = get_handlers()
        self.render('oauth2/regapp.html',allh=allh)

    def post(self):
        url = self.get_argument('url','')
        name = self.get_argument('name','')
        access = self.get_argument('access','')
        description = self.get_argument('description','')
        client_id=ObjectId()
        secret = oauth.RsaEncryption().encrypt(str(client_id))
        MongoIns().m_insert("oauth2_app", dbname='cas',dbhost = __conf__.CAS_DB_HOST,
            **{'url':url,'_id':client_id,'secret':secret,'name':name,'description':description,'access':access})

        self.write(dict(client_id=str(client_id),secret=secret))

@url(r"/oauth2/auth")
class RequestTokenHandler(BaseHandler):
    def get(self):
        # http://127.0.0.1:8887/oauth2/auth?client_id=59dc294535f9a85e465d75b1&redirect_uri=http://baidu.com&response_type=code&state=sina7d3521db1a403d39cee2815ff42289ce
        uri = self.request.uri
        oauth_request = oauth.Request.from_request(self.request.uri)
        self.render('oauth2/index.html',uri = uri,oauth_request=oauth_request)
    def post(self):
        username = self.get_argument('name')
        pwd = self.get_argument('pwd')
        oauth_request = oauth.Request.from_request(self.request.uri)
        user = MongoIns().m_find_one('passport', dbname='cas',dbhost = __conf__.CAS_DB_HOST, username = username)
        redirect_uri = oauth_request.parameters.get('redirect_uri')
        client_id = oauth_request.parameters.get('client_id')
        app = MongoIns().m_find_one("oauth2_app", dbname='cas',dbhost = __conf__.CAS_DB_HOST,url=redirect_uri)
        if hashlib.md5(pwd).hexdigest() == user.get('pwd') and app:
            code = oauth.Code().set(user.get('_id'))
            oauth_request = oauth.Request.from_request('GET',self.request.uri)
            redirect_uri= redirect_uri+'?code=' +code+'&state='+oauth_request.parameters.get('state','')
            self.redirect(redirect_uri)
            return
        else:
            self.write(dict(status=False,msg='用户授权失败，请检查用户名(密码)'))

@url(r"/oauth2/access_token")
class AccessTokenHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.Request.from_request(self.request.uri)
        # 验证appid＆secret
        #http://127.0.0.1:8887/oauth2/app/access_token?client_id=59dc294535f9a85e465d75b1&secret=926e1cc30543aa8c78a16fa74e5119ccb0f135ed9f2ac891ab7e5fff0adafe6ce2e8e279c325f25ecafbda50740b0e88b402667dce2e865ef456286b2f0ff6e1c5d96d9b25fdd0638d82ed47ab89cf043d182af294ca018499206acc61e109dea66e2565b6a0c4af322e57d6eb6032a080ef4bd3e50072faa78063a666cc4e05&code=1df913dac4a47da3488f1211805af23cfa8f0611565ea88761827409c5036d3dd0abcd28de4c33872792a893e81b63c05a4d2666a326203d1fa86386a182ba42a59fec14b537e1a85ef084e4675d71a89504eec6d03a038000df3e0a1712535d3f3d48227fcf87cb4dbca5fea7eaf80b3873a316546bb26220fdde53ca2149d5&state=sina7d3521db1a403d39cee2815ff42289ce
        client_id = oauth_request.parameters.get('client_id')
        secret = oauth_request.parameters.get('secret')
        app = MongoIns().m_find_one('oauth2_app', dbname='cas',dbhost = __conf__.CAS_DB_HOST, _id = ObjectId(client_id))
        if app.get('secret') == secret:
            code = oauth_request.parameters.get('code')
            owner = oauth.Code().get(code)
            user = MongoIns().m_find_one('passport', dbname='cas',dbhost = __conf__.CAS_DB_HOST, _id = ObjectId(owner))
            access_str = owner + ',' + user.get('pwd')
            access_token = oauth.RsaEncryption().encrypt(access_str)
            refresh_str = owner + ',' + str(EXPIRES_IN)
            refresh_token = oauth.RsaEncryption().encrypt(refresh_str)

            MongoIns().m_insert('oauth2_user', dbname='cas',dbhost = __conf__.CAS_DB_HOST,client_id = client_id, owner = owner,EXPIRES_IN=EXPIRES_IN,start=time.time())
            self.write(dict(status=True,access_token=access_token,refresh_token=refresh_token,expires_in=EXPIRES_IN))
        else:
            self.write(dict(status=False,msg='app验证失败'))


@url(r"/oauth2/app/access_token")
class AppAccessTokenHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.Request.from_request(self.request.uri)
        # 验证appid＆secret
        # http://127.0.0.1:8888/oauth2/app/access_token?client_id=59df2a6235f9a852f687e612&secret=c2e81a083b0b6ec16bafa580fe7887be16da4ae40cd01f7aa62d1901b8a73ed08c0e7274c3e23927dfe3a4a9729bdbe704568e5d812dd9aa369e2edadbf47fe895fb488c34b651237075529acd0c56ccad1bf09bee24d8f568d14ea933fb81606f6b64409a773310101c8573a3ed1fb4c3bacf5e6e173f8abddae56c45f044db
        client_id = oauth_request.parameters.get('client_id')
        secret = oauth_request.parameters.get('secret')
        app = MongoIns().m_find_one('oauth2_app', dbname='cas',dbhost = __conf__.CAS_DB_HOST, _id = ObjectId(client_id))
        if app.get('secret') == secret:
            token, expires_in = oauth.AppToken().get_token({'client_id':client_id,'owner':client_id,
                'secret':client_id})
            self.write(dict(status=True,access_token=token,expires_in=expires_in))
            status,msg = oauth.AppToken().verify(token)
            print msg,status
        else:
            self.write(dict(status=False,msg='app验证失败'))

@url(r"/oauth2/refresh")
class RefreshTokenHandler(BaseHandler):
    def get(self):
        oauth_request = oauth.Request.from_request(self.request.uri)
        refresh_token = oauth_request.parameters.get('refresh_token')
        refresh_token = oauth.RsaEncryption().decrypt(refresh_str)
        owner = refresh_token.split(',')[0]
        user = MongoIns().m_update('oauth2_user',{'owner':owner}, dbname='cas',dbhost = __conf__.CAS_DB_HOST, start = time.time())
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
        oauth_request = oauth.Request.from_request(self.request.uri)
        access_token = oauth_request.parameters.get('access_token')
        access_token = oauth.RsaEncryption().decrypt(refresh_str)
        owner = refresh_token.split(',')[0]
        user = MongoIns().m_del('oauth2_user', owner = owner,dbname='cas',dbhost = __conf__.CAS_DB_HOST)
        self.wfile(dict(status=True,msg='取消授权成功'))








