'''
1
Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution.

Example:
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
'''
class Solution(object):

    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # sort 
        nums2 = sorted(nums)
        import copy
        nums3 = copy.copy(nums2) 
        # iterate
        for i in nums3:
            nums2.remove(i)  # makes list shorten a bit, means index in for will get value of more a bit. 
            print i
            if (target-i) in nums2:
                if nums.index(i) == nums.index(target-i):
                    index_a = nums.index(i); nums.remove(i)
                    print [index_a, nums.index(i)+1]
                    return [index_a, nums.index(i)+1]
                print [nums.index(i), nums.index(target-i)]
                return [nums.index(i), nums.index(target-i)]

# or 
a = [1,37,2,40,3,4,5,8,7,44,55,12]

def b(c, d, n):
    if c+d == n:
        return True
    else:
        return False

def x(a, n):
    result = []
    for i in a:
        index_i = a.index(i)
        for j in a[ :index_i ]+a[ index_i+1: ]:
            if b(i, j, n):
                result.append( (index_i, a.index(j)) )
            continue
    return result

print x(a, 45)            



