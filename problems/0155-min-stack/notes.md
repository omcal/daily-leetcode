---
number: 155
title: Min Stack
difficulty: Medium
tags: [design, stack]
date: 2026-08-15
url: https://leetcode.com/problems/min-stack/
---

## Approach

Keep a second stack that mirrors the main one but stores the minimum of
everything at or below that level: `minStack.append(min(value, minStack[-1]))`.
Pops stay in sync, so `getMin` is just the top. Seeding with `inf` removes the
empty-stack special case.

## Complexity

- Time: O(1) per operation
- Space: O(n)
