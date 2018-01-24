class listNode:  
    def __init__(self,x):  
        self.val = x  
        self.next  = None          
    def createList(self,a):  
        if a is None:  
           print 'no elements'  
           return  
        head=listNode(a[0])  
        p=head  
        i=1  
        n=len(a)  
        while i<n:  
            t=listNode(a[i])  
            p.next=t  
            p=t  
            i=i+1  
        return head  
    def scanList(self,head):  
       if head is None:  
          print "no elements"  
          return  
       print head.val  
       while head.next:  
             p=head.next  
             print p.val  
             head=p               
    def sortList(self, head):  
        if head is None or head.next is None:  
            return head  
        mid = (head.val + head.next.val) / 2  
        if head.val > head.next.val:  
            lhead, rhead = head.next, head  
        else:  
            lhead, rhead = head, head.next  
        lit, rit = lhead, rhead  
        it = head.next.next         
        while it is not None:  
            if it.val > mid:  
                rit.next = it  
                rit = it                  
            else:  
                lit.next = it  
                lit = it   
            it = it.next  
        lit.next, rit.next = None, None  
        lhead = self.sortList(lhead)  
        rhead = self.sortList(rhead)  
        it = lhead  
        while it.next is not None:  
            it = it.next  
        it.next = rhead  
        return lhead  

if __name__ == '__main__':
    l=listNode(0)  
    a=[2,5,9,3,6,1,0,7,4,19]  
    head=l.createList(a)  
    import pdb;pdb.set_trace()
    print 'old list:'  
    l.scanList(head)  
    newhead=l.sortList(head)  
    print 'sorted list:'  
    l.scanList(newhead)