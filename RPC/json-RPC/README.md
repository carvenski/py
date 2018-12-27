
### json-RPC协议: 一种基于http+json实现的轻量级简单型RPC协议

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


