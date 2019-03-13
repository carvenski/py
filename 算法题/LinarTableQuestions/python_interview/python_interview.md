
# python面试常见知识点总结:

### GIL 全局解释器锁:
python解释器被一个全局解释器锁保护着，它确保"任何时候都只有一个Python线程执行" !    
所以,GIL最大的问题就是Python的多线程程序并不能利用多核CPU的优势 （比如一个使用了多个线程的计算密集型程序只会在一个单CPU上面运行）    
在讨论普通的GIL之前，有一点要强调的是GIL只会影响到那些严重依赖CPU的程序（比如计算型的）,因为它需要占用很多cpu去并行计算但此时python却无法充分利用多核cpu的计算力.    
而如果你的程序大部分只会涉及到I/O，比如网络交互，那么使用多线程就很合适， 因为它们大部分时间都在等待,这本身就不需要占用很多cpu去计算.    

#### 如何解决cpu计算型程序的GIL缺点:
* 1.使用多进程代替多线程,使用multiprocessing模块
* 2.使用C扩展,使用C语言写cpu计算型的程序(包括使用C的多线程等利用多核cpu),然后在python中调用C扩展(注意C扩展的运行和python解释器是在2个独立进程中)

#### IPC 多进程通信:
* 1.使用多进程都能访问到的共享内存(如multiprocessing.Value/multiprocessing.Array/multiprocessing.sharedctypes等)
* 2.使用多进程都能访问到的队列(如multiprocessing.Queue和multiprocessing.Manager.Queue,或直接运行个第三方的独立的队列进程如rabbitmq)     
    ** multiprocessing.Queue,其中multiprocessing.Queue Returns a process shared queue implemented using a pipe and a few locks/semaphores,这个Queue使用管道实现.    
    ** multiprocessing.Manager.Queue,其中multiprocessing.Manager就是一个作为共享内存的进程对象,这个Queue使用共享内存实现.     
* 3.使用socket通信 
* 4.使用管道通信(multiprocessing.Pipe)
* 5.使用信号量(signal)

#### 进程/线程/协程:
* 进程和线程区别:    
进程在执行过程中拥有独立的内存单元，而多个线程共享进程的内存.一个程序至少有一个进程,一个进程至少有一个线程(主线程).    
每个独立的线程有一个程序运行的入口、顺序执行序列和程序的出口.但是线程不能够独立执行,必须依存在进程中,由进程提供多个线程执行控制.     
从逻辑角度来看,多线程的意义在于一个进程中,可以有多个执行部分同时执行(最初就是为了并行而提出的).      

* 线程和协程区别:    
协程就是轻量的线程,线程频繁切换需要昂贵的上下文切换开销,效率太低且没必要.所以,就在一个线程中开多个协程,协程切换就无需上下文切换,很轻量,效率更高了.    
(使用python的generator实现协程,generator可以暂停一个函数的执行过会再回来继续执行的特性就是协程的特点)


#### web框架:
django/flask/web.py/tornado/gevent/sqlalchemy
* web框架的原理: MVC模式    
* 实现一个web框架的思路:    
    ** 封装http协议的细节,例如header/body等的解析,封装出request/response对象来使用(或者对接好http server直接获取req/res),
    ** 路由功能,把url匹配到对应的handler函数中处理,
	** 封装常见sql/nosql数据库的ORM操作,
	** cookie/session/token/安全验证/redis缓存/等等web系统常用功能的实现,


#### mysql:
* 基础sql语法
* 查询优化/深入了解使用索引/使用explain分析性能
* mysql性能优化



#### nosql数据库mongodb:


#### k-v数据库redis/memcache做缓存,优化访问速度:


#### linux:
* linux常用命令
* Linux系统原理


#### 云计算/OpenStack/docker:




#### 消息队列:
rabbitmq/kafka



#### http服务器nginx/apache + uwsgi/gunicorn:



#### git使用



#### 数据结构和算法常见笔试题/字符串型题目/递归+for循环解法为主:



####





















































