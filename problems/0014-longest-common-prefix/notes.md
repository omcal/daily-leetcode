---
number: 14
title: Longest Common Prefix
difficulty: Easy
tags: [array, string, trie]
date: 2026-08-01
url: https://leetcode.com/problems/longest-common-prefix/
---

## Approach

Vertical scan: walk column i over every string. Stop as soon as some
string is exhausted or disagrees with `strs[0][i]`; the collected chars
are the prefix.

## Complexity

- Time: O(n * m), m = prefix length
- Space: O(m)
