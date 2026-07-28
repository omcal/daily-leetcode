#!/usr/bin/env python3
"""
Curated problem lists (Blind 75, NeetCode, ...) and progress against them.

A list lives in lists/<slug>.json:

Lists are a *view*, not a gate: solving something outside every list still
counts toward the totals and the streak. Off-list solves are surfaced
explicitly so they don't feel invisible.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTS_DIR = ROOT / "lists"

DONE, TODO = "✅", "⬜"


def load_lists(lists_dir: Path = LISTS_DIR):
    """Load every lists/*.json, sorted by list name."""
    if not lists_dir.exists():
        return []
    out = []
    for path in sorted(lists_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("name", path.stem)
        data.setdefault("problems", [])
        data["slug"] = path.stem
        out.append(data)
    out.sort(key=lambda d: d["name"])
    return out


def percent(done: int, total: int) -> int:
    return round(100 * done / total) if total else 0


def list_progress(data, solved_by_number):
    """(solved_count, total) for one list."""
    numbers = {p["number"] for p in data["problems"]}
    return len(numbers & set(solved_by_number)), len(numbers)


def off_list_solves(lists, solved_by_number):
    """Solved problems that appear in no curated list, newest first."""
    listed = {p["number"] for data in lists for p in data["problems"]}
    return [
        row for number, row in sorted(solved_by_number.items()) if number not in listed
    ]


def render_list_markdown(data, solved_by_number) -> str:
    """Render one list to its own markdown page, ticking off what's solved."""
    done, total = list_progress(data, solved_by_number)

    lines = [f"# {data['name']}", ""]
    if data.get("note"):
        lines.append(f"{data['note']}")
        lines.append("")
    if data.get("url"):
        lines.append(f"Original list: <{data['url']}>")
        lines.append("")
    lines.append(f"**{done} / {total}** solved ({percent(done, total)}%)")
    lines += [
        "",
        "| | # | Problem | Difficulty | Mine |",
        "|---|---|---------|------------|------|",
    ]

    for p in data["problems"]:
        row = solved_by_number.get(p["number"])
        tick = DONE if row else TODO
        title = p["title"] + (" 🔒" if p.get("paid_only") else "")
        url = p.get("url") or f"https://leetcode.com/problems/{p['slug']}/"
        mine = f"[solution](../{row['folder']}/)" if row else "—"
        lines.append(
            f"| {tick} | {p['number']} | [{title}]({url}) "
            f"| {p.get('difficulty', '?')} | {mine} |"
        )

    return "\n".join(lines) + "\n"


def build_lists_block(lists, solved_by_number) -> str:
    """The compact per-list summary that goes in the README."""
    if not lists:
        return "_No curated lists yet._\n"

    # Blank-line separated so each list stays its own paragraph, however
    # many there are.
    blocks = []
    for data in lists:
        done, total = list_progress(data, solved_by_number)
        blocks.append(
            f"**[{data['name']}](lists/{data['slug']}.md)** — "
            f"{done}/{total} ({percent(done, total)}%)"
        )

    extra = off_list_solves(lists, solved_by_number)
    if extra:
        blocks.append(f"_Plus {len(extra)} solved outside the list.")
    return "\n\n".join(blocks) + "\n"


def write_list_pages(lists, solved_by_number, lists_dir: Path = LISTS_DIR):
    """Write lists/<slug>.md for each list. Returns the paths written."""
    written = []
    for data in lists:
        path = lists_dir / f"{data['slug']}.md"
        path.write_text(render_list_markdown(data, solved_by_number), encoding="utf-8")
        written.append(path)
    return written
