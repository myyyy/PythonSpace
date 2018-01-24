# -*- coding:utf-8 -*-

class Queue(object):
    def __init__(self,size):
        self.size = size
        self.queue = []

    def isfull(self):
        return bool(len(self.queue)>=self.size)
    def isempty(self):
        return bool(len(self.queue)==0)
    def pop(self):
        if self.isempty():
            print 'now is empty'
        else:
            self.queue.pop(0)
    def push(self,x):
        if self.isfull():
            print 'queue is full'
        else:
            self.queue.append(x)
    def showstack(self):
        print self.queue

if __name__ == '__main__':
    st = Queue(10)
    for i in range(10):
        st.push(i)
    st.showstack()
    st.push(22)
    st.pop()
    st.showstack()
    st.push(3)
    st.showstack()