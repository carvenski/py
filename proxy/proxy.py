#encoding=utf-8
import socket
import threading
import re
import traceback

# 提取目地服务器地址
def getAddr(data):    
    data = data.decode('utf8')
    re_result = re.search("Host: (.*)\r\n", data)
    host = re_result.group(1)
    addr = host.split(":")
    if len(addr) == 1:
        return (addr[0], 80)
    return (addr[0], int(addr[1]))

# 等待server数据,转发回client
def waitServerResponse(server, client):
    try:
        while 1:
            data = server.recv(10240)
            if not data:
                break
            client.sendall(data)
    except:
        pass

def handleClientReq(conn, caddr):
    try:
        https_addr = None
        server = None
        while 1:            
            data = conn.recv(10240) # buffer=1M
            # 空数据则关闭连接
            if not data:
                break
            # 代理https请求时,client会先发送个CONNECT请求告知目的地址
            if b"CONNECT" in data:
                # 提取https请求中的目地地址
                https_addr = getAddr(data)
                conn.send(b"HTTP/1.1 200 Connection established\r\n\r\n")
                print("https请求connect完成")
                continue
            # 提取http请求中的目地地址
            if not https_addr:
                addr = getAddr(data)
                print( '发给目的服务器数据：',data )
            else:
                addr = https_addr
                print( '您的连接是https,发送的数据已经被加密...',)
            # 连接目地服务器
            if not server:
                print( "目的服务器：", addr)
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                
                server.connect(addr)
                # 启动一个等待server response的线程
                t = threading.Thread(target=waitServerResponse, args=(server, conn)).start()
            server.sendall(data) #将请求数据发给目的服务器              
        print("连接代理完成：", caddr)
    except Exception as e:
        print('代理的客户端异常：%s, ERROR:%s'%(caddr,e))
        traceback.print_exc()
    finally:
        # 关闭连接
        conn.close()
        server.close()

def serve():
    PORT=10086
    IP = "0.0.0.0"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(10)
    print('代理服务器启动在 %s:%s...' % (IP,PORT))
    try:
        while True:
            conn, addr = s.accept()
            print('\n连接来自: ', addr)
            # 多线程处理请求
            t = threading.Thread(target=handleClientReq, args=(conn, addr)).start()
    finally:
        s.close()

try:
    serve()
except Exception as e:
    print( '代理服务器异常', e)



