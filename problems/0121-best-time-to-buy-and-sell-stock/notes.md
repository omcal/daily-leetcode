---
number: 121
title: Best Time to Buy and Sell Stock
difficulty: Easy
tags: [array, dynamic-programming]
date: 2026-08-08
url: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
---

## Approach

Track the cheapest price seen so far; at each day the best profit is
`price - minSoFar`. Keep the running maximum.

## Complexity

- Time: O(n)
- Space: O(1)
