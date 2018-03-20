# -*- coding: utf-8 -*-

class Node(object):
    def __init__(self, arg,_next=None):
        self.val=arg
        self.next=_next
        

class LinkedList(object):
    """linkpy"""
    lang = property(lambda self:self.len())
    def __init__(self, arg=None):
        self.head=arg


    def creat(self,_list):
        if not _list:
            print '空链表'
            return
        self.head=Node(_list[0])
        _head = self.head
        for i in _list[1:]:
            node = Node(i)
            _head.next=node
            _head=node
        return self.head

    def show(self,head):
        if not head:
            print '空链表'
            return
        a=[str(head.val)]
        while head.next:
            _head = head.next
            a.append(str(_head.val))
            head=_head
        print ','.join(a)
    def append(self,val):
        node = Node(val)
        pre = self.head
        if not self.head:
            self.head = node
        else:
            while pre.next:
                pre = pre.next
            pre.next=node
    def len(self):
        l = 0
        pre = self.head
        while pre.next:
            pre = pre.next
            l+=1
        return l
    def delete(self,index):
        """
        负索引，索引为0删除第一个，这些功能还没有写
        """
        pre = self.head
        head = None
        if not self.head or self.lang<index:
            pass
        else:
            while index>0:
                head = pre
                print head
                pre = pre.next
                index-=1
            if head:
                head.next=pre.next
    def get(self,index):
        pre = self.head
        if not self.head or self.lang<index:
            return None
        else:
            while index>0:
                pre = pre.next
                index-=1
            return pre
    def _inster_sort(self,head):
        if head == None:
            return head
        p = Node(0)
        while head:
            node = p
            print p.val,p.next,head.next
            while node.next!=None and node.next.val<head.val:
                node = node.next
            tmp = head.next
            head.next,node.next = node.next,head
            head = tmp
        return p.next 
if __name__ == '__main__':
    a=[2,1,3,6,2,4]
    link = LinkedList()
    head = link.creat(a)
    LinkedList().show(head)
    # head = LinkedList()._inster_sort(head)
    link.append(8)
    a = link.get(2)
    print a.val
    l = link.delete(0)
    # print a.val
    LinkedList().show(head)
