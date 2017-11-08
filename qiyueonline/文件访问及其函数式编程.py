"""
文件访问及函数式编程学习笔记
"""

# 文件读写的三种方式：

# 第一种
# 直接读入

file1 = open("numpy_1.py","r")
file2 = open("output.txt","w")

while True:
    line = file1.readline()
    file2.write(line)
    if not line:
        break
file1.close()
file2.close()

# 文件读取的三种方法
# read()
# readline()
# readlines()
file1 = open("output.txt","r")
print(file1.read())
file1.close()
file1 = open("output.txt","r")
print(file1.readlines())
file1.close()

# 文件迭代器
file2 = open("output.txt","w")
for line in open("numpy_1.py"):
    file2.write(line)

# 第三种方式
# 文件上下文管理器
with open("numpy_1.py","r") as f :
    data = f.read()
print(data)

# 二进制文件读取，处理
# 二进制文件读取后，一般需要decode() 解码
import pickle
file3 = open("out.dat","wb")
file3.write(pickle.dumps(data))
file3.close()
file4 = open("out.dat","rb")
data = file4.read()
print(pickle.loads(data))
file4.close()


# os 库的用法
# 操作目录与文件
import os
print(os.name,os.environ)
# 获得绝对路径
print(os.path.abspath("."))
# 添加目录
path = os.path.join(os.path.abspath("."),"output")
print(path)
# 创建目录&删除目录
# os.mkdir(path)
# os.rmdir(path)

# 拆分目录
pathsplit = os.path.split(path)
print(pathsplit)
# 拆分文件后缀名
pathtext = os.path.splitext(os.path.join(os.path.abspath("."),"numpy_1.py"))
print(pathtext)

# 文件重命名
os.rename(os.path.join(os.path.abspath("."),"out.dat"),"output")
# 删除文件
os.remove("output")

# shutil 库 补充os库不足的功能
import shutil
shutil.copyfile("output.dat","output1.dat")
# 列出当前目录下的py文件
print([x for x in os.listdir(".") if os.path.isfile(x) and os.path.splitext(x)[1] == ".py"])
# 列出当前目录下的目录
print([x for x in os.listdir(".") if os.path.isdir(x)])
# 列出当前目录下的文件
print([x for x in os.listdir(".") if os.path.isfile(x)])

# 序列化和反序列化
# 序列化 pickle 和 json
# python 2 和 python 3 里面的 pickle 不一样
# 以下方式可以保证兼容性
# try:
#     import cPickle as pickle
# except ImportError:
#     import pickle

# 高阶函数
# abs(-10)
print(abs(-10))

# 一个简单的高阶函数
def testf(x,y,f):
    return f(x)+f(y)
rel = testf(-10,20,abs)
print(rel)

# 匿名函数
# python使用lambda 来创建一个匿名函数
# lambda 只是一个表达式，函数体比def 简单得多
# 一些辅助工具  reduce 处理 list
# reduce      reduce(func,list)
from functools import reduce
f = lambda x,y:x+y
print(f(2,3))
rel1 = reduce(f,[1,2,3,4])
rel2 = reduce(f,[1,2,3,4],10)
print(rel1,rel2)

# map    map(func,list,...)
#  list
#        --->  list (一一对应原来的list)
#  f()

f = lambda x:x+5
f1 = lambda x,y:x+y
l = map(f,[1,2,3])
print(list(l))
l1 = map(f1,[1,2,3,4],[3,4,5,6])
print(list(l1))

# filter 实现数据过滤
# filter(func,list)
print(list(filter(lambda x:x<5,[1,2,3,4,5,6,6,7,9])))

# 以上三个公式 熟练运用就可以实现复杂运算


# 装饰器（高阶函数）  decorator
#
def hello(fn):
    def wrapper():
        print("hello ",fn.__name__)
        fn()
        print("goodbye",fn.__name__)
    return wrapper

def hi(fn):
    def wrapper():
        print("hello1 ",fn.__name__)
        fn()
        print("goodbye",fn.__name__)
    return wrapper

