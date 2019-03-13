"""
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this:
(you may want to display this pattern in a fixed font for better legibility)
n = 3:
P   A   H   N
A P L S I I G
Y   I   R

n = 4:
P    I    N 
A  L S  I G 
Y A  H R  
P    I  
And then read line by line: "PAHNAPLSIIGYIR"
Write the code that will take a string and make this conversion given a number of rows:
string convert(string text, int nRows);
convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".
"""

s = "qwertyuiopasdfghjklzxcvbnm"
# s= "PAYPALISHIRING"

n = 3  #rows
l = ['' for i in xrange(0, n)]  #使用一个[]存放每一行的字符,递归累加即可

def x(cursor=0):
    try:
        for i in xrange(0, n):
            l[i] += s[cursor]
            cursor += 1
        for j in (range(0, n))[::-1][1:-1]:
            l[j] += s[cursor]
            cursor += 1
        x(cursor)
    except IndexError:
        print('(cursor already in end:%s == string length:%s )' % (cursor, len(s) ))
        print(" origin string is: "+ s +"\n zigzag string is: " + "".join(l))

x()
        
    
    
