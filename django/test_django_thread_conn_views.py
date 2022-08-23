#encoding=utf8
import time
from django.http import HttpResponse

from concurrent.futures import ThreadPoolExecutor

from .models import *


def func(i):
    # 测试django orm的多线程并发/连接机制 这里触发数据库查询
    qs = User.objects.filter(name=i)
    return (i, len(qs))

# ===========================================================
# init thread pool, make thread local conn created already
# there will be 10 threads and 10 connections in background.
tasks = range(100)
pool = ThreadPoolExecutor(max_workers=10)
results = pool.map(func, tasks)
[print(result) for result in results]
print("== init thread pool and conn ok ==")

def test_db(request):

    t0 = time.time()
    for i in tasks:
        print(func(i))
    
    t1 = time.time()
    # 1.每次新建 线程池和连接  测试效果不咋地 时间没有优化多少 每次新建都有开销
    # with ThreadPoolExecutor(max_workers=10) as pool:
    #         results = pool.map(func, tasks)
    #         [print(result) for result in results]

    # 2.复用已经初始化好的 线程池和连接
    results = pool.map(func, tasks)
    [print(result) for result in results]

    t2 = time.time()
    
    print('顺序执行:  time= ', t1-t0) # 800ms
    print('并发执行:  time= ', t2-t1) # 150ms

    return HttpResponse("test db ok")
