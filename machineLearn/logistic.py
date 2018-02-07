#-*- coding:utf-8 -*-
import numpy as np
import math
"""
基于逻辑回归的梯度下降算法的实现
"""
#['不浮出水面是否可以生存','是否有脚蹼','是否属于鱼类']
traindata = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']]

dataMatIn = [[1,1,1,],
            [1,1,1,],
            [1,1,0,],
            [1,0,1,],
            [1,0,1,]]
classLabels = [1,1,0,0,0]
# labels = ['不浮出水面是否可以生存','是否有脚蹼']
labels = ['no sufacing','flippers']

def loadDataSet():
    dataMat = [];labelMat =[]
    fr = open('test.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1/(1+np.exp(-inX))

def gradAscent(dataMatIn,classLabels):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    m,n = np.shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = np.ones((n,1))
    import pdb;pdb.set_trace()
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat-h)
        weights = weights + alpha*dataMatrix.transpose()*error
    return weights

if __name__ == '__main__':
     a = gradAscent(dataMatIn, classLabels)
     print a