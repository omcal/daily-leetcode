---
number: 1929
title: Concatenation of Array
difficulty: Easy
tags: [array, simulation]
date: 2026-07-29
url: https://leetcode.com/problems/concatenation-of-array/
---

## Approach

Allocate a 2n array and fill index i with `nums[i % n]`, which wraps
back to the start for the second copy.

## Complexity

- Time: O(n)
- Space: O(n) for the output
