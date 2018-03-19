#coding:utf-8
# 用Python读取大文件（上）
#方法一：
"""
利用open（“”， “”）系统自带方法生成的迭代对象
for line in f 这种用法是把文件对象f当作迭代对象， 
系统将自动处理IO缓冲和内存管理， 这种方法是更加pythonic的方法。 比较简洁。 
"""
with open('class_var.py') as f:
    for line in f:
        print line


#方法二：

"""将文件切分成小段，每次处理完小段内容后，释放内存

这里会使用yield生成自定义可迭代对象， 即generator， 每一个带有yield的函数就是一个generator。   """
#此方法不一定按行读取
def read_in_block(file_path):  
    BLOCK_SIZE = 1024  
    with open(file_path, "r") as f:  
        while True:  
            block = f.read(BLOCK_SIZE)  # 每次读取固定长度到内存缓冲区  
            if block: 
                yield block  
                # import  pdb;pdb.set_trace() 
            else:  
                return  # 如果读取到文件末尾，则退出  
    
    
def test3():  
    file_path = "class_var.py"  
    for block in read_in_block(file_path):  
        print block  


## 以下不可取！！！！！！！！！！！！！！！

"""read （）的方法是一次性把文件的内容以字符串的方式读到内存， 放到一个字符串变量中
readlines（）的方法是一次性读取所有内容， 并按行生成一个list 

因为read（）和readlines（）是一次性把文件加载到内存， 如果文件较大，
甚至比内存的大小还大， 内存就会爆掉。 所以，这两种方法只适合读取小的文件。 """
def test1():  
    with open("/tmp/test.log", "r") as f:  
        print f.read()  

def test1():  
    with open("/tmp/test.log", "r") as f:  
        print f.read()  


if __name__ == '__main__':
    test3()