"""
128. Longest Consecutive Sequence
Difficulty: Medium
Link: https://leetcode.com/problems/longest-consecutive-sequence/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        mySet=set(nums)
        result=0
        temp=0
        for i in nums:
            if i-1 not in mySet:
                temp=1
                while i+1 in mySet:
                    temp+=1
                    i+=1
                result=max(temp,result)
        return result
