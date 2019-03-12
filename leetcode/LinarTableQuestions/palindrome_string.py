
''' find symmetry/palindrome string like 'abhba' 'xxyy' '''
a = 'adabbhbbaarhjjhwfvfkdhviuftghoituutdfgdggfhfggjjkjjutghkjlioipplltwertyiioouuttyyuyyicvggouuyy'
i = 1

def go(x, y):
    if a[x] == a[y]:
        x -= 1; y += 1
        go(x, y)
    else:
        if (i-x) > 1:
            print(a[x+1:y])

a = a + ' '  # cause a[i+1] will raise a Exception !
for s in a[1:-1]:
    if a[i] == a[i+1]:
        print a[i]+a[i+1]
        x = i; y = i + 1
        go(x, y)
    else:
        x = i - 1; y = i + 1
        go(x, y)
    i += 1




