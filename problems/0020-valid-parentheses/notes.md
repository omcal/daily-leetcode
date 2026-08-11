---
number: 20
title: Valid Parentheses
difficulty: Easy
tags: [bracket-sequences, stack, string]
date: 2026-08-11
url: https://leetcode.com/problems/valid-parentheses/
---

## Approach

Push the *expected* closing bracket whenever an opener is seen. On a
closer, it must equal the top of the stack. Valid iff nothing is left
over at the end.

## Complexity

- Time: O(n)
- Space: O(n)
