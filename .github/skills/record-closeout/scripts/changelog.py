#!/usr/bin/env python3
"""Maintain CHANGELOG.md from git commit history (deterministic closeout helper).

Groups commit subjects by date, newest first. On first run it builds the file
from full history; on later runs it appends only commits newer than the last
recorded one.

The last recorded commit is tracked by an embedded **commit-SHA marker**
(``<!-- changelog:last-commit <sha> -->``) rather than by the latest date
heading. This fixes a real bug: date-based tracking (``--after=<date>``) dropped
commits made on the *same day* as the latest heading, because ``--after`` is
date-exclusive. Because human editors reword bullets, deduping by subject is not
reliable either -- the SHA marker is the only robust cursor.

Output is UTF-8 (no BOM) with CRLF line endings on every OS, so the file
satisfies the documentation constraint (NFR-DOCS-01) even on Linux/CI.

Usage:
    python changelog.py [--path CHANGELOG.md]

Run from the repository root (the directory containing .git/).

Inspired by the DeepLearning.AI Spec-Driven Development course; reimplemented
and hardened for the Control Tower record-closeout skill.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DATE_FMT = "%Y-%m-%d"
MARKER_PREFIX = "<!-- changelog:last-commit "
MARKER_SUFFIX = " -->"


def git(args: list[str]) -> str:
    """Run a git command from the current directory and return stdout."""
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def head_sha() -> str | None:
    """Return the HEAD commit SHA, or None if the repo has no commits."""
    try:
        out = git(["rev-parse", "HEAD"]).strip()
    except subprocess.CalledProcessError:
        return None
    return out or None


def commits_by_date(revrange: str | None = None) -> dict[str, list[str]]:
    """Return {date: [subject, ...]} newest-first from git log.

    When revrange is given (e.g. ``<sha>..HEAD``) only that range is listed.
    """
    cmd = ["log", "--date=short", "--format=%ad|%s"]
    if revrange:
        cmd.append(revrange)
    grouped: dict[str, list[str]] = defaultdict(list)
    for line in git(cmd).splitlines():
        if "|" in line:
            date, subject = line.split("|", 1)
            grouped[date.strip()].append(subject.strip())
    return grouped


def find_marker(text: str) -> str | None:
    """Return the tracked commit SHA from the marker, or None if absent."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(MARKER_PREFIX) and stripped.endswith(MARKER_SUFFIX):
            sha = stripped[len(MARKER_PREFIX):-len(MARKER_SUFFIX)].strip()
            return sha or None
    return None


def latest_dated_heading(text: str) -> str | None:
    """Return the first '## YYYY-MM-DD' heading found, or None."""
    for line in text.splitlines():
        if line.startswith("## "):
            candidate = line[3:].strip()
            try:
                datetime.strptime(candidate, DATE_FMT)
                return candidate
            except ValueError:
                continue
    return None


def marker_line(sha: str) -> str:
    return f"{MARKER_PREFIX}{sha}{MARKER_SUFFIX}"


def total(grouped: dict[str, list[str]]) -> int:
    return sum(len(v) for v in grouped.values())


def render_section(date: str, subjects: list[str]) -> list[str]:
    return [f"\n## {date}\n", *(f"- {subject}\n" for subject in subjects)]


def write_crlf(path: Path, text: str) -> None:
    """Write UTF-8 (no BOM) with CRLF newlines regardless of platform."""
    normalized = text.replace("\r\n", "\n").replace("\n", "\r\n")
    path.write_bytes(normalized.encode("utf-8"))


def build_full(grouped: dict[str, list[str]], head: str) -> str:
    parts = ["# Changelog\n", marker_line(head) + "\n"]
    for date in sorted(grouped, reverse=True):
        parts.extend(render_section(date, grouped[date]))
    return "".join(parts)


def heading_index(lines: list[str], date: str) -> int | None:
    target = f"## {date}"
    for i, line in enumerate(lines):
        if line.strip() == target:
            return i
    return None


def merge(existing: str, grouped: dict[str, list[str]], head: str) -> str:
    """Insert new commits into existing content and refresh the marker.

    New dates get a section at the top (newest-first); dates that already have a
    heading get their bullets inserted at the top of that date's list.
    """
    lines = [line for line in existing.splitlines(keepends=True) if find_marker(line) is None]
    title_end = 1 if lines and lines[0].startswith("# ") else 0
    lines[title_end:title_end] = [marker_line(head) + "\n"]
    new_section_at = title_end + 1

    for date in sorted(grouped):  # oldest first, so the newest ends up on top
        subjects = grouped[date]
        idx = heading_index(lines, date)
        if idx is not None:
            pos = idx + 1
            if pos < len(lines) and lines[pos].strip() == "":
                pos += 1  # keep the blank line between heading and bullets
            lines[pos:pos] = [f"- {subject}\n" for subject in subjects]
        else:
            lines[new_section_at:new_section_at] = render_section(date, subjects)
    return "".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update CHANGELOG.md from git history.")
    parser.add_argument("--path", default="CHANGELOG.md",
                        help="changelog file path (default: CHANGELOG.md)")
    args = parser.parse_args(argv)
    path = Path(args.path)

    head = head_sha()
    if head is None:
        print("No commits found - nothing to write.")
        return 0

    if not path.exists():
        grouped = commits_by_date()
        if not grouped:
            print("No commits found - nothing to write.")
            return 0
        write_crlf(path, build_full(grouped, head))
        print(f"Created {path} with {total(grouped)} entries; tracking from {head[:9]}.")
        return 0

    existing = path.read_text(encoding="utf-8")
    marker = find_marker(existing)

    if marker:
        grouped = commits_by_date(f"{marker}..HEAD")
        if not grouped:
            print("No new commits since last entry - changelog is up to date.")
            return 0
        write_crlf(path, merge(existing, grouped, head))
        print(f"Added {total(grouped)} new entries to {path}; tracking from {head[:9]}.")
        return 0

    # Legacy changelog with no marker: preserve the old cross-day behaviour for
    # the transition (a date cannot be resolved to a commit), then install the
    # marker so future same-day commits are captured precisely.
    last = latest_dated_heading(existing)
    grouped: dict[str, list[str]] = defaultdict(list)
    if last:
        for line in git(["log", "--date=short", "--format=%ad|%s", f"--after={last}"]).splitlines():
            if "|" in line:
                date, subject = line.split("|", 1)
                grouped[date.strip()].append(subject.strip())
        grouped.pop(last, None)
    else:
        grouped = commits_by_date()

    write_crlf(path, merge(existing, grouped, head))
    if grouped:
        print(f"Added {total(grouped)} entries and initialized SHA tracking from {head[:9]}.")
    else:
        print(f"Initialized same-day-safe SHA tracking from {head[:9]}; no cross-day commits to add.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
