#!/bin/bash/env python3
# -*- coding:utf-8 -*-
L=[]
for i in range(3):
    print('Please enter username:')
    L.append(input())

print('You Enter user:',L)
#name=[]
def nomalize(name):
    return name[0].upper()+name[1:].lower()
from functools import reduce
L2=list(map(nomalize,L))
print(L2)
