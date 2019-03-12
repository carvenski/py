# encoding=utf-8 

# re模块 ： # 常用 正则表达式 写法：
re.findall('[a-z][0-9]', 'a2s3d4f5')  # return a list of all matched substr.
'''
---------------------------------------------------------------------------------------------
\d     一个数字 = [0-9], \D是非数字
\w     一个字母/数字/下划线
.      匹配除换行符\n之外的任意一个字符
*      匹配前一个字符0次或无限次
+      匹配前一个字符1次或无限次
?      匹配前一个字符0次或1次
{n}    匹配前一个字符n次. 
{m, n} 匹配前一个字符m次到n次(省略m默认m=0,省略n默认n=无限次)   
[]     在此范围内的如 [a-z] [0-9].  []里面加上^则是取反
\      转义字符,如匹配字符串中的 1*,则需要写成 1\* 即可
\s     匹配空格符/制表符/回车符等表示分隔意义的字符,它等价于[ /t/r/n/f/v](注意最前面有个空格). \S是非空白字符
^      严格匹配行首
$      严格匹配行尾
|      或者,如 [a-z|\*]

()           匹配()中的正则表达式,并且一个()自动作为一个`组`,组号默认从1递增,后面可用\组号来引用该组匹配到的字符
(?P<name>)   除了原有的数字组号,给组起个名字,后面可用(?P=name)来引用该组匹配到的字符
			 (注意：re.findall()函数只返回()里匹配的字符.)
---------------------------------------------------------------------------------------------
'''

import random
random.random()        #产生一个0-1之间的随机的浮点数
random.randrange(1, 10)   #随机产生一个1-9的数


range(1, 10, 2) # start ,stop(不取), step
range(5)        # [0,1,2,3,4] 默认从0开始
 

os.system('ls')  #执行命令


module = __import__('module_name')
func = getattr(module, 'function_name')


sys.path           #返回模块的搜索路径
os.path            # 文件路径

os.getcwd()  #获取当前工作目录
os.remove()  #删除一个文件
os.mkdir('dirname')  

'1:2:3:4'.split(':', 2)  # 分割字符串 2次 
'xxxxx'.replace('old', 'new')
' xxxooo  '.strip()             # 去掉字符两边的空格和回车换行符  


sys.argv  # 执行脚本时的 参数列表


## open函数的 'r/w/+' 意思是  '读/写/追加'
with open('xx.txt', 'rw') as f:
	print f.read() # read all lines 

with open('xx.txt', 'rw') as f:
	for line in f.readlines():    # list of lines  //而readline函数是一次读一行
		print line

with open('xx.txt', 'rw') as f:
	for line in f: print line     # 等于 readlines()


import traceback
traceback.print_exc()


# 无锁线程
def test():
	print 'test'
import threading  
t = threading.Thread(target=test, args=[], kwargs={})   # 当然可传参数
t.start()  

# 加锁线程
import threading
mutex = threading.Lock() #创建锁对象  
def test():  
    mutex.acquire() #加锁  
    print 'test'  
    mutex.release() #解锁   
for i in range(5):  
    t = threading.Thread(target=test, args=[], kwargs={})  
    t.start()  


import webbrowser
webbrowser.open("http://www.baidu.com")


# profile模块 + pstats模块是标准 Python 性能分析器.  $ profile.py hello.py
import profile
import pstats
def func():
    for i in range(1000):
        print i
profile.run("func()")
# or
p = profile.Profile()
p.run("func()")
s = pstats.Stats(p)
s.sort_stats("time", "name").print_stats()


import datetime
datetime.datetime.now()  # datetime 对象
datetime.datetime.now().__str__()  # 转成了str

import time
time.time()  #时间戳
time.clock()  #当前时间

time.sleep(10) # 睡眠10s


# copy模块：  
copy.copy(a)        #复制对象        潜拷贝    传值
copy.deepcopy(a)    #复制对象的引用  深拷贝    传引用


from collections import namedtuple
Point=namedtuple('Point', ['x', 'y'])  # 只存属性的 类
p = Point(1, 2)
print p.x   


# six : Six is a Python 2 and 3 compatibility library


dir()/vars()/help()  # python的 帮助函数,非常好用.


hasattr(obj,name) # 查看一个obj的name space中是否有name
getattr(obj,name) # 得到一个obj的name space中的一个name
setattr(obj,name,value) # 为一个obj的name space中的一个name指向vale这个object
delattr(obj,name) # 从obj的name space中删除一个name


