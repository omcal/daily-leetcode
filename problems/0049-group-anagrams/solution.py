"""
49. Group Anagrams
Difficulty: Medium
Link: https://leetcode.com/problems/group-anagrams/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        dict1={}
        for word in strs:
            hashedWord=''.join(sorted(word))
            if hashedWord not in dict1:
                dict1[hashedWord]=[word]
            else:
                dict1[hashedWord].append(word)
        return dict1.values() # type: ignore