
s = "-12dfghjk+f43fcd+cdf-23"

def is_int(cursor, num):
    if s[cursor] in '0123456789':
        num += s[cursor]
        if cursor == len(s) - 1:
            return num
        cursor += 1
        num = is_int(cursor, num)
    return num
        
num = ""
for i in xrange(0, len(s)):
    if s[i] in '0123456789':
        if i != 0 and s[i-1] in ['+', '-']:
            num = s[i-1] + num
        num = is_int(i, num)
        print(num)
        break

            
# can't solve them very quickly, thinking is too slow...



