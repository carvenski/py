# 给小白的Python简明教程(python3)

#### 程序的基本概念
```python
输入 + 计算/存储 + 输出 = 程序
```

#### 2个基本函数的介绍
```python
输入函数: input()
输出函数: print()

#例子：
input("please put your name here: ")  # 程序会等待用户输入
print("your name is: ")               # 程序会打印输出
```

#### python中的缩进
```python
#在python中不需要写其他语言里的大括号{}来表示层次的缩进,但是要以4个空格作为一个层次的缩进.
# 例子:

# 条件语句里的缩进
if a == 1:
    print(1)
else:    
    if a == 2:
        print(2)
    else:
        if a == 3:
            print(3)

# 定义一个函数时,函数名和函数体的缩进
def add(a, b):
    print(a + b)
```


#### 3个基本数据类型 + 2个复合数据类型
```python
#中文名    英文名    例子
数值型     int       0, 1, 100
字符串型   str       "hello", "hi", "how are you"
布尔型     bool      true, false

列表型     list      [1, 2, 3], ["a", "b", "c"]
字典型     dict      {"name": "michael", "salary": 50000}, {"address": "SH", "weather": "snowing"}
```

#### 变量
```python
# 变量就是给一个值取个名字的意思
a = 1
b = "hi, hello"
c = true
d = [1, 2, 3]
e = {"food": "apple"}
```


#### 控制语句
```python
# 条件判断语句: 如果...就...否则...
if a < 1:
    print 0
else:
    print 2

# 嵌套的条件判断语句
if a < 1:
    print 0
elif < 2:
    print 1
else:
    print 2

# 循环语句:
# for循环
for i in [1, 2, 3, 4, 4]:
    print(i)

for k, v in {"name": "python", "age": 15}:
    print(k)
    print(v)

# while循环
print("while start")
a = 1
while a < 10:
    print(a)
    a = a + 1
print("while end")
```

#### 函数
```python
# 函数是程序的基本组织单位,可以说程序就是由一个个函数组成的
# 把一些通用的代码组合起来就是函数

# 函数的定义: def 函数名(参数):
def add(a, b):
    c = a + b
    print(c)

# 函数的使用: 函数名(参数)
add(1, 2)
```


#### 包
```python
# 包的概念其实就是文件夹和文件
# 包/模块/第三方库,都是一个意思,就是写好的代码放在文件里给别人引用,相同的功能你就不需要重复写了.
# 其实python的强大之一就在于各种功能的包很多,基本上你需要什么功能都有对应的包来用(pip install 包名)
一个文件就是一个包
一个文件夹也可以是一个包(此时需要在该文件夹下面建立一个叫__init__.py的文件)
```

#### ...
























