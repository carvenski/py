import time
import asyncio
from concurrent.futures import ThreadPoolExecutor


async def f1(name):
    try:
        print("f1-%s funtion started, waiting 5 seconds..." % name)
        await asyncio.sleep(5)
        if 5 < name < 10: raise Exception("test exception")
        print("f1-%s funtion finished." % name)
    except Exception as e:
        print("==== f1-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


async def f2(name):
    try:
        print("f2-%s funtion started, waiting 5 seconds..." % name)
        # use `asyncify` to make sync funtion async(run in threadpool, go did this too !)
        await asyncify(time.sleep, 5)
        if name < 10: raise Exception("test exception")
        print("f2-%s funtion finished." % name)
    except Exception as e:
        print("==== f2-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


async def producer(name, q, counter):
    try:
        i = 0
        while True:
            # do produce staff:
            # await asyncio.sleep(1) 
            print("producer %s put %s" % (name, i))            
            while True:
                try:
                    # await q.put(i) VS q.put_nowait(i)
                    q.put_nowait(i)
                    break
                except asyncio.QueueFull:
                    await asyncio.sleep(1)
                    continue
            
            i += 1
            if i > 100:
                print("producer %s done" % name)
                counter.done()
                break            
    except Exception as e:
        print("==== producer-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


async def consumer(name, q, counter):
    try:
        while not (q.empty() and counter.all_done()):
            try:
                # await q.get() VS q.get_nowait()
                item = q.get_nowait()
            except asyncio.QueueEmpty:
                # wait producer put into queue
                await asyncio.sleep(1)
                continue

            # do consume staff:         
            # await asyncio.sleep(1) 
            print("consumer %s get %s" % (name, item))
        print("consumer %s done" % name)
    except Exception as e:
        print("==== consumer-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


# init
THREAD_POOL_SIZE = 100
QUEUE_SIZE = 1000
executor = ThreadPoolExecutor(THREAD_POOL_SIZE)
loop = asyncio.get_event_loop()
"""
mostly we have sync function inside producer/consumer coroutine to do some works,
and we wrap that sync function into a threadpool to become async(call it worker here),
but notice that:
    it's the producer/consumer coroutine which operate the queue[put/get item from it],
    and the worker just use the item.
    we can't directly operate queue from worker because it runs in threadpool(not thread safe!), 
    but can operate queue in coroutine.
**** The queue is not thread safe but coroutine safe !! ****
"""
# The Queue is not thread safe but coroutine safe !!
q = asyncio.Queue(maxsize=QUEUE_SIZE) 


"""    
concurrent.futures.Future is different from asyncio.Future !!!!
The asyncio.Future is intended to be used with event loops and is awaitable, while the former isn't. 
`loop.run_in_executor` provides the necessary interoperability between the two.

or you can use `asyncio.wrap_future(future, *, loop=None)` to 
convert a concurrent.futures.Future to a asyncio.Future.
"""
# asyncify run a func in threadpool & wrap concurrent.futures.Future to asyncio.Future:
def asyncify(func, *args, **kw):
    concurrent_future = executor.submit(func, *args, **kw)
    async_future = asyncio.wrap_future(concurrent_future)
    return async_future


# producer Counter
class ProducerCounter(object):
    def __init__(self, count):
        self.count = count
        # add thread lock here, actually lock is no need in python coroutine !
        from threading import Lock
        self.lock = Lock()

    def done(self):
        # actually lock is no need
        self.lock.acquire()
        self.count -= 1
        self.lock.release()

    def all_done(self):
        return self.count == 0


# start all coroutines
futures = []
for i in range(100):
	futures.append(f1(i))
	futures.append(f2(i))

PRODUCER_NUM = 10
counter = ProducerCounter(PRODUCER_NUM)

for j in range(PRODUCER_NUM):
	futures.append(producer(j, q, counter))
for k in range(PRODUCER_NUM*10):
	futures.append(consumer(k, q, counter))

loop.run_until_complete(asyncio.wait(futures))
print("all coroutines finished, loop stopped.")

# close
loop.close()
executor.shutdown()



