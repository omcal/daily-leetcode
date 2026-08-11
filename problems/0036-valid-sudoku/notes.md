---
number: 36
title: Valid Sudoku
difficulty: Medium
tags: [array, hash-table, matrix]
date: 2026-07-31
url: https://leetcode.com/problems/valid-sudoku/
---

## Approach

One pass over the 81 cells, with a set per row, per column, and per 3x3
box keyed by `(r//3, c//3)`. A digit already present in any of the three
means invalid.

## Complexity

- Time: O(1) - fixed 9x9 board
- Space: O(1)
