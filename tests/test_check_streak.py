"""Tests for the streak check that drives the reminder workflow.

The point of these is that a bug here is silent: a wrong verdict either
spams the group or -- worse -- never fires and nobody notices.
"""
import datetime
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_streak  # noqa: E402


def row(number, date, title="Some Problem"):
    return {
        "number": number,
        "title": title,
        "difficulty": "Easy",
        "tags": [],
        "date": date,
        "url": "",
        "folder": f"problems/{number:04d}-x",
    }


DAY = datetime.date(2026, 8, 10)


def test_solved_yesterday_is_not_stale():
    """Midnight run: yesterday's solve counts, the day was used."""
    result = check_streak.summarize([row(1, "2026-08-09")], DAY, max_idle_days=1)
    assert result["stale"] is False
    assert result["days_idle"] == 1


def test_solved_today_is_not_stale():
    result = check_streak.summarize([row(1, "2026-08-10")], DAY, max_idle_days=1)
    assert result["stale"] is False
    assert result["days_idle"] == 0


def test_a_full_missed_day_is_stale():
    """Nothing on 08-09, so at midnight on 08-10 the streak is broken."""
    result = check_streak.summarize([row(1, "2026-08-08")], DAY, max_idle_days=1)
    assert result["stale"] is True
    assert result["days_idle"] == 2


def test_empty_repo_is_stale():
    result = check_streak.summarize([], DAY, max_idle_days=1)
    assert result["stale"] is True
    assert result["days_idle"] is None
    assert result["last_date"] == ""


def test_latest_date_wins_over_problem_order():
    rows = [row(500, "2026-08-01"), row(1, "2026-08-09")]
    result = check_streak.summarize(rows, DAY, max_idle_days=1)
    assert result["last_date"] == "2026-08-09"
    assert result["solved_total"] == 2


def test_last_titles_lists_everything_solved_that_day():
    rows = [row(1, "2026-08-09", "Two Sum"), row(9, "2026-08-09", "Palindrome Number")]
    result = check_streak.summarize(rows, DAY, max_idle_days=1)
    assert result["last_titles"] == ["Palindrome Number", "Two Sum"]


def test_max_idle_days_widens_the_grace_period():
    rows = [row(1, "2026-08-07")]  # 3 days before DAY
    assert check_streak.summarize(rows, DAY, max_idle_days=1)["stale"] is True
    assert check_streak.summarize(rows, DAY, max_idle_days=2)["stale"] is True
    assert check_streak.summarize(rows, DAY, max_idle_days=3)["stale"] is False


def test_unparseable_dates_are_ignored():
    rows = [row(1, "2026-08-09"), row(2, "not-a-date")]
    result = check_streak.summarize(rows, DAY, max_idle_days=1)
    assert result["last_date"] == "2026-08-09"


@pytest.mark.parametrize("date_str", ["2026-08-08", "2026-08-09"])
def test_message_mentions_the_last_solve(date_str):
    result = check_streak.summarize([row(1, date_str, "Two Sum")], DAY, max_idle_days=1)
    message = check_streak.render_message(result, repo_url="https://example.com/repo")
    assert date_str in message
    assert "Two Sum" in message
    assert "https://example.com/repo" in message


def test_message_for_empty_repo_does_not_claim_a_broken_streak():
    result = check_streak.summarize([], DAY, max_idle_days=1)
    message = check_streak.render_message(result)
    assert "henüz çözülmüş problem yok" in message


def test_github_output_is_written(tmp_path, monkeypatch):
    output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    result = check_streak.summarize([row(1, "2026-08-08")], DAY, max_idle_days=1)

    check_streak.write_github_output(result, "line one\nline two")

    written = output.read_text(encoding="utf-8")
    assert "stale=true\n" in written
    assert "days_idle=2\n" in written
    assert "last_date=2026-08-08\n" in written
    # Multi-line values must use the heredoc form or Actions rejects them.
    assert "message<<STREAK_EOF\nline one\nline two\nSTREAK_EOF\n" in written


def test_github_output_is_skipped_outside_actions(monkeypatch):
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    result = check_streak.summarize([], DAY, max_idle_days=1)
    check_streak.write_github_output(result, "x")  # must not raise
