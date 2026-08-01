"""
14. Longest Common Prefix
Difficulty: Easy
Link: https://leetcode.com/problems/longest-common-prefix/
"""

class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""
        if len(strs) == 1:
            return strs[0]
        
        prefix = []
        for i in range(len(strs[0])):
            for j in range(1, len(strs)):
                if i >= len(strs[j]) or strs[0][i] != strs[j][i]:
                    return "".join(prefix)
            
            prefix.append(strs[0][i])
            
        return "".join(prefix)