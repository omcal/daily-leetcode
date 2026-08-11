---
number: 1
title: Two Sum
difficulty: Easy
tags: [array, hash-table]
date: 2026-07-28
url: https://leetcode.com/problems/two-sum/
---

## Approach

Scan once, keeping a hash map of value -> index. For each `num`, check
whether `target - num` was already seen; if so the pair is found.

## Complexity

- Time: O(n)
- Space: O(n)
