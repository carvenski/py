

# use thread pool to wrap a sync function to make it async for gevent/tornado coroutine !!

1.配合tornado使用：
使用线程池实现tornado中异步函数的原理:
需要新建一个future对象,在主线程里立即返回该future对象放在这里先(该future对象就是2个线程间通信的东西，另一个线程通知主线程它的阻塞任务完成的方式),
再开启另一个线程去跑那个阻塞的函数,并传入那个future对象，当那个线程里阻塞函数完成时，把结果写入到future对象里并且修改future对象的状态值为done，
这样在主线程里的loop检测队列时就会知道那个future对象的状态已经done了,就会调用它所在的那个协程去继续运行.
可以配合tornado用线程池来包装阻塞函数，使其异步，就可以使用tornado来yield该函数了（laisky的tars就是这么干的）
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
    res = yield sync_to_async(time.sleep, 5)  #在这里yield时会把该future返回到调度器里去,加入到事件队列里面受监控了.
    print res
    print('---------test async sleep done')

@coroutine
def test_async_requests():
    print('---------test async requests')
    res = yield sync_to_async(requests.get, 'http://www.npr.org')
    print res
    print('---------test async requests done')
# ===========================================================================================
  


1.配合gevent使用：
使用greenlet来手动切换协程,类似future的作用.
需要新建一个greenlet对象,在新开的线程里传入这个greenlet对象,并将该greenlet对象立即返回到主线程,并greenlet.switch()切换协程,
当另一个线程里阻塞函数执行完成后,把结果放到那个greenlet里面,并设置其状态为done,
则当loop检测到该greenlet状态已经ok的时候就会回到它的协程继续执行了.
def async_function_for_gevent():










