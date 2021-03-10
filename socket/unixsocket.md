## Python3 UNIX domain sockets使用代码实现
```python
一、说明
背景一：大学的时候学网络编程，经常看到说socket有AF_UNIX、AF_INET和AF_INET6三个协议族，AF_UNIX一般不用、AF_INET是IPv4的、AF_INET6是IPv6的。基于这种说教一直以来写网络编程，上来协议族就写AF_INET，AF_UNIX是什么怎么用一直没深究。

背景二：毕业后多接触Linux，也经常用netstat看端口监听情况，在较长一段时间内也不懂“netstat -ltnp”、"netstat -unp"，上来就是“netstat -anp”。这样导致的问题就是在最后总是有“Active UNIX domain sockets”一项，而且经常占很长的一个版面，要往前拉很久才能看到前面的tcp和udp。

背景三：今天早上看《Linux内核源代码情景分析》的进程间通信章节，发现AF_UNIX和UNIX domain sockets竟是一个东西，同时解决了两个困惑，真想击节称叹。 


二、使用代码实现
2.1 服务端示例代码
复制代码
import socket

class SocketServer:
    def __init__(self):
        # 常规tcp监听写法
        # server_address = ('127.0.0.1', 9999)
        # socket_family = socket.AF_INET
        # socket_type = socket.SOCK_STREAM

        # unix domain sockets 监听写法
        server_address = '/tmp/uds_socket'
        socket_family = socket.AF_UNIX
        socket_type = socket.SOCK_STREAM

        # 其他代码完全一样
        self.sock = socket.socket(socket_family, socket_type)
        self.sock.bind(server_address)
        self.sock.listen(1)
        print(f"listening on '{server_address}'.")
        pass

    def wait_and_deal_client_connect(self):
        while True:
            connection, client_address = self.sock.accept()
            data = connection.recv(1024)
            print(f"recv data from client '{client_address}': {data.decode()}")
            connection.sendall("hello client".encode())

    def __del__(self):
        self.sock.close()

if __name__ == "__main__":
    socket_server_obj = SocketServer()
    socket_server_obj.wait_and_deal_client_connect()
复制代码
 

2.2 客户端示例代码
复制代码
import socket

class SocketClient:
    def __init__(self):
        pass

    def connect_to_server(self):
        # 常规tcp连接写法
        # server_address = ('127.0.0.1', 9999)
        # socket_family = socket.AF_INET
        # socket_type = socket.SOCK_STREAM

        # unix domain sockets 连接写法
        server_address = '/tmp/uds_socket'
        socket_family = socket.AF_UNIX
        socket_type = socket.SOCK_STREAM

        # 其他代码完全一样
        sock = socket.socket(socket_family, socket_type)
        sock.connect(server_address)
        sock.sendall("hello server".encode())
        data = sock.recv(1024)
        print(f"recv data from server '{server_address}': {data.decode()}")
        sock.close()

if __name__ == "__main__":
    socket_client_obj = SocketClient()
    socket_client_obj.connect_to_server()
复制代码
 

三、运行结果
3.1 运行步骤
第一步：启动服务端
第二步：运行客户端
第三步：再回头看服务端输出
可以看到客户端与服务端成功通过UNIX domain sockets进行通信。


3.2 其他的佐证
上边的截图确实能说明服务端与客户端能够进行通信，为了更有说服力地说明使用的就是UNIX domain sockets本身，我们可以提供其他一些佐证。
使用netstat查看是监听存在：
 查看指定的/tmp/uds_socket存在，且是一个大小为0的文件：

 

四、关于进程通信的其他一些问题
 4.1 关于UNIX domain sockets的说明
在Unix的发展史中，AT&T和BSD是两大主力。在进程间通信方面两者着重点各有不同。

AT&T保留传统的Unix IPC写法，着重对其实现细节加以打磨，形成了SysV IPC通信机制；而BSD则直接将机器内部进程间通信视为不同机器进程间通信的一个特例，将两者在写法上都统一为socket的形式。

由于socket在单机实现上与SysV IPC并没有很大差别，而又与跨机器进程间通信的写法相统一，所以socket成为了更常用的通信形式。

另外这里要注意，socket在单机实现上与SysV IPC并没有很大差别，这就意味着socket单机实现上与socket跨机器实现上是有较大差别的，最直接的一点是由于是在单台机器上报文的传递并不需要复杂的TCP等协议去保证其顺序性，所以从性能等方面讲AF_UNIX会优于AF_INET。

 

 4.2 为什么现在的框架监听一堆端口
在上家公司测试基于spring boot开发的一套系统时，发现spring boot监听了一堆的端口，当时问领导说进程间通信使用管道不就好了吗为什么要监听一堆端口呢，他说现在大多数也都通过socket的方式监听端口进行通信。

现在想来他的说法也不够清晰准确。进程间通信，旧的方法是管道、新的方法是UNIX domain sockets（AF_UNIX），spring boot等使用AF_INET这种成本更高的的形式一是为了方便地使用http二是为了方便分布式。

实际上就是不懂tcp socket和unix socket的不同使用场景而已。
```


 
