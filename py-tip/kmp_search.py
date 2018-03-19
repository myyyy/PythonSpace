# coding:utf-8
#阮一峰字符串匹配的KMP算法
#http://www.ruanyifeng.com/blog/2013/05/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm.html

def getnext(a,next):  
    al = len(a)  
    next[0] = -1  
    k = -1  
    j = 0  
    while j < al-1:  
        if k == -1 or a[j] == a[k]:  
            j += 1  
            k += 1  
            next[j] = k  
        else:  
            k = next[k]  
  
def KmpSearch(a,b):  
    i = j = 0  
    al = len(a)  
    bl = len(b)  
    while i < al and j < bl:  
        print 'i',i,'j',j
        if j == -1 or a[i] == b[j]:  
            i += 1  
            j += 1  
        else:  
            print next
            j = next[j]  
    if j == bl:  
        return i-j  
    else:  
        return -1  
  
a = 'ABABCABDABBGAFDSBVSABDABB'  
b = 'AFDSB'  
next = [0]*len(b)  
getnext(b,next)  
t = KmpSearch(a,b)  
# import pdb;pdb.set_trace()
print(next)  
print(t)



#KMP  
def kmp_match(s, p):  
    m = len(s); n = len(p)  
    cur = 0#起始指针cur  
    table = partial_table(p)  
    while cur<=m-n:  
        for i in range(n):  
            if s[i+cur]!=p[i]:  
                cur += max(i - table[i-1], 1)#有了部分匹配表,我们不只是单纯的1位1位往右移,可以一次移动多位  
                break  
        else:  
            return True  
    return False  
  
#部分匹配表  
def partial_table(p):  
    '''''partial_table("ABCDABD") -> [0, 0, 0, 0, 1, 2, 0]'''  
    prefix = set()  
    postfix = set()  
    ret = [0]  
    for i in range(1,len(p)):  
        prefix.add(p[:i])  
        postfix = {p[j:i+1] for j in range(1,i+1)}  
        ret.append(len((prefix&postfix or {''}).pop()))  
    return ret  
  

print kmp_match("BBC ABCDAB ABCDABCDABDE", "ABCDABD")  