# 本文简单介绍python进程模块multiprocessing提供的 进程池 和 线程池 的用法：
```python
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

''' 
进程池/线程池的使用有4个函数: 
map
map_async
apply
apply_async
'''
```

## --------------------------------------进程池----------------------------------------
进程池的使用有四种方式：apply_async、apply、map_async、map    
其中apply_async和map_async是异步的，也就是启动进程函数之后会继续执行后续的代码不用等待进程函数返回    
apply_async和map_async方式提供了一写获取进程函数状态的函数：ready()、successful()、get()    

PS：join()语句要放在close()语句后面。

实例代码如下：
```python
# -*- coding: utf-8 -*-
import multiprocessing
import time

def func(msg):
    print('msg: ', msg)
    time.sleep(1)
    print('********')
    return 'func_return: %s' % msg

if __name__ == '__main__':
    # apply_async
    print('\n--------apply_async------------')
    pool = multiprocessing.Pool(processes=4)
    results = []
    for i in range(10):
        msg = 'hello world %d' % i
        result = pool.apply_async(func, (msg, ))
        results.append(result)
    print('apply_async: 不堵塞')

    for i in results:
        i.wait()  # 等待进程函数执行完毕

    for i in results:
        if i.ready():  # 进程函数是否已经启动了
            if i.successful():  # 进程函数是否执行成功
                print(i.get())  # 进程函数返回值

    # apply
    print('\n--------apply------------')
    pool = multiprocessing.Pool(processes=4)
    results = []
    for i in range(10):
        msg = 'hello world %d' % i
        result = pool.apply(func, (msg,))
        results.append(result)
    print('apply: 堵塞')  # 执行完func才执行该句
    pool.close()
    pool.join()  # join语句要放在close之后
    print(results)

    # map
    print('\n--------map------------')
    args = [1, 2, 4, 5, 7, 8]
    pool = multiprocessing.Pool(processes=5)
    return_data = pool.map(func, args)
    print('堵塞')  # 执行完func才执行该句
    pool.close()
    pool.join()  # join语句要放在close之后
    print(return_data)

    # map_async
    print('\n--------map_async------------')
    pool = multiprocessing.Pool(processes=5)
    result = pool.map_async(func, args)
    print('ready: ', result.ready())
    print('不堵塞')
    result.wait()  # 等待所有进程函数执行完毕

    if result.ready():  # 进程函数是否已经启动了
        if result.successful():  # 进程函数是否执行成功
            print(result.get())  # 进程函数返回值
```

## ------------------------------------线程池------------------------------------------
线程池的使用方式和进程池一样.

实例代码如下：
```python
# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import time

def fun(msg):
    print('msg: ', msg)
    time.sleep(1)
    print('********')
    return 'fun_return %s' % msg

# map_async
print('\n------map_async-------')
arg = [1, 2, 10, 11, 18]
async_pool = ThreadPool(processes=4)
result = async_pool.map_async(fun, arg)
print(result.ready())  # 线程函数是否已经启动了
print('map_async: 不堵塞')
result.wait()  # 等待所有线程函数执行完毕
print('after wait')
if result.ready():  # 线程函数是否已经启动了
    if result.successful():  # 线程函数是否执行成功
        print(result.get())  # 线程函数返回值

# map
print('\n------map-------')
arg = [3, 5, 11, 19, 12]
pool = ThreadPool(processes=3)
return_list = pool.map(fun, arg)
print('map: 堵塞')
pool.close()
pool.join()
print(return_list)

# apply_async
print('\n------apply_async-------')
async_pool = ThreadPool(processes=4)
results =[]
for i in range(5):
    msg = 'msg: %d' % i
    result = async_pool.apply_async(fun, (msg, ))
    results.append(result)

print('apply_async: 不堵塞')
# async_pool.close()
# async_pool.join()
for i in results:
    i.wait()  # 等待线程函数执行完毕

for i in results:
    if i.ready():  # 线程函数是否已经启动了
        if i.successful():  # 线程函数是否执行成功
            print(i.get())  # 线程函数返回值

# apply
print('\n------apply-------')
pool = ThreadPool(processes=4)
results =[]
for i in range(5):
    msg = 'msg: %d' % i
    result = pool.apply(fun, (msg, ))
    results.append(result)

print('apply: 堵塞')
print(results)
```

