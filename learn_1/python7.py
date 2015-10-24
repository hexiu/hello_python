#!/usr/bin/env python3
#-*- coding:utf-8 -*-

def calc(*numbers):
        sum=0
        for n in numbers:
            sum=sum+n*n
        return sum

#L=input('hello:');
L=[1,2,3,4]

M=calc(L[0],L[1],L[2])
print(M)
N=calc(*L)
print(N)
