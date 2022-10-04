import requests
url = "http://baidu.com"

# add `timeout` param 
r = requests.get(url, timeout=10)

print(r.status_code)
print(r.content)

# timeout param of requests lib

# :param timeout: 
# (optional) How many seconds to wait for the server to send data before giving up, 
# as a float, or a :ref:`(connect timeout, read  timeout) <timeouts>` tuple.
# :type timeout: float or tuple




