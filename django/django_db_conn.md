## django的数据库连接机制

###### 多线程处理请求
```
django会使用一个线程去处理一个http请求
在每个请求的处理过程中，如果使用了django的orm去操作数据库了，
就会自动在该请求所处的线程的全局空间里（Thread Local）去查找db connection,
如果为空就会为该线程创建一条db connection并绑定到Thread Local上，
在请求处理完后，如果该线程也不需要保持的话，django也会负责自动去关闭该conncetion。
```

###### uwsgi的线程池工作模式 + django
```
一般来说http server的多线程工作模式是会保持着几个固定线程去等待处理请求的，也就应该是保持着几个固定的数据库连接。
然而实测效果是django自带的runserver每个请求进来就会开个线程去处理，处理完了又销毁了这个线程，是没有线程池的。
生产上一般用uwsgi的多线程工作模式，它里面会有个线程池，可配置一个threads数量。
但是实测uwsgi的线程池效果也是一样，还是在在不停的创建和关闭连接。
```

###### 最终发现：
```
其实不关uwsgi线程池的事，是django自己在每个请求结束时会发信号去检查MAX_CONN_AGE的值并且自动关闭当前Thread Local里的连接。。
那么有一种做法就是设置MAX_CONN_AGE的值大于0即可，这样django就会保持连接一定存活时间，下次请求就可以复用当前Thread Local里的连接了。
```

###### 但是这么做还是有风险: 请求内部用户自己创建多线程并且使用orm查询数据库的情况
```
如果用户自己在django中也创建了多线程去跑并发任务，并且在线程里面还使用了orm去操作数据库，
那么django orm还是会替你自动到当前的线程的Thread Local里面去找connection使用，
没有就会创建一个，而且这个conn还是有MAX_CONN_AGE存活时间的! 这样就会导致mysql那边出现大量保持连接却又没用的conn！
而且这种情况下django orm是不会替你去释放这个db connection的，它只管替你建连接去用，但是不会替你去释放连接(因为是用户自己创建的线程)。
所以在一个请求内部，你自己新建的线程里用完了后，需要记得去调用下conn.close()释放连接，否则当前线程使用的连接就不会被释放。
这尼玛都是坑啊。。。
```

### 更好的做法: use SQLAlchemy conn pool
```
除了设置django MAX_CONN_AGE > 0 来实现db连接复用的方式之外，
还有一个更好的做法：就是替换django自带的这个DB Engine class,把它换成SQLAlchemy等自带线程池的引擎。
这样，上层的django orm啥都不用动，只需要替换底层的一个DB Engine class即可,
然后django原先的每次请求会去connect和close conn的做法，就会被透明地替换成 get和put back from conn pool机制了。
只需要根据并发线程数设置好合适的连接池的数量即可。
这才是django这个坑的更好的解决方案。。
```

[django多线程数据库连接不释放问题参考](https://github.com/slackapi/bolt-python/issues/280)      
[django实现连接池方案参考](https://lockshell.com/2019/08/28/django-db-connection-pool/)        




