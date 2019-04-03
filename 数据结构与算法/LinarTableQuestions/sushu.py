#encoding=utf8

# 判断素数[101 - 200]
def sushu(num):
    for i in range(2, num):
        if num%i == 0: # 判断素数的关键
            return True # 不是素数
        continue

a= []
for i in range(101, 201):
    if not sushu(i):
        a.append(i)

print a
