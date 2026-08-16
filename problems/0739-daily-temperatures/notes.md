---
number: 739
title: Daily Temperatures
difficulty: Medium
tags: [array, monotonic-stack, stack]
date: 2026-08-16
url: https://leetcode.com/problems/daily-temperatures/
---

## Approach

Iterate backwards from right to left using a monotonic decreasing stack that
stores indices of future days. For each day, pop indices whose temperatures are
less than or equal to the current temperature (shadowed elements). If the stack
is non-empty, the top represents the nearest warmer day (`stack[-1] - i`);
otherwise, no warmer day exists (remains 0). Push the current index onto the stack.

## Complexity

- Time: O(n)
- Space: O(n)
