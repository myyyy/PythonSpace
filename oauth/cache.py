#!encoding=utf-8
import time
import threading
import Queue

"""
    Cache().setex(k, v, timeout)
    Cache().get(k)
"""


class Cache(object):
    c1 = {}      # 数据缓存 1   key: (value, expire)
    c2 = {}      # 数据缓存 2   key: (func, args, kwargs)
    _queue = Queue.Queue()


    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance_'):
            #print 'Cache __new__'
            orig = super(Cache, cls)
            cls._instance_ = orig.__new__(cls, *args, **kw)

            t = threading.Thread(target=cls._instance_.timer)
            t.setDaemon(True)
            t.start()

            t = threading.Thread(target=cls._instance_.timer_c2)
            t.setDaemon(True)
            t.start()

            t = threading.Thread(target=cls._instance_._queue_consumer)
            t.setDaemon(True)
            t.start()

        return cls._instance_

    def setex(self, k, v, ex = None):
        """
            k, v, ex = expire
        """
        if ex: ex = time.time() + ex
        self.c1[k] = (v, ex)

    def set_c2(self, k, func, *args, **kwargs):
        self.c2[k] = (func, args, kwargs)

    def get(self, k):
        return self.c1.get(k)[0] if self.c1.has_key(k) else None

    def timer(self):
        while True:
            now = time.time()
            for k, v in self.c1.items():
                if v[1] and now > v[1]:
                    self.c1.pop(k, None)

            time.sleep(10)

    def timer_c2(self):
        while True:
            now = time.time()
            for k, v in self.c2.items():
                func, args, kwargs = v
                func(*args, **kwargs)
                self.c2.pop(k, None)

            time.sleep(2)

    def queue_set(self, func, *args, **kwargs):
        self._queue.put((func, args, kwargs))

    def _queue_consumer(self):
        while True:
            func, args, kwargs = self._queue.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    Cache().setex(1, 2, 6)
    for i in range(10):
        print Cache().get(1)
        time.sleep(1)

    import tornado.ioloop
    tornado.ioloop.IOLoop.instance().start()

