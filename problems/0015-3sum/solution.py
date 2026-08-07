"""
15. 3Sum
Difficulty: Medium
Link: https://leetcode.com/problems/3sum/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums=sorted(nums)
        result=[]

        for i,j in  enumerate(nums):
            if nums[i-1]==nums[i] and i>0:
                continue
            l=i+1
            r=len(nums)-1
            while l<r:
                ans=j+nums[l]+nums[r]
                if ans==0:
                    result.append([j,nums[l],nums[r]])
                    l+=1
                    while l<r and nums[l]==nums[l-1]:
                        l+=1
                elif ans>0:
                    r-=1
                elif ans<0:
                    l+=1
        return result