## django的数据库连接机制
```
多线程处理请求:
django会使用一个线程去处理一个http请求
在每个请求的处理过程中，如果使用了django的orm去操作数据库了，
就会自动在该请求所处的线程的全局空间里（Thread Local）去查找db connection,
如果为空就会为该线程创建一条db connection并绑定到Thread Local上，
在请求处理完后，如果该线程也不需要保持的话，django也会负责自动释放该conncetion。
一般来说django的多线程工作模式是会保持着几个线程等待处理请求的，也就会对应保持着几个数据库连接。
实测效果是django每个请求进来就会开个线程去处理，处理完了又销毁了这个线程，连个线程池都没有。。。
uwsgi的多线程工作模式是不是加了这个线程池?

但是，如果用户自己在django中也创建了多线程去跑并发任务，并且在线程里面还使用了orm去操作数据库，
则django orm还是会替你自动到当前的线程的Thread Local里面去找connection使用，没有就会创建一个，
但是这种情况下django是不会替你去释放这个db connection的，它只管替你建连接去用，但是不会替你去释放连接。
坑啊。。。
```
[django多线程数据库连接不释放问题参考](https://github.com/slackapi/bolt-python/issues/280)


