# LeetCode Solutions

[![CI](https://github.com/omcal/daily-leetcode/actions/workflows/ci.yml/badge.svg)](https://github.com/omcal/daily-leetcode/actions/workflows/ci.yml)
[![Streak Reminder](https://github.com/omcal/daily-leetcode/actions/workflows/streak-reminder.yml/badge.svg)](https://github.com/omcal/daily-leetcode/actions/workflows/streak-reminder.yml)

<!-- STATS_START -->
**2 solved** · Easy 2 · Medium 0 · Hard 0  
**Current streak: 1 day** · longest 1
<!-- STATS_END -->

<!-- LISTS_START -->
_No curated lists yet._
<!-- LISTS_END -->

<!-- PROBLEMS_TABLE_START -->
| # | Title | Difficulty | Tags | Date |
|---|-------|------------|------|------|
| 0001 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | array, hash-table | 2026-07-28 |
| 0009 | [Palindrome Number](https://leetcode.com/problems/palindrome-number/) | Easy | math | 2026-07-28 |
<!-- PROBLEMS_TABLE_END -->

## Otomasyon

| Workflow | Ne zaman | Ne yapar |
|---|---|---|
| [CI](.github/workflows/ci.yml) | her push / PR | `pytest` (Python 3.9 + 3.12), README güncel mi kontrolü |
| [Update README](.github/workflows/update-readme.yml) | `master`'a çözüm push'landığında | README istatistiklerini yeniden üretip commit'ler |
| [Streak Reminder](.github/workflows/streak-reminder.yml) | her gece 00:05 TRT | bir gün çözüm girilmediyse listeye e-posta + WhatsApp atar |

Hatırlatıcının secret kurulumu: [.github/NOTIFICATIONS.md](.github/NOTIFICATIONS.md)
