```python
#encoding=utf8

# thread version:
from threading import Thread
from Queue import Queue; ThreadQueue = CoroutineQueue = Queue 
import time

def producer(q):
    i = 0
    while not q.full():
        print('-------producer woring------')
        q.put('haha')
        if i > 10: break
        i += 1
        time.sleep(1)
    global is_producing; is_producing = False

def consumer(q):
    global is_producing
    while not q.empty() or is_producing:
        print('-------consumer woring------')
        q.get()
        time.sleep(1)

thread_queue = ThreadQueue(10)
is_producing = True  #不能传入线程去修改值,因为它是传值不是传引用!!所以直接使用了global,但最好是用Event之类的对象.
producer_thread = Thread(target=producer, kwargs={'q': thread_queue})
consumer_thread = Thread(target=consumer, kwargs={'q': thread_queue})
thread_list = [producer_thread, consumer_thread]
print('--------------thread start--------------')
for t in thread_list:
    t.start()
for t in thread_list:
    t.join()
print('--------------thread end--------------')
```

