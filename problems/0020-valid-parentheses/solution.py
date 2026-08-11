"""
20. Valid Parentheses
Difficulty: Easy
Link: https://leetcode.com/problems/valid-parentheses/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class Solution:
    def isValid(self, s: str) -> bool:
        myStack=[]
        myDict={'{':'}','[':']','(':')'}
        for i in s:
            if i in myDict.keys():
                myStack.append(myDict[i])
            elif i in myDict.values():
                if not myStack or   i!=myStack.pop():
                    return False
            else:
                return False
        return len(myStack)==0
