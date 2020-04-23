package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"net/url"
	"os"
	"strings"
)

func main() {
	var port string
	if len(os.Args) > 1 {
		port = os.Args[1]
	} else {
		// 默认监听 10086
		port = "10086"
	}
	li, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Println("error listent ", err)
		return
	}
	defer li.Close()
	log.Println("代理服务器启动在: " + port)
	var i int
	//死循环监听
	clientData := make([]byte, 4096)
	for {
		client, err := li.Accept()
		if err != nil {
			log.Println("监听错误", err)
			break
		}
		i++
		n, err := client.Read(clientData)

		log.Println("请求内容 : \n ", string(clientData[:n]))

		var method, host, address string
		fmt.Sscanf(string(clientData[:bytes.IndexByte(clientData, '\n')]), "%s%s", &method, &host)

		hostPortUrl, err := url.Parse(host)
		if err != nil {
			// log.Println("出现错误：", err)
			hostPortUrl, _ = url.Parse("//" + host)
		}

		if hostPortUrl.Opaque == "443" {
			address = hostPortUrl.Scheme + ":443"
		} else {
			if strings.Index(hostPortUrl.Host, ":") == -1 {
				address = hostPortUrl.Host + ":80"
			} else {
				address = hostPortUrl.Host
			}
		}

		//获得了请求host和port，开始拨号进行tcp连接
		server, err := net.Dial("tcp", address)
		if err != nil {
			log.Println(err)
			return
		}

		// 代理https的原理：client要先发送个connect请求指定发给谁
		if method == "CONNECT" {
			fmt.Fprint(client, "HTTP/1.1 200 Connection established\r\n\r\n")
		} else {
			// http则直接发送数据
			server.Write(clientData[:n])
		}

		// 转发数据
		go io.Copy(server, client)
		go io.Copy(client, server)
	}
}
