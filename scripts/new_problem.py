#!/usr/bin/env python3
"""
Scaffold a new LeetCode problem folder from templates/.

Usage:
    python scripts/new_problem.py 1 "Two Sum" --difficulty Easy --tags array,hash-table --func twoSum
    python scripts/new_problem.py 206 "Reverse Linked List" -d Easy -t linked-list -f reverseList

    # Or let LeetCode fill in the title/difficulty/tags for you:
    python scripts/new_problem.py 42 --fetch
    python scripts/new_problem.py 42 "Trapping Rain Water" --fetch   # keep your title, fetch the rest

Creates:
    problems/0001-two-sum/
        solution.py
        test_solution.py
        notes.md
"""
import argparse
import datetime
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
TEMPLATES_DIR = ROOT / "templates"

DIFFICULTIES = ("Easy", "Medium", "Hard")

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
LEETCODE_QUESTION_LIST_QUERY = """
query problemsetQuestionList($skip: Int, $limit: Int, $filters: QuestionListFilterInput) {
  questionList: questionList(categorySlug: "", skip: $skip, limit: $limit, filters: $filters) {
    questions: data {
      frontendQuestionId: questionFrontendId
      title
      titleSlug
      difficulty
      topicTags { slug }
    }
  }
}
"""


def slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def pad(number: int) -> str:
    return f"{number:04d}"


def render(text: str, **kwargs) -> str:
    for key, value in kwargs.items():
        text = text.replace(f"{{{{{key}}}}}", str(value))
    return text


def normalize_difficulty(value: str) -> str:
    normalized = value.strip().capitalize()
    if normalized not in DIFFICULTIES:
        raise ValueError(
            f"Unknown difficulty {value!r}. Expected one of: {', '.join(DIFFICULTIES)}"
        )
    return normalized


def clean_tags(raw: str) -> list:
    seen = []
    for tag in raw.split(","):
        tag = tag.strip().lower()
        if tag and tag not in seen:
            seen.append(tag)
    return sorted(seen)


def find_existing_folder_for_number(number: int, problems_dir: Path = PROBLEMS_DIR):
    """Return the existing problems/ folder for this problem number, if any."""
    if not problems_dir.exists():
        return None
    prefix = f"{pad(number)}-"
    for folder in problems_dir.iterdir():
        if folder.is_dir() and folder.name.startswith(prefix):
            return folder
    return None


def fetch_from_leetcode(number: int, timeout: float = 6.0):
    """Look up a problem's title/difficulty/tags on leetcode.com by its number.

    Returns a dict on success, or None if the lookup failed (network error,
    unexpected response shape, or no matching problem). Never raises.
    """
    payload = {
        "query": LEETCODE_QUESTION_LIST_QUERY,
        "variables": {
            "skip": 0,
            "limit": 5,
            "filters": {"searchKeywords": str(number)},
        },
        "operationName": "problemsetQuestionList",
    }
    request = urllib.request.Request(
        LEETCODE_GRAPHQL_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "leetcode-repo-scaffolder",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None

    try:
        questions = body["data"]["questionList"]["questions"]
    except (KeyError, TypeError):
        return None

    for question in questions:
        if str(question.get("frontendQuestionId")) == str(number):
            return {
                "title": question["title"],
                "slug": question["titleSlug"],
                "difficulty": question["difficulty"],
                "tags": sorted(t["slug"] for t in question.get("topicTags", [])),
            }
    return None


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new LeetCode problem folder.")
    parser.add_argument("number", type=int, help="LeetCode problem number, e.g. 1")
    parser.add_argument("title", nargs="?", default=None,
                         help="Problem title, e.g. 'Two Sum' (omit to fetch it from LeetCode)")
    parser.add_argument("-d", "--difficulty", default=None,
                         help="Easy/Medium/Hard (case-insensitive)")
    parser.add_argument("-t", "--tags", default=None,
                         help="Comma-separated tags, e.g. array,hash-table")
    parser.add_argument("-f", "--func", default="solve",
                         help="Name of the main solution method, e.g. twoSum")
    parser.add_argument("-u", "--url", default="",
                         help="Link to the problem on leetcode.com (auto-guessed if omitted)")
    parser.add_argument("--fetch", action="store_true",
                         help="Fetch title/difficulty/tags from leetcode.com to fill in "
                              "whatever wasn't passed explicitly")
    parser.add_argument("--force", action="store_true",
                         help="Overwrite files if the folder already exists")
    args = parser.parse_args()

    if args.number <= 0:
        sys.exit(f"Problem number must be positive, got {args.number}")

    if not TEMPLATES_DIR.exists():
        sys.exit(f"Templates directory not found: {TEMPLATES_DIR}")

    fetched = None
    if args.title is None or args.fetch:
        fetched = fetch_from_leetcode(args.number)
        if args.title is None and fetched is None:
            sys.exit(
                f"No title given and the LeetCode lookup for #{args.number} failed.\n"
                "Pass a title explicitly, e.g.:\n"
                f'  python scripts/new_problem.py {args.number} "Problem Title" -d Easy -t tag1,tag2'
            )

    title = args.title or fetched["title"]

    if args.difficulty is not None:
        try:
            difficulty = normalize_difficulty(args.difficulty)
        except ValueError as exc:
            sys.exit(str(exc))
    elif fetched is not None:
        difficulty = fetched["difficulty"]
    else:
        difficulty = "Unknown"

    if args.tags is not None:
        tags_list = clean_tags(args.tags)
    elif fetched is not None:
        tags_list = fetched["tags"]
    else:
        tags_list = []

    slug = slugify(title)
    folder_name = f"{pad(args.number)}-{slug}"
    folder = PROBLEMS_DIR / folder_name

    existing = find_existing_folder_for_number(args.number)
    if existing is not None and existing.name != folder_name and not args.force:
        sys.exit(
            f"Problem #{args.number} already exists as {existing.name}, "
            f"which doesn't match the requested slug {folder_name!r}.\n"
            "Check for a typo in the title, or pass --force if this is intentional."
        )

    if folder.exists() and not args.force:
        print(f"Folder already exists: {folder}")
        print("Use --force to overwrite files in it.")
        sys.exit(1)

    folder.mkdir(parents=True, exist_ok=True)

    tags_yaml = "[" + ", ".join(tags_list) + "]" if tags_list else "[]"

    if args.url:
        url = args.url
    elif fetched:
        url = f"https://leetcode.com/problems/{fetched['slug']}/"
    else:
        url = f"https://leetcode.com/problems/{slug}/"

    context = {
        "number": args.number,
        "number_padded": pad(args.number),
        "title": title,
        "difficulty": difficulty,
        "tags": tags_yaml,
        "date": datetime.date.today().isoformat(),
        "func": args.func,
        "url": url,
    }

    files = {
        "solution.py": TEMPLATES_DIR / "solution.py",
        "test_solution.py": TEMPLATES_DIR / "test_solution.py",
        "notes.md": TEMPLATES_DIR / "notes.md",
    }

    for filename, template_path in files.items():
        if not template_path.exists():
            sys.exit(f"Missing template: {template_path}")

    for filename, template_path in files.items():
        template_text = template_path.read_text(encoding="utf-8")
        rendered = render(template_text, **context)
        (folder / filename).write_text(rendered, encoding="utf-8")

    source = "fetched from leetcode.com" if fetched and args.title is None else (
        "fetched, title kept from CLI" if fetched else "manual"
    )
    print(f"Created {folder} ({source})")
    for filename in files:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()
