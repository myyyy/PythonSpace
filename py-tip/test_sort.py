# -*- coding:utf-8 -*-

import unittest
from sort import *


class TestSort(unittest.TestCase):
    """
    使用Python自带的unittest模块，编写sort.py测试用例
    """
    arr = [2,4,0,3,1]
    def test_quick_sort(self):
        b = quick_sort(self.arr,0,len(self.arr)-1)
        self.assertEquals(b,sorted(self.arr))
    def test_bobble_sort(self):
        b = bobble_sort(self.arr)
        self.assertEquals(b,sorted(self.arr))
    def test_insert_sort(self):
        b = insert_sort(self.arr)
        self.assertEquals(b,sorted(self.arr))
if __name__ == '__main__':  
    unittest.main()