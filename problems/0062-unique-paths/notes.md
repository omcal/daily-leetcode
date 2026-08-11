---
number: 62
title: Unique Paths
difficulty: Medium
tags: [combinatorics, dynamic-programming, math]
date: 2026-08-10
url: https://leetcode.com/problems/unique-paths/
---

## Approach

Bottom-up DP over one row: `paths[j] = right + below`. Iterate the row
right-to-left m-1 times, keeping only the previous row.

## Complexity

- Time: O(m * n)
- Space: O(n)
