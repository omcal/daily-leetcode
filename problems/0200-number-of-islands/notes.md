---
number: 200
title: Number of Islands
difficulty: Medium
tags: [array, breadth-first-search, depth-first-search, matrix, union-find]
date: 2026-08-04
url: https://leetcode.com/problems/number-of-islands/
---

## Approach

Scan the grid; on an unvisited '1', increment the count and DFS in four
directions, marking cells visited so the whole island is consumed at once.

## Complexity

- Time: O(r * c)
- Space: O(r * c) for the visited set and recursion
