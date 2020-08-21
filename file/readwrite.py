"""
无论是使用w/wb模式去写文件,最终都是会转成bytes去写进文件.
区别的是最终写的bytes里的数字是多少.
不同的编码规则不一样.
"""
s = "你好,测试二进制读写."
b = s.encode('utf8')

# write str
with open("z1", 'w') as f:
    f.write(s)

# write bytes with encoding
with open("z2", 'wb') as f:
    f.write(b)

# write bytes wihtout encoding
with open("z3", 'wb') as f:
    # 相当于自定义个编码规则,别人不知道编码规则, +10
    b = bytes([i + 10 for i in b]) 
    f.write(b)



