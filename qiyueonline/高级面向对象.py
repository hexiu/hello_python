# 高级面向对象编程
# __slots__  和 property
# 方法和属性的动态绑定
# 使用 __solts__  限定 class 实例能够添加的属性
# __solts__ 仅对当前类实例起作用，对继承的子类不起作用的
# 例子代码：
import traceback

from types import MethodType

class MyClass(object):
    # pass
    __slots__ = ['name','set_name']

def set_name(self,name):
    self.name = name

cls = MyClass()
cls.name = 'Tom'
cls.set_name = MethodType(set_name,cls)
cls.set_name("Jerry")
print(cls,cls.name)
# try:
#     cls.age = 30
# except AttributeError:
#     traceback.print_exc()
# print(cls,cls.name)

#  __slots__ 实例二  继承类
class ExClass(MyClass):
    pass

exclass = ExClass()
exclass.name = "Jerry"
exclass.age = 30
print(exclass.age,exclass.name)

# property 特性
# 直接暴露属性的局限性
# 使用 get/set 方法
# 利用@property 简化 get/set 方法
# 利用@property 实现只读属性
# 装饰器与property实现（学有余力的同学可以研究一下）
# 例子代码：
class Student(object):
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self,value):
        if not isinstance(value,int):
            raise ValueError("not int")
        elif (value < 0) or (value > 100):
            raise ValueError("not between 0 -- 100")
        self._score = value

    @property
    def double_score(self):
        return self._score * 2

s = Student()
s.score = 75
print(s.score)
# try:
#     s.score = "75"
# except ValueError:
#     traceback.print_exc()
# try:
#     s.score = 175
# except ValueError:
#     traceback.print_exc()
# print(s.double_score)
#
# try:
#     s.double_score = 130
# except AttributeError:
#     traceback.print_exc()

# 模拟实现一个property
# 课后自己baidu什么是描述器以及详细的应用 **
# 实现了 __set__ / __get__ / __del__ 方法的类称为描述器
class MyProperty(object):
    def __init__(self,fget = None,fset = None,fdel = None):
        print("__init__",fget)
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self,instance,cls):
        if self.fget:
            print("fget")
            return self.fget(instance)
    def __set__(self,instance,value):
        if self.fset:
            print("fset")
            return self.fset(instance,value)
    def __delete__(self,instance):
        if self.fdel:
            print("fdel")
            return self.fdel(instance)
    def getter(self,fn):
        self.fget = fn
    def setter(self,fn):
        self.fset = fn
    def deler(self,fn):
        self.fdel = fn

class Stu(object):
    @MyProperty
    def score(self):
        return self._score

    @score.setter
    def set_score(self,value):
        print(value)
        self._score = value

s = Stu()
s.score = 95
print(s.score,"rel")


# 控制类输出
class MyClass1:
    def __init__(self,name):
        self.name = name
    '''
    def __str__(self):
            return "hello "+self.name
    '''

print(MyClass1("jaxiu"),__name__)

# 迭代器
class Fib100(object):
    def __init__(self):
        self._1,self._2 = 0,1
    def __iter__(self):
        return self
    def __next__(self):
        self._1,self._2 = self._2 , self._1 + self._2
        if self._1 > 100:
            raise StopIteration()
        return self._1

for i in Fib100():
    print(i)

# 魔术函数，修改类的行为
class Fib():
    def __getitem__(self, item):
        # print(item)
        a,b = 1,1
        for i in range(item):
            a,b = b,a+b
        return a

f = Fib()
print(f[1])
print(f[5])
print(f[8])
# print(f[1:2:3])


# __call__,可以使实例可以被调用
class MyClass2():
    def __call__(self):
        print("You can call cls() directly.")

cls = MyClass2()
cls()
print(callable(cls))
print(callable(max))
print(callable([1,2,3,4]))
print(callable('str'))
print(callable(None))

# 枚举
from enum import Enum
Month = Enum('Month',('Jan','Feb','Mar','Apr'))
for name,member in Month.__members__.items():
    print(name,"=>",member,",",member.value)
# print(dir(Month),dir(Month.__members__))
jan = Month.Jan
print(jan)

