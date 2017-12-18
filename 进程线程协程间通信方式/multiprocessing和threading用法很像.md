## multiprocessing模块和threading模块提供的api使用方式一样，
## 只不过进程是使用Process类，线程是使用Thread类，类下面的函数一样的用法...
```python
from threading import Thread
from multiprocessing import Process

def test(i):
    print('----in thread/process----%s' % i )

# 1.直接新建Process/Thread对象即可：
p1 = Process(target=test, args=(3,))
# p1.daemon = True   #设置deamon
p1.start()
# p1.join()          #调用join

t1 = Thread(target=test, args=(3,))
# t1.setDaemon(True)
t1.start()
# t1.join()


# 2.继承Process/Thread类,实现run方法：
class MyProcess(Process):
    def __init__(self, i):
        Process.__init__(self)
        self.i = i
    def run(self):
        print('----in thread/process----%s' % self.i )

class MyThreads(Thread):
    def __init__(self, i):
        Process.__init__(self)
        self.i = i
    def run(self):
        print('----in thread/process----%s' % self.i )
        
```

Process对象与Thread对象的用法相同，拥有is_alive()、join([timeout])、run()、start()、terminate()等方法。       
属性有：authkey、daemon（要通过start()设置）、exitcode(进程在运行时为None、如果为–N，表示被信号N结束）、name、pid。      
此外multiprocessing包中也有Lock/Event/Semaphore/Condition类，用来同步进程，其用法也与threading包中的同名类一样。     
multiprocessing的很大一部份与threading使用同一套API，只不过换到了多进程的情境。      

