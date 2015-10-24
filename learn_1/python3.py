#-*-coding:utf-8-*-

#height=input("height:")
#float(height)
#weight=input("weight:")
#float(weight)
height=1.75
weight=70.5
bmi=weight/(height * height)
if bmi<18.5:
    print('so low')
elif bmi<25:
    print('usual')
elif bmi<28:
    print('zhong')
elif bmi<32:
    print('fat')
elif bmi>32:
    print('so fat')

    
