"""
62. Unique Paths
Difficulty: Medium
Link: https://leetcode.com/problems/unique-paths/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row=[1]*n
        for i in range(m-1):
            newRow=[1]*n
            for j in range(n-2,-1,-1):
                newRow[j]=row[j]+newRow[j+1]
            row=newRow
        return row[0]