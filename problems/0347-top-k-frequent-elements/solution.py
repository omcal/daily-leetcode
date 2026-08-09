"""
347. Top K Frequent Elements
Difficulty: Medium
Link: https://leetcode.com/problems/top-k-frequent-elements/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count={}
        fre=[[] for i in range(len(nums)+1)]
        
        for n in nums:
            count[n] = 1 + count.get(n, 0)
        for z, t in count.items():
            fre[t].append(z)

        result=[]

        for i in range(len(fre)-1,0,-1):
            for elem in fre[i]:
                result.append(elem)
                if len(result)==k:
                    return result