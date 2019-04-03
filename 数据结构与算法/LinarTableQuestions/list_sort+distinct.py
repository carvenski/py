#encoding=utf8

l = [1, 2, 3, 6, 10, 10, 9, 9, 6, 5, 2, 2, 0, 0]
#    i->                      <- j   

# 思路:使用2个指针从头尾开始扫描(使用了多个指针但合起来也是O(n)而已!),比较i,j值,谁小谁推进.
# (有很多题目都可以使用 '多个指针同时扫描' 的方法来实现遍历!! 而不仅仅是1个指针从头到尾的扫法.)
def f(l):
    a, b = 0, len(l)-1
    c, d = (l[0] if l[0] <= l[-1] else l[-1]) - 1, []
    while a <= b:
        if l[a] <= l[b]:
             if l[a] > c:
                 c = l[a]
                 d.append(c)
             a += 1
        if l[a] > l[b]:
             if l[b] > c:
                 c = l[b]
                 d.append(c)              
             b -= 1
    return d
             
print(f(l))
