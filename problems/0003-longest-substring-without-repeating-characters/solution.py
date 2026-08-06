"""
3. Longest Substring Without Repeating Characters
Difficulty: Medium
Link: https://leetcode.com/problems/longest-substring-without-repeating-characters/
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        mySet=set()
        result=0
        l=0
        for r in range(len(s)):
            while s[r] in mySet:
                mySet.remove(s[l])
                l+=1
            mySet.add(s[r])
            result=max(result,r-l+1)
        return result