locals()  #返回一个局部name space,用dictionary表示
globals() #返回一个全局name space,用dictionary表示


any()  # Return True if bool(x) is True for any x in the iterable.        If the iterable is empty, return False.
all()  # Return True if bool(x) is True for all values x in the iterable. If the iterable is empty, return True.


round(1.2345, 2)  # 保留2位小数
sorted([1,5,3], key=lambda i: i['name'], reverse=True)  # 排序

enumerate(iterable)  #show (index, value) of iterable, index default to 0,
for i in enumerate(['a','b','c']): print i  # (0,'a') (1,'b') (2,'c')  利用enumerate()函数,可以在每次循环中同时得到下标和元素


'_'.join([1,2,3])  #就是把一个list中所有的串按照你定义的分隔符连接起来



# 单例模式：
class Singleton(object):
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

# 共享属性：
clas Box(object):
    _dict = {}
    def __new__(cls, *args, **kwargs):
        ob = super(cls, *args, **kwargs).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._dict
        return ob

# 装饰器版本单例模式写法：
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances：
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]
    return get_instance

@singleton
class ClassName(object):
    pass    


# import 实现的单例模式：
# mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass
 
my_singleton = My_Singleton()
 
# to use
from mysingleton import my_singleton
my_singleton.foo()

"""
GIL:python线程全局锁
线程全局锁(Global Interpreter Lock),即Python为了保证线程安全而采取的独立线程运行的限制,说白了就是一个核只能在同一时间运行一个线程.
解决办法就是多进程和下面的协程(协程也只是单CPU,但是能减小切换代价提升性能).
协程
简单点说协程是进程和线程的升级版,进程和线程都面临着内核态和用户态的切换问题而耗费许多切换时间,而协程就是用户自己控制切换的时机,不再需要陷入系统的内核态.
Python里最常见的yield就是协程的思想!可以查看第九个问题
"""

# is是对比地址, ==是对比值

#  鸭子类型:

# “当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”

# 我们并不关心对象是什么类型，到底是不是鸭子，只关心行为。

# 比如在python中，有很多file-like的东西，比如StringIO,GzipFile,socket。它们有很多相同的方法，我们把它们当作文件使用。

# 又比如list.extend()方法中,我们并不关心它的参数是不是list,只要它是可迭代的,所以它的参数可以是list/tuple/dict/字符串/生成器等.

# 鸭子类型在动态语言中经常使用，非常灵活，使得python不想java那样专门去弄一大堆的设计模式。


# decorator
import time  
   
def timeit(func):  
    def wrapper():  
        start = time.clock()  
        func()  
        end =time.clock()  
        print 'used:', end - start  
    return wrapper  
   
@timeit  
def foo():  
    print 'in foo()'  
   
foo()  


# 归并相同key的值到list, 使用defaultdict(list)
import collections
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = collections.defaultdict(list)
for k, v in s:
    d[k].append(v)  # 就是将该dict的 k:v 的 v 都默认设置成 list 了 
list(d.items())



# 冒泡排序
def bubble(l):
    # for i in l[1:]:
        # index_i = l.index(i)   ## 使用l.index函数的问题就在于 `相同数的索引只取前一个` !! 会导致错误
    for index_i in range(1, len(l) ):
        def x(index_i):         
            if index_i >= 1:
                if l[index_i] <= l[index_i-1]:
                    l[index_i-1], l[index_i] = l[index_i], l[index_i-1]
                index_i = index_i - 1
                x(index_i)
        x(index_i)
    return l
   
print bubble([222,221,5,2000, 5,1,13, 12,6,999,333,23,2000,4,9,333,45,90,2,0, 777,120,456]) 


# 进程池
import multiprocess
class ProcessPool(object):
    def __init__(self, total):
        self.total = total
        self.current = 0

    def run(self, func, args=(), kwargs={}):
        while self.current < self.total:
            self._run(self, func, args, kwargs)

    def _run(self, func, args, kwargs):
        p = multiprocess.Process(target=func, args=args, kwargs=kwargs)
        p.start()   # tip: process will exit automatical when it's task is over
        self.current += 1

# 函数参数不能出现: 默认值=list 的写法 !! 这是python的一个bug !!
def x(a, b=[])
    b.append(a)  # 这个list b 在内存里不会被回收, x函数会使用同一个 list !!
    print b


























