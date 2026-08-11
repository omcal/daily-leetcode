---
number: 704
title: Binary Search
difficulty: Easy
tags: [array, binary-search]
date: 2026-07-30
url: https://leetcode.com/problems/binary-search/
---

## Approach

Standard binary search on the sorted array. `mid = l + (r - l) // 2`
avoids overflow; move the boundary past mid each step. Return -1 if the
range empties.

## Complexity

- Time: O(log n)
- Space: O(1)
