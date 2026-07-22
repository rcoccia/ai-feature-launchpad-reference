#!/usr/bin/env python3
"""Thin branch/diff gate for the immediate Change Record cutover."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from change_record import (
    ChangeRecordError,
    load_change_record,
    monotonic_problems,
    review_recording_problems,
)

DATED_RECORD = re.compile(r"^changes/\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
BASELINE = "changes/0000-control-tower-baseline.md"
FULL_SHA = re.compile(r"\b[0-9a-f]{40}(?:[0-9a-f]{24})?\b")
BASELINE_TRIGGER = "legacy-baseline-retirement"
PHASE_HEADING = re.compile(r"^##\s+(.+?)\s*$")
CHECKBOX_ITEM = re.compile(r"^\s*-\s+\[([ xX])\]\s+")
BASELINE_OBLIGATIONS = {
    "FUN-CHANGE-01",
    "FUN-ROADMAP-01",
    "NFR-DOCS-01",
    "FUN-MERGE-01",
}


@dataclass(frozen=True)
class DiffEntry:
    status: str
    old_path: str | None
    path: str


def _git(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *(str(arg) for arg in args)],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _root() -> Path:
    result = _git("rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "cannot resolve repository root")
    return Path(result.stdout.strip()).resolve()


def _resolve_base(base: str | None) -> str:
    if base:
        return base
    for candidate in ("origin/master", "master"):
        if _git("rev-parse", "--verify", "--quiet", candidate).returncode == 0:
            return candidate
    return "HEAD~1"


def _entries_between(
    start: str, end: str, *, detect_renames: bool, merge_base: bool
) -> tuple[list[DiffEntry], str | None]:
    detection = (
        ("--find-renames", "--find-copies", "--find-copies-harder")
        if detect_renames
        else ("--no-renames",)
    )
    separator = "..." if merge_base else ".."
    revision = f"{start}{separator}{end}"
    result = _git("diff", "--name-status", *detection, revision)
    if result.returncode != 0:
        return [], result.stderr.strip() or f"cannot diff {revision}"
    entries: list[DiffEntry] = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) == 3:
            entries.append(DiffEntry(status[0], parts[1], parts[2]))
        elif len(parts) == 2:
            entries.append(DiffEntry(status[0], None, parts[1]))
        else:
            return [], f"cannot parse git diff row: {line}"
    return entries, None


def _entries(base: str, *, detect_renames: bool) -> tuple[list[DiffEntry], str | None]:
    return _entries_between(
        base, "HEAD", detect_renames=detect_renames, merge_base=True
    )


def _git_text(base: str, relative: str) -> str | None:
    result = _git("show", f"{base}:{relative}")
    return result.stdout if result.returncode == 0 else None


def _canonical_phase_from_text(text: str) -> tuple[str | None, str | None]:
    script = (
        Path(__file__).resolve().parents[2]
        / ".github"
        / "skills"
        / "bootstrap-tower"
        / "scripts"
        / "scaffold_constitution.py"
    )
    if not script.is_file():
        return None, f"canonical Roadmap selector is unavailable: {script}"
    with tempfile.TemporaryDirectory() as directory:
        constitution = Path(directory)
        (constitution / "roadmap.md").write_text(text, encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(script),
                "--current-phase",
                str(constitution),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    if result.returncode != 0:
        return None, result.stderr.strip() or "base Roadmap selector failed"
    return result.stdout.strip(), None


def _phase_is_delivered(text: str, heading: str) -> bool:
    lines = text.splitlines()
    target = f"## {heading}"
    starts = [index for index, line in enumerate(lines) if line == target]
    if len(starts) != 1:
        return False
    start = starts[0]
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if PHASE_HEADING.fullmatch(lines[index])
        ),
        len(lines),
    )
    section = lines[start + 1 : end]
    if any(line.strip() == "**Status:** deferred" for line in section):
        return False
    states = [
        match.group(1).lower()
        for line in section
        if (match := CHECKBOX_ITEM.match(line))
    ]
    return bool(states) and all(state == "x" for state in states)


def _roadmap_closeout_allowed(
    root: Path, base: str, record: object, roadmap_heading: str
) -> bool:
    """Allow the anchored current phase to become delivered in this governed change."""
    if record.status == "draft" or record.roadmap == roadmap_heading:
        return False
    base_text = _git_text(base, "constitution/roadmap.md")
    candidate_path = root / "constitution" / "roadmap.md"
    if base_text is None or not candidate_path.is_file():
        return False
    base_heading, error = _canonical_phase_from_text(base_text)
    if error is not None or base_heading != record.roadmap:
        return False
    try:
        candidate_text = candidate_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    return _phase_is_delivered(candidate_text, record.roadmap)


def discover_record(base: str) -> tuple[str | None, str | None]:
    """Return the one dated Change Record changed in base...HEAD."""
    entries, error = _entries(base, detect_renames=False)
    if error:
        return None, error
    records = sorted(
        entry.path
        for entry in entries
        if entry.status in {"A", "M"} and DATED_RECORD.fullmatch(entry.path)
    )
    if len(records) != 1:
        return None, (
            "pull-request range must add or modify exactly one dated Change Record "
            f"(found {len(records)})"
        )
    return records[0], None


def _parse_base_record(
    root: Path, base: str, relative: str, constraints: Path
) -> tuple[object | None, list[str]]:
    text = _git_text(base, relative)
    if text is None:
        return None, []
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / PurePosixPath(relative).name
        path.write_text(text, encoding="utf-8")
        companion_relative = f"changes/{path.stem}/design-under-test.md"
        companion_text = _git_text(base, companion_relative)
        if companion_text is not None:
            companion = path.with_suffix("") / "design-under-test.md"
            companion.parent.mkdir()
            companion.write_text(companion_text, encoding="utf-8")
        try:
            return load_change_record(path, constraints), []
        except ChangeRecordError as exc:
            return None, [f"base {relative}: {problem}" for problem in exc.problems]


def _reviewed_target_record(
    root: Path, record: object, relative: str, constraints: Path
) -> tuple[object | None, list[str]]:
    target = record.final_reviewed_target
    if not target:
        return None, ["reviewed Change Record has no latest reviewed target"]
    if _git("cat-file", "-e", f"{target}^{{commit}}").returncode != 0:
        return None, [f"reviewed target commit is unavailable: {target}"]
    if _git("merge-base", "--is-ancestor", target, "HEAD").returncode != 0:
        return None, [f"reviewed target is not an ancestor of HEAD: {target}"]
    target_record, problems = _parse_base_record(root, target, relative, constraints)
    if problems:
        return None, [f"reviewed target {target}: {problem}" for problem in problems]
    if target_record is None:
        return None, [f"reviewed target does not contain {relative}: {target}"]
    if target_record.status != "confirmed":
        return None, [
            f"reviewed target {target} has status '{target_record.status}' "
            "(expected 'confirmed')"
        ]
    return target_record, []


def _baseline_exception(
    root: Path, dated_record: Path, no_rename: list[DiffEntry], problems: list[str]
) -> None:
    specs = [entry for entry in no_rename if entry.path.startswith("specs/")]
    baseline_added = any(
        entry.path == BASELINE and entry.status == "A" for entry in no_rename
    )
    if not specs:
        if baseline_added:
            problems.append(
                "changes/0000-control-tower-baseline.md is reserved for deletion-only specs/ retirement"
            )
        return
    if any(entry.status != "D" for entry in specs):
        problems.append("new changes may not add or modify any path under specs/")
        return
    baseline_entry = next(
        (entry for entry in no_rename if entry.path == BASELINE and entry.status == "A"),
        None,
    )
    if baseline_entry is None:
        problems.append(
            "deleting specs/ requires a newly added changes/0000-control-tower-baseline.md"
        )
        return
    record_text = dated_record.read_text(encoding="utf-8")
    baseline_path = root / BASELINE
    baseline_text = baseline_path.read_text(encoding="utf-8") if baseline_path.is_file() else ""
    if BASELINE_TRIGGER not in record_text or BASELINE not in record_text:
        problems.append(
            "baseline deletion Change Record must name the legacy-baseline-retirement trigger "
            "and link changes/0000-control-tower-baseline.md"
        )
    match = FULL_SHA.search(baseline_text)
    if match is None:
        problems.append("baseline index must pin one full immutable commit")
    elif _git("cat-file", "-e", f"{match.group(0)}^{{commit}}").returncode != 0:
        problems.append(f"baseline index commit is not resolvable: {match.group(0)}")


def _required_obligations(
    entries: list[DiffEntry], architecture_triggered: bool
) -> set[str]:
    """Return only obligations whose applicability is certain from changed paths."""
    required = set(BASELINE_OBLIGATIONS)
    paths = {
        path
        for entry in entries
        for path in (entry.path, entry.old_path)
        if path is not None
    }
    if any(
        path == "constitution/mission.md" or path == "constitution/constraints.md"
        for path in paths
    ):
        required.add("FUN-AUTONOMY-01")
    if any(
        (
            path.startswith("framework/scripts/")
            or (
                path.startswith(".github/skills/")
                and "/scripts/" in path
            )
        )
        and path.endswith(".py")
        for path in paths
    ):
        required.update({"FUN-DETERMINISM-01", "NFR-EVAL-01"})
    if architecture_triggered:
        required.add("FUN-ARCHREVIEW-01")
    if any(path.startswith(".github/agents/") and path.endswith(".agent.md") for path in paths):
        required.add("TEC-AGENTCFG-01")
    if any(
        path.startswith(("framework/", ".github/skills/", ".github/agents/"))
        for path in paths
    ):
        required.add("TEC-DOMAIN-01")
    return required


def check(
    base: str,
    constraints: Path,
    roadmap_heading: str | None = None,
) -> list[str]:
    root = _root()
    no_rename, error = _entries(base, detect_renames=False)
    if error:
        return [error]
    detected, error = _entries(base, detect_renames=True)
    if error:
        return [error]
    problems: list[str] = []

    relative, discovery_error = discover_record(base)
    if discovery_error is not None or relative is None:
        problems.append(discovery_error or "dated Change Record discovery failed")
        return problems
    record_path = root / Path(*PurePosixPath(relative).parts)

    allowed_changes = {
        relative,
        f"changes/{record_path.stem}/design-under-test.md",
        BASELINE,
    }
    unexpected = sorted(
        entry.path
        for entry in no_rename
        if entry.path.startswith("changes/") and entry.path not in allowed_changes
    )
    if unexpected:
        problems.append(
            f"dated record has unexpected companion/change path(s): {', '.join(unexpected)}"
        )
    for entry in detected:
        paths = {entry.path, entry.old_path or ""}
        if entry.status in {"R", "C"} and any(path.startswith("specs/") for path in paths):
            problems.append("copying or renaming a specs/ path is forbidden after activation")

    try:
        record = load_change_record(record_path, constraints)
    except ChangeRecordError as exc:
        problems.extend(exc.problems)
        return problems
    activated = {obligation.constraint_id for obligation in record.obligations}
    missing_required = sorted(
        _required_obligations(no_rename, record.architecture_triggered) - activated
    )
    if missing_required:
        problems.append(
            "mechanically required obligation row(s) missing: "
            + ", ".join(missing_required)
        )

    old, old_problems = _parse_base_record(root, base, relative, constraints)
    problems.extend(old_problems)
    transition_old = old
    if record.status == "reviewed":
        target_record, target_problems = _reviewed_target_record(
            root, record, relative, constraints
        )
        problems.extend(target_problems)
        if target_record is not None:
            transition_old = target_record
            target_text = _git_text(record.final_reviewed_target, relative)
            if target_text is None:
                problems.append(
                    f"cannot read Change Record from reviewed target: {relative}"
                )
            else:
                try:
                    candidate_text = record_path.read_text(encoding="utf-8")
                except (OSError, UnicodeError) as exc:
                    problems.append(f"cannot read candidate Change Record: {exc}")
                else:
                    problems.extend(
                        review_recording_problems(
                            target_record, record, target_text, candidate_text
                        )
                    )
            reviewed_entries, reviewed_diff_error = _entries_between(
                record.final_reviewed_target,
                "HEAD",
                detect_renames=False,
                merge_base=False,
            )
            if reviewed_diff_error:
                problems.append(
                    "cannot validate reviewed-target frozen diff: "
                    f"{reviewed_diff_error}"
                )
            else:
                changed_outside_record = sorted(
                    entry.path
                    for entry in reviewed_entries
                    if entry.path != relative
                )
                if changed_outside_record:
                    problems.append(
                        "reviewed transition may change only its canonical Change Record; "
                        "post-target path(s): "
                        + ", ".join(changed_outside_record)
                    )
    if old is None or old.status == "draft":
        if (
            roadmap_heading is not None
            and record.roadmap != roadmap_heading
            and not _roadmap_closeout_allowed(root, base, record, roadmap_heading)
        ):
            problems.append(
                f"{record_path}: roadmap anchor '{record.roadmap}' does not match "
                f"canonical current phase '{roadmap_heading}'"
            )
    if transition_old is not None:
        problems.extend(monotonic_problems(transition_old, record))

    changed_outside_record = [
        entry.path
        for entry in no_rename
        if entry.path not in allowed_changes and not entry.path.startswith("specs/")
    ]
    if record.status == "draft" and any(entry.path != relative for entry in no_rename):
        problems.append(
            "draft Change Record cannot accompany implementation, design, or migration changes"
        )

    _baseline_exception(root, record_path, no_rename, problems)
    return problems


def _canonical_phase(root: Path) -> tuple[str | None, str | None]:
    script = root / ".github" / "skills" / "bootstrap-tower" / "scripts" / "scaffold_constitution.py"
    if not script.is_file() or not (root / "constitution" / "roadmap.md").is_file():
        return None, None
    result = subprocess.run(
        [sys.executable, "-B", str(script), "--current-phase", str(root / "constitution")],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None, result.stderr.strip() or "canonical Roadmap selector failed"
    return result.stdout.strip(), None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Change Record branch contract.")
    parser.add_argument("--base", default=None, help="base ref (default: origin/master)")
    parser.add_argument(
        "--constraints",
        type=Path,
        default=Path("constitution/constraints.md"),
        help="constraint artifact used to resolve obligation ids",
    )
    args = parser.parse_args(argv)
    try:
        root = _root()
    except RuntimeError as exc:
        print(f"check_change_record: {exc}", file=sys.stderr)
        return 2
    base = _resolve_base(args.base)
    heading, phase_error = _canonical_phase(root)
    if phase_error:
        print(f"check_change_record: {phase_error}", file=sys.stderr)
        return 2
    constraints = args.constraints if args.constraints.is_absolute() else root / args.constraints
    problems = check(base, constraints, heading)
    if problems:
        print("FUN-CHANGE-01 FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"change-record gate OK: exactly one governed record is valid (base={base}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
