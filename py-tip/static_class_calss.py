# -*- coding:utf-8 -*-

# 一、实例方法
# 实例方法就是类的实例能够使用的方法。如下：
# 复制代码 代码如下:

class Foo:
    def __init__(self, name):
        self.name = name
    def hi(self):
        print self.name
if __name__ == '__main__':
    foo01 = Foo('letian')
    foo01.hi()
    print type(Foo)
    print type(foo01)
    print id(foo01)
    print id(Foo)

# 二、静态方法
# 静态方法是一种普通函数，就位于类定义的命名空间中，它不会对任何实例类型进行操作。使用装饰器@staticmethod定义静态方法。类对象和实例都可以调用静态方法：
# 复制代码 代码如下:

class Foo:
    val = 0 #类变量
    def __init__(self, name):
        self.name = name
    def hi(self):
        print self.name
    @staticmethod
    def add(a, b):
        print a + b
if __name__ == '__main__':
    print '二、静态方法'
    foo01 = Foo('letian')
    foo01.hi()
    foo01.add(1,2)
    Foo.add(1, 2)
# 三、类方法
# 类方法是将类本身作为对象进行操作的方法。类方法使用@classmethod装饰器定义，其第一个参数是类，约定写为cls。类对象和实例都可以调用类方法：
# 复制代码 代码如下:

class Foo:
    name = 'letian '
    @classmethod
    def hi(cls, x):
        print cls.name * x
if __name__ == '__main__':
    foo01 = Foo()
    foo01.hi(2)
    Foo.hi(3)

# super用来执行父类中的函数，例如：
# 复制代码 代码如下:

class Foo(object):
    def hi(self):
        print 'hi,Foo'
class Foo2(Foo):
    def hi(self):
        super(Foo2, self).hi()
if __name__ == '__main__':
    foo2 = Foo2()
    foo2.hi()
#  hi,Foo


# 类变量定义在类的定义之后，实例变量则是以为self.开头。例如：
# 复制代码 代码如下:

class Foo(object):
    val = 0 #类变量
    def __init__(self):
        self.val = 1 #实例变量
if __name__ == '__main__':
    foo = Foo()
    print foo.val
    print Foo.val
# 1
# 0

