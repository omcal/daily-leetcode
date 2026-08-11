---
number: 15
title: 3Sum
difficulty: Medium
tags: [array, sorting, two-pointers]
date: 2026-08-07
url: https://leetcode.com/problems/3sum/
---

## Approach

Sort, then fix each `nums[i]` and two-pointer over the rest for the pair
summing to `-nums[i]`. Skip duplicate anchors and duplicate left values
so each triplet is emitted once.

## Complexity

- Time: O(n^2)
- Space: O(1) beyond the sort and output
