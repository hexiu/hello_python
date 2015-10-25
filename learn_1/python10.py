#!/usr/bin/env python
#-*- coding:utf-8 -*-

def fact(n):
    if n==1:
        return 1
    return n*fact(n-1)

for m in range(10):
    i=fact(m+1)
    print(i)

