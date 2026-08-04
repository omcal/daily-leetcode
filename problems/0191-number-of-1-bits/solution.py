"""
191. Number of 1 Bits
Difficulty: Easy
Link: https://leetcode.com/problems/number-of-1-bits/
"""


class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n != 0:
            n &= (n - 1)
            count += 1
        return count