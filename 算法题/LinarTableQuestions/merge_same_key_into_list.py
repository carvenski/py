# encoding=utf-8

# 归并相同key的值到list, 使用defaultdict(list)
import collections
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]

d = collections.defaultdict(list) #this set default value type = list
for k, v in s:
    d[k].append(v)  # 就是将该dict的 k:v 的 v 都默认设置成 list 了 
print(d)

# or
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = {}
for k,v in s:
    if k not in d:
        d[k] = []
    d[k].append(v)
print(d)



