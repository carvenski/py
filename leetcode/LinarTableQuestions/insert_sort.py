#encoding=utf8

# insert sort
ls = [1, 2, 67, 0, 23, 6, 888, 3, 100, 21, 44, 17, 5]
#     0  1                i->
#                    <-j              

# 交换排序 ?
def exchange_sort(l):
    for i in range(1, len(l)):  # 1 - (length-1)
        j = i-1
        while 1:
            if l[j] > l[j+1]:  # by exchange j & i
                l[j], l[j+1] = l[j+1], l[j]
                if j > 0:
                    j -= 1
                else:
                    break
            else:
                break
    print(l)

# 插入排序
def insert_sort(l):
    for i in range(1, len(l)):  # 1 - (length-1) 
        j = i-1
        while 1:
            if l[j] > l[i]:  # by insert i after j
                if j > 0:
                    j -= 1
                    continue
                else:
                    l.insert(0, l[i]); del l[i+1];
                    break
            if j == (i - 1): break
            l.insert(j+1, l[i]); del l[i+1];
            break
    print(l)

exchange_sort(ls[:]) 
insert_sort(ls[:])



