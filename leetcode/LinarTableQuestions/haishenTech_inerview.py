# encoding=utf8
l = [2, 11, 34, 22, 35, 10, 37, 3, 5, 17, 18, 82, 90, 35]
#            i ->
#       min          max
#                               i ->
#                                  j ->  

# find max profit and buy/sell date(index is date)
def max_profit_v1(l):
    _min = 0; _max = 1; p = l[1]-l[0]
    for i in xrange(len(l)):
        for j in xrange(i, len(l)):
            if l[j] - l[i] > p:
                _min = i
                _max = j
                p = l[j] - l[i]
    print(p, _min, _max)

def max_profit_v2(l):
    _min = 0; _max = 1; pmin = 0; pmax = 1; p = l[1]-l[0]
    for i in xrange(len(l)):
        if l[i] < l[_min]:  #在循环中记录最大最小值               
            _min = i
        if l[i] > l[_max]:
            _max = i
        if (_min < _max) and ((l[_max]-l[_min]) > p): #但仅当时间顺序正确才更新profit
            pmin = _min                               #必定会找到唯一的_min和_max !!
            pmax = _max
            p = l[_max] - l[_min] 
    print(p, pmin, pmax)

max_profit_v1(l[:])
max_profit_v2(l[:])            



