# -*- coding: utf-8 -*-
import tornado
from tornado.gen import coroutine, sleep, multi, Future
from tornado.httpclient import AsyncHTTPClient
import threading
import time
import requests

# -------------------------------------------------- use tornado -------------------------------------------------------
ioloop = tornado.ioloop.IOLoop()

def _stop(future):
    ioloop.stop()

def run_until_complete(future, ioloop=ioloop):
    """Keep running untill the future is done"""
    ioloop.add_future(future, _stop) 
    ioloop.start()
# ---------------------------------------------------------------------------------------------------------------------

# ===========================================================================================
# use threadpool to make a sync function async, use future in tornado to communicate:
def sync_to_async(sync_f, *args):
    f = Future()
    # use closure here:
    def wrapper():
        res = sync_f(*args)
        f.set_result(res)  # keypoint !!
    threading.Thread(target=wrapper).start()  #使用多线程去跑同步阻塞函数,跑完后把值设置到future里面即可.
    return f

@coroutine
def test_async_sleep():
    print('---------test async sleep')
    res = yield sync_to_async(time.sleep, 5)
    print res
    print('---------test async sleep done')

@coroutine
def test_async_requests():
    print('---------test async requests')
    res = yield sync_to_async(requests.get, 'http://www.npr.org')
    print res
    print('---------test async requests done')
# ===========================================================================================

@coroutine
def test_1():
    print('---------1')
    yield sleep(3)
    print('---------2')
    yield sleep(2)
    print('---------1')

@coroutine
def test_2():
    print('---------start request')
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch('http://www.npr.org')
    print('---------response ok')
    print(res)
    yield sleep(2)
    print('---------haha')

def main():
    run_until_complete(multi([test_1(), test_2(), test_async_sleep(), test_async_requests() ]))

main()




