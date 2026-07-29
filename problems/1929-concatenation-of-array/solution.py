"""
1929. Concatenation of Array
Difficulty: Easy
Link: https://leetcode.com/problems/concatenation-of-array/
"""


class Solution:
    def getConcatenation(self, nums):

        n = len(nums)
        ans = [0] * (2 * n)

        for i in range(2 * n):
            ans[i] = nums[i % n]

        return ans
