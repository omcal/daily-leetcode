---
number: 682
title: Baseball Game
difficulty: Easy
tags: [array, simulation, stack]
date: 2026-08-03
url: https://leetcode.com/problems/baseball-game/
---

## Approach

Stack of recorded scores plus a running total. `+` pushes the sum of the
top two, `D` pushes double the top, `C` pops and subtracts; numbers are
pushed as-is. Adjust the total on every operation.

## Complexity

- Time: O(n)
- Space: O(n)
