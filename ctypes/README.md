## ctypes
*使用ctypes调用so库,增强python的cpu计算型任务的性能*
python可以使用ctypes调用.so动态库(windows上就是dll库)
而c/rust/go都可以编译成.so库文件
所以,python可使用ctypes去联合c/rust/go的性能

## ctypes使用示例
```python
import ctypes
import time

# 1.使用ctypes调用go编译的.so库
so = ctypes.CDLL("./mylib.so")
t = time.time()
so.foo.restype = ctypes.c_longlong  # ctypes需要做一些C数据类型转换,否则结果可能不精确
r = so.foo(1, 9)
print(r)
# 耗时 2ms
print("cgo, time=%s" % (time.time()-t))  
    
t = time.time()
# 2.测试python自己的cpu计算速度
sum = 0
for i in range(1000000):
    sum += i
print(sum)
# 耗时 200ms
print("python, time=%s" % (time.time()-t))

# cpu计算型的任务速度提升了100倍
```







