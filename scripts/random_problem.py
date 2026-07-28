#!/usr/bin/env python3
"""Print the number of a random LeetCode problem I haven't solved yet.

Picks from the whole problem set, skipping only what's already in problems/.

Usage:
    python scripts/random_problem.py
"""

import json
import random
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"

URL = "https://leetcode.com/graphql"
QUERY = """
query problemsetQuestionList($skip: Int, $limit: Int) {
  questionList: questionList(categorySlug: "", skip: $skip, limit: $limit, filters: {}) {
    total: totalNum
    questions: data {
      frontendQuestionId: questionFrontendId
    }
  }
}
"""


def already_solved():
    if not PROBLEMS_DIR.exists():
        return set()
    numbers = set()
    for folder in PROBLEMS_DIR.iterdir():
        match = re.match(r"(\d+)-", folder.name)
        if folder.is_dir() and match:
            numbers.add(int(match.group(1)))
    return numbers


def fetch(skip, limit=1):
    request = urllib.request.Request(
        URL,
        data=json.dumps(
            {
                "query": QUERY,
                "variables": {"skip": skip, "limit": limit},
                "operationName": "problemsetQuestionList",
            }
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "leetcode-repo-random",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)["data"]["questionList"]


def main():
    solved = already_solved()
    try:
        total = fetch(0)["total"]
        for _ in range(30):
            question = fetch(random.randrange(total))["questions"][0]
            number = int(question["frontendQuestionId"])
            if number in solved:
                continue
            print(number)
            return
    except Exception as exc:
        sys.exit(f"lookup failed: {exc}")
    sys.exit("gave up finding an unsolved problem")


if __name__ == "__main__":
    main()
