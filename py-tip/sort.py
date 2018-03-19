# -*- coding:utf-8 -*-

def insert_sort(lists):
    """
    ##插入排序
    插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，
    从而得到一个新的、个数加一的有序数据，算法适用于少量数据的排序，时间复杂度为O(n^2)。
    是稳定的排序方法。插入算法把要排序的数组分成两部分：第一部分包含了这个数组的所有元素，
    但将最后一个元素除外（让数组多一个空间才有插入的位置），而第二部分就只包含这一个元素（即待插入元素）。
    在第一部分排序完成后，再将这个最后元素插入到已排好序的第一部分中。
    [3, 4, 2, 1]
    [3, 2, 4, 1]
    [2, 3, 4, 1]
    [2, 3, 1, 4]
    [2, 1, 3, 4]
    [1, 2, 3, 4]
    [1, 2, 3, 4]

    """
    count = len(lists)
    for i in range(1,count):
        key = lists[i]
        j = i-1
        while j>=0:
            if lists[j]>key:
                lists[j],lists[j+1]=key,lists[j]
            print lists
            j-=1

    return lists

def bobble_sort(lists):
    """
    从第一个开始依次向后比较２,然后按照顺序进行交换
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [2, 7, 3, 6, 4, 35, 9, 86, 1, 2, 0, 8] 0
    [1, 7, 3, 6, 4, 35, 9, 86, 2, 2, 0, 8] 0
    [1, 7, 3, 6, 4, 35, 9, 86, 2, 2, 0, 8] 0
    [0, 7, 3, 6, 4, 35, 9, 86, 2, 2, 1, 8] 0
    [0, 7, 3, 6, 4, 35, 9, 86, 2, 2, 1, 8] 0
    [0, 3, 7, 6, 4, 35, 9, 86, 2, 2, 1, 8] 1
    [0, 3, 7, 6, 4, 35, 9, 86, 2, 2, 1, 8] 1
    [0, 3, 7, 6, 4, 35, 9, 86, 2, 2, 1, 8] 1
    [0, 3, 7, 6, 4, 35, 9, 86, 2, 2, 1, 8] 1
    [0, 3, 7, 6, 4, 35, 9, 86, 2, 2, 1, 8] 1
    [0, 3, 7, 6, 4, 35, 9, 86, 2, 2, 1, 8] 1
    [0, 2, 7, 6, 4, 35, 9, 86, 3, 2, 1, 8] 1
    [0, 2, 7, 6, 4, 35, 9, 86, 3, 2, 1, 8] 1
    [0, 1, 7, 6, 4, 35, 9, 86, 3, 2, 2, 8] 1
    [0, 1, 7, 6, 4, 35, 9, 86, 3, 2, 2, 8] 1
    [0, 1, 6, 7, 4, 35, 9, 86, 3, 2, 2, 8] 2
    [0, 1, 4, 7, 6, 35, 9, 86, 3, 2, 2, 8] 2
    [0, 1, 4, 7, 6, 35, 9, 86, 3, 2, 2, 8] 2
    """
    count=len(lists)
    for i in range(0,count):
        for j in range(i+1,count):
            if lists[i]>lists[j]:
                lists[i],lists[j] = lists[j],lists[i]
            print lists,i
    return lists




def quick_sort(l,left,right):
    """
    参考http://developer.51cto.com/art/201403/430986.htm
    """
    if left >=right:
        return l
    key = l[left]
    low=left
    high = right
    while left<right:
        while left<right and l[right]>=key:
            right-=1
        l[left]=l[right]
        while left<right and l[left]<=key:
            left+=1
        l[right] = l[left]
    l[right] = key
    print left-1,low,high
    quick_sort(l, low, left - 1)
    quick_sort(l, left + 1, high)
    return l




def ShellInsetSort(array, len_array, dk):  # 直接插入排序
    for i in range(dk, len_array):  # 从下标为dk的数进行插入排序
        position = i
        current_val = array[position]  # 要插入的数

        index = i
        j = int(index / dk)  # index与dk的商
        index = index - j * dk

        # while True:  # 找到第一个的下标，在增量为dk中，第一个的下标index必然 0<=index<dk
        #     index = index - dk
        #     if 0<=index and index <dk:
        #         break


        # position>index,要插入的数的下标必须得大于第一个下标
        while position > index and current_val < array[position-dk]:
            array[position] = array[position-dk]  # 往后移动
            position = position-dk
        else:
            array[position] = current_val



def ShellSort(array, len_array):  # 希尔排序
    dk = int(len_array/2)  # 增量
    while(dk >= 1):
        ShellInsetSort(array, len_array, dk)
        print(">>:",array)
        dk = int(dk/2)


if __name__ == '__main__':
    arr = [2,4,0,3,1]
    ShellSort(arr,len(arr))
    print arr

