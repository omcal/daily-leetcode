"""
739. Daily Temperatures
Difficulty: Medium
Link: https://leetcode.com/problems/daily-temperatures/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


# There is a brute force solution o^2

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]: # type: ignore
        stack = []
        n = len(temperatures)

        result = [0] * n
      
        for i in range(n - 1, -1, -1):
            while stack and temperatures[stack[-1]] <= temperatures[i]:
                stack.pop()
          
            if stack:
                result[i] = stack[-1] - i
            stack.append(i)
      
        return result
