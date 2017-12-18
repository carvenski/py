

#覆盖写文件:
with open('xxxx.log', 'w') as f:
    f.write('test')

    
#追加写文件:
with open('xxxx.log', 'a') as f:
    f.write('test')

#换行追加写文件:
with open('xxxx.log', 'a') as f:
    f.write('test' + '\n')  # 手动加 \n 换行
# --------------------------------------------------------------------    
#按行读文件:
with open('xxxx.log', 'r') as f:
    for line in f:  # 直接for循环f即可,f是个迭代器,每次自动读一行
        print(line.strip())  # 一定要去除头尾空格和换行符

# 一次读10行:
with open('xxxx.log', 'r') as f:
    l = []
    for i in f:
        l.append(i.strip())
        if len(l) == 10:
            print(l)
            l = []
    if l:  # 末尾的几行零头别忘了
        print l

        

