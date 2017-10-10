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
            print 'no elements'
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
            print 'no elements'
            return
        a=[str(head.val)]
        while head.next:
            _head = head.next
            a.append(str(_head.val))
            head=_head
        print ','.join(a)

    def sort(self,head):
        if not head:
            print 'no elements'
            return
        new = Node(0)
        while head.next:
            node=new
            nl = head.next
            while node.next is not None and node.next.val < head.val:
                node= node.next
            head.next = node.next
            node.next=head
            head = nl
        return head
if __name__ == '__main__':
    a=[2,1]
    head = LinkedList().creat(a)
    LinkedList().show(head)
    import pdb;pdb.set_trace()
    head = LinkedList().sort(head)
    print '1111'