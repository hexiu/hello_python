# 面向对象相关基础

"""
类：具有相同属性的集合
对象：object  类的实例

类的命名规则：使用驼峰命名法
"""
class Foo(object):
    name = "axiu"
    def bar(self):
        print("you are %s" % self.name)
        print("bar")
    def hello(self,name):
        print("i am %s" % name)

f = Foo()
f.bar()
f.hello("jaxiu")

# 构造函数
class Foo1(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def hi(self):
        print("I am %s,age is %d" % (self.name,self.age))

axiu = Foo1("jaxiu",21)
axiu.hi()

# 访问限制
axiu.age = 22
axiu.hi()

class Student(object):
    def __init__(self,name,age):
        self.__name = name
        self.__age = age

    def hi(self):
        print("I am ",self.__name,"My age is ",self.__age)

    def set_age(self,age):
        self.__age=age

axiu1 = Student("jaxiu",23)
axiu1.hi()
axiu1.set_age(26)
axiu1.hi()

# 面向对象的三大特性      封装、继承、多态
# 封装   (以上就是封装)

class Student1(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def detail(self):
        print(self.name,self.age)

class PrimaryStudent(Student1):
    def lol(self):
        print(self.name,"不服来战")

class CollegeStudent(Student1):
    def __init__(self,name,age,gf):
        self.name = name
        self.age = age
        self.gf = gf
    def gf_detail(self):
        print("GF:",self.gf)

pstu = PrimaryStudent("jaxiu",33)
pstu.lol()
pstu.detail()
cstu = CollegeStudent("axiu",23,"lmw")
cstu.detail()
cstu.gf_detail()

#  注不可以使用隐藏变了，使用隐藏变量容易出现莫名奇妙的问题

# 多类继承
# 查找类的方法
# 经典类 使用深度优先检索
# 新的类 使用广度优先检索

# 经典类的写法
class c1 :
    pass
class c2(c1):
    pass

# 新类
class N1(object):
    pass
class N2(N1):
    pass

# eg:
class D(object):
    def bar(self):
        print("D.bar")

class C(D):
    def bar(self):
        print("C.bar")
    # pass

class B(D):
    pass

class A(B,C):
    pass

a = A()
a.bar()
# 当前使用的方式都是 广度优先，故结果是 C.bar


# 多态
# python 本身是不支持多态的，也用不到多态，多态的概念一般用于 java和C# 这一类强类型的语言中，而python 崇尚 “鸭子类型（Duck Typing）”





