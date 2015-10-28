#!/bin/bash/env python3
# -*- coding:utf-8 -*-

print('Please enter a number string:')
s=input()

from functools import reduce

def str2float(s):
    def char2num(c):
        return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'.':'.'}[c]
    L=list(map(char2num,s))
    count=index=0
    for x in L:
        if x=='.':
            index=count
        count+=1
    L.pop(index)
    def fn(x,y):
        return x*10+y
    return reduce(fn,L)/pow(10,count-1-index)




print(str2float(s))
