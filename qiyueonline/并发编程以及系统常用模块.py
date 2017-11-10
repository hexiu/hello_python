"""
主要内容：
python 多进程与多线程的实现
python使用hadoop分布式计算库 mrjob
python使用spark分布式计算库 pyspark
例子： 分别使用mapReduce 和 Spark 实现wordcount
正则表达式简介
日期和时间
常用内置模块 collections  itertools
"""

# 进程与线程
# 进程：程序的一次执行（程序装载入内存，系统分配资源运行）
# # 每个进程有自己的内存空间，数据栈等，只能使用进程间通信，而不能直接共享信息
# 线程：所有线程运行在同一个进程中，共享相同的运行环境
# # 每个独立的线程有一个程序运行入口，顺序执行序列和程序的出口
# # 线程的运行可以被抢占（中断），或者暂时挂起（睡眠），让其他的线程运行（让步）
# # 一个进程中的各个线程间共享同一个数据空间.

# 全局解释器锁GIL
# GIL 全称为 全局解释器锁 (global Interpreter Lock),GIL并不是python的特性,它是在实现python解析器(Cpython)时所引入的一个概念
# GIL是一把全局排他锁,同一时刻只有一个线程在运行,
# # 毫无疑问全局锁的存在会对多线程的效率有不小的影响,甚至就几乎等于python是个单线程的程序
# # mulitiprocessing库的出现很大程度上为了弥补thread库因为GIL而低效的缺陷，它完整的复制了一套thread所提供的接口方便迁移，唯一不同就是它使用了多进程而不是多线程，
# # 每个进程有自己的独立GIL,因此不会出现进程间的GIL争抢

# 顺序执行单线程 与 同时执行两个并发线程
from threading import Thread
import time

def my_counter():
    i = 0
    for _ in range(100000000):
        i = i + 1
    return True

# 顺序执行的单线程
# main1
def main1():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print("main1 Total Time: {} ".format(end_time - start_time))

# 同时执行的两个并发线程
# main2
def main2():
    thread_array = {}
    start_time = time.time()
    for tid in range(2):
        t = Thread(target = my_counter)
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print("main2 Total time: {} ".format(end_time - start_time))

# main1()
# main2()

# join() 阻塞进程直到线程执行完毕

# python 多进程
# fork 操作
# # 调用一次，返回两次，因为操作系统自动把当前的进程称为父进程，复制了一份（称为子进程），然后分别在父进程和子进程内返回，子进程永远返回0，
# # 而父进程返回子进程的进程ID，子进程只需要调用getppid()就可以获得父进程的ID
# import os
#
# print('Process (%s) start ....' % os.getpid())
# pid = os.fork()
# if pid == 0 :
#     print("I am child process (%s) and my parent is %s . " % (os.getpid(),os.getppid()))
# else:
#     print("I (%s) just created a child process (%s)." % (os.getpid(),pid))

# 由于windows没有 fork() ， 以上代码 故windows下无法运行

# multiprocessing
# multiprocessing 是跨平台版本的多进程模块，它提供了一个Process类，来代表一个进程对象，下面是示例代码：
from multiprocessing import Process
# 前面已经引用过
# import time
def f(n):
    # 没有sleep（） 可能不会顺序输出
    # time.sleep(1)
    print(n*n)

# if __name__ == '__main__':
#     for i in range(10):
#         p = Process(target=f,args=[i,])
#         p.start()
#         # 使用join（） 同样可以保证顺序输出
#         # p.join()

# 以上程序如果是单进程需要10s执行时间，而多进程为10个进程并行执行，只需1s多的时间


# 进程间通讯 queue
# Queue 是多进程安全的队列，可以使用Queue实现多进程之间的数据传递
from multiprocessing import Process,Queue
# import time
def write(q):
    for i in ['A','B','C','D','E']:
        print('Put %s to queue ' % i )
        q.put(i)
        time.sleep(0.1)

def read(q):
    while True:
        v = q.get(True)
        print('Get %s from Queue ' % v)

# if __name__ == '__main__':
#     q = Queue()
#     pw = Process(target=write,args=(q,))
#     pr = Process(target=read,args=(q,))
#     pw.start()
#     pr.start()
#     pr.join()
#     pr.terminate()


# 进程池 Pool
# 用于批量创建子进程 ， 可以灵活控制子进程的数量
from multiprocessing import Pool
import time
def func(x):
    print(x*x)
    time.sleep(0.1)
    return x*x

