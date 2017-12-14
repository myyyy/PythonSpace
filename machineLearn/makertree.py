#-*- coding:utf-8 -*-

#['不浮出水面是否可以生存','是否有脚蹼','是否属于鱼类']
traindata = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']]

#计算给定数据的香农熵
from math import log
def calc_shannon_ent(traindata):
    num_entries = len(traindata)
    label_counts = {}
    for featVec in traindata:
        label = featVec[-1]
        label_counts.setdefault(label,0)
        label_counts[label]+=1
    print label_counts
    shannon_ent = 0.0
    for k,v in label_counts.items():
        prob = float(v)/num_entries
        print prob,-prob*log(prob,2)
        shannon_ent +=-prob*log(prob,2)
    return shannon_ent

def split_data(traindata,axis,rvalue):
    rdata=[]
    traindata = copy.deepcopy(traindata)
    for featVec in traindata:
        if featVec[axis] == rvalue:
            featVec.pop(axis)
            rdata.append(featVec)
    print  traindata
    return rdata

if __name__ == '__main__':
    # shannon_ent = calc_shannon_ent(traindata)
    # print shannon_ent
    print split_data(traindata,0,1)
    print traindata
