"""
1. Two Sum
Difficulty: Easy
Link: https://leetcode.com/problems/two-sum/
"""
import collections
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]: # type: ignore
        my_dict = collections.defaultdict(int)
        for i, num in enumerate(nums):
            if target - num in my_dict:
                return [my_dict[target - num], i]
            my_dict[num] = i
        