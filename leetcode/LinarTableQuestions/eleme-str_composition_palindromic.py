
# all str compositions in this list, find which compositions are palindromic ? 
x = ['daad', 'ok', '123dcf', 'dcvcd', 'sdwdac', 'sa23fdf', 'adwd2e4', 'cdvf', 'vvfgrxzcd','as', 'sa', 'f', 'cde12vd', 'cf']
#                     j1                          <= i =>                                        j2
#                               k2                                      k1 

# how to get all str compositions ?






def is_panlindromic(s):
    n = len(s)
    if n%2 == 0:
        if s[0:n/2] == s[n/2:][::-1]:
            return True        
    if n%2 == 1:
        if s[0:(n-1)/2] == s[(n+1)/2+1-1:][::-1]:
            return True

def is_panlindromic2(s):
    pass

""" not include all compositions !
for i in range(len(x)):
    # j1 < i
    _sum = ''
    for j1 in range(i + 1):
        _sum += x[i - j1]
        if is_panlindromic(_sum):
            print('_sum:', _sum, 'i:', i, 'j1:', j1)
    
    # j2 > i
    _sum = ''
    for j2 in range(len(x) - i):
        _sum += x[i + j2]
        if is_panlindromic(_sum):
            print('_sum:', _sum, 'i:', i, 'j2:', j2)
"""            
        
