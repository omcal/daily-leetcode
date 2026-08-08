"""
121. Best Time to Buy and Sell Stock
Difficulty: Easy
Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices)<=1:
            return 0
        result=0
        startingPoint=prices[0]
        for i in prices:
            result=max(result,i-startingPoint)
            startingPoint=min(i,startingPoint)
        return result
