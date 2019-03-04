```python
#encoding=utf8

# coroutine/greenlet version:
import gevent
from gevent import Greenlet, sleep as gevent_sleep
from Queue import Queue; ThreadQueue = CoroutineQueue = Queue 

def producer(q):
    i = 0
    while not q.full():
        print('-------producer woring------')
        q.put('haha')
        if i > 10: break
        i += 1
        gevent_sleep(1)
    global is_producing; is_producing = False

def consumer(q):
    global is_producing
    while not q.empty() or is_producing:
        print('-------consumer woring------')
        q.get()
        gevent_sleep(1)

greenlet_queue = ThreadQueue(10)
is_producing = True  # 多协程和多线程一样直接访问全局变量即可,当然最好也是使用Event对象
producer_greenlet = Greenlet(run=producer, **{'q': greenlet_queue})
consumer_greenlet = Greenlet(run=consumer, **{'q': greenlet_queue})
greenlet_list = [producer_greenlet, consumer_greenlet]
print('--------------greenlet start--------------')
for t in greenlet_list:
    t.start()
for t in greenlet_list:
    t.join()    #or gevent.joinall(greenlet_list)  #调用join来等待所有greenlet运行结束,用法和线程一样...
print('--------------greenlet end--------------')

```

