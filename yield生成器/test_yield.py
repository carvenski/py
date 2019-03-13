def x():
    print("start")
    n = 5
    while n > 0:
        yield n
        n -= 1
    print("end")
    return 1

a = x()

print a.next()
print a.next()
print a.next()
print a.next()
print a.next()

print ".6"
print a.next()

print ".7"
print a.next()
