理解Python并发编程一篇就够了 - 进程篇

在上一节理解Python并发编程一篇就够了 - 线程篇讲了一些线程的技术，本节我们接着说进程。

上节说到由于GIL（全局解释锁）的问题，多线程并不能充分利用多核处理器，如果是一个CPU计算型的任务，应该使用多进程模块 multiprocessing 。
它的工作方式与线程库完全不同，但是两种库的语法却非常相似。multiprocessing给每个进程赋予单独的Python解释器，这样就规避了全局解释锁所带来的问题。

我们首先把上节的例子改成单进程和多进程的方式来对比下性能：

```python
import time
import multiprocessing
def profile(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)
        end   = time.time()
        print 'COST: {}'.format(end - start)
    return wrapper
def fib(n):
    if n<= 2:
        return 1
    return fib(n-1) + fib(n-2)
@profile
def nomultiprocess():
    fib(35)
    fib(35)
@profile
def hasmultiprocess():
    jobs = []
    for i in range(2):
        p = multiprocessing.Process(target=fib, args=(35,))
        p.start()
        jobs.append(p)
    for p in jobs:
        p.join()
nomultiprocess()
hasmultiprocess()
```

运行的结果还不错：

1
2
3

	

❯ python profile_process.py
COST: 4.66861510277
COST: 2.5424861908

虽然多进程让效率差不多翻了倍，但是需要注意，其实这个时间就是2个执行fib(35)，最慢的那个进程的执行时间而已。不管怎么说，GIL的问题算是极大的缓解了。
进程池

有一点要强调：任务的执行周期决定于CPU核数和任务分配算法。
上面例子中hasmultiprocess函数的用法非常中规中矩且常见，但是我认为更好的写法是使用Pool，也就是对应线程池的进程池:


```python
from multiprocessing import Pool
pool = Pool(2)
pool.map(fib, [35] * 2)
```
其中map方法用起来和内置的map函数一样，却有多进程的支持。

PS: 之前在一分钟让程序支持队列和并发，我就提到过使用multiprocessing.Pool实现纯Python的MapReduce。有兴趣的可以去了解下。
dummy

我之前使用多线程/多进程都使用上面的方式，在好长一段时间里面对于多进程和多线程之前怎么选择都搞得不清楚，
偶尔会出现要从多线程改成多进程或者多进程改成多线程的时候，痛苦。看了一些开源项目代码，我发现了好多人在用multiprocessing.dummy这个子模块，
「dummy」这个词有「模仿」的意思，它虽然在多进程模块的代码中，但是接口和多线程的接口基本一样。官方文档中这样说：

    multiprocessing.dummy replicates the API of multiprocess    
    ing but is no more than a wrapper around the threading
    module.

恍然大悟！！！如果分不清任务是CPU密集型还是IO密集型，我就用如下2个方法分别试：

```python
from multiprocessing import Pool
from multiprocessing.dummy import Pool
```
哪个速度快就用那个。从此以后我都尽量在写兼容的方式，这样在多线程/多进程之间切换非常方便。

在这里说一个我个人的经验和技巧：现在，如果一个任务拿不准是CPU密集还是I/O密集型，且没有其它不能选择多进程方式的因素，都统一直接上多进程模式。
基于Pipe的parmap

进程间的通信（IPC）常用的是rpc、socket、pipe（管道）和消息队列（queue）。多进程模块中涉及到了后面3种。我们先看一个官网给出的，最基本的管道的例子：

```python
from multiprocessing import Process, Pipe
def f(conn):
    conn.send(['hello'])
    conn.close()
parent_conn, child_conn = Pipe()
p = Process(target=f, args=(child_conn,))
p.start()
print parent_conn.recv()
p.join()
```
其中Pipe返回的是管道2边的对象：「父连接」和「子连接」。当子连接发送一个带有hello字符串的列表，父连接就会收到，所以parent_conn.recv()就会打印出来。
这样就可以简单的实现在多进程之间传输Python内置的数据结构了。但是先说明，不能被xmlrpclib序列化的对象是不能这么传输的。

上上个例子中提到的hasmultiprocess函数使用了Pool的map方法，用着还不错。但是在实际的业务中通常要复杂的多，比如下面这个例子：

```python
class CalculateFib(object):
    @classmethod
    def fib(cls, n):
        if n<= 2:
            return 1
        return cls.fib(n-1) + cls.fib(n-2)
    def map_run(self):
        pool = Pool(2)
        print pool.map(self.fib, [35] * 2)
        
cl = CalculateFib()
cl.map_run()
```
fib由于某些原因需要放在了类里面，我们来执行一下：

