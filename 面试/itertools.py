#coding:utf-8
#来一个例子?让我们看看4匹马比赛有多少个排名结果:
import itertools
def horse(a):
        print list(itertools.permutations(a))

def main():
    pass

if __name__ == '__main__':
    horse(range(3))