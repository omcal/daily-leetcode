# LeetCode Solutions

[![CI](https://github.com/omcal/daily-leetcode/actions/workflows/ci.yml/badge.svg)](https://github.com/omcal/daily-leetcode/actions/workflows/ci.yml)
[![Streak Reminder](https://github.com/omcal/daily-leetcode/actions/workflows/streak-reminder.yml/badge.svg)](https://github.com/omcal/daily-leetcode/actions/workflows/streak-reminder.yml)

<!-- STATS_START -->
**8 solved** · Easy 6 · Medium 2 · Hard 0  
**Current streak: 2 days** · longest 5
<!-- STATS_END -->

<!-- LISTS_START -->
_No curated lists yet._
<!-- LISTS_END -->

<!-- PROBLEMS_TABLE_START -->
| # | Title | Difficulty | Tags | Date |
|---|-------|------------|------|------|
| 0001 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | array, hash-table | 2026-07-28 |
| 0009 | [Palindrome Number](https://leetcode.com/problems/palindrome-number/) | Easy | math | 2026-07-28 |
| 0014 | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | Easy | array, string, trie | 2026-08-01 |
| 0036 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | Medium | array, hash-table, matrix | 2026-07-31 |
| 0200 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | array, breadth-first-search, depth-first-search, matrix, union-find | 2026-08-04 |
| 0682 | [Baseball Game](https://leetcode.com/problems/baseball-game/) | Easy | array, simulation, stack | 2026-08-03 |
| 0704 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | array, binary-search | 2026-07-30 |
| 1929 | [Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) | Easy | array, simulation | 2026-07-29 |
<!-- PROBLEMS_TABLE_END -->

## Otomasyon

| Workflow | Ne zaman | Ne yapar |
|---|---|---|
| [CI](.github/workflows/ci.yml) | her push / PR | `pytest` (Python 3.9 + 3.12), README güncel mi kontrolü |
| [Update README](.github/workflows/update-readme.yml) | `master`'a çözüm push'landığında | README istatistiklerini yeniden üretip commit'ler |
| [Streak Reminder](.github/workflows/streak-reminder.yml) | her gece 00:05 TRT | bir gün çözüm girilmediyse listeye e-posta + WhatsApp atar |

Hatırlatıcının secret kurulumu: [.github/NOTIFICATIONS.md](.github/NOTIFICATIONS.md)