❯ python parmap.py
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 810, in __bootstrap_inner
    self.run()
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 763, in run
    self.__target(*self.__args, **self.__kwargs)
  File "/Library/Python/2.7/site-packages/multiprocessing-2.6.2.1-py2.7-macosx-10.9-intel.egg/multiprocessing/pool.py", line 225, in _handle_tasks
    put(task)
PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed

欧欧，出错了。解决方案有很多。我们先演示一个使用管道处理的例子：

```python
from multiprocessing import Pool, Process, Pipe
from itertools import izip
def spawn(f):
    def func(pipe, item):
        pipe.send(f(item))
        pipe.close()
    return func
def parmap(f, items):
    pipe = [Pipe() for _ in items]
    proc = [Process(target=spawn(f),
                    args=(child, item))
            for item, (parent, child) in izip(items, pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [parent.recv() for (parent, child) in pipe]
    
    
class CalculateFib(object):
    ...
    def parmap_run(self):
        print parmap(self.fib, [35] * 2)
    
    
cl = CalculateFib()
cl.parmap_run()
```
这个parmap的作用就是对每个要处理的单元（在这里就是一次 fib(35)）创建一个管道，在子进程中，子连接执行完传输给父连接。

它确实可以满足一些场景。但是我们能看到，它并没有用进程池，也就是一个要处理的单元就会创建一个进程，这显然不合理。
队列

多线程有Queue模块实现队列，多进程模块也包含了Queue类，它是线程和进程安全的。现在我们给下面的生产者/消费者的例子添加点难度，也就是用2个队列：
一个队列用于存储待完成的任务，另外一个用于存储任务完成后的结果：

```python
import time
from multiprocessing import Process, JoinableQueue, Queue
from random import random
tasks_queue = JoinableQueue()
results_queue = Queue()
def double(n):
    return n * 2
def producer(in_queue):
    while 1:
        wt = random()
        time.sleep(wt)
        in_queue.put((double, wt))
        if wt > 0.9:
            in_queue.put(None)
            print 'stop producer'
            break
def consumer(in_queue, out_queue):
    while 1:
        task = in_queue.get()
        if task is None:
            break
        func, arg = task
        result = func(arg)
        in_queue.task_done()
        out_queue.put(result)
processes = []
p = Process(target=producer, args=(tasks_queue,))
p.start()
processes.append(p)
p = Process(target=consumer, args=(tasks_queue, results_queue))
p.start()
processes.append(p)
tasks_queue.join()
for p in processes:
    p.join()
while 1:
    if results_queue.empty():
        break
    result = results_queue.get()
    print 'Result:', result
```
咋眼看去，和线程的那个队列例子已经变化很多了：

    生产者已经不会持续的生产任务了，如果随机到的结果大于0.9就会给任务队列tasks_queue put一个None，然后把循环结束掉
    消费者如果收到一个值为None的任务，就结束，否则执行从tasks_queue获取的任务，并把结果put进results_queue
    生产者和消费者都结束后（又join方法保证），从results_queue挨个获取执行结果并打印出来

进程的Queue类并不支持task_done和join方法，需要使用特别的JoinableQueue，而搜集结果的队列results_queue使用Queue就足够了。

回到上个CalculateFib的例子，我们用队列再对parmap改造一下，让它支持指定进程池的大小：

```python
from multiprocessing import Queue, Process, cpu_count
def apply_func(f, q_in, q_out):
    while not q_in.empty():
        i, item = q_in.get()
        q_out.put((i, f(item)))
def parmap(f, items, nprocs = cpu_count()):
    q_in, q_out = Queue(), Queue()
    proc = [Process(target=apply_func, args=(f, q_in, q_out))
            for _ in range(nprocs)]
    sent = [q_in.put((i, item)) for i, item in enumerate(items)]
    [p.start() for p in proc]
    res = [q_out.get() for _ in sent]
    [p.join() for p in proc]
    return [item for _, item in sorted(res)]
```
其中使用enumerate就是为了保留待执行任务的顺序，在最后排序用到。
同步机制

multiprocessing的Lock、Condition、Event、RLock、Semaphore等同步原语和threading模块的机制是一样的，用法也类似，限于篇幅，就不一一的展开了。
进程间共享状态

