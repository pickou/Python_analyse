__author__ = 'yjc'
#write at 2016.8.17
from pandas import *
from numpy import *
import operator
import csv
import time
#return a tpye of ndarray(numpy)
def Read_csv(filename='train.csv'):
    df=read_csv(filename)
    return df.values
#get train_data and labels
def Get_train_data(train_array):
    train=train_array[:,1:]
    labels=train_array[:,0]
    return train,labels
#get test_data
def Get_test_data():
    return Read_csv(filename='test.csv')
#implement knn on any vector of a test_number
def knn_classify(inX,train,labels,k):
    train_size=train.shape[0]
    #tile(repeat inX 'train_size' times in column)
    diffMat=tile(inX,(train_size,1))-train
    sqDiffMat=diffMat**2
    sqDistMat=sqDiffMat.sum(axis=1)
    distMat=sqDistMat**0.5
    sortedDistIndicies=distMat.argsort()
    #vote for classification
    classCount={}
    for i in range(k):
        voteLabel=labels[sortedDistIndicies[i]]
        classCount[voteLabel]=classCount.get(voteLabel,0)+1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def classfy_hand_digits():
    train,labels=Get_train_data(Read_csv())
    test=Get_test_data()
    test_num=test.shape[0]
    resultLabels=[]
    print("here is the digits program")
    for i in range(test_num):
	start_time=time.clock()
        indX=test[i,:]
        resultLabel=knn_classify(indX,train,labels,3)
        resultLabels.append((i+1,resultLabel))
        cycletime=time.clock()-start_time
	print("%d takes left,you need waiting about %.2f hours"%(test_num-1-i,(test_num-1-i)*cycletime/3600))    
    return resultLabels
def savefile2csv(list_result):
    resultcsv=open('knn_digit_recognize.csv','w')
    writer=csv.writer(resultcsv)
    writer.writerow(['ImageId','Label'])
    writer.writerows(list_result)
    resultcsv.close()
    
if __name__=='__main__':
    resultLabels= classfy_hand_digits()
    savefile2csv(resultLabels)
