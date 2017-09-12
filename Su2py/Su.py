from tornado.web import RequestHandler
from redis import Redis

class SuHandler(object):
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

    def get_redis(cls,host=__conf__.CACHE_HOST):
        h,p = host.split(":") if ":" in host else (host, 6379)
        if not hasattr(cls,'__cache__') or (cls.__cache__ and not cls.__cache__.ping()):
            cls.__cache__ = Redis(
                host=h, port=int(p), socket_timeout=__conf__.SOCK_TIMEOUT)
        return cls.__cache__

     def session(self, key, val=None, expire= None):
        '''
        redis session for tornado
        '''
        expire = expire or __conf__.SESSION_EXPIRE
        return self.get_redis().setex(key, val, expire) if val else self.get_redis().get(key)

    def clear_session(self, key):
        self.get_redis().delete(key)