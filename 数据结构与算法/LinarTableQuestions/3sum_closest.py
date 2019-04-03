"""
Given an array S of n integers, find three integers in S such that the sum is closest to a given number, target. Return
the sum of the three integers. You may assume that each input would have exactly one solution.

    For example, given array S = {-1 2 1 -4}, and target = 1.

    The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
"""
S = [-1, 0, 1, 2, -1, -4, 4, -2]
target = 2
min_diff = S[0] + S[1] + S[2]

def find_3sum(l):
    ijk = []
    for i in xrange(len(l)):
        for j in xrange(i+1, len(l)):
            for k in xrange(j+1, len(l)):
                if abs(l[i]+l[j]+l[k]-target) < abs(min_diff-target):
                    ijk = [l[i],l[j],l[k]]
    print(ijk, min_diff)

find_3sum(S)                    



