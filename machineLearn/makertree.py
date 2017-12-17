#-*- coding:utf-8 -*-
import copy
#['不浮出水面是否可以生存','是否有脚蹼','是否属于鱼类']
traindata = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']]
# labels = ['不浮出水面是否可以生存','是否有脚蹼']
labels = ['no sufacing','flippers']

#计算给定数据的香农熵
from math import log
def calc_shannon_ent(traindata):
    """
    香农熵计算公说明：H(x) = E[I(xi)] = E[ log(2,1/p(xi)) ] = -∑p(xi)log(2,p(xi)) (i=1,2,..n)
    其中，x表示随机变量，与之相对应的是所有可能输出的集合，定义为符号集,随机变量的输出用x表示。
    P(x)表示输出概率函数。

    一般而言，当一种信息出现概率更高的时候，表明它被传播得更广泛，或者说，被引用的程度更高。我们可以认为，从信息传播的角度来看，
    信息熵可以表示信息的价值。这样子我们就有一个衡量信息价值高低的标准，可以做出关于知识流通问题的更多推论。
    """
    num_entries = len(traindata)
    label_counts = {}
    for featVec in traindata:
        label = featVec[-1]
        label_counts.setdefault(label,0)
        label_counts[label]+=1
    shannon_ent = 0.0
    for k,v in label_counts.items():
        prob = float(v)/num_entries
        shannon_ent +=-prob*log(prob,2)
    return shannon_ent

def split_data(traindata,axis,rvalue):
    """
    根据划分数据的特征(axis)，需要返回的特征值(rvalue)，返回划分后的数据值
    """
    rdata=[]
    traindata = copy.deepcopy(traindata)
    for featVec in traindata:
        if featVec[axis] == rvalue:
            featVec.pop(axis)
            rdata.append(featVec)
    return rdata

def chooseBestFeatureToSplit(traindata):
    """
    熵 增宜最高 的特征就是最好的选择
    """
    numFeature = len(traindata[0])-1#记录所有的特征个数
    baseEntropy = calc_shannon_ent(traindata)#记录原始香农熵
    bestInfoGain,bestFeature = 0.0,-1
    # print 'numFeature',numFeature
    for i in range(numFeature):#循环特征个数
        #i 表示第几个特征
        featlist = set([e[i]for e in traindata])#取出某个特征的所有可能
        # print 'featlist',featlist
        newEntropy=0.0
        for value in featlist:
            subData = split_data(traindata,i,value)#按选取的特征进行分类器分类
            prob = len(subData)/float(len(traindata))
            newEntropy+=prob*calc_shannon_ent(subData)#计算分类之后的数据的香农熵
            print 'subData',i,'-',value,':',subData,newEntropy            
        infoGain = baseEntropy-newEntropy#算出香农熵增益
        if(infoGain > bestInfoGain):#比较香农熵增益
            bestInfoGain = infoGain
            bestFeature = i#返回特征下标，此处记录的是特征的下标
    return bestFeature

def majorityEnt(classList):
    """
    返回出现最多的分类的名称
    classlist = [0,1,1,0,0,0]
    """
    classCount = {}
    for vote in classList:
        classCount.setdefault(vote,0)
        classCount[vote] += 1
    sorteClassCount = sorted(classCount.items(),key=lambda x: x[1],reverse=True)
    return sorteClassCount[0][0]

def createTree(traindata,_labels):
    """
    创建自动分类树
    """
    print 'createTreecreateTree:'
    labels = copy.deepcopy(_labels)
    classList = [i[-1] for i in traindata]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(traindata[0]) == 1:
        return majorityEnt(classList)
    #bestFeat 最佳分类的下标
    bestFeat = chooseBestFeatureToSplit(traindata)
    print 'bestFeat',bestFeat
    bestFeatLabel = labels[bestFeat]
    print 'bestFeatLabel',bestFeatLabel,'del labels[bestFeat]',labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    #计算出最佳分类的 分类数 以数组的方式存储
    featValues = set([i[bestFeat] for i in traindata])
    print 'featValues',featValues
    for value in featValues:
        subLabels = labels[:]
        print labels,subLabels
        print '(split_data(traindata,bestFeat,value),subLabels):',traindata,bestFeat,value,subLabels
        
        myTree[bestFeatLabel][value] = createTree(split_data(traindata,bestFeat,value),subLabels)
    return myTree
if __name__ == '__main__':
    # shannon_ent = calc_shannon_ent(traindata)
    # print shannon_ent
    # print split_data(traindata,0,1)
    # print traindata
    # print chooseBestFeatureToSplit(traindata)
    # print traindata
    # print majorityEnt([0,1,0,1,0,0])
    print createTree(traindata,labels)
    
    myTree = createTree(traindata,labels)
    #使用matplotlib画图
    from treeploter import *
    print getNumLeafs(myTree)
    print getTreeDepath(myTree)