#### 非阻塞socket原理 + selector本质
```
参考:https://blog.csdn.net/hguisu/article/details/7453390

我们把一个SOCKET接口设置为非阻塞(调用set_non_blocking)就是告诉内核
当所请求的I/O操作无法完成时，不要将进程睡眠，而是返回一个错误
这样我们的I/O操作函数将不断的测试数据是否已经准备好，如果没有准备好，继续测试，直到数据准备好为止
                                                                                                                                      
把SOCKET设置为非阻塞模式，即通知系统内核：在调用Sockets API时，不要让线程睡眠，而应该让函数立即返回
在返回时，该函数返回一个错误代码。图所示，一个非阻塞模式套接字多次调用recv()函数的过程
前三次调用recv()函数时，内核数据还没有准备好。因此，该函数立即返回WSAEWOULDBLOCK错误代码
第四次调用recv()函数时，数据已经准备好，被复制到程序的缓冲区中，recv()函数返回成功，程序开始处理数据
                                                                                                                                      
*******************************************************************************************
从以上可知: 其实selector/epoll这些东西本质上做的事也就是: 轮训socket而已,你的数据好没好啊? 
从selector的api可以看出:把一组socket传给它,然后它自己阻塞(内部在轮训),哪个好了就通知你,调用回调函数
*******************************************************************************************

默认情况下，socket的connect/accept/recv/send都是阻塞读写的，需要设置为非阻塞模式(set_non_blocking)

所以,selector的本质就是封装了"轮训socket的操作,然后通知你挨个处理数据准备好的socket..."
```

## selectors — High-level I/O multiplexing(New in python3.4)

#### Introduction
```python
This module allows high-level and efficient I/O multiplexing, built upon the select module primitives. 
Users are encouraged to use this module instead, unless they want precise control over the OS-level primitives used.

It defines a BaseSelector abstract base class, along with several concrete implementations (KqueueSelector, EpollSelector…), 
that can be used to wait for I/O readiness notification on multiple file objects. 
In the following, “file object” refers to any object with a fileno() method, or a raw file descriptor. See file object.

DefaultSelector is an alias to the most efficient implementation available on the current platform: 
this should be the default choice for most users.

Note The type of file objects supported depends on the platform: 
  on Windows, sockets are supported, but not pipes, 
  whereas on Unix, both are supported (some other types may be supported as well, such as fifos or special file devices).
  
See also select Low-level I/O multiplexing module.
```

#### Classes
```python
Classes hierarchy:

BaseSelector
+-- SelectSelector
+-- PollSelector
+-- EpollSelector
+-- DevpollSelector
+-- KqueueSelector

In the following, events is a bitwise mask indicating which I/O events should be waited for on a given file object. 
It can be a combination of the modules constants below:

Constant	Meaning
EVENT_READ	Available for read
EVENT_WRITE	Available for write

class selectors.SelectorKey
A SelectorKey is a namedtuple used to associate a file object to its underlying file descriptor, selected event mask and attached data. 
It is returned by several BaseSelector methods.

fileobj
File object registered.

fd
Underlying file descriptor.

events
Events that must be waited for on this file object.

data
Optional opaque data associated to this file object: for example, this could be used to store a per-client session ID.

class selectors.BaseSelector
A BaseSelector is used to wait for I/O event readiness on multiple file objects. 
It supports file stream registration, unregistration, and a method to wait for I/O events on those streams, with an optional timeout.
It’s an abstract base class, so cannot be instantiated. Use DefaultSelector instead, or one of SelectSelector, KqueueSelector etc. 
if you want to specifically use an implementation, and your platform supports it. 
BaseSelector and its concrete implementations support the context manager protocol.

abstractmethod register(fileobj, events, data=None)
Register a file object for selection, monitoring it for I/O events.

fileobj is the file object to monitor. It may either be an integer file descriptor or an object with a fileno() method. 
events is a bitwise mask of events to monitor. data is an opaque object.

This returns a new SelectorKey instance, or raises a ValueError in case of invalid event mask or file descriptor, 
or KeyError if the file object is already registered.

abstractmethod unregister(fileobj)
Unregister a file object from selection, removing it from monitoring. A file object shall be unregistered prior to being closed.

fileobj must be a file object previously registered.

This returns the associated SelectorKey instance, or raises a KeyError if fileobj is not registered. 
It will raise ValueError if fileobj is invalid (e.g. it has no fileno() method or its fileno() method has an invalid return value).

modify(fileobj, events, data=None)
Change a registered file object’s monitored events or attached data.

This is equivalent to BaseSelector.unregister(fileobj)() followed by BaseSelector.register(fileobj, events, data)(), 
except that it can be implemented more efficiently.

This returns a new SelectorKey instance, or raises a ValueError in case of invalid event mask or file descriptor, 
or KeyError if the file object is not registered.

abstractmethod select(timeout=None)
Wait until some registered file objects become ready, or the timeout expires.

If timeout > 0, this specifies the maximum wait time, in seconds. 
If timeout <= 0, the call won’t block, and will report the currently ready file objects. 
If timeout is None, the call will block until a monitored file object becomes ready.

This returns a list of (key, events) tuples, one for each ready file object.

key is the SelectorKey instance corresponding to a ready file object. events is a bitmask of events ready on this file object.

Note This method can return before any file object becomes ready or the timeout has elapsed if the current process receives a signal: 
in this case, an empty list will be returned.

Changed in python3.5: 
The selector is now retried with a recomputed timeout when interrupted by a signal if the signal handler did not raise an exception
(see PEP 475 for the rationale), instead of returning an empty list of events before the timeout.

close()
Close the selector.

This must be called to make sure that any underlying resource is freed. The selector shall not be used once it has been closed.

get_key(fileobj)
Return the key associated with a registered file object.

This returns the SelectorKey instance associated to this file object, or raises KeyError if the file object is not registered.

abstractmethod get_map()
Return a mapping of file objects to selector keys.

This returns a Mapping instance mapping registered file objects to their associated SelectorKey instance.

class selectors.DefaultSelector
The default selector class, using the most efficient implementation available on the current platform. 
This should be the default choice for most users.

class selectors.SelectSelector
select.select()-based selector.

class selectors.PollSelector
select.poll()-based selector.

class selectors.EpollSelector
select.epoll()-based selector.

fileno()
This returns the file descriptor used by the underlying select.epoll() object.

class selectors.DevpollSelector
select.devpoll()-based selector.

fileno()
This returns the file descriptor used by the underlying select.devpoll() object.

New in version 3.5.

class selectors.KqueueSelector
select.kqueue()-based selector.

fileno()
This returns the file descriptor used by the underlying select.kqueue() object.
```


#### Examples
*Here is a simple "echo server" implementation*
```python
# EchoServer.py
# 使用select去监控server socket,每当client发起访问,回调函数就会新建一个conn.
# 再注册新建的conn到selector中,每当client发送了data,回调函数就会读取并返回该data,然后关闭conn.
import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
```        
        
