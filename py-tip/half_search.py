#coding:utf-8
def half_search(lst,value,low,high):
    if high < low:  
        return None
    mid = (low + high)/2
    if lst[mid] > value:  
        return half_search(lst, value, low, mid-1)  
    elif lst[mid] < value:  
        return half_search(lst, value, mid+1, high)  
    else:  
        return mid  
def binary_search_loop(lst,value):  
    low, high = 0, len(lst)-1  
    while low <= high:  
        mid = (low + high) / 2  
        if lst[mid] < value:  
            low = mid + 1  
        elif lst[mid] > value:  
            high = mid - 1
        else:
            return mid  
    return None

if __name__ == '__main__':
    N = [1,2,3,4,8,9,10]
    val = half_search(N,8,0,len(N))
    print val