---
number: 3
title: Longest Substring Without Repeating Characters
difficulty: Medium
tags: [hash-table, sliding-window, string]
date: 2026-08-06
url: https://leetcode.com/problems/longest-substring-without-repeating-characters/
---

## Approach

Sliding window with a set of the characters currently inside it. Extend
right; while the new char is already in the set, shrink from the left.
Track the largest window size.

## Complexity

- Time: O(n)
- Space: O(min(n, alphabet))
