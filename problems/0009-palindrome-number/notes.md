---
number: 9
title: Palindrome Number
difficulty: Easy
tags: [math]
date: 2026-07-28
url: https://leetcode.com/problems/palindrome-number/
---

## Approach

Negatives are never palindromes. Otherwise stringify and compare the
i-th character with its mirror from the end.

## Complexity

- Time: O(d) for d digits
- Space: O(d) for the string
