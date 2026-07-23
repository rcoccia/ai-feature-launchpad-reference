#!/usr/bin/env python3
"""Thin branch/diff gate for the immediate Change Record cutover."""
from __future__ import annotations

import argparse
import json
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


@dataclass(frozen=True)
class RoadmapPhaseProjection:
    heading: str
    heading_line: int
    status: str | None
    status_line: int | None
    checked_count: int
    unchecked_count: int
    disposition: str

    @property
    def is_deferred(self) -> bool:
        return self.status == "deferred"

    @property
    def is_delivered(self) -> bool:
        return self.checked_count > 0 and self.unchecked_count == 0


@dataclass(frozen=True)
class RoadmapProjection:
    lifecycle: str | None
    lifecycle_line: int | None
    current_heading: str | None
    current_line: int | None
    is_complete: bool
    phases: tuple[RoadmapPhaseProjection, ...]
    diagnostics: tuple[str, ...]

    @property
    def by_heading(self) -> dict[str, RoadmapPhaseProjection]:
        return {phase.heading: phase for phase in self.phases}


class RoadmapProjectionError(RuntimeError):
    """The canonical analyzer could not supply a closed normalized projection."""


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


def _scaffold_script(root: Path) -> Path:
    script = root / ".github" / "skills" / "bootstrap-tower" / "scripts" / "scaffold_constitution.py"
    if not script.is_file():
        raise RoadmapProjectionError(f"canonical Roadmap analyzer is unavailable: {script}")
    return script


def _expect_keys(value: dict[str, object], expected: set[str], label: str) -> None:
    missing = sorted(expected - value.keys())
    unknown = sorted(value.keys() - expected)
    if missing or unknown:
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if unknown:
            details.append(f"unknown {', '.join(unknown)}")
        raise RoadmapProjectionError(f"{label} has invalid field set: {'; '.join(details)}")


