#### 1.进程有自己独立的堆和栈,多进程的创建是linux fork原理,而多进程间的通信则是采用多进程共享内存实现的.
##### 共享内存（Shared Memory）是最简单的进程间通信方式，它允许多个进程访问相同的内存，一个进程改变其中的数据后，其他的进程都可以看到数据的变化。

共享内存是进程间最快速的通信方式：
｀进程共享同一块内存空间。
｀访问共享内存和访问私有内存一样快。
｀不需要系统调用和内核入口。
｀不造成不必要的内存复制。

内核不对共享内存的访问进行同步，因此程序员必须自己提供同步。

使用共享内存：
｀某个进程分配内存段。
｀使用这个内存段的进程要连接（attach）这个内存段。
｀每个进程使用完共享内存段后，要分离（detach）这个内存段。
｀在某个地方，必须有一个进程来销毁这个内存段。

Linux的内存模型：
｀每个进程的虚拟内存被分为页（page）。
｀每个进程维护自己的内存地址到虚拟内存页之间的映射。
｀实际的数据存在于进程的内存地址上。
｀尽管每个进程有自己的地址空间，多个进程的映射还是可以指向相同的页。

所有的共享内存段的大小，都是Linux内存页大小的整数倍。
Linux的页大小是4KB，不过程序员应该使用getpagesize函数来获得这个值。

=====================================================================

##### python的多进程间的共享内存: (注意："多进程的共享内存" 和 "多线程的共享所在进程的内存" 的原理是不一样的!但都可以访问共享的值来通信.)
##### multiprocessing.Queue和multiprocessing.Manager.Queue的多进程通信的实现原理,包括multiprocessing.Value/Array和multiprocessing.Manager.list/dict等应该都是采用共享内存实现的.
##### 当然一般多进程通信使用multiprocessing.Queue和multiprocessing.Manager.Queue就够了...
```python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print num.value
    print arr[:]
```

```python
from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    l = manager.list(range(10))

    p = Process(target=f, args=(d, l))
    p.start()
    p.join()

    print d
    print l
```
python的multiprocessing模块提供两种共享内存，sharedctypes与Manager，   
Manager效率较低，但支持远程共享内存。   
sharedctypes效率较高，快Manager两个数量级，在多进程访问时与普通内存访问相当     
代码如下：    
```python
import array
from datetime import datetime, timedelta

size = 1000000
def tranverse(a):
    t = datetime.now()
    for i in range(size):
        a[i]
    print 'elapsed %s'% (datetime.now()- t)

a = array.array('i', [i for i in range(size)])
print 'test array'
tranverse(a)

a = {}
for i in range(size):
    a[i] = i
print 'test dict'
tranverse(a)

from multiprocessing import Manager
manager = Manager()
a = manager.list([i for i in range(size)])
print 'test shared manager list'
tranverse(a)

from multiprocessing.sharedctypes import RawArray
a = RawArray( 'i', [i for i in range(size)] )
print 'test sharedctypes list in main process'
tranverse(a)

from multiprocessing import Process
ps = [Process(target=tranverse, args=(a, )) for i in range(8)]
print 'test sharedctypes list in subprocess'
for p in ps:
    p.start()
for p in ps:
    p.join()
```
#### 2.线程有自己独立的栈,但多线程间会共享进程的全局变量
##### (注意："多进程的共享内存" 和 "多线程的共享所在进程的内存" 的原理是不一样的!但都可以访问共享的值来通信.)
多线程主要使用threading模块或者multiprocessing.dummy.Pool模块

#### 3.协程(轻量级的线程)和线程几乎一样,有自己独立的栈,但多协程间也会共享进程的全局变量

==============================================================================
### 总结:无论是多进程/多线程/多协程之间的通信/数据交换/避免竞态条件,最简单实用的方式就是使用Queue.(goroutine里面叫channel)
==============================================================================

