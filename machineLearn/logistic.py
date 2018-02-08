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
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat-h)
        weights = weights + alpha*dataMatrix.transpose()*error
    return weights

def plotBestFit(wei):
    import matplotlib.pyplot as plt
    weights = wei.getA()
    dataMat, labelMat = dataMatIn,classLabels
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1,ycord1 = [],[]
    xcord2,ycord2 = [],[]
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x = np.arange(-3,3,0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    print labelMat
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()



if __name__ == '__main__':
     a = gradAscent(dataMatIn, classLabels)
     print a
     plotBestFit(a)


# success
#-*- coding:utf-8 -*-
# import numpy as np
# import math
# """
# 基于逻辑回归的梯度下降算法的实现
# """
# #['不浮出水面是否可以生存','是否有脚蹼','是否属于鱼类']
# traindata = [[1,1,'yes'],
#             [1,1,'yes'],
#             [1,0,'no'],
#             [0,1,'no'],
#             [0,1,'no']]

# dataMatIn = [[1,1,],
#             [1,1,],
#             [1,0,],
#             [0,1,],
#             [0,1,]]
# classLabels = [1,1,0,0,0]
# # labels = ['不浮出水面是否可以生存','是否有脚蹼']
# labels = ['no sufacing','flippers']

# def loadDataSet():
#     dataMat = [];labelMat =[]
#     fr = open('test.txt')
#     for line in fr.readlines():
#         lineArr = line.strip().split()
#         dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
#         labelMat.append(int(lineArr[2]))
#     return dataMat,labelMat

# def sigmoid(inX):
#     return 1/(1+np.exp(-inX))

# def gradAscent(dataMatIn,classLabels):
#     dataMatrix = np.mat(dataMatIn)
#     labelMat = np.mat(classLabels).transpose()
#     m,n = np.shape(dataMatrix)
#     alpha = 0.001
#     maxCycles = 500
#     weights = np.ones((n,1))
#     for k in range(maxCycles):
#         h = sigmoid(dataMatrix*weights)
#         error = (labelMat-h)
#         weights = weights + alpha*dataMatrix.transpose()*error
#     return weights

# def plotBestFit(wei):
#     import matplotlib.pyplot as plt
#     weights = wei.getA()
#     dataMat, labelMat = dataMatIn,classLabels
#     dataArr = np.array(dataMat)
#     n = np.shape(dataArr)[0]
#     xcord1,ycord1 = [],[]
#     xcord2,ycord2 = [],[]
#     for i in range(n):
#         if int(labelMat[i]) == 1:
#             xcord1.append(dataArr[i,0])
#             ycord1.append(dataArr[i,1])
#         else:
#             xcord2.append(dataArr[i,0])
#             ycord2.append(dataArr[i,1])
#     fig = plt.figure()
#     ax = fig.add_subplot(1,1,1)
#     ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
#     ax.scatter(xcord2,ycord2,s=30,c='green')
#     x = np.arange(-3,3,0.1)
#     y = (1-weights[0]*x)/weights[1]
#     print labelMat
#     import pdb;pdb.set_trace()
#     ax.plot(x,y)
#     plt.xlabel('X1')
#     plt.ylabel('X2')
#     plt.show()


# def plotBestFit(wei):
#     import matplotlib.pyplot as plt
#     weights = wei.getA()
#     dataMat, labelMat = dataMatIn,classLabels
#     dataArr = np.array(dataMat)
#     n = np.shape(dataArr)[0]
#     xcord1,ycord1 = [],[]
#     xcord2,ycord2 = [],[]
#     for i in range(n):
#         if int(labelMat[i]) == 1:
#             xcord1.append(dataArr[i,0])
#             ycord1.append(dataArr[i,1])
#         else:
#             xcord2.append(dataArr[i,0])
#             ycord2.append(dataArr[i,1])
#     fig = plt.figure()
#     ax = fig.add_subplot(1,1,1)
#     ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
#     ax.scatter(xcord2,ycord2,s=30,c='green')
#     x = np.arange(-3,3,0.1)
#     y = (1-weights[0]*x)/weights[1]
#     print labelMat
#     import pdb;pdb.set_trace()
#     ax.plot(x,y)
#     plt.xlabel('X1')
#     plt.ylabel('X2')
#     plt.show()

# if __name__ == '__main__':
#      a = gradAscent(dataMatIn, classLabels)
#      print a
#      plotBestFit(a)
