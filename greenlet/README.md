#### 使用greenlet(C实现)也可以实现和yield一样的函数跳转功能,即"协程"的功能.
```
   python界的3大协程框架:
   基于yield的函数跳转功能/协程,加上epoll和socket等,实现的协程框架 => tornado/twisted
   基于greenlet的函数跳转功能/协程,加上epoll和socket等,实现的协程框架 => gevent
```
