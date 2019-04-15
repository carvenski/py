'''
Given a string, find the length of the longest substring without repeating characters.
Examples:
Given "abcabcbb", the answer is "abc", which the length is 3.
Given "bbbbb", the answer is "b", with the length of 1.
Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
'''
a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'()*+,-./:;<=>?@[]^_`{|"

def lengthOfLongestSubstring(self, x):
        def go(i2, s, l):
            if i2+1 < len(x) and x[i2+1] not in s:
                i2 += 1
                s += x[i2] 
                go(i2, s, l)
            else:
                l[1] = i2 - i - 1
                if len(s) > l[0]:
                    l[0] = len(s)

        l = [0, 0]
        for i in range(len(x) ):
            go(i+l[1], x[i:i+l[1]+1], l)
        return l[0]

print lengthOfLongestSubstring(a)



