import time

# v1---------------------------------------------
#THIS IS TOO SLOW !! REPEATED COMPUTING...

# def fib_recursive_no_cache(n):
#     if n < 2:
#         return n
#     else:
#         print n
#         return fib_recursive_no_cache(n-1) + fib_recursive_no_cache(n-2)

# t = time.time()
# print 'res: ', fib_recursive_no_cache(46)
# print 'fib_recursive_no_cache time: ', time.time() - t, 
# print '\n'

# v2---------------------------------------------
def deco(f):
    # cache fib(n)
    dic = {}
    def w(*args, **kw):
        k = args[0]
        if k not in dic:
            dic[k] = f(*args, **kw)                    
        return dic[k]
    return w

@deco
def fib_recursive(n):
    if n < 2:
        return n
    else:
        # print n
        return fib_recursive(n-1) + fib_recursive(n-2)

t = time.time()
print 'res: ', fib_recursive(46)
print 'fib_recursive time: ', time.time() - t, 
print '\n'


# v3---------------------------------------------
def fib_while(n):
    a , b = 0 ,1
    while n:
        a , b = b , a + b
        n -= 1
    return b

t = time.time()
print 'res: ', fib_recursive(46)
print 'fib_while time: ', time.time() - t, 



        
