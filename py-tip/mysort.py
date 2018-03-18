# coding:utf-8

def quick_sort(NM,L,R):
    if L>=R:return
    key = NM[L]
    low,high = L,R
    while L<R:
        while L<R and NM[L]<=key:
            L+=1
        while L<R and NM[R]>key:
            R-=1
        NM[L],NM[R] = NM[R],NM[L]
    if NM[L-1]<key:
        NM[low]=NM[L-1]
        NM[L-1] = key
    print L-2,L,NM[L-2],NM
    quick_sort(NM,low,L-2)
    quick_sort(NM,L,high)
    return NM
def select_sort(NM):
    """
   基本思想：第1趟，在待排序记录r1 ~ r[n]中选出最小的记录，将它与r1交换；
   第2趟，在待排序记录r2 ~ r[n]中选出最小的记录，将它与r2交换；
   以此类推，第i趟在待排序记录r[i] ~ r[n]中选出最小的记录，将它与r[i]交换，
   使有序序列不断增长直到全部排序完毕。
    """
    l = len(NM)
    for i in range(l):
        min = NM[i]
        for j in range(i+1,l):
            if NM[j]<NM[i]:
                NM[i],NM[j]=NM[j],NM[i]
    return NM

def insert_sort(NM):
    """
    插入排序原理很简单，讲一组数据分成两组，我分别将其称为有序组与待插入组。
    每次从待插入组中取出一个元素，与有序组的元素进行比较，并找到合适的位置，
    将该元素插到有序组当中。就这样，每次插入一个元素，有序组增加，待插入组减少。
    直到待插入组元素个数为0。当然，插入过程中涉及到了元素的移动。
    """
    l = len(NM)
    for i in range(1,l):
        key = NM[i]
        j = i-1
        while j>=0:
            print NM[j],key,NM
            if NM[j]<key:
                NM[j+1]=NM[j]
                NM[j]=key
            j-=1
    return NM

def bubble_sort(NM):
    l = len(NM)
    for i in range(l):
        for j in range(i+1,l):
            if NM[i]>NM[j]:
                NM[j],NM[i] = NM[i],NM[j]
    return NM
if __name__=='__main__':
    N = [2,4,1,2,3,42,1,4,2,6,1,7,8,7,2]
    # NM = quick_sort(N,0,len(N)-1)
    # NM = select_sort(N)
    # NM = insert_sort(N)
    NM = bubble_sort(N)
    print NM