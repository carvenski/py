#encoding=utf-8

# ------------------------------------------------------------------------------------------------
# class A叫做'旧式类',class A(object)叫做'新式类'(它们在多重继承和@property等处会体现出区别)
class A(object):  # class A
    #类变量
    x = 'test class variable'
    
    #类私有变量
    __y = 'test private class variable'

    def __init__(self, arg='test instance variable'):
        self.arg = arg
        
    #类方法(必须加上@classmethod装饰器,否则无效)
    #仅仅修改self为cls是不够的,它们都只是形参而已!
    @classmethod
    def a_(cls):
        print cls.__y

    #静态方法(必须加上@staticmethod装饰器,否则无效)
    @staticmethod
    def a__(arg='test staticmethod'):
        print arg
        
    #实例方法
    def a(self):
        print self.arg
        
    #实例方法,只是加个_开头提示程序员应当视之为私有方法.
    def _a(self):
        print self.arg

    #类私有方法,仅可在类内部访问,也不会被继承.
    def __a(self):
        print self.arg

    #以__开头且结尾的方法是python的特殊魔术方法,可以从外部访问.
    #(自己写的方法不要以此方式命名!)
    def __a__(self):
        print '__a__'

class B(A):
    pass

#在内存中,类变量和类的所有方法(包括实例方法)都是存放在类本身的内存处,只有实例变量是存放在实例对象的内存处.
#每个对象都会存一个指向自己类的指针,然后使用类变量和方法时都靠指针来寻找并调用.
b = B()
print dir(b)
print dir(B)
b.a()
B.a_()
B.a__()

# ============================= python class的各种魔术方法使用示例 ================================================= #
#__enter__/__exit__
class TestContextManager(object):
    def __enter__(self):
        print('in __enter__')
        
    def __exit__(self, ex_type, ex_value, trace):
        print('in __exit__')
        #u can handle exception here or raise it 
        print(ex_type, ex_value, trace)
        #if return True  in __exit__, exception won't be raised outside !!
        #if return False in __exit__, exception will  be raised outside !!
        return True

with TestContextManager() as t:
    2/0

print('test exception in with-as raised outside')

# ------------------------------------------------------------------------------------------------
#__new__/__init__/__del__
from os.path import join

class FileObject:
    '''给文件对象进行包装从而确认在删除时文件流关闭'''

    def __init__(self, filepath='~', filename='sample.txt'):
        #读写模式打开一个文件
        self.file = open(join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file

class Word(str):
    def __new__(cls, word):
        # 注意我们必须要用到__new__方法，因为str是不可变类型, 所以我们必须在创建的时候将它初始化
        if ' ' in word:
            print "Value contains spaces. Truncating to first space."
            word = word[:word.index(' ')] #单词是第一个空格之前的所有字符
        return str.__new__(cls, word)
        #return super(Word, cls).__new__(cls, word)

# ------------------------------------------------------------------------------------------------
#__cmp__/__eq__/__ne__/__lt__/__gt__
class Word(str):
    '''存储单词的类，定义比较单词的几种方法'''
    def __new__(cls, word):
        # 注意我们必须要用到__new__方法，因为str是不可变类型
        # 所以我们必须在创建的时候将它初始化
        if ' ' in word:
            print "Value contains spaces. Truncating to first space."
            word = word[:word.index(' ')] #单词是第一个空格之前的所有字符
        return str.__new__(cls, word)

    def __eq__(self, other):
        return len(self) == len(other)
    def __gt__(self, other):
        return len(self) > len(other)
    def __lt__(self, other):
        return len(self) < len(other)
    def __ge__(self, other):
        return len(self) >= len(other)
    def __le__(self, other):
        return len(self) <= len(other)

w1 = Word('adddf')
w2 = Word('wef')
print(w1 == w2); print(w1 > w2); print(w1 >= w2)

# ------------------------------------------------------------------------------------------------
# 重载操作符(很少用到吧)
'''
__pos__ 实现正号的特性(比如 +some_object)
__neg__ 实现负号的特性(比如 -some_object)
__abs__ 实现内置 abs() 函数的特性。
__invert__ 实现 ~ 符号的特性。
__add__ 实现加法
__sub__ 实现减法
__mul__ 实现乘法。
__floordiv__ 实现 // 符号实现的整数除法
__div__ 实现 / 符号实现的除法
__mod__ 实现取模算法 % 
__divmod___ 实现内置 divmod() 算法
__pow__ 实现使用 ** 的指数运算
'''

# ------------------------------------------------------------------------------------------------
#__call__: 实现了__call__方法的类的对象,可以像函数那样被调用:
class A:
    def __init__(self):
        self.a = 0
    def __call__(self):
        print("=====haha, i'm instance, but i can be called like method...====")
        
aa = A() # A()是对象的新建然后初始化的过程,走的是__new__和__init__
aa()     # aa()就是把对象当函数那样调用,走的就是__call__


# ------------------------------------------------------------------------------------------------










