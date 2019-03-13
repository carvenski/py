import time
# python2 need to install tornado & futures `pip install tornado futures`
import tornado
from tornado.gen import coroutine, sleep as tornado_sleep, multi, Future
from tornado.queues import Queue, QueueEmpty, QueueFull
from concurrent.futures import ThreadPoolExecutor


@coroutine
def f1(name):
    try:
        print("f1-%s funtion started, waiting 5 seconds..." % name)
        yield tornado_sleep(5)
        if 5 < name < 10: raise Exception("test exception")
        print("f1-%s funtion finished." % name)
    except Exception as e:
        print("==== f1-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


@coroutine
def f2(name):
    try:
        print("f2-%s funtion started, waiting 5 seconds..." % name)
        # use `asyncify` to make sync funtion async(run in threadpool, go did this too !)
        yield asyncify(time.sleep, 5)
        if 5 < name < 10: raise Exception("test exception")
        print("f2-%s funtion finished." % name)
    except Exception as e:
        print("==== f2-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


@coroutine
def producer(name, q, counter):
    try:
        i = 0
        while True:
            # do produce staff:
            # yield tornado_sleep(1)
            print("producer %s put %s" % (name, i))
            while True:
                try:
                    # yield q.put(i) VS q.put_nowait(i)
                    q.put_nowait(i)
                    break
                except QueueFull:
                    yield tornado_sleep(1)
                    continue

            i += 1
            if i > 100:
                print("producer %s done" % name)
                counter.done()
                break
    except Exception as e:
        print("==== producer-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception


@coroutine
def consumer(name, q, counter):
    try:
        while not (q.empty() and counter.all_done()):
            try:
                # yield q.get() VS q.get_nowait()
                item = q.get_nowait()
            except QueueEmpty:
                # wait producer put into queue
                yield tornado_sleep(1)
                continue

            # do consume staff:
            # yield tornado_sleep(1)
            print("consumer %s get %s" % (name, item))
        print("consumer %s done" % name)
    except Exception as e:
        print("==== consumer-%s funtion has EXCEPTION !! ====" % name)
        # do sth to handle exception

# init
THREAD_POOL_SIZE = 100
QUEUE_SIZE = 1000
executor = ThreadPoolExecutor(THREAD_POOL_SIZE)
loop = tornado.ioloop.IOLoop()
q = Queue(maxsize=QUEUE_SIZE)

# asyncify run a func in threadpool:
def asyncify(func, *args, **kw):
    future = executor.submit(func, *args, **kw)
    return future

def run_until_complete(future, ioloop=loop):
    """Keep running untill the future is done"""
    def _stop(future):        
        loop.stop()
        print("all coroutines finished, loop stopped.")
    ioloop.add_future(future, _stop)
    ioloop.start()    

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
for k in range(PRODUCER_NUM * 10):
	futures.append(consumer(k, q, counter))

run_until_complete(multi(futures))

# close
loop.close()
executor.shutdown()
