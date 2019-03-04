
import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print 'Waiting for connection...'

while True:
    # 接受一个新连接:
    ## ============================================================================================
    ## 开启一个server socket监听客户端请求,然后它会为每个客户端生成单独的一个socket对象与之通信 !!
    ## 在Linux底层实现原理上,一个server socket会为每个过来的客户端连接创建一个socket文件并通过读写它来与之通信.
    
    # Linux 一切皆文件,Linux一个socket程序的执行流(结果就是得到一个fd,让我们能够通过fd去操作socket所创建的一个文件对象) .
    ## ============================================================================================
    sock, addr = s.accept()  
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

def tcplink(sock, addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr
