#!/usr/bin/env python3
"""Autonomy-envelope gate (constraint FUN-AUTONOMY-01, critique C13).

Enforces the load-bearing edge of the copilot / autopilot boundary: a change to the
governing constitution — `constitution/mission.md` or `constitution/constraints.md` (Vision and
Constraints, "the governed truth") — must be accompanied by a recorded human decision,
i.e. a NEW ADR under `constitution/decisions/`. The copilot may drive the loop autonomously,
but it may not silently rewrite Vision or Constraints without a recorded decision
(Manifesto tenets 1, 8, 11).

Roadmap movement (ticking a checkbox in `constitution/roadmap.md`) is ordinary loop mechanics
and is deliberately NOT gated here, to avoid ceremony. Other stop conditions (drift,
ambiguity, generic boundary crossings) remain judgment triggers, documented in
`framework/doctrine/operating-model.md`, not this deterministic check.

Deterministic and fail-closed. Compares HEAD against a base ref via git.

Usage:
    python framework/scripts/check_autonomy.py [--base REF]
"""
from __future__ import annotations

import argparse
import subprocess
import sys

CONSTITUTION = {"constitution/mission.md", "constitution/constraints.md"}
ADR_PREFIX = "constitution/decisions/ADR-"


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def _resolve_base(base: str | None) -> str:
    if base:
        return base
    for candidate in ("origin/master", "master"):
        if _git("rev-parse", "--verify", "--quiet", candidate).returncode == 0:
            return candidate
    return "HEAD~1"


def _changed(base: str) -> tuple[list[tuple[str, str]], str | None]:
    """Return [(status, path), ...] for base...HEAD, or ([], error)."""
    result = _git("diff", "--name-status", f"{base}...HEAD")
    if result.returncode != 0:
        return [], result.stderr.strip() or f"cannot diff against {base}"
    rows: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            rows.append((parts[0], parts[-1]))  # (status, path); path=new for renames
    return rows, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Autonomy-envelope gate (FUN-AUTONOMY-01).")
    parser.add_argument("--base", default=None,
                        help="base ref to diff against (default: origin/master, then master, then HEAD~1)")
    args = parser.parse_args(argv)

    base = _resolve_base(args.base)
    rows, error = _changed(base)
    if error is not None:
        print(f"check_autonomy: {error}", file=sys.stderr)
        return 2

    constitution_changed = sorted({path for _st, path in rows if path in CONSTITUTION})
    adr_added = [path for status, path in rows
                 if status.startswith("A") and path.startswith(ADR_PREFIX) and path.endswith(".md")]

    if constitution_changed and not adr_added:
        print("FUN-AUTONOMY-01 FAILED: the constitution changed without a recorded "
              "decision (ADR).", file=sys.stderr)
        for path in constitution_changed:
            print(f"  - changed: {path}", file=sys.stderr)
        print(f"  add an ADR under constitution/decisions/ (ADR-YYYYMMDD-NN-*.md) recording the "
              f"human decision. (base={base})", file=sys.stderr)
        return 1

    if constitution_changed:
        print(f"autonomy gate OK: constitution change recorded by {', '.join(adr_added)} "
              f"(base={base}).")
    else:
        print(f"autonomy gate OK: no constitution change in range (base={base}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
