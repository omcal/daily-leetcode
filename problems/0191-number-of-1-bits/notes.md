---
number: 191
title: Number of 1 Bits
difficulty: Easy
tags: [bit-manipulation, divide-and-conquer]
date: 2026-08-05
url: https://leetcode.com/problems/number-of-1-bits/
---

## Approach

Brian Kernighan: `n &= n - 1` clears the lowest set bit. Count the
iterations until n is zero.

## Complexity

- Time: O(set bits)
- Space: O(1)
