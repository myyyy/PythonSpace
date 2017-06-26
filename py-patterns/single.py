# -*- coding:utf-8 -*-

def singleton(cls, *args, **kw):
    import pdb;pdb.set_trace()
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class MyClass4(object):
    a = 1
    def __init__(self, x=0):
        self.x = x

one = MyClass4(3)
two = MyClass4()

two.a = 3
print one.a
#3
print id(one)
#29660784
print id(two)
#29660784
print one == two
#True
print one is two
#True
print one.x
one.x = 1
print one.x
#1
print two.x
#1