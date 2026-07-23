"""Scaffold and validate a three-file constitution directory.

The default mode copies missing constitution templates into a target
constitution folder. The check mode validates that the target files have the
required Markdown shape and constraint metadata blocks. The readiness mode
runs the shape check plus extra inception-readiness sub-checks: the portable
method baseline IDs are present, every hard constraint carries a verification,
every Roadmap phase is valid and a current phase exists, and the Mission
Success section is non-empty. Current-phase mode prints the selected canonical
Roadmap heading.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

CONSTITUTION_FILES = ("mission.md", "constraints.md", "roadmap.md")
MISSION_SECTIONS = ("Purpose", "Target users", "Scope", "Success", "Non-goals")
CONSTRAINT_KEYS = (
    "id",
    "category",
    "statement",
    "severity",
    "status",
    "source",
    "reference",
    "projection",
    "residual",
)
CAPTURE_KEYS = CONSTRAINT_KEYS + ("verification",)
VALID_CATEGORIES = {"technical", "functional", "non_functional"}
VALID_SEVERITIES = {"hard", "soft"}
VALID_SOURCES = {"stakeholder", "regulation", "normative_spec", "architecture_decision"}
PHASE_HEADING = re.compile(r"^##(?!#)\s+Phase\b", re.IGNORECASE)
SECTION_HEADING = re.compile(r"^#{1,2}(?!#)\s+")
GOAL_FIELD = re.compile(r"^\s*(?:Goal:|\*\*Goal:\*\*)\s*(.*?)\s*$", re.IGNORECASE)
STATUS_FIELD = re.compile(r"^\s*\*\*Status:\*\*\s*(.*?)\s*$")
CHECKBOX_ITEM = re.compile(r"^- \[([ xX])\]\s+(\S.*)$")
REQUIRED_PORTABLE_CONSTRAINT_IDS = (
    "FUN-CHANGE-01",
    "FUN-ROADMAP-01",
    "NFR-DOCS-01",
    "FUN-MERGE-01",
    "FUN-ARCHREVIEW-01",
)


class ToolError(Exception):
    """A user-facing failure that should be printed without a traceback."""


@dataclass(frozen=True)
class RoadmapPhase:
    """One canonical Roadmap phase and its source locations."""

    heading: str
    heading_line: int
    goal_line: int | None
    status: str | None
    status_line: int | None
    checkbox_lines: tuple[int, ...]
    checked_count: int
    unchecked_count: int

    @property
    def is_deferred(self) -> bool:
        return self.status == "deferred"

    @property
    def is_delivered(self) -> bool:
        return bool(self.checkbox_lines) and self.unchecked_count == 0


@dataclass(frozen=True)
class RoadmapAnalysis:
    """Fully validated phases and their selected current phase."""

    phases: tuple[RoadmapPhase, ...]
    dispositions: tuple[str, ...]
    current: RoadmapPhase | None
    errors: tuple[str, ...]


def templates_dir() -> Path:
    """Return the constitution templates directory (the skill's own assets)."""
    return Path(__file__).resolve().parent.parent / "assets"


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file, converting expected I/O failures to ToolError."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ToolError(f"error: {path}: not valid UTF-8") from exc
    except OSError as exc:
        raise ToolError(f"error: {path}: cannot read file: {exc}") from exc


def scaffold(specs_dir: Path, force: bool) -> int:
    """Create missing constitution files from byte-exact templates."""
    source_dir = templates_dir()
    try:
        specs_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ToolError(f"error: {specs_dir}: cannot create directory: {exc}") from exc

    for name in CONSTITUTION_FILES:
        source = source_dir / name
        destination = specs_dir / name
        if not source.is_file():
            raise ToolError(f"error: missing template: {source}")
        if destination.exists() and not force:
            print(f"skipped {destination} (exists)")
            continue
        existed_before = destination.exists()
        try:
            shutil.copyfile(source, destination)
        except OSError as exc:
            raise ToolError(f"error: failed to copy {source} to {destination}: {exc}") from exc
        action = "overwrote" if existed_before else "created"
        print(f"{action} {destination}")
    return 0


def markdown_heading_text(line: str) -> str | None:
    """Return heading text for an ATX markdown heading line, if present."""
    match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
    if not match:
        return None
    return match.group(1).strip()


def validate_mission(path: Path) -> list[str]:
    """Validate required mission section headings."""
    text = read_text_file(path)
    headings = [heading for line in text.splitlines() if (heading := markdown_heading_text(line))]
    missing = []
    for label in MISSION_SECTIONS:
        label_lower = label.casefold()
        if not any(heading.casefold().startswith(label_lower) for heading in headings):
            missing.append(label)
    if missing:
        return [f"{path}: missing mission section heading(s): {', '.join(missing)}"]
    return []


def strip_scalar(value: str) -> str:
    """Strip common scalar quoting and inline comments from a simple YAML-like value."""
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'\"', "'"}:
        value = value[1:-1]
    return value.strip()


