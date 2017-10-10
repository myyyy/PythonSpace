# -*- coding: utf-8 -*-

class Node(object):
    def __init__(self, arg,_next=None):
        self.val=arg
        self.next=_next
        

class LinkedList(object):
    """linkpy"""
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
    a=[2,1,3]
    head = LinkedList().creat(a)
    LinkedList().show(head)
    head = LinkedList()._inster_sort(head)
    LinkedList().show(head)
