# coding:utf-8
import time
import logging
from functools import wraps

"""
warps:
Python装饰器（decorator）在实现的时候，
被装饰后的函数其实已经是另外一个函数了（函数名等函数属性会发生改变），
为了不影响，Python的functools包中提供了一个叫wraps的decorator来消除这样的副作用。
写一个decorator的时候，最好在实现之前加上functools的wrap，它能保留原有函数的名称和docstring。
"""

#装时器限定函数运行次数
def fun_time(t):
    _dict={}
    def decorate(fun):
        @wraps(fun)
        def inner(*arg,**kw):
            # print len(_dict),_dict
            if len(_dict)<t:
                _dict[time.time()] = fun
                fun(*arg,**kw)
                # print fun.__name__
            else:
                return None
        return inner
    return decorate

#装时器限定函数10s运行n次数
def fun_time2(t,during):
    _dict={}
    def decorate(fun):
        _name = str(fun.__name__) 
        _dict.setdefault(_name,[])
        print _name
        def inner(*arg,**kw):
            # print len(_dict),_dict
            if  _dict[_name]:
                if  len(_dict[_name])<t:
                    _dict[_name].append(time.time())
                    fun(*arg,**kw)
                elif _dict[_name][-1]<(time.time()-during):
                    _dict[_name]=[time.time()]
                    fun(*arg,**kw)
                else:
                    return None
            else:
                _dict[_name].append(time.time())
                fun(*arg,**kw)
        return inner
    return decorate

@fun_time(2)
def args(*args,**kw):
    print args,kw



if __name__ == '__main__':
    # args(1,2,3,a=2)
    args(*(1,),**{'a':2})
    args(*(2,),**{'a':2})
    print args.__name__
    # time.sleep(1)
    args(*(3,),**{'a':2})
    args(*(4,),**{'a':2})
    args(*(5,),**{'a':2})
    
    

    
    
    
    