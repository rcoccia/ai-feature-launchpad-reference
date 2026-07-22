#!/usr/bin/env python3
"""Deterministic pre-check for the `architecture-review` gate (constraint FUN-ARCHREVIEW-01).

The confirmation-bias problem the field test surfaced: the architect designs AND judges its
own design. The fix is producer != judge applied to the *design* — an independent challenge
BEFORE code. This script is only the deterministic half: it verifies a design is *challenge-
able*, i.e. well-formed enough to be attacked. It does NOT judge the design's merit (that is
the reviewer-agent's hostile semantic checklist).

A design is challenge-able when:
  1. design-under-test - a terse `design-under-test.md` exists and is non-empty (this, and
     NOT the ADR's persuasive prose, is what the challenger receives — the structural defence
     against "two Sonnets converging");
  2. alternatives      - the ADR weighed >= 2 real alternatives (a single-option ADR has
     nothing to challenge);
  3. negative consequence - the ADR names at least one negative/risk/trade-off consequence
     (an all-upside ADR is a red flag: unexamined cost);
  4. constraint resolution - any constraint.id cited in the design-under-test resolves in the
     constraints file (the design is anchored to the contract, not floating).

Placeholder ids (`<TEC-...>`) never resolve and never count. Standard library only.
Fail-closed: any problem exits non-zero. Run from the repository root.

Usage:
    python check_architecture.py <design_dir> --adr <ADR_PATH> --constraints <CONSTRAINTS_PATH>

Use explicit `--adr` and `--constraints` for the canonical separated layout: the design directory
contains `design-under-test.md`, while the ADR and constraints live elsewhere. The shorthand
remains supported only when `<design_dir>` contains an ADR file (`adr.md` or `ADR-*.md`) and
`constraints.md`. Constraints otherwise resolve against, in order: --constraints,
<design_dir>/constraints.md, constitution/constraints.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"\b[A-Z]{2,5}(?:-[A-Z0-9]+)+-\d+\b")
ALTERNATIVES_RE = re.compile(r"alternativ", re.IGNORECASE)
CONSEQUENCES_RE = re.compile(r"consequen|conseguenz", re.IGNORECASE)
NEGATIVE_RE = re.compile(r"negativ|rischi|\brisks?\b|contro|trade.?off", re.IGNORECASE)
SUBHEADING_RE = re.compile(r"^#{3,}\s+\S")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]\s+|\d+[.)]\s+)\S")
MIN_ALTERNATIVES = 2


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _section_body(text: str, heading_re: re.Pattern[str]) -> str | None:
    """Body of the first heading matching `heading_re`, up to the next same-or-higher heading."""
    lines = text.splitlines()
    start = None
    start_level = 0
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m and heading_re.match(m.group(2).strip()):
            start = i
            start_level = len(m.group(1))
            break
    if start is None:
        return None
    body: list[str] = []
    for ln in lines[start + 1:]:
        m = re.match(r"^(#{1,6})\s", ln)
        if m and len(m.group(1)) <= start_level:
            break
        body.append(ln)
    return "\n".join(body)


def _count_alternatives(section: str) -> int:
    """Count subheadings first; fall back to top-level list items."""
    subheadings = sum(1 for ln in section.splitlines() if SUBHEADING_RE.match(ln))
    if subheadings:
        return subheadings
    return sum(1 for ln in section.splitlines() if LIST_ITEM_RE.match(ln))


def _find_adr(design_dir: Path) -> Path | None:
    direct = design_dir / "adr.md"
    if direct.is_file():
        return direct
    adrs = sorted(design_dir.glob("ADR*.md"))
    return adrs[0] if adrs else None


def _constraints_ids(design_dir: Path, override: str | None) -> set[str]:
    candidates = [Path(override)] if override else []
    candidates += [design_dir / "constraints.md", Path("constitution") / "constraints.md"]
    for c in candidates:
        if c.is_file():
            return set(ID_RE.findall(_read(c)))
    return set()


def check(design_dir: Path, constraints_override: str | None,
          adr_override: str | None = None) -> list[str]:
    problems: list[str] = []
    if not design_dir.is_dir():
        return [f"{design_dir}: not a directory"]

    dut = design_dir / "design-under-test.md"
    if not dut.is_file():
        problems.append(f"{design_dir}: missing design-under-test.md "
                        "(the terse artifact the challenger receives instead of the ADR)")
    elif not _read(dut).strip():
        problems.append(f"{design_dir}: design-under-test.md is empty")

    adr = Path(adr_override) if adr_override else _find_adr(design_dir)
    if adr is None or not adr.is_file():
        problems.append(f"{design_dir}: no ADR file (adr.md, ADR-*.md, or --adr) to check")
        return problems

    adr_text = _read(adr)

    alt = _section_body(adr_text, ALTERNATIVES_RE)
    if alt is None:
        problems.append(f"{adr.name}: no 'Alternatives' section — a design with no weighed "
                        "alternative has nothing to challenge")
    else:
        n = _count_alternatives(alt)
        if n < MIN_ALTERNATIVES:
            problems.append(f"{adr.name}: only {n} alternative(s) in 'Alternatives' "
                            f"(need >= {MIN_ALTERNATIVES} to be challenge-able)")

    cons = _section_body(adr_text, CONSEQUENCES_RE)
    if cons is None:
        problems.append(f"{adr.name}: no 'Consequences' section")
    elif not NEGATIVE_RE.search(cons):
        problems.append(f"{adr.name}: 'Consequences' names no negative/risk/trade-off "
                        "(an all-upside ADR hides its cost)")

    if dut.is_file():
        cited = set(ID_RE.findall(_read(dut)))
        if cited:
            known = _constraints_ids(design_dir, constraints_override)
            missing = sorted(cited - known)
            if missing:
                problems.append(f"design-under-test.md: constraint id(s) not found in "
                                f"constraints: {', '.join(missing)}")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic architecture-review pre-check.")
    parser.add_argument("design_dir", help="dir with design-under-test.md")
    parser.add_argument("--constraints", default=None,
                        help="constraints.md to resolve ids (explicit for separated layout)")
    parser.add_argument("--adr", default=None,
                        help="ADR path (explicit when not colocated in design_dir)")
    args = parser.parse_args(argv)

    problems = check(Path(args.design_dir), args.constraints, args.adr)
    if problems:
        print("architecture-review pre-check FAILED (design not challenge-able):")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"architecture-review pre-check OK: {args.design_dir} is challenge-able "
          "(design-under-test present, alternatives weighed, cost named).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
