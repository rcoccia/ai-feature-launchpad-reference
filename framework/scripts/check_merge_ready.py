#!/usr/bin/env python3
"""Governed-merge gate over the canonical Change Record."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path, PurePosixPath

from change_record import ChangeRecordError, load_change_record, merge_ready_problems
from check_change_record import (
    _canonical_phase,
    _resolve_base,
    _root,
    check as check_branch,
    discover_record,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Governed-merge gate (FUN-MERGE-01).")
    parser.add_argument("--base", default=None, help="base ref (default: origin/master)")
    parser.add_argument(
        "--record",
        type=Path,
        help="check one Change Record directly instead of discovering it from the branch diff",
    )
    parser.add_argument(
        "--constraints",
        type=Path,
        default=Path("constitution/constraints.md"),
        help="constraint artifact used to resolve routed residuals",
    )
    args = parser.parse_args(argv)
    try:
        root = _root()
    except RuntimeError as exc:
        print(f"check_merge_ready: {exc}", file=sys.stderr)
        return 2
    constraints = args.constraints if args.constraints.is_absolute() else root / args.constraints
    base = _resolve_base(args.base)

    if args.record is None:
        heading, phase_error = _canonical_phase(root)
        if phase_error:
            print(f"check_merge_ready: {phase_error}", file=sys.stderr)
            return 2
        branch_problems = check_branch(base, constraints, heading)
        if branch_problems:
            print("FUN-MERGE-01 FAILED: Change Record branch contract is invalid:", file=sys.stderr)
            for problem in branch_problems:
                print(f"  - {problem}", file=sys.stderr)
            return 1
        relative, discovery_error = discover_record(base)
        if discovery_error is not None or relative is None:
            print(f"check_merge_ready: {discovery_error}", file=sys.stderr)
            return 2
        record_path = root / Path(*PurePosixPath(relative).parts)
    else:
        record_path = args.record if args.record.is_absolute() else root / args.record

    try:
        record = load_change_record(record_path, constraints)
    except ChangeRecordError as exc:
        print("FUN-MERGE-01 FAILED: Change Record is malformed:", file=sys.stderr)
        for problem in exc.problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    problems = merge_ready_problems(record, constraints)
    if problems:
        print("FUN-MERGE-01 FAILED: governed merge is not ready:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(
        "governed-merge gate OK: "
        f"{record.path.name} records STABLE/PROMOTE, complete evidence, closeout, "
        "and routed-residual dispositions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