multiprocessing提供的在进程间共享状态的方式有2种：
共享内存

主要通过Value或者Array来实现。常见的共享的有以下几种：

In : from multiprocessing.sharedctypes import typecode_to_type
In : typecode_to_type
Out:
{'B': ctypes.c_ubyte,
 'H': ctypes.c_ushort,
 'I': ctypes.c_uint,
 'L': ctypes.c_ulong,
 'b': ctypes.c_byte,
 'c': ctypes.c_char,
 'd': ctypes.c_double,
 'f': ctypes.c_float,
 'h': ctypes.c_short,
 'i': ctypes.c_int,
 'l': ctypes.c_long,
 'u': ctypes.c_wchar}

而且共享的时候还可以给Value或者Array传递lock参数来决定是否带锁，如果不指定默认为RLock。

我们看一个例子：
```python
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_bool, c_double
lock = Lock()
class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]
def modify(n, b, s, arr, A):
    n.value **= 2
    b.value = True
    s.value = s.value.upper()
    arr[0] = 10
    for a in A:
        a.x **= 2
        a.y **= 2
n = Value('i', 7)
b = Value(c_bool, False, lock=False)
s = Array('c', 'hello world', lock=lock)
arr = Array('i', range(5), lock=True)
A = Array(Point, [(1.875, -6.25), (-5.75, 2.0)], lock=lock)
p = Process(target=modify, args=(n, b, s, arr, A))
p.start()
p.join()
print n.value
print b.value
print s.value
print arr[:]
print [(a.x, a.y) for a in A]
```
主要是为了演示用法。有2点需要注意：

    并不是只支持typecode_to_type中指定那些类型，只要在ctypes里面的类型就可以。
    arr是一个int的数组，但是和array模块生成的数组以及list是不一样的，它是一个SynchronizedArray对象，支持的方法很有限，
    比如append/extend等方法是没有的。

输出结果如下：

1
2
3
4
5
6

❯ python shared_memory.py
49
True
HELLO WORLD
[10, 1, 2, 3, 4]
[(3.515625, 39.0625), (33.0625, 4.0)]

服务器进程

一个multiprocessing.Manager对象会控制一个服务器进程，其他进程可以通过代理的方式来访问这个服务器进程。
常见的共享方式有以下几种：

    Namespace。创建一个可分享的命名空间。
    Value/Array。和上面共享ctypes对象的方式一样。
    dict/list。创建一个可分享的dict/list，支持对应数据结构的方法。
    Condition/Event/Lock/Queue/Semaphore。创建一个可分享的对应同步原语的对象。

看一个例子：
```python
from multiprocessing import Manager, Process
def modify(ns, lproxy, dproxy):
    ns.a **= 2
    lproxy.extend(['b', 'c'])
    dproxy['b'] = 0
manager = Manager()
ns = manager.Namespace()
ns.a = 1
lproxy = manager.list()
lproxy.append('a')
dproxy = manager.dict()
dproxy['b'] = 2
p = Process(target=modify, args=(ns, lproxy, dproxy))
p.start()
print 'PID:', p.pid
p.join()
print ns.a
print lproxy
print dproxy
```
在id为8341的进程中就可以修改共享状态了：

❯ python manager.py
PID: 8341
1
['a', 'b', 'c']
{'b': 0}

分布式的进程间通信

有时候没有必要舍近求远的选择更复杂的方案，其实使用Manager和Queue就可以实现简单的分布式的不同服务器的不同进程间的通信（C/S模式）。

首先在远程服务器上写如下的一个程序：
```python
from multiprocessing.managers import BaseManager
host = '127.0.0.1'
port = 9030
authkey = 'secret'
shared_list = []
class RemoteManager(BaseManager):
    pass
RemoteManager.register('get_list', callable=lambda: shared_list)
mgr = RemoteManager(address=(host, port), authkey=authkey)
server = mgr.get_server()
server.serve_forever()
```
现在希望其他代理可以修改和获取到shared_list的值，那么写这么一个客户端程序：
```python
from multiprocessing.managers import BaseManager
host = '127.0.0.1'
port = 9030
authkey = 'secret'
class RemoteManager(BaseManager):
    pass
RemoteManager.register('get_list')
mgr = RemoteManager(address=(host, port), authkey=authkey)
mgr.connect()
l = mgr.get_list()
print l
l.append(1)
print mgr.get_list()
```
注意，在client上的注册没有添加callable参数。

