#!/usr/bin/env python3
"""
Check whether anyone has solved a problem recently enough, for the nudge bot.

Reads the same problems/*/notes.md frontmatter that update_readme.py does,
finds the most recent solve date, and decides whether the repo has gone
quiet. Prints a JSON summary to stdout and, when running inside GitHub
Actions, writes the same fields to $GITHUB_OUTPUT.

Usage:
    python scripts/check_streak.py
    python scripts/check_streak.py --max-idle-days 2
    python scripts/check_streak.py --today 2026-08-01   # pretend it's that day

Exits 0 whether or not the repo is stale -- staleness is a result, not an
error. A non-zero exit means the check itself couldn't run.
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import update_readme  # noqa: E402  (needs the sys.path line above)

# Turkey has been on permanent UTC+3 since 2016, so a fixed offset is a safe
# fallback when the tz database isn't installed.
DEFAULT_TZ = "Europe/Istanbul"
FALLBACK_OFFSET = datetime.timedelta(hours=3)


def today_in(tz_name: str) -> datetime.date:
    try:
        from zoneinfo import ZoneInfo

        return datetime.datetime.now(ZoneInfo(tz_name)).date()
    except Exception:
        tz = datetime.timezone(FALLBACK_OFFSET)
        return datetime.datetime.now(tz).date()


def summarize(rows, today: datetime.date, max_idle_days: int) -> dict:
    """Build the staleness verdict from parsed problem rows."""
    dates = update_readme.parse_dates(rows)
    current, longest = update_readme.compute_streaks(dates, today=today)

    if not dates:
        return {
            "stale": True,
            "days_idle": None,
            "last_date": "",
            "last_titles": [],
            "solved_total": len(rows),
            "current_streak": 0,
            "longest_streak": longest,
            "today": today.isoformat(),
            "max_idle_days": max_idle_days,
        }

    last_date = dates[-1]
    days_idle = (today - last_date).days
    last_titles = [r["title"] for r in rows if r["date"] == last_date.isoformat()]

    return {
        "stale": days_idle > max_idle_days,
        "days_idle": days_idle,
        "last_date": last_date.isoformat(),
        "last_titles": sorted(last_titles),
        "solved_total": len(rows),
        "current_streak": current,
        "longest_streak": longest,
        "today": today.isoformat(),
        "max_idle_days": max_idle_days,
    }


def render_message(result: dict, repo_url: str = "") -> str:
    """The human-facing nudge, in Turkish -- reused for both mail and WhatsApp."""
    if result["days_idle"] is None:
        lines = [
            "Repo'da henüz çözülmüş problem yok.",
            "İlk problemi çözüp seriyi başlatma sırası sizde.",
        ]
    else:
        titles = ", ".join(result["last_titles"]) or "-"
        days = result["days_idle"]
        # This also renders on a forced test run, when the streak is fine --
        # so don't announce a broken streak unless it actually broke.
        if result["stale"]:
            status = f"Üzerinden {days} gün geçti — seri kırıldı."
            call_to_action = "Bugün bir problem çözüp seriyi yeniden başlatalım."
        else:
            status = f"Üzerinden {days} gün geçti — seri hâlâ ayakta."
            call_to_action = "Seriyi sürdürmek için bugün de bir problem çözelim."
        lines = [
            f"Son çözüm: {result['last_date']} ({titles})",
            status,
            f"Toplam {result['solved_total']} problem · en uzun seri {result['longest_streak']} gün.",
            "",
            call_to_action,
        ]
    if repo_url:
        lines += ["", repo_url]
    return "\n".join(lines)


def write_github_output(result: dict, message: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    days_idle = "" if result["days_idle"] is None else str(result["days_idle"])
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"stale={'true' if result['stale'] else 'false'}\n")
        handle.write(f"days_idle={days_idle}\n")
        handle.write(f"last_date={result['last_date']}\n")
        handle.write(f"solved_total={result['solved_total']}\n")
        # Multi-line values need the heredoc form.
        handle.write("message<<STREAK_EOF\n")
        handle.write(message.rstrip("\n") + "\n")
        handle.write("STREAK_EOF\n")


def main():
    parser = argparse.ArgumentParser(description="Check how long the repo has been quiet.")
    parser.add_argument("--max-idle-days", type=int, default=1,
                        help="Alert when the last solve is older than this many days (default: 1)")
    parser.add_argument("--tz", default=os.environ.get("STREAK_TZ", DEFAULT_TZ),
                        help=f"Timezone the day boundary is measured in (default: {DEFAULT_TZ})")
    parser.add_argument("--today", default=None,
                        help="Override today's date as YYYY-MM-DD (for testing)")
    parser.add_argument("--repo-url", default=os.environ.get("REPO_URL", ""),
                        help="Link appended to the reminder message")
    parser.add_argument("--message-only", action="store_true",
                        help="Print just the reminder text, for piping into notify.py")
    args = parser.parse_args()

    if args.max_idle_days < 0:
        sys.exit(f"--max-idle-days must be >= 0, got {args.max_idle_days}")

    if args.today:
        try:
            today = datetime.date.fromisoformat(args.today)
        except ValueError:
            sys.exit(f"--today must be YYYY-MM-DD, got {args.today!r}")
    else:
        today = today_in(args.tz)

    result = summarize(update_readme.collect_problems(), today, args.max_idle_days)
    message = render_message(result, args.repo_url)

    write_github_output(result, message)

    if args.message_only:
        print(message)
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- message ---\n{message}", file=sys.stderr)


if __name__ == "__main__":
    main()