@hello
@hi
def foo():
    print("I am foo")

foo()

# 以上代码在执行时，相当于      func =  hello(hi(func))          类似  func = decorator_one(decorator_two(func))


# 同时，还可以给 decorator 带一个参数
# eg:
#
# @decorator(arg1,arg2)
# def func():
#     pass
# 相当于 func = decorator(arg1,arg2)(func)

def makeHtmlTag(tag,*args,**kwargs):
    def real_decorator(fn):
        css_class = " class = '{0}'".format(kwargs["css_class"])\
                                        if "css_class" in kwargs else ""
        def wrapper(*args,**kwargs):
            return "<" + tag + css_class + ">" + fn(*args,**kwargs) + "</" + tag + ">"
        return wrapper
    return real_decorator

@makeHtmlTag(tag="b")
@makeHtmlTag(tag="i",css_class="italic_class")
def hii():
    return "hello world"

print(hii())

# *args 和 **kwargs   解释
#  args 有一个* 表示的是一个 list（类似的数据格式）
#  kwargs 有两个 *   表示的是一个 dict（类似的数据格式）

# Decorator 也可以使用class样式

class myDecorator(object):
    def __init__(self,fn):
        print("inside myDecorator.__init__*()")
        self.fn = fn
    def __call__(self, *args, **kwargs):
        self.fn()
        print("inside myDecorator.__call__()")

@myDecorator
def aFunc():
    print("inside aFunc()")
# 初始化 myDecorator 类
print("finish decorator aFunc()")
# 运行func
aFunc()
# result:
# inside myDecorator.__init__*()
# finish decorator aFunc()
# inside aFunc()
# inside myDecorator.__call__()

class makeHtmlTagClass():
    def __init__(self,tag,css_class):
        self.tag = tag
        self.css_class = " class = '{0}'".format(css_class)\
                                            if css_class != "" else ""
    def __call__(self, fn):
        def wrapper(*args,**kwargs):
            return "<" + self.tag + self.css_class + ">" + fn(*args,**kwargs) + "</" + self.tag +">"
        return wrapper

@makeHtmlTagClass(tag="b",css_class="blod_class")
@makeHtmlTagClass(tag="a",css_class="")
def html(arg):
    return "hi,this is decorator class, {0},{1} ".format(arg,str(html.__name__))
print(html("html"))

# 装饰器的副作用
# 因为 decorator 的因素，我们原本的函数已经变成一个叫做wrapper的函数
# 比如 再调用 __name__() ，他会告诉你 ，这是wrapper，而不是 之前的函数名
# 当然，功能是不受任何影响的，有些人会不爽
# 在functool 包中提供了一个叫wrap的decorator 来消除副作用 ：
from functools import wraps
def hello2(fn):
    @wraps(fn)
    def wrapper():
        print("hello,{}".format(fn.__name__))
        fn()
        print("goodbye,{}".format(fn.__name__))
    return wrapper

@hello2
def test1():
    print("test wrap {}".format(test1.__name__))

test1()

# 示例：斐波那契数列
def memo(fn):
    cache = {}
    miss = object()
    @wraps(fn)
    def wrapper(*args):
        result = cache.get(args,miss)
        if result is miss :
            # print("miss")
            result = fn(*args)
            cache[args] = result
        # print("arg:",args,"cache:",cache)
        return result
    return wrapper

@memo
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
print(fib(10))


# 偏函数
print("12345",int("12345"))
print("12345",int("12345",base = 8))
print("12345",int("12345",base = 16))
print("12345",int("101101",base = 2))

# functools.partial 就是帮助我们创建一个偏函数的，不需要我们自己定义int2()，可以直接下面创建一个新的函数int2()
from functools import partial
int2 = partial(int,base=2)
print(int2("10001"))
kw = {"base":2}
print(int("100010",**kw))
max2 = partial(max,6)
print(max2(5,6,7))
l = [1,2,3,4,5,6,7,7,8]
l1=[10,9,8]
max3 = partial(max,*l)
print(max3(10))


# 作业：
# 结合上一节课作业，完善





