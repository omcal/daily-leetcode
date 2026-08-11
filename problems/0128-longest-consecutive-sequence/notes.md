---
number: 128
title: Longest Consecutive Sequence
difficulty: Medium
tags: [array, hash-table, union-find]
date: 2026-08-09
url: https://leetcode.com/problems/longest-consecutive-sequence/
---

## Approach

Put everything in a set. Only start counting at a sequence *head* - a
value with no `x - 1` in the set - then walk upward. Each element is
visited at most twice.

## Complexity

- Time: O(n)
- Space: O(n)
