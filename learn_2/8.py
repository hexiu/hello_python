#!/bin/bash/env python3
# -*- coding:utf-8 -*-

from functools import reduce

def prod(L):
    return reduce(lambda x,y:x*y,L)
print (prod([1,2,3]))

def str2float(s):
    numList=list(map(lambda s:{'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'.':'.'}[s],s))
    index=0
    while(numList[index]!='.'):
        index=index+1
    del numList[3]
    return reduce(lambda x,y:x*10+y,numList)/pow(10,index)

print(str2float('123.456'))
