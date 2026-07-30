"""
704. Binary Search
Difficulty: Easy
Link: https://leetcode.com/problems/binary-search/
"""

'''
Example 1:

Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
Example 2:

Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1


'''
class Solution:
    def search(self, nums, target: int):
        res=-1
        l=0
        r=len(nums)-1
        while(l<=r):
            mid=(r-l)//2+l
            if target==nums[mid]:
                return mid
            elif nums[mid]>target:
                r=mid-1
            else:
                l=mid+1
        return res


