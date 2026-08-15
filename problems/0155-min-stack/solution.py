"""
155. Min Stack
Difficulty: Medium
Link: https://leetcode.com/problems/min-stack/
"""
# LeetCode's judge preloads these, so solutions pasted from the site rely on
# them without importing. Locally and in CI nothing is preloaded -- keeping
# them here means a pasted solution imports cleanly instead of dying on a
# NameError at collection time. Drop whichever you don't use.
import collections  # noqa: F401
from typing import List, Optional  # noqa: F401


class MinStack:

    def __init__(self):
        self.stack = []
        self.minStack=[float('inf')]


    def push(self, value: int) -> None:
        self.stack.append(value)
        self.minStack.append(min(value,self.minStack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1] # type: ignore
        


