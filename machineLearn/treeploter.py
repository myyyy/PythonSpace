#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
decisionNode = dict(boxstyle='sawtooth',fc='0.8')
leafNode = dict(boxstyle='round4',fc='0.8')
arrow_args = dict(arrowstyle="<-")

def plot_node(nodetxt,centerPt,parentpt,nodetype):
    creatPlot.ax1.annotate(nodetxt,xy=parentpt,xycoords='axes fraction',
    xytext = centerPt,textcoords='axes fraction',va='center',ha="center",bbox=nodetype,arrowprops=arrow_args)
def creatPlot():
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    creatPlot.ax1 = plt.subplot(111,frameon=False)
    plot_node('jcnode',(0.5,0.1),(0.1,0.5),decisionNode)
    plot_node('yjd',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for k,v in secondDict.items():
        if isinstance(v,dict):
            numLeafs += getNumLeafs(secondDict[k])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepath(myTree):
    numLeafs = 0
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for k,v in secondDict.items():
        if isinstance(v,dict):
            print '***********:',secondDict
            print '-----------:',v
            thisDepth += getTreeDepath(secondDict[k])
        else:
            thisDepth = 1
        if thisDepth>maxDepth:maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt,parentPt,txtString):
    xmid = (parentPt[0]-cntrPt[0]/2.0+cntrPt[0])
    ymid = (parentPt[1]-cntrPt[1]/2.0+cntrPt[1])
    creatPlot.ax1.text(xmid,ymid,txtString)
    
if __name__ == '__main__':
    creatPlot()