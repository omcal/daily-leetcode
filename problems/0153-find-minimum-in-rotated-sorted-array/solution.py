"""
153. Find Minimum in Rotated Sorted Array
Difficulty: Medium
Link: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401

class Solution:
    def findMin(self, arr: List[int]) -> int:
        l,r=0,len(arr)-1

        while l<r:
            mid=(l+r)//2
            if arr[mid]>arr[r]:
                l=mid+1
            else:
                r=mid
        return arr[l]