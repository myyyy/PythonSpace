# -*- coding:utf-8 -*-
# 利用python 数组实现堆栈
# 堆栈是一个后进先出的数据结构，其工作方式就像一堆汽车排队进去一个死胡同里面，最先进去的一定是最后出来。
class stack(object):
    def __init__(self,size):
        self.size = size
        self.stack = []
        self.top = -1

    def isfull(self):
        return bool(len(self.stack)>=self.size)
    def isempty(self):
        return bool(len(self.stack)==0)
    def pop(self):
        if self.isempty():
            print 'now is empty'
        else:
            return self.stack.pop()
    def push(self,x):
        if self.isfull():
            print 'stack is full'
        else:
            self.stack.append(x)
    def showstack(self):
        print self.stack
    
if __name__ == '__main__':
    st = stack(10)
    for i in range(10):
        st.push(i)
    st.showstack()
    st.push(22)
    st.pop()
    st.showstack()
    st.push(3)
    st.showstack()


            
