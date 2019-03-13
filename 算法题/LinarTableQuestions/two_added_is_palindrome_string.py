
'''return index of two string in list when them added is a palindrome '''        
a = ['asd', 'aba', 'dfg', 'dfd', 'ass', 'ssa']
c = ['ab', 'a']

def b(string):
    length = len(string)
    if length%2 == 0:
        # if string[:length/2][-1:] == string[length/2:]: #取反不是[-1:], 而是[::-1]  !!!
        if string[:length/2][::-1] == string[length/2:]:
            return True
        else:
            return False
    else:
        # if string[:(length-1)/2][-1:] == string[(length+1)/2:]:
        if string[:(length-1)/2][::-1] == string[(length+1)/2:]:
            return True
        else:
            return False

def x(a):
    result = []
    for i in a:
        index_i = a.index(i)
        for j in a[ :index_i ]+a[ index_i+1: ]:
            if b(i+j):
                result.append( (index_i, a.index(j)) )
            continue
    return result

print x(c)
print x(a)
