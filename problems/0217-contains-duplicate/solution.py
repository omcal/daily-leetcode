"""
217. Contains Duplicate
Difficulty: Easy
Link: https://leetcode.com/problems/contains-duplicate/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool: # type: ignore
        return len(set(nums))!=len(nums)