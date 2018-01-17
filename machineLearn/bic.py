#-*- coding:utf-8 -*-
import numpy as np
"""
朴素贝叶斯分类器实现单词划分
"""
traindata=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],  
    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],  
    ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],  
    ['stop', 'posting', 'stupid', 'worthless', 'garbage'],  
    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],  
    ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']] 
classVec = [0,1,0,1,0,1]#(1:侮辱性，０:正常言论)
def createVocabList(traindata):
    vocabSet = set([])
    for d in traindata:
        vocabSet = vocabSet|set(d)
    return list(vocabSet)
#词集模型（set-of-words model）：每个词是否出现，每个词只能出现一次
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:print 'the word:%s is not in my vocablary!'%word
    return returnVec
# 朴素贝叶斯词袋模型  
# 词袋模型（bag-of-words model）：一个词可以出现不止一次
def bagOfWords2VecMN(vocabList, inputSet):  
    returnVec = [0] * len(vocabList)  
    for word in inputSet:  
        if word in vocabList:  
            returnVec[vocabList.index(word)] += 1  
    return returnVec  

def trainNB0(trainMatrix, trainCategory):
    
    """
    朴素贝叶斯分类器训练函数    
    trainMatrix: 文档矩阵，  
    trainCategory: 由每篇文档类别标签所构成的向量  
    """
    numTrainDocs = len(trainMatrix)  
    numWords = len(trainMatrix[0]) 
    pAbusive = sum(trainCategory) / float(numTrainDocs)  
    p0Num = np.ones(numWords);  
    p1Num = np.ones(numWords);  
    p0Denom = 2.0;  
    p1Denom = 2.0;  
    for i in range(numTrainDocs):  
        if trainCategory[i] == 1:  
            p1Num += trainMatrix[i]  
            p1Denom += sum(trainMatrix[i])  
        else:  
            p0Num += trainMatrix[i]  
            p0Denom += sum(trainMatrix[i]) 
    p1Vect = np.log(p1Num / p1Denom)  
    p0Vect = np.log(p0Num / p0Denom)  
    return p0Vect, p1Vect, pAbusive 

# 朴素贝叶斯分类函数  
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):  
    import pdb; pdb.set_trace()
    p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)  
    p0 = sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)  
    if p1 > p0:    
        return 1  
    else:  
        return 0

def testingNB():  
    listOPosts, listClasses = traindata, classVec
    myVocabList = createVocabList(listOPosts)  
    trainMat = []  
    for postinDoc in listOPosts:  
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))  
      
    p0V, p1V, pAb = trainNB0(np.array(trainMat), np.array(listClasses))  
      
    testEntry = ['love', 'my', 'dalmation']  
    thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
    print thisDoc
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)  
  
    testEntry = ['stupid', 'garbage']  
    thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))  
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb) 
if __name__ == '__main__':
    myVocabList = createVocabList(traindata)
    # print myVocabList,traindata[1]
    print bagOfWords2VecMN(myVocabList,['my', 'my', 'has', 'flea', 'problems', 'help', 'please'])
    print setOfWords2Vec(myVocabList,['my', 'my', 'has', 'flea', 'problems', 'help', 'please'])
    # trainMat=[]
    # print 'myVocabList',myVocabList
    # for p in traindata:
    #     trainMat.append(setOfWords2Vec(myVocabList,p))
    #     print 'p',p
    # print 'trainMat',trainMat,classVec
    # p0Vect, p1Vect, pAbusive = trainNB0(trainMat,classVec)
    # print p0Vect
    # print p1Vect
    # print pAbusive
    # testingNB()
    