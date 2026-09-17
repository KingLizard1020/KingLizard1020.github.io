#!/usr/bin/env python3
"""Fail if commits on this branch are authored or co-authored by Cursor."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

FORBIDDEN = (
    "cursoragent@cursor.com",
    "co-authored-by: cursor agent",
    "made-with: cursor",
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def pr_range() -> str | None:
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path:
        return None
    event = json.loads(Path(path).read_text())
    pr = event.get("pull_request")
    if not pr:
        return None
    return f"{pr['base']['sha']}..{pr['head']['sha']}"


def main() -> int:
    rng = pr_range()
    if rng:
        log = git("log", "--format=%an <%ae>%n%cn <%ce>%n%B%n---", rng)
        if not log.strip():
            print(f"No commits in {rng}.")
            return 0
    elif os.environ.get("GITHUB_BASE_REF"):
        base = os.environ["GITHUB_BASE_REF"]
        subprocess.check_call(["git", "fetch", "--quiet", "origin", base])
        rng = f"origin/{base}..HEAD"
        log = git("log", "--format=%an <%ae>%n%cn <%ce>%n%B%n---", rng)
    else:
        log = git("log", "-1", "--format=%an <%ae>%n%cn <%ce>%n%B")

    lowered = log.lower()
    hits = [needle for needle in FORBIDDEN if needle in lowered]
    if hits:
        print("Commit attribution includes Cursor. Author and commit as the")
        print("repo owner, and do not add a Cursor co-author trailer.")
        print()
        print(log)
        return 1
    print("Attribution check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
