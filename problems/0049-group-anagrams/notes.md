---
number: 49
title: Group Anagrams
difficulty: Medium
tags: [array, hash-table, sorting, string]
date: 2026-08-08
url: https://leetcode.com/problems/group-anagrams/
---

## Approach

Key each word by its sorted letters; anagrams collide on the same key.
Return the buckets.

## Complexity

- Time: O(n * k log k) for k = word length
- Space: O(n * k)
