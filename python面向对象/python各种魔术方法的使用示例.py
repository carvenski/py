#encoding=utf-8

# ------------------------------------------------------------------------------------------------
# class A叫做'旧式类',class A(object)叫做'新式类'(它们在多重继承和@property等处会体现出区别)
class A(object):  # class A
    #类变量
    x = 'test class variable'
    
    #类私有变量
    __y = 'test private class variable'

    #类变量可以在实例方法和类方法中使用self和cls来访问,或对象和类也可访问.
    #实例变量只能在实例方法中使用self访问,或对象直接访问.
    #即:类变量和类方法对象也可访问,但实例变量和实例方法只能实例可访问.
    
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
b = B()
print dir(b)
print dir(B)
b.a()
B.a_()
B.a__()

# ------------------------------------------------------------------------------------------------
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
#python class的各种魔术方法使用示例:

