def _parse_projection(raw: str, returncode: int) -> RoadmapProjection:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RoadmapProjectionError(f"canonical Roadmap analyzer emitted malformed JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise RoadmapProjectionError("canonical Roadmap analyzer projection must be one JSON object")
    _expect_keys(
        value,
        {
            "lifecycle",
            "lifecycle_line",
            "current",
            "is_complete",
            "phases",
            "diagnostics",
        },
        "Roadmap projection",
    )
    lifecycle = value["lifecycle"]
    lifecycle_line = value["lifecycle_line"]
    current = value["current"]
    is_complete = value["is_complete"]
    phases_raw = value["phases"]
    diagnostics_raw = value["diagnostics"]
    if lifecycle is not None and lifecycle != "complete":
        raise RoadmapProjectionError("Roadmap projection lifecycle is not null or 'complete'")
    if (
        lifecycle_line is not None
        and (type(lifecycle_line) is not int or lifecycle_line < 1)
    ):
        raise RoadmapProjectionError("Roadmap projection lifecycle_line is not an integer or null")
    if type(is_complete) is not bool:
        raise RoadmapProjectionError("Roadmap projection is_complete is not a boolean")
    if not isinstance(phases_raw, list) or not isinstance(diagnostics_raw, list):
        raise RoadmapProjectionError("Roadmap projection phases and diagnostics must be arrays")
    if any(not isinstance(item, str) for item in diagnostics_raw):
        raise RoadmapProjectionError("Roadmap projection diagnostics must contain only strings")
    current_heading: str | None = None
    current_line: int | None = None
    if current is not None:
        if not isinstance(current, dict):
            raise RoadmapProjectionError("Roadmap projection current must be an object or null")
        _expect_keys(current, {"heading", "heading_line"}, "Roadmap projection current")
        if (
            not isinstance(current["heading"], str)
            or not current["heading"]
            or type(current["heading_line"]) is not int
            or current["heading_line"] < 1
        ):
            raise RoadmapProjectionError("Roadmap projection current fields have invalid types")
        current_heading = current["heading"]
        current_line = current["heading_line"]
    phases: list[RoadmapPhaseProjection] = []
    for index, item in enumerate(phases_raw, start=1):
        if not isinstance(item, dict):
            raise RoadmapProjectionError(f"Roadmap projection phase[{index}] must be an object")
        _expect_keys(
            item,
            {
                "heading",
                "heading_line",
                "status",
                "status_line",
                "checked_count",
                "unchecked_count",
                "disposition",
            },
            f"Roadmap projection phase[{index}]",
        )
        if (
            not isinstance(item["heading"], str)
            or not item["heading"]
            or type(item["heading_line"]) is not int
            or item["heading_line"] < 1
            or (
                item["status"] is not None
                and item["status"] != "deferred"
            )
            or (
                item["status_line"] is not None
                and (
                    type(item["status_line"]) is not int
                    or item["status_line"] < 1
                )
            )
            or type(item["checked_count"]) is not int
            or item["checked_count"] < 0
            or type(item["unchecked_count"]) is not int
            or item["unchecked_count"] < 0
            or not isinstance(item["disposition"], str)
            or item["disposition"] not in {"deferred", "delivered", "current", "planned"}
        ):
            raise RoadmapProjectionError(
                f"Roadmap projection phase[{index}] fields have invalid values or types"
            )
        phases.append(
            RoadmapPhaseProjection(
                heading=item["heading"],
                heading_line=item["heading_line"],
                status=item["status"],
                status_line=item["status_line"],
                checked_count=item["checked_count"],
                unchecked_count=item["unchecked_count"],
                disposition=item["disposition"],
            )
        )
    if len({phase.heading for phase in phases}) != len(phases):
        raise RoadmapProjectionError("Roadmap projection phase headings must be unique")
    diagnostics = tuple(diagnostics_raw)
    if is_complete and (
        lifecycle != "complete"
        or current is not None
        or diagnostics
    ):
        raise RoadmapProjectionError("Roadmap projection complete state is internally inconsistent")
    expected_returncode = 1 if diagnostics else 0
    if returncode != expected_returncode:
        raise RoadmapProjectionError(
            "canonical Roadmap analyzer exit code disagrees with projection diagnostics"
        )
    return RoadmapProjection(
        lifecycle=lifecycle,
        lifecycle_line=lifecycle_line,
        current_heading=current_heading,
        current_line=current_line,
        is_complete=is_complete,
        phases=tuple(phases),
        diagnostics=diagnostics,
    )


def _roadmap_projection(root: Path, constitution: Path) -> RoadmapProjection:
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(_scaffold_script(root)),
            "--roadmap-analysis",
            str(constitution),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode not in {0, 1} or result.stderr:
        detail = result.stderr.strip() or f"exit {result.returncode}"
        raise RoadmapProjectionError(f"canonical Roadmap analyzer transport failed: {detail}")
    return _parse_projection(result.stdout, result.returncode)


def _roadmap_projection_from_text(root: Path, text: str) -> RoadmapProjection:
    with tempfile.TemporaryDirectory() as directory:
        constitution = Path(directory)
        (constitution / "roadmap.md").write_text(text, encoding="utf-8")
        return _roadmap_projection(root, constitution)


def _canonical_phase(root: Path) -> tuple[str | None, str | None]:
    """Return the valid current heading while allowing a valid complete Roadmap."""
    try:
        projection = _roadmap_projection(root, root / "constitution")
    except RoadmapProjectionError as exc:
        return None, str(exc)
    if projection.diagnostics:
        return None, projection.diagnostics[0]
    return projection.current_heading, None


def _lifecycle_authorization_problems(
    root: Path, record: object, entries: list[DiffEntry]
) -> list[str]:
    record_path = record.path
    if record.status == "draft" or not record.roadmap_lifecycle_adr:
        return [
            f"{record_path}: Roadmap lifecycle transition requires confirmed "
            "'Initial human confirmation' and a '## Roadmap lifecycle authorization' ADR"
        ]
    adr = record.roadmap_lifecycle_adr
    if not any(entry.status == "A" and entry.path == adr for entry in entries):
        return [
            f"{record_path}: Roadmap lifecycle ADR must be newly added in the same "
            f"governed change: {adr}"
        ]
    adr_path = root / Path(*PurePosixPath(adr).parts)
    try:
        text = adr_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return [f"{record_path}: Roadmap lifecycle ADR cannot be read: {adr}"]
    if not any(line == "- **status:** accepted" for line in text.splitlines()):
        return [f"{adr_path}: Roadmap lifecycle ADR must declare exact status 'accepted'"]
    return []


def _roadmap_transition_problems(
    root: Path,
    record: object,
    entries: list[DiffEntry],
    base: RoadmapProjection,
    candidate: RoadmapProjection,
) -> list[str]:
    problems = [*candidate.diagnostics]
    if base.diagnostics:
        problems.extend(f"base Roadmap invalid: {item}" for item in base.diagnostics)
        return problems

    base_phase = base.by_heading.get(record.roadmap)
    candidate_phase = candidate.by_heading.get(record.roadmap)
    lifecycle_changed = base.lifecycle != candidate.lifecycle

    if base.lifecycle == "complete" and candidate.lifecycle is None:
        new_headings = set(candidate.by_heading) - set(base.by_heading)
        eligible_new = [
            phase
            for heading, phase in candidate.by_heading.items()
            if heading in new_headings
            and not phase.is_deferred
            and phase.unchecked_count > 0
        ]
        if not eligible_new:
            problems.append(
                f"{root / 'constitution' / 'roadmap.md'}: incomplete Roadmap reopen: "
                "removing '**Lifecycle:** complete' requires at least one newly added "
                "non-deferred phase with an unchecked item in the same governed change"
            )
        if candidate.current_heading != record.roadmap:
            problems.append(
                f"{record.path}: roadmap anchor '{record.roadmap}' does not match "
                f"canonical current phase '{candidate.current_heading or '<none>'}'"
            )
        problems.extend(_lifecycle_authorization_problems(root, record, entries))
        return problems

    if base.lifecycle is None and candidate.lifecycle == "complete":
        if (
            base.current_heading != record.roadmap
            or base_phase is None
            or candidate_phase is None
            or candidate_phase.is_deferred
            or not candidate_phase.is_delivered
            or not candidate.is_complete
        ):
            problems.append(
                f"{record.path}: roadmap anchor '{record.roadmap}' does not satisfy "
                "the intentional final-phase completion predicate"
            )
        problems.extend(_lifecycle_authorization_problems(root, record, entries))
        return problems

    if lifecycle_changed:
        problems.append(
            f"{record.path}: unsupported Roadmap lifecycle transition "
            f"{base.lifecycle or '<absent>'} -> {candidate.lifecycle or '<absent>'}"
        )

    if candidate.current_heading == record.roadmap:
        return problems
    if (
        base.current_heading == record.roadmap
        and candidate_phase is not None
        and not candidate_phase.is_deferred
        and candidate_phase.is_delivered
        and candidate.current_heading is not None
    ):
        return problems
    if (
        base.current_heading == record.roadmap
        and candidate_phase is not None
        and not candidate_phase.is_deferred
        and candidate_phase.is_delivered
        and candidate.current_heading is None
        and candidate.lifecycle is None
    ):
        problems.append(
            f"{root / 'constitution' / 'roadmap.md'}: final-phase closeout requires a "
            "valid top-level '**Lifecycle:** complete' plus the confirmed human "
            "authorization and ADR in the same governed change"
        )
        return problems
    problems.append(
        f"{record.path}: roadmap anchor '{record.roadmap}' does not match canonical "
        f"current phase '{candidate.current_heading or '<none>'}'"
    )
    return problems


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
    _legacy_expected_heading: str | None = None,
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
    base_roadmap_text = _git_text(base, "constitution/roadmap.md")
    candidate_roadmap = root / "constitution" / "roadmap.md"
    if base_roadmap_text is not None and candidate_roadmap.is_file():
        base_projection = _roadmap_projection_from_text(root, base_roadmap_text)
        candidate_projection = _roadmap_projection(root, candidate_roadmap.parent)
        if old is None or old.status == "draft":
            problems.extend(
                _roadmap_transition_problems(
                    root,
                    record,
                    no_rename,
                    base_projection,
                    candidate_projection,
                )
            )
    elif (base_roadmap_text is None) != (not candidate_roadmap.is_file()):
        problems.append("base and candidate must both contain constitution/roadmap.md")

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
    constraints = args.constraints if args.constraints.is_absolute() else root / args.constraints
    try:
        problems = check(base, constraints)
    except RoadmapProjectionError as exc:
        print(f"check_change_record: {exc}", file=sys.stderr)
        return 2
    if problems:
        print("FUN-CHANGE-01 FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"change-record gate OK: exactly one governed record is valid (base={base}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