##################################################################
# 元类
##################################################################
# 运行时动态创建 vs 编译时定义
# 使用type创建新类型
# metaclass（元类）
# # metaclass -> class -> instance
# # 继承和动态绑定可以解决问题吗？
# # __new__ 函数
# ORM 框架实例分析
# # 实例：
def init(self,name):
    self.name = name

def say_hello(self):
    print('Hello,%s !' % self.name)

# 注意第二个参数必须是元组，所以需要是(object,),使解释器认为是元组,以下方式都可以创建Hello 类
# Hello = type('Hello',(object,),dict(__init__=init,hello=say_hello))
Hello = type('Hello',(object,),{'__init__':init,'hello':say_hello})
################
# class Hello(object):
#   def __init__(): ...
#   def hello(): ...
################
h = Hello('jaxiu')
h.hello()

# 元类实例
#  __new__ 函数，控制类是如何实现的
# 使用最多的时 修改 attrs
def add(self,value):
    self.append(value)

#  metaclass 必须继承自type ，可以用于控制别的类的创建
class ListMetaClass(type):
    def __new__(cls, name,bases,attrs):
        print(cls)
        print(name)
        print(bases,type(bases))
        print(attrs,type(attrs))
        # attrs['add'] = lambda self,value:self.append(value)
        attrs['add'] = add
        attrs['name'] = 'Tom'
        return type.__new__(cls,name,bases,attrs)
class MyList(list,metaclass=ListMetaClass): #额外增加add方法，实际等价于append()
    pass

mli = MyList()
mli.add(1)
mli.add(2)
mli.add(3)
print(mli.name)
print(mli)

# ORM的实现
class Field:
    def __init__(self,name,col_type):
        self.name = name
        self.type = col_type
class IntegerField(Field):
    def __init__(self,name):
        super(IntegerField,self).__init__(name,'integer')
class StringField(Field):
    def __init__(self,name):
        super(StringField,self).__init__(name,'varchar(1024)')

class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name == "Model":
            return type.__new__(cls,name,bases,attrs)
        print("Model name: %s " % name )
        mappings = {}
        for k,v in attrs.items():
            if isinstance(v,Field):
                print('Field name : %s ' % k )
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)

class Model(dict,metaclass=ModelMetaclass):
    def __init__(self,**kwargs):
        super(Model,self).__init__(**kwargs)

    def __getattr__(self, key):
        try :
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        print(self.__mappings__)
        for k,v in self.__mappings__.items():
            print(k,v,"rel")
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self,k,None))
        print(fields,params,args)
        sql = 'insert into %s(%s) values(%s)' % (self.__table__,','.join(fields),','.join(params))
        print("sql",sql)
        print("args",args)

class User(Model):
    id = IntegerField('id')
    name = StringField('name')

# u = User(id=100,name='Tom')
u = User()
u.id = 100
u.name = 'Tom'
u.save()
print(u)

# super 是 调用 父类的构造函数 ，或者父类的方法

# 异常处理
# 为什么使用异常？
# 异常的抛出与捕捉
# traceback使用
# logging 使用与配置
# 实例
try :
    r = 10 / 1.0
except ZeroDivisionError as e:
    print(e)
    r = 1
else:
    print("no")
finally:
    print("on")
print(r)


# 单元测试
import unittest
class MyDict(dict):
    pass

class TestMyDict(unittest.TestCase):
    def setUp(self):
        print("测试前装备")
    def test_init(self):
        d = MyDict(one = 1,two = 2 )
        self.assertEqual(d['one'],1)
        self.assertEqual(d['two'],2)
    def tearDown(self):
        print("测试后清理")
    def test_nothing(self):
        pass

if __name__  == '__main__':
    unittest.main()

# python test_module.py
# python -m unittest test_module
# python -m unittest test_module.test_Class.
# python -m unittest test_module.Tese_Class.test_method








































# 作业
# 利用@property 给一个Screen 对象加上 width 和 height 属性，以及一个只读属性 resolution
# 自己实现一个orm 例子代码
# 实现一个类，支持以下方式输出小于1000的所有素数
# 查资料，使用getitem 实现切片

