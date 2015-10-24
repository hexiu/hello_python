#!/usr/bin/env python3
#-*- coding:utf-8 -*-

def person(name,age,**kw): 
    print('name:',name,'age:',age,'other:',kw)

person('Axiu',19)

person('Bob',35,city='Beijing',job='Engineer')