def yaml_blocks(text: str) -> tuple[list[tuple[int, list[str]]], list[str]]:
    """Extract ```yaml fenced blocks and report unclosed fences."""
    blocks: list[tuple[int, list[str]]] = []
    errors: list[str] = []
    in_yaml = False
    start_line = 0
    current: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not in_yaml:
            if stripped == "```yaml":
                in_yaml = True
                start_line = line_number
                current = []
            continue
        if stripped == "```":
            blocks.append((start_line, current))
            in_yaml = False
            current = []
            continue
        current.append(line)

    if in_yaml:
        errors.append(f"unclosed yaml fence opened at line {start_line}")
    return blocks, errors


def parse_constraint_block(lines: Iterable[str]) -> dict[str, str]:
    """Parse key/value pairs needed from a YAML-like constraint block."""
    values: dict[str, str] = {}
    key_pattern = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")
    for line in lines:
        match = key_pattern.match(line)
        if match:
            key, value = match.groups()
            if key in CAPTURE_KEYS and key not in values:
                values[key] = strip_scalar(value)
    return values


def validate_constraints(path: Path) -> list[str]:
    """Validate constraint fenced blocks and required enum values."""
    text = read_text_file(path)
    blocks, fence_errors = yaml_blocks(text)
    errors = [f"{path}: {message}" for message in fence_errors]

    if not blocks:
        errors.append(f"{path}: no ```yaml constraint blocks found")
        return errors

    for index, (start_line, lines) in enumerate(blocks, start=1):
        values = parse_constraint_block(lines)
        block_name = values.get("id") or f"block {index} at line {start_line}"
        missing = [key for key in CONSTRAINT_KEYS if key not in values]
        if missing:
            errors.append(f"{path}: constraint {block_name}: missing key(s): {', '.join(missing)}")
        category = values.get("category")
        if category is not None and category not in VALID_CATEGORIES:
            errors.append(
                f"{path}: constraint {block_name}: invalid category '{category}' "
                f"(expected one of: {', '.join(sorted(VALID_CATEGORIES))})"
            )
        severity = values.get("severity")
        if severity is not None and severity not in VALID_SEVERITIES:
            errors.append(
                f"{path}: constraint {block_name}: invalid severity '{severity}' "
                f"(expected one of: {', '.join(sorted(VALID_SEVERITIES))})"
            )
        for key in ("source", "reference", "projection", "residual"):
            raw = values.get(key)
            if raw is None:
                continue
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(
                    f"{path}: constraint {block_name}: '{key}' is not valid inline JSON: "
                    f"{exc.msg}"
                )
                continue
            if not isinstance(parsed, list):
                errors.append(f"{path}: constraint {block_name}: '{key}' must be a JSON array")
            elif key == "source":
                if not parsed:
                    errors.append(f"{path}: constraint {block_name}: 'source' must not be empty")
                elif any(item not in VALID_SOURCES for item in parsed):
                    errors.append(
                        f"{path}: constraint {block_name}: invalid source value "
                        f"(expected: {', '.join(sorted(VALID_SOURCES))})"
                    )
    return errors


def _phase_error(path: Path, phase: RoadmapPhase, line: int, message: str) -> str:
    return (
        f"{path}:{line}: phase '{phase.heading}' "
        f"(heading line {phase.heading_line}): {message}"
    )


