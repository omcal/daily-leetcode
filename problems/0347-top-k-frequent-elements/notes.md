---
number: 347
title: Top K Frequent Elements
difficulty: Medium
tags: [array, hash-table, heap, bucket-sort]
date: 2026-08-09
url: https://leetcode.com/problems/top-k-frequent-elements/
---

## Approach

Count occurrences in a dict, then bucket sort: `fre[c]` holds every value seen
exactly `c` times. Since no value can occur more than `len(nums)` times the
buckets are bounded, so walking them from the highest count downward yields the
top k without a sort or a heap.

## Complexity

- Time: O(n)
- Space: O(n)
