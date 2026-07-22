#!/usr/bin/env python3
"""Constraint provenance gate for roadmap Phase 17 / ADR-17.

This gate proves structure and local reproducibility only. It does not claim to
prove source authenticity, honest classification, or semantic coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from constraint_model import ConstraintBlock, ConstraintModelError, json_array, parse_constraints, scalar

ALLOWED_SOURCES = {
    "stakeholder",
    "regulation",
    "normative_spec",
    "architecture_decision",
}
AUTHORITY_SOURCES = ALLOWED_SOURCES - {"stakeholder"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
DEFAULT_CONSTRAINTS = Path("constitution/constraints.md")


def _git_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise ConstraintModelError("cannot resolve git repository root")
    return Path(result.stdout.strip()).resolve()


def _tracked(root: Path, relative: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _repo_file(root: Path, raw: Any, label: str) -> tuple[Path | None, str | None]:
    if not isinstance(raw, str) or not raw.strip():
        return None, f"{label}: path must be a non-empty string"
    value = raw.strip()
    if "\\" in value:
        return None, f"{label}: path must use repository-relative '/' separators"
    posix = PurePosixPath(value)
    if posix.is_absolute() or ".." in posix.parts or value in {".", ""}:
        return None, f"{label}: path must stay inside the repository"
    relative = posix.as_posix()
    candidate = (root / Path(*posix.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, f"{label}: path escapes the repository"
    if not candidate.is_file():
        return None, f"{label}: file does not exist: {relative}"
    if not _tracked(root, relative):
        return None, f"{label}: file is not git-tracked: {relative}"
    return candidate, None


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dict_items(block: ConstraintBlock, key: str, errors: list[str]) -> list[dict[str, Any]]:
    try:
        items = json_array(block, key)
    except ConstraintModelError as exc:
        errors.append(str(exc))
        return []
    if any(not isinstance(item, dict) for item in items):
        errors.append(
            f"{block.path}: constraint {block.constraint_id}: '{key}' entries must be objects"
        )
        return []
    return items


def _string_items(block: ConstraintBlock, key: str, errors: list[str]) -> list[str]:
    try:
        items = json_array(block, key)
    except ConstraintModelError as exc:
        errors.append(str(exc))
        return []
    if any(not isinstance(item, str) or not item.strip() for item in items):
        errors.append(
            f"{block.path}: constraint {block.constraint_id}: '{key}' entries "
            "must be non-empty strings"
        )
        return []
    return [item.strip() for item in items]


def _validate_block(
    block: ConstraintBlock, root: Path, seen_residuals: set[str]
) -> list[str]:
    errors: list[str] = []
    prefix = f"{block.path}: constraint {block.constraint_id}"
    severity = scalar(block, "severity")
    if severity not in {"hard", "soft"}:
        errors.append(f"{prefix}: severity must be 'hard' or 'soft'")

    sources = _string_items(block, "source", errors)
    if not sources:
        errors.append(f"{prefix}: 'source' must be a non-empty JSON array")
    elif len(sources) != len(set(sources)):
        errors.append(f"{prefix}: 'source' contains duplicates")
    invalid_sources = sorted(set(sources) - ALLOWED_SOURCES)
    if invalid_sources:
        errors.append(f"{prefix}: invalid source value(s): {', '.join(invalid_sources)}")

    references = _dict_items(block, "reference", errors)
    reference_sources: list[str] = []
    for index, reference in enumerate(references, start=1):
        label = f"{prefix}: reference[{index}]"
        required = ("source", "id", "version", "path", "sha256")
        missing = [key for key in required if not reference.get(key)]
        if missing:
            errors.append(f"{label}: missing field(s): {', '.join(missing)}")
            continue
        ref_source = reference["source"]
        if not isinstance(ref_source, str):
            errors.append(f"{label}: source must be a string")
            continue
        reference_sources.append(ref_source)
        if ref_source not in AUTHORITY_SOURCES:
            errors.append(f"{label}: source '{ref_source}' is not an authority source")
        if ref_source not in sources:
            errors.append(f"{label}: source '{ref_source}' is not declared in constraint source")
        for key in ("id", "version"):
            if not isinstance(reference[key], str) or not reference[key].strip():
                errors.append(f"{label}: {key} must be a non-empty string")
        expected_hash = reference["sha256"]
        if not isinstance(expected_hash, str) or not SHA256.fullmatch(expected_hash):
            errors.append(f"{label}: sha256 must be 64 lowercase hexadecimal characters")
            continue
        target, path_error = _repo_file(root, reference["path"], label)
        if path_error:
            errors.append(path_error)
        elif target is not None and _hash(target) != expected_hash:
            errors.append(f"{label}: sha256 does not match {reference['path']}")

    for source in sorted(set(sources) & AUTHORITY_SOURCES):
        count = reference_sources.count(source)
        if count != 1:
            errors.append(f"{prefix}: source '{source}' requires exactly one reference (found {count})")
    extra_sources = sorted(set(reference_sources) - set(sources))
    if extra_sources:
        errors.append(f"{prefix}: reference source(s) not declared: {', '.join(extra_sources)}")

    projections = _string_items(block, "projection", errors)
    if len(projections) != len(set(projections)):
        errors.append(f"{prefix}: 'projection' contains duplicates")
    for projection in projections:
        target, path_error = _repo_file(root, projection, f"{prefix}: projection")
        if path_error:
            errors.append(path_error)
        elif target is not None and target.suffix.lower() != ".py":
            errors.append(f"{prefix}: projection must point to a Python gate: {projection}")

    residuals = _dict_items(block, "residual", errors)
    local_residuals: set[str] = set()
    for index, residual in enumerate(residuals, start=1):
        label = f"{prefix}: residual[{index}]"
        required = ("id", "statement", "route")
        missing = [key for key in required if not residual.get(key)]
        if missing:
            errors.append(f"{label}: missing field(s): {', '.join(missing)}")
            continue
        residual_id = residual["id"]
        if not isinstance(residual_id, str) or not residual_id.strip():
            errors.append(f"{label}: id must be a non-empty string")
            continue
        residual_id = residual_id.strip()
        if residual_id in local_residuals or residual_id in seen_residuals:
            errors.append(f"{label}: duplicate residual id '{residual_id}'")
        local_residuals.add(residual_id)
        seen_residuals.add(residual_id)
        if residual["route"] != "review":
            errors.append(f"{label}: route must be 'review'")
        if not isinstance(residual["statement"], str) or not residual["statement"].strip():
            errors.append(f"{label}: statement must be a non-empty string")

    if severity == "hard" and not projections and not residuals:
        errors.append(f"{prefix}: hard constraint must declare a projection or residual")
    return errors


def check(path: Path, root: Path) -> int:
    try:
        blocks = parse_constraints(path)
    except ConstraintModelError as exc:
        print(f"check_provenance: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    seen_residuals: set[str] = set()
    for block in blocks:
        errors.extend(_validate_block(block, root, seen_residuals))
    if errors:
        print("constraint provenance FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"constraint provenance OK: {len(blocks)} constraint(s) in {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate constraint provenance (Phase 17).")
    parser.add_argument("--path", type=Path, default=DEFAULT_CONSTRAINTS)
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument(
        "--allow-missing-constitution",
        action="store_true",
        help="treat a missing default constitution as a pre-inception greenfield",
    )
    args = parser.parse_args(argv)
    try:
        root = _git_root(args.root)
    except ConstraintModelError as exc:
        print(f"check_provenance: {exc}", file=sys.stderr)
        return 2
    path = args.path if args.path.is_absolute() else root / args.path
    default_path = (root / DEFAULT_CONSTRAINTS).resolve()
    if args.allow_missing_constitution and path.resolve() == default_path and not path.exists():
        print("constraint provenance skipped: no constitution yet (pre-inception greenfield)")
        return 0
    return check(path, root)


if __name__ == "__main__":
    sys.exit(main())