# if __name__ == '__main__':
#     # 定义启动的进程数量
#     pool = Pool(processes=5)
#     res_list = []
#     for i in range(10):
#         # 以异步并行的方式启动程序，如果要同步等待的方式，可以再每次启动进程后，调用res.get()方法，也可以使用pool.apply()
#         # res = pool.apply_async(func,[i,])
#         res = pool.apply(func,[i,])
#         # res.get()
#         print("-----------------------------------:",i)
#         res_list.append(res)
#     pool.close()
#     pool.join()
#     for r in res_list:
#         # print("result",(r.get(timeout=1)))
#         print("result",r)


# 多进程与多线程对比
# 在一般情况下 多个进程的内存资源是相互独立的，多个线程可以共享同一进程中的内存资源

# from multiprocessing import Process
import threading
# import time
lock = threading.Lock()

def run(info_list,n):
    lock.acquire()
    info_list.append(n)
    lock.release()
    print("%s" % info_list)

# if __name__ == '__main__':
#     info = []
#     for i in range(10):
#         # target 为子进程执行程序，args传参
#         p = Process(target=run,args=[info,i])
#         p.start()
#         p.join()
# # 这里的time sleep 为了让输出整齐，让主进程的执行等一下子进程
#     time.sleep(1)
#     print("--------------threading---------------")
#     for i in range(10):
#         p = threading.Thread(target=run,args=[info,i])
#         p.start()
#         p.join()


# 函数式编程
# 三大特性
# # immutable data 不可变数据
# # first class function 函数像变量一样使用
# # 尾递归优化，每次递归重用stack

# 好处：
# # parallelization 并行
# # lazy evaluation 惰性求值
# # determinism 确定性

# 函数式编程：
# http://coolshell.cn/artucles/10822.html

# 函数式编程技术
# 技术
# 实例：
def inc(x):
    def incx(y):
        return x+y
    return incx
inc2 = inc(2)
inc5 = inc(5)
print(inc2(5))
print(inc5(7))

# #  map & reduce
# #  pipeline
# #  recursing
# #  currying
# #  higher Order function 高阶函数
# #


# python 中的 lamba ， map ， filter ， reduce
g = lambda x : x * 2
print(g(2))
print((lambda x:x*4)(4))

for n in ['qi','yue','he']:
    print(len(n))

name_len = map(len,['qi','yue','he'])
print(list(name_len))

def toUpper(item):
    return item.upper()

upper_name = map(toUpper,['qi','yue','he'])
print(list(upper_name))

items = [1,2,3,4,5,-6]
for i in items:
    print(i**2)

square = list(map(lambda i:i**2,items))
print(square)

filter_r = list(filter(lambda x:x<3,items))
print(filter_r)

from functools import reduce
reduce_r = reduce(lambda x,y:x+y,items)
print(reduce_r)
# 求数列平均数
rel = reduce(lambda x,y:x+y ,items)/len(items)
# 求数列中正数的平均数
rel_z = reduce(lambda x,y:x+y ,filter(lambda x:x>0,items))/len(items)
print(rel,rel_z)

# Hadoop
# Apache 开源组织的一个分布式开源框架
# 核心设计： MapReduce 和 HDFS（Hadoop Distributed File System）
# MapReduce 思想：任务的分解与结果的汇总

# 基于Linux管道的 MapReduce
# map
import sys
with open("output.txt","w") as f :
    for line in open("input.txt","r") :
        ls = line.split(',')
        for word in ls:
            if len(word.strip()) != 0 :
                f.write(word + ',' + str(1) + "\n")

# reduce
import sys
word_dict = {}
for line in open("output.txt","r"):
    ls = line.split(',')
    word_dict.setdefault(ls[0],0)
    word_dict[ls[0]] += int(ls[1])

for word in word_dict:
    print(word,word_dict[word])

# 基于linux 管道的MapReduce
# cat wordcount.input | python mapper.py | python reducer.py | sort -k 2r
# 将上述的代码的文件操作 全部改为 os.stdin 即可，将map的结果不写文件 输出即可


# Hadoop Streaming & mrjob
# # Hadoop 有 java 和 Streaming 两种方式来编写MapReduce 任务
# # java 的优点是 计算效率高，并且部署方便，直接打包成一个jar文件就行了
# # Hadoop Steaming 是 Hadoop 提供的一个编程工具，它允许用户使用任何可执行文件或者脚本文件作为 Mapper 和 Reducer

# Streaming 单机测试
# # cat input | mapper | sort | reducer > output
# mrjob 实质上就是在Hadoop Steaming 的命令行上包了一层，有了统一的python界面，无需你再去直接调用 Hadoop Streaming 命令。

