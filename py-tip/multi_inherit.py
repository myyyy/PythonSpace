# -*- coding:utf-8 -*-
#参考链接：https://segmentfault.com/a/1190000004018476
class P1(object):
   def foo(self):
       print 'p1-foo' 
 
class P2(object): 
   def foo(self): 
       print 'p2-foo' 
   def bar(self): 
       print 'p2-bar' 

class F1(object):
   def bar(self): 
       print 'F1-bar' 


class C1 (P1,P2): 
   pass
 
class C2 (P1,P2): 
   # def bar(self): 
       # print 'C2-bar'
    pass
 
class D(F1,C2): 
   pass

if __name__ == '__main__':
  d=D()
  d.bar()
  d.foo()