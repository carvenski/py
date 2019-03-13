"""
Given n non-negative integers a1, a2, ..., an, where each represents a point at coordinate (i, ai). n vertical lines are
drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a
container, such that the container contains the most water.

Note: You may not slant the container.
"""

a = [20,3,6,3,7,12,4,1,7]

def max_containter(l):
    res = [0, 1, (1-0)*1]
    for i in xrange(len(l)):
        for j in xrange(i+1, len(l)):
            s = (j-i)*(l[j] if l[j]<l[i] else l[i])
            if s > res[2]:
                res = [i, j, s]
    print res

max_containter(a)

# can you use just one loop ??


                
            
