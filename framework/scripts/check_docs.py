#!/usr/bin/env python3
"""Fail-closed documentation gate for constraint NFR-DOCS-01.

Scans tracked Markdown files and fails (non-zero exit) if any has:
  - a UTF-8 BOM,
  - a lone LF (an 0x0A not preceded by 0x0D, i.e. not CRLF),
  - an unbalanced number of ``` code-fence lines.

Markdown line endings are enforced primarily and structurally by .gitattributes
(``* text=auto eol=crlf``); this check adds BOM and code-fence enforcement (which
git does not normalize) and acts as a working-tree guard. Standard library only.

Usage:
    python framework/scripts/check_docs.py [--path FILE ...]

Run from the repository root. Exit code 0 = clean, 1 = at least one violation.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def tracked_markdown() -> list[Path]:
    """Return tracked *.md paths, falling back to a filesystem walk."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--", "*.md"],
            capture_output=True, text=True, check=True,
        ).stdout
        files = [Path(line) for line in out.splitlines() if line.strip()]
        if files:
            return files
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return [p for p in Path(".").rglob("*.md") if ".git" not in p.parts]


def violations(path: Path) -> list[str]:
    """Return a list of NFR-DOCS-01 violations for a single file."""
    data = path.read_bytes()
    issues: list[str] = []
    if data.startswith(b"\xef\xbb\xbf"):
        issues.append("has a UTF-8 BOM")
    lone = sum(1 for i, byte in enumerate(data)
               if byte == 0x0A and (i == 0 or data[i - 1] != 0x0D))
    if lone:
        issues.append(f"has {lone} lone LF (expected CRLF)")
    text = data.decode("utf-8", errors="replace")
    fences = sum(1 for line in text.splitlines() if line.startswith("```"))
    if fences % 2 != 0:
        issues.append(f"has {fences} code-fence lines (unbalanced)")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="NFR-DOCS-01 documentation gate (fail-closed).",
    )
    parser.add_argument("--path", nargs="*", default=None,
                        help="explicit markdown paths to check (default: all tracked *.md)")
    args = parser.parse_args(argv)

    files = [Path(p) for p in args.path] if args.path else tracked_markdown()
    files = sorted({p for p in files if p.is_file()})
    if not files:
        print("No markdown files to check.")
        return 0

    failed = False
    for path in files:
        for issue in violations(path):
            failed = True
            print(f"{path}: {issue}", file=sys.stderr)

    if failed:
        print("NFR-DOCS-01: documentation gate FAILED.", file=sys.stderr)
        return 1
    print(f"NFR-DOCS-01: {len(files)} markdown file(s) OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
