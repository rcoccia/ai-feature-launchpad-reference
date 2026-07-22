#!/usr/bin/env python3
"""Deterministic pre-check for a reviewable Change Record implementation target."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "framework" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from change_record import ChangeRecordError, load_change_record, reviewable_problems


def check_record(record_path: Path, constraints: Path) -> list[str]:
    try:
        record = load_change_record(record_path, constraints)
    except ChangeRecordError as exc:
        return exc.problems
    if record.status != "confirmed":
        return [
            f"{record_path}: implementation target status is '{record.status}' "
            "(expected 'confirmed')"
        ]
    return [f"{record_path}: {problem}" for problem in reviewable_problems(record)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed Change Record review pre-check.")
    parser.add_argument("record", type=Path, help="dated Change Record path")
    parser.add_argument(
        "--constraints",
        type=Path,
        default=Path("constitution/constraints.md"),
        help="constraint artifact used to resolve activated obligation ids",
    )
    args = parser.parse_args(argv)
    problems = check_record(args.record, args.constraints)
    if problems:
        print("review-slice pre-check FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"review-slice pre-check OK: {args.record} is reviewable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
