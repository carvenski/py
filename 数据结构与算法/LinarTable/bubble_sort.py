#encoding=utf8

# 冒泡排序
def bubble(l):
    # for i in l[1:]:
        # index_i = l.index(i)   ## 使用l.index函数的问题就在于 `相同数的索引只取前一个` !! 会导致错误
    for index_i in range(1, len(l) ):
        def x(index_i):         
            if index_i >= 1:
                if l[index_i] <= l[index_i-1]:
                    l[index_i-1], l[index_i] = l[index_i], l[index_i-1]
                index_i = index_i - 1
                x(index_i)
        x(index_i)
    return l
   
print bubble([222,221,5,2000, 5,1,13, 12,6,999,333,23,2000,4,9,333,45,90,2,0, 777,120,456]) 