# Hadoop 实例 eg ：
# HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop -*- streaming.jar \
# -input myInputDirs \
# -output myOutputDir \
# mapper Mapper.py
# reducer Reducerr.py
# file Mapper.py
# file reducer.py

# mrjob 实现 wordcount
from mrjob.job import MRJob
class MRWordFrequencyCount(MRJob):
    def mapper(self,_,line):
        yield "chars",len(line)
        yield "words",len(line.split())
        yield "lines",1
    def reducer(self,key,values):
        yield key,sum(values)

# if __name__ == '__main__':
#     MRWordFrequencyCount.run()

# Spark 是基于map reduce 算法实现的分布式计算框架
# # Spark 的中间输出和结果输出 可以保存在内存中，从而不再需要读写hdfs
# # Spark 能更好的用于数据挖掘与机器学习等需要的迭代map reduce的算法中

# Spark SQL |  Spark Streaming | Mlib（machine learning）| GraphX（graph）
#            Apache Spark

# spark 与 hadoop 的结合
# Spark 可以直接对 HDFS 进行数据的读写，同样支持 Spark on YARN，Spark 可以与MapReduce 云运行于相同的集群中，共享存储资源与计算
# # 本地模式
# # standalone 模式
# # Mesoes 模式
# # yarn 模式

# RDD （Spark 核心）
# 弹性分布式数据集 Resilient Distributed  Datasets
# # 集群节点上不可变，已分区对象
# # 可序列化
# # 可以控制存储级别，（内存，硬盘）来进行重用
# 计算特性
# # 血统 lineage
# # 惰性计算 lazy evaluation
# 生成方式
# # 文件读取
# # 来自父RDD

# 算子 Transformation & Actions
# 查看一个表

# Spark 运算逻辑
# 查询资料进行理解
# spark 几乎都在内存中操作，故spark运算会比hadoop 快一些

# PySpark 实现 WorkCount
# # import sys
# from operator import add
# from pyspark import SparkContext
# sc = SparkContext()
# lines = sc.textFile("stormofswords.csv")
# counts = lines.flatMap(lambda x:x.split(","))\
#             .map(lambda x:(x,1))\
#             .reduceByKey(add)
# output = counts.collect()   # [RDD 序列化的输出 ]
# output = filter(lambda x:not x[0].isnumer(),sorted(output,key=lambda x:x[1],reverse= True))   # 过滤信息
# for (word,count) in output[:10]:
#     print("%s:%i" % (word,count))
# sc.stop()

# 可以使用内存做cache ， 例如斐波那契数列 ， spark 比 hadoop 快 百倍

# 正则表达式
# 两种模式匹配 ， 搜索 search（） 和 匹配 match（）
import re
with open("input.txt") as f :
    data = f.read()
    print(data)
    m = re.match(r'l',data)
    print(m.group())
    m1 = re.search(r'a.*',data)
    print(m1.group())
    m2 = re.findall(r'a.',data)
    print(m2)
    m3 = re.search(r'(\w+),(\w+),',data)
    print(m3.group(2))
    print(m3.group(1))
    print(m3.group(0))

# group 分组,见上面
# 匹配邮箱 r'[\w.-]+@[\w.-]+'

# 时间和日期模块
# time datetime
import time
print(time.localtime())
print(time.localtime().tm_year)

# 有用的内建函数
# enumerate
l = [1,2,3]
for i in range(len(l)):
    print(i,l[i])

for index,text in enumerate(l):
    print(index,text)

# 集合模块 collections
# collections 是python内建的一个集合模块，提供了许多有用的集合
# deque 是为了高效的实现插入和删除操作的双向列表，适用于队列和栈
# OrderedDict 的key 会按照插入顺序进行顺序排列
# Counter 是一个简单的计数器，也是dict的一个子类

# 迭代器 itertools  (查资料)
# 为类序列对象提供一个类似序列的接口
# 无限迭代器
#  count()     cycle()      repeat()
# 在最短输入序列终止的迭代器
# chain()  izip()等等
# 代码示例
# from itertools import repeat,count
# print(list(repeat(10,3)))
# for i in count(20):
#     print(i)
#     if i>30 :
#         break
# 组合生成器
# product()
# permutations() 等的
from itertools import product,permutations,combinations,combinations_with_replacement
print(list(product('ABC',repeat=2)))
print(list(permutations('ABC',2)))
print(list(combinations('ABC',2)))
print(list(combinations_with_replacement('ABC',2)))

# 好好学习，还需更多的投入
# 2017/11/10 星期五
# jaxiu 西安邮电大学东区 宿舍








