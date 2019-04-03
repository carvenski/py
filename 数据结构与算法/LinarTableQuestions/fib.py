
'''fibonaqi generator '''
def fibonaqi(n):
    a, b = 0, 1
    while n:
        a, b = b, a+b
        yield b
        n -= 1
print fibonaqi(10)


def fib1(n):
    a, b = 0,1
    while n:
        yield b
        a, b = b,a
        n -= 1



def fib2(n):
    if n <= 1:
        return n
    return fib2(n-1) + fib2(n-2)



print fib2(30)