def analyze_roadmap(path: Path) -> RoadmapAnalysis:
    """Parse, validate, derive state, and select the canonical current phase."""
    if not path.is_file():
        return RoadmapAnalysis(
            (), (), None, (f"{path}: missing required constitution file roadmap.md",)
        )

    lines = read_text_file(path).splitlines()
    starts = [index for index, line in enumerate(lines) if PHASE_HEADING.match(line)]
    if not starts:
        return RoadmapAnalysis(
            (), (), None, (f"{path}: no phase heading found matching '^##\\s+Phase'",)
        )

    phases: list[RoadmapPhase] = []
    errors: list[str] = []
    seen_headings: dict[str, int] = {}

    for start in starts:
        end = next(
            (index for index in range(start + 1, len(lines)) if SECTION_HEADING.match(lines[index])),
            len(lines),
        )
        heading = markdown_heading_text(lines[start]) or lines[start].removeprefix("##").strip()
        heading_line = start + 1
        status: str | None = None
        status_line: int | None = None
        goal_line: int | None = None
        checkbox_lines: list[int] = []
        checked_count = 0
        unchecked_count = 0

        duplicate_heading_line = seen_headings.get(heading)
        if duplicate_heading_line is None:
            seen_headings[heading] = heading_line

        status_declarations: list[tuple[int, str]] = []
        for index in range(start + 1, end):
            line = lines[index]
            line_number = index + 1
            if match := STATUS_FIELD.match(line):
                status_declarations.append((line_number, match.group(1).strip()))
            if match := GOAL_FIELD.match(line):
                if match.group(1).strip() and goal_line is None:
                    goal_line = line_number
            if match := CHECKBOX_ITEM.match(line):
                checkbox_lines.append(line_number)
                if match.group(1) == " ":
                    unchecked_count += 1
                else:
                    checked_count += 1

        if status_declarations:
            status_line, status = status_declarations[0]

        phase = RoadmapPhase(
            heading=heading,
            heading_line=heading_line,
            goal_line=goal_line,
            status=status,
            status_line=status_line,
            checkbox_lines=tuple(checkbox_lines),
            checked_count=checked_count,
            unchecked_count=unchecked_count,
        )
        phases.append(phase)

        phase_errors: list[tuple[int, str]] = []
        if duplicate_heading_line is not None:
            phase_errors.append(
                (
                    heading_line,
                    _phase_error(
                        path,
                        phase,
                        heading_line,
                        "duplicate phase heading; "
                        f"first declaration is at line {duplicate_heading_line}",
                    ),
                )
            )
        for duplicate_line, _ in status_declarations[1:]:
            phase_errors.append(
                (
                    duplicate_line,
                    _phase_error(
                        path,
                        phase,
                        duplicate_line,
                        "duplicate '**Status:**' declaration; "
                        f"first declaration is at line {status_line}",
                    ),
                )
            )
        if status_line is not None and status != "deferred":
            shown = status if status else "<blank>"
            phase_errors.append(
                (
                    status_line,
                    _phase_error(
                        path,
                        phase,
                        status_line,
                        f"invalid '**Status:**' value '{shown}' (expected exactly 'deferred')",
                    ),
                )
            )
        if goal_line is None:
            phase_errors.append(
                (
                    heading_line,
                    _phase_error(
                        path, phase, heading_line, "missing a non-empty 'Goal:' declaration"
                    ),
                )
            )
        if not checkbox_lines:
            phase_errors.append(
                (
                    heading_line,
                    _phase_error(path, phase, heading_line, "has no valid top-level checkbox item"),
                )
            )
        errors.extend(message for _, message in sorted(phase_errors, key=lambda item: item[0]))

    if errors:
        return RoadmapAnalysis(tuple(phases), (), None, tuple(errors))

    current = next(
        (
            phase
            for phase in phases
            if not phase.is_deferred and phase.unchecked_count > 0
        ),
        None,
    )
    if current is None:
        errors.append(
            f"{path}: Roadmap exhausted: no non-deferred phase has an unchecked item; "
            "re-cadence the Roadmap"
        )
    dispositions = tuple(
        "deferred"
        if phase.is_deferred
        else "delivered"
        if phase.is_delivered
        else "current"
        if phase is current
        else "planned"
        for phase in phases
    )
    return RoadmapAnalysis(tuple(phases), dispositions, current, tuple(errors))


def check(specs_dir: Path) -> int:
    """Validate all constitution files without writing anything."""
    errors: list[str] = []
    paths = {name: specs_dir / name for name in CONSTITUTION_FILES}
    for name, path in paths.items():
        if not path.is_file():
            errors.append(f"{path}: missing required constitution file {name}")

    if not errors:
        roadmap_analysis = analyze_roadmap(paths["roadmap.md"])
        errors.extend(validate_mission(paths["mission.md"]))
        errors.extend(validate_constraints(paths["constraints.md"]))
        errors.extend(roadmap_analysis.errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"valid constitution shape: {specs_dir}")
    return 0


