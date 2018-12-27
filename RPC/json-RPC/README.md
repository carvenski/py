
### json-RPC协议: 一种基于http+json实现的轻量级简单型RPC协议
```
rpc协议的实现既可以基于http协议,也可以基于tcp/ip协议(socket).
rpc协议的主要参数就是要传入 函数名+函数参数.
```

[json-RPC协议内容](http://wiki.geekdream.com/Specification/json-rpc_2.0.html)

[一个python版的json-rpc包](https://pypi.org/project/json-rpc/)


```python
pip install json-RPC
```

#### Server demo
```
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher

@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b

    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    run_simple('localhost', 4000, application)


```

#### Server demo
```python
import requests
import json

def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "echo",
        "params": ["echome!"],
        "jsonrpc": "2.0",
        "id": 0,
    
    }

    resp = requests.post(url, data=json.dumps(payload), headers=headers).json()
    print(resp)

if __name__ == "__main__":
    main()

```

#### rpc和http
```
rpc和http的差别不大,rpc协议设计的初衷是为了调用其他机器上的函数,返回结果(所谓远程方法调用).
这个需求本身就可以直接使用http协议完成:不同的路由对应调用不同的函数而已.

在微服务中,每个服务对外暴露自己的服务功能,提供给调用方使用,既可以以http暴露调用,也可以以rpc暴露调用.
例如alibaba的dubbo框架本身即是个rpc框架,也是个微服务框架.
而SpringCloud+SpringBoot框架是基于http的微服务框架.

"服务"这个概念不受限于任何协议,基于任何协议的某种Server,它对外提供某种服务,都可以是个微服务.
例如,http server/rpc server/NFS server/Echo Server/NTP srever...它们都基于tcp/ip(socket),监听ip:port,对外提供服务.
```

#### 常见协议设计的几个考虑点
[深入理解RPC消息协议设计](https://www.imooc.com/article/264839)


