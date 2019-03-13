"""
Write a function to find the longest common prefix string amongst an array of strings.
"""
l = ['hello', 'hehah', 'heli']

def find_prefix(l):
    i = 0
    prefix = ''
    while 1:
        s = l[0][i]
        res = map(lambda x: x==s, [e[i] for e in l])
        if all(res):
            prefix += s
            i += 1
        else:
            break
    print(prefix)

find_prefix(l)

# 性能不够好,循环太多??
