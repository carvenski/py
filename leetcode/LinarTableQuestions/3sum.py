"""
Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? Find all unique triplets in the
array which gives the sum of zero.
Note:
Elements in a triplet (a,b,c) must be in non-descending order. (ie, a <= b <= c)
The solution set must not contain duplicate triplets.
    For example, given array S = {-1 0 1 2 -1 -4},
    A solution set is:
    (-1, 0, 1)
    (-1, -1, 2)
"""
S = [-1, 0, 1, 2, -1, -4, 4, -2]

def find_3sum(l):
    for i in xrange(len(l)):
        for j in xrange(i+1, len(l)):
            for k in xrange(j+1, len(l)):
                if l[i]+l[j]+l[k]==0:
                    print(l[i],l[j],l[k])

find_3sum(S)                    

# must use 3 loops ??


