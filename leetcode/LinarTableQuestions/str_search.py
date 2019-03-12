
s = "cmdshjcbdsjvhgdj1abc1cdhfbjffabcjfvmbfjbjfabcabc"
m = "abc"

# 1.simple search substr:
def search(string, match):
    for i in xrange(len(string)):
        if string[i] == match[0]:
            j = 0
            while 1:
                if (i+j)<len(string) and string[i+j] == match[0+j]:
                    j += 1
                    if j == len(match):
                        print("[found] match in index %s: %s" % (i, string[i:(i+len(match))]))
                        break
                else:                     
                    break

search(s, m)                    

# 2.KMP search substr:
def search_KMP():
    pass













