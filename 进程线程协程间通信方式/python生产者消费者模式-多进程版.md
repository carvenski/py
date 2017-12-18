```python
#encoding=utf8

# process version:
from multiprocessing import Process, Queue as ProcessQueue, Value #Value是在共享内存的,多进程都可以访问
import time

def producer(q, is_producing):
    i = 0
    while not q.full():
        print('-------producer woring------')
        q.put('haha')
        if i > 10: break
        i += 1
        time.sleep(1)
    is_producing.value = False

def consumer(q, is_producing):
    while not q.empty() or is_producing.value:
        print('-------consumer woring------')
        q.get()
        time.sleep(1)

def main():
    process_queue = ProcessQueue(10)
    is_producing = Value('b', True) # 多进程间需要使用一个共享布尔值来判断生产者是否停止生产了 
    producer_process = Process(target=producer, kwargs={'q': process_queue, 'is_producing': is_producing})
    consumer_process = Process(target=consumer, kwargs={'q': process_queue, 'is_producing': is_producing})
    process_list = [producer_process, consumer_process]
    print('--------------process start--------------')
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()
    print('--------------process end--------------')

if __name__ == '__main__':
    main()
```

