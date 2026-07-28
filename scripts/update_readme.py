#!/usr/bin/env python3
"""
Regenerate README.md with solve stats and a table of every solved problem.

Scans problems/*/notes.md for YAML frontmatter (number, title,
difficulty, tags, date, url), computes a streak + tag breakdown,
and writes them into README.md between marker comments, leaving
the rest of the README untouched.

Usage:
    python scripts/update_readme.py

Tip: wire this into a git pre-commit hook or a GitHub Action so
the stats never go stale.
"""
import datetime
import re
from pathlib import Path

import problem_lists

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
README_PATH = ROOT / "README.md"

STATS_START = "<!-- STATS_START -->"
STATS_END = "<!-- STATS_END -->"
LISTS_START = "<!-- LISTS_START -->"
LISTS_END = "<!-- LISTS_END -->"
TABLE_START = "<!-- PROBLEMS_TABLE_START -->"
TABLE_END = "<!-- PROBLEMS_TABLE_END -->"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            value = [v.strip() for v in inner.split(",") if v.strip()]
        data[key] = value
    return data


def collect_problems():
    rows = []
    if not PROBLEMS_DIR.exists():
        return rows
    for folder in sorted(PROBLEMS_DIR.iterdir()):
        notes = folder / "notes.md"
        if not folder.is_dir() or not notes.exists():
            continue
        meta = parse_frontmatter(notes.read_text(encoding="utf-8"))
        if not meta.get("number"):
            continue
        rows.append({
            "number": int(meta.get("number", 0)),
            "title": meta.get("title", folder.name),
            "difficulty": meta.get("difficulty", "Unknown"),
            "tags": meta.get("tags", []),
            "date": meta.get("date", ""),
            "url": meta.get("url", ""),
            "folder": f"{PROBLEMS_DIR.name}/{folder.name}",
        })
    rows.sort(key=lambda r: r["number"])
    return rows


def parse_dates(rows):
    dates = set()
    for r in rows:
        if not r["date"]:
            continue
        try:
            dates.add(datetime.date.fromisoformat(r["date"]))
        except ValueError:
            continue
    return sorted(dates)


def compute_streaks(dates, today=None):
    """Return (current_streak, longest_streak) in days, counting one solve-day as 1."""
    if not dates:
        return 0, 0

    today = today or datetime.date.today()
    longest = 1
    run = 1
    for prev, curr in zip(dates, dates[1:]):
        if (curr - prev).days == 1:
            run += 1
        else:
            longest = max(longest, run)
            run = 1
    longest = max(longest, run)

    last_solved = dates[-1]
    if (today - last_solved).days > 1:
        return 0, longest

    current = 1
    for i in range(len(dates) - 1, 0, -1):
        if (dates[i] - dates[i - 1]).days == 1:
            current += 1
        else:
            break
    return current, longest


def build_stats(rows) -> str:
    if not rows:
        return "_No problems solved yet — the streak starts today._\n"

    counts = {"Easy": 0, "Medium": 0, "Hard": 0, "Unknown": 0}
    for r in rows:
        counts[r["difficulty"]] = counts.get(r["difficulty"], 0) + 1

    dates = parse_dates(rows)
    current, longest = compute_streaks(dates)

    lines = [
        f"**{len(rows)} solved** · Easy {counts['Easy']} · Medium {counts['Medium']} · Hard {counts['Hard']}  ",
    ]
    if current > 0:
        lines.append(f"**Current streak: {current} day{'s' if current != 1 else ''}** · longest {longest}")
    else:
        lines.append(f"Streak's cold — longest run was {longest} day{'s' if longest != 1 else ''}. Solve one today.")

    return "\n".join(lines) + "\n"


def build_table(rows) -> str:
    if not rows:
        return "_No problems solved yet._\n"

    lines = [
        "| # | Title | Difficulty | Tags | Date |",
        "|---|-------|------------|------|------|",
    ]
    for r in rows:
        title_cell = f"[{r['title']}]({r['url']})" if r["url"] else r["title"]
        tags = ", ".join(r["tags"]) if isinstance(r["tags"], list) else r["tags"]
        lines.append(f"| {r['number']:04d} | {title_cell} | {r['difficulty']} | {tags} | {r['date']} |")
    return "\n".join(lines) + "\n"


def replace_block(content: str, start: str, end: str, body: str) -> str:
    """Replace the first start..end block, or append one if absent.

    Only the first occurrence is touched on purpose: if a stray duplicate
    marker pair ever ends up in the README (a bad merge, say), filling both
    would keep the duplicate silently in sync forever instead of letting it
    be noticed and deleted.
    """
    block = f"{start}\n{body}{end}"
    if start in content and end in content:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        return pattern.sub(lambda _: block, content, count=1)
    return content.rstrip() + "\n\n" + block + "\n"


def update_readme(rows):
    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
    else:
        content = (
            f"# LeetCode Solutions\n\n"
            f"{STATS_START}\n{STATS_END}\n\n"
            f"{LISTS_START}\n{LISTS_END}\n\n"
            f"{TABLE_START}\n{TABLE_END}\n"
        )

    solved_by_number = {r["number"]: r for r in rows}
    lists = problem_lists.load_lists()

    content = replace_block(content, STATS_START, STATS_END, build_stats(rows))
    content = replace_block(content, LISTS_START, LISTS_END,
                            problem_lists.build_lists_block(lists, solved_by_number))
    content = replace_block(content, TABLE_START, TABLE_END, build_table(rows))

    README_PATH.write_text(content, encoding="utf-8")

    pages = problem_lists.write_list_pages(lists, solved_by_number)
    print(f"Updated {README_PATH} with {len(rows)} problems.")
    for page, data in zip(pages, lists):
        done, total = problem_lists.list_progress(data, solved_by_number)
        print(f"  - {page.relative_to(ROOT)}: {done}/{total}")


def main():
    update_readme(collect_problems())


if __name__ == "__main__":
    main()
