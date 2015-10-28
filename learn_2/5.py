#!/bin/bash/env python3
# -*- coding:utf-8 -*-

L=['HELLO','WORLD','NI',19,'HAO',None]
L1=[]
L2=[]
for x in L:
    print(x)
    if isinstance(x,str):
        L1.append(x.lower())
    else:
        L2.append(x)
print('L1=',L1,'L2=',L2)
