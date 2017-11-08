# 判断有没有迭代属性
from collections import Iterable
# 判断是不是迭代器（依靠 next 生成下一个数据）
from collections import Iterator

# this is fib()
def f(limit):
    n,a,b = 0,0,1
    while n < limit:
        yield b
        a,b = b,a+b
        n += 1
    return 'done'

print(type(f))
print(isinstance(f(10),Iterator))
print(isinstance(f(10),Iterable))
# 迭代器是一个惰性计算，比如生成器
i = 1
fa = f(10)
while i<10 :
    print(next(fa))
    i += 1


