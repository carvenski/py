#encoding=utf-8

prices = [11, 0, 1, 12, 45, 46, 11, 5, 11, 1, 8, 2, 24]

def biggest_profit(prices):
    # 记录最小价格和最大差值,遍历即可:
    max_ = [prices[0], prices[1]-prices[0] ]
    for i in xrange(0, len(prices)-1 ):
        if prices[i] < max_[0]:
            max_[0] = prices[i]
        if prices[i] - max_[0] > max_[1]:
            max_[1] = prices[i] - max_[0]

    print(max_)

biggest_profit(prices)


'''find two price to buy and sell to get biggest profit in prices list'''
a = [1, 23, 3, 11, 4, 21, 45, 2, 7, 10, 25]

max_ = a[1] - a[0]
max_index = (max_, 0, 1)
for i in a:
    index_i = a.index(i)
    for j in a[ index_i+1: ]:    # 性能不够好: 2个循环 !!
        diff = j - i
        if diff > 0 and diff > max_:
            max_ = diff
            max_index = (max_, a.index(i), a.index(j) ) 
        continue
print max_index

# --------- better way to solve this problem(just use one loop !!)---------
prices = [11, 0, 5, 12, 45, 11, 5, 11, 1, 8, 2, 24]

def biggest_profit(prices):
    # 记录最小价格和最大差值,遍历即可:
    max_ = [prices[0], prices[1]-prices[0] ]
    for i in xrange(0, len(prices)-1 ):
        if prices[i] < max_[0]:
            max_[0] = prices[i]
        if prices[i] - max_[0] > max_[1]:
            max_[1] = prices[i] - max_[0]

    print(max_)

biggest_profit(prices)
