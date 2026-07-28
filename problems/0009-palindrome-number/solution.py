"""
9. Palindrome Number
Difficulty: Easy
Link: https://leetcode.com/problems/palindrome-number/
"""

class Solution:
    def isPalindrome(self, x: int) -> bool:  # type: ignore
        if x < 0:
            return False
        a= str(x)
        for i in range(len(a)):
            if a[i]!=a[len(a)-1-i]:
                return False
        return True