def readiness_constraints(path: Path) -> list[str]:
    """Require the portable method baseline and hard-constraint verification."""
    text = read_text_file(path)
    blocks, _ = yaml_blocks(text)
    errors: list[str] = []
    constraint_ids: set[str] = set()
    for index, (start_line, lines) in enumerate(blocks, start=1):
        values = parse_constraint_block(lines)
        name = values.get("id") or f"block {index} at line {start_line}"
        if values.get("id"):
            constraint_ids.add(values["id"])
        if values.get("severity") == "hard" and not values.get("verification", "").strip():
            errors.append(f"{path}: constraint {name}: hard constraint has no non-empty 'verification'")
    missing = [
        constraint_id
        for constraint_id in REQUIRED_PORTABLE_CONSTRAINT_IDS
        if constraint_id not in constraint_ids
    ]
    if missing:
        errors.append(
            f"{path}: missing portable Control Tower baseline constraint id(s): "
            f"{', '.join(missing)}; copy the inherited baseline blocks from "
            ".github/skills/bootstrap-tower/assets/constraints.md and keep product "
            "constraints separate"
        )
    return errors


def readiness_mission(path: Path) -> list[str]:
    """The mission Success section must have at least one content line."""
    text = read_text_file(path)
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        heading = markdown_heading_text(line)
        if heading and heading.casefold().startswith("success"):
            start = i
            break
    if start is None:
        return [f"{path}: missing Success section heading"]
    end = len(lines)
    for k in range(start + 1, len(lines)):
        if markdown_heading_text(lines[k]) is not None:
            end = k
            break
    if not any(line.strip() for line in lines[start + 1:end]):
        return [f"{path}: Success section has no content"]
    return []


def readiness(specs_dir: Path) -> int:
    """Validate constitution shape plus inception-readiness sub-checks."""
    errors: list[str] = []
    paths = {name: specs_dir / name for name in CONSTITUTION_FILES}
    for name, path in paths.items():
        if not path.is_file():
            errors.append(f"{path}: missing required constitution file {name}")
    if not errors:
        roadmap_analysis = analyze_roadmap(paths["roadmap.md"])
        errors.extend(validate_mission(paths["mission.md"]))
        errors.extend(validate_constraints(paths["constraints.md"]))
        errors.extend(roadmap_analysis.errors)
        errors.extend(readiness_constraints(paths["constraints.md"]))
        errors.extend(readiness_mission(paths["mission.md"]))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"constitution ready for the loop: {specs_dir}")
    return 0


def current_phase(specs_dir: Path) -> int:
    """Print the normalized current phase heading as a machine-readable line."""
    analysis = analyze_roadmap(specs_dir / "roadmap.md")
    if analysis.errors:
        for error in analysis.errors:
            print(error, file=sys.stderr)
        return 1
    assert analysis.current is not None
    print(analysis.current.heading)
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Scaffold or shape-check mission.md, constraints.md, and roadmap.md.",
    )
    parser.add_argument(
        "specs_dir",
        nargs="?",
        default="constitution",
        help="target constitution directory (default: constitution)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate constitution shape without writing files",
    )
    parser.add_argument(
        "--readiness",
        action="store_true",
        help="shape check plus inception-readiness sub-checks (no writes)",
    )
    parser.add_argument(
        "--current-phase",
        action="store_true",
        help="print the selected current Roadmap phase heading (no writes)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing files in scaffold mode",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line tool."""
    parser = build_parser()
    args = parser.parse_args(argv)
    specs_dir = Path(args.specs_dir)

    try:
        if args.current_phase and (args.check or args.readiness or args.force):
            print(
                "error: --current-phase cannot be used with --check/--readiness/--force",
                file=sys.stderr,
            )
            return 2
        if args.check or args.readiness:
            if args.force:
                print("error: --force cannot be used with --check/--readiness", file=sys.stderr)
                return 2
            return readiness(specs_dir) if args.readiness else check(specs_dir)
        if args.current_phase:
            return current_phase(specs_dir)
        return scaffold(specs_dir, args.force)
    except ToolError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())