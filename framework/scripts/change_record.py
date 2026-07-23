#!/usr/bin/env python3
"""Dependency-free parser and normalized model for Control Tower Change Records."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath

from constraint_model import ConstraintModelError, json_array, parse_constraints, scalar

FRONTMATTER_KEYS = {"change", "status", "roadmap"}
STATUSES = {"draft", "confirmed", "reviewed"}
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d+$")
DATED_RECORD_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$"
)
FRONTMATTER_LINE_RE = re.compile(r'^([a-z][a-z0-9_-]*):\s*("(?:[^"\\]|\\.)*")$')
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
SUBHEADING_RE = re.compile(r"^###\s+(.+?)\s*$")
NUMBERED_RE = re.compile(r"^\s*\d+\.\s+(\S.*?)\s*$")
LABEL_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.*?)\s*$")
PLACEHOLDER_RE = re.compile(
    r"^(?:<.*>|todo(?:\b.*)?|tbd(?:\b.*)?|pending(?:\b.*)?|n/?a|unknown|-+|\?+)$",
    re.IGNORECASE,
)
REQUIRED_SECTIONS = {
    "intent and first human confirmation",
    "activated proof obligations",
    "short implementation plan",
    "evidence",
    "corrections",
    "independent final review",
}
EVIDENCE_RESULTS = {"pass", "fail", "pending"}
DISPOSITIONS = {"covered", "accepted-risk", "follow-up"}
CLOSEOUT_DISPOSITIONS = {"delivered", "remaining", "discovered", "evidence"}
FINAL_ATTEMPT_LABELS = (
    "Reviewer/date",
    "Reviewed target",
    "Remote",
    "Ref",
    "Start local head",
    "Start remote head",
    "Completion local head",
    "Completion remote head",
    "Stability",
    "Returned verdict",
    "Gates",
    "Evidence",
    "Summary",
)
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
ROADMAP_LIFECYCLE_ADR_RE = re.compile(
    r"^constitution/decisions/ADR-\d{8}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)


class ChangeRecordError(ValueError):
    """A malformed or lifecycle-invalid Change Record."""

    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__("; ".join(problems))


@dataclass(frozen=True)
class Obligation:
    constraint_id: str
    reason: str
    expected_evidence: str
    initial_state: str


@dataclass(frozen=True)
class EvidenceEntry:
    constraint_id: str
    result: str
    evidence: str


@dataclass(frozen=True)
class ResidualDisposition:
    residual_id: str
    disposition: str
    notes: str


@dataclass(frozen=True)
class ChangeRecord:
    path: Path
    change: str
    status: str
    roadmap: str
    outcome: str
    initial_confirmation: str
    roadmap_lifecycle_adr: str
    obligations: tuple[Obligation, ...]
    plan_steps: tuple[str, ...]
    evidence: tuple[EvidenceEntry, ...]
    corrections: tuple[str, ...]
    architecture_triggered: bool
    architecture_verdict: str
    final_reviewed_target: str
    final_verdict: str
    final_stability: str
    final_attempts: tuple[str, ...]
    residual_dispositions: tuple[ResidualDisposition, ...]
    closeout: tuple[tuple[str, str], ...]
    sections: dict[str, str]

    @property
    def evidence_by_constraint(self) -> dict[str, EvidenceEntry]:
        """Return the latest append-only evidence attempt for each obligation."""
        return {entry.constraint_id: entry for entry in self.evidence}

    @property
    def disposition_by_residual(self) -> dict[str, ResidualDisposition]:
        return {entry.residual_id: entry for entry in self.residual_dispositions}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ChangeRecordError([f"{path}: cannot read UTF-8 Change Record: {exc}"]) from exc


def _protected_review_content(
    text: str, expected_status: str, path: Path
) -> tuple[str | None, list[str]]:
    """Normalize only the two fields permitted to change while recording final review."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    problems: list[str] = []
    try:
        frontmatter_end = lines.index("---", 1)
    except ValueError:
        return None, [f"{path}: cannot protect malformed frontmatter"]
    status_line = f'status: "{expected_status}"'
    status_indexes = [
        index
        for index in range(1, frontmatter_end)
        if lines[index].startswith("status:")
    ]
    if len(status_indexes) != 1 or lines[status_indexes[0]] != status_line:
        problems.append(
            f"{path}: expected exact frontmatter transition line '{status_line}'"
        )
    review_indexes = [
        index
        for index, line in enumerate(lines)
        if line == "## Independent final review"
    ]
    if len(review_indexes) != 1:
        problems.append(
            f"{path}: expected exactly one '## Independent final review' section"
        )
    if problems:
        return None, problems
    lines[status_indexes[0]] = 'status: "confirmed"'
    review_start = review_indexes[0]
    review_end = next(
        (
            index
            for index in range(review_start + 1, len(lines))
            if HEADING_RE.fullmatch(lines[index])
        ),
        len(lines),
    )
    protected = lines[: review_start + 1] + ["<returned-review-body>"] + lines[review_end:]
    return "\n".join(protected), []


def review_recording_problems(
    old: ChangeRecord, new: ChangeRecord, old_text: str, new_text: str
) -> list[str]:
    """Protect every normalized record byte outside the returned final-review body."""
    if old.status != "confirmed" or new.status != "reviewed":
        return []
    old_protected, problems = _protected_review_content(
        old_text, "confirmed", old.path
    )
    new_protected, new_problems = _protected_review_content(
        new_text, "reviewed", new.path
    )
    problems.extend(new_problems)
    if not problems and old_protected != new_protected:
        problems.append(
            f"{new.path}: protected Change Record content changed during final review recording"
        )
    return problems


def _placeholder(value: str) -> bool:
    value = value.strip().strip("`")
    return not value or bool(PLACEHOLDER_RE.fullmatch(value))


def _cells(row: str) -> list[str]:
    return [cell.strip().strip("`") for cell in row.strip().strip("|").split("|")]


def _separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells)


def _table(
    section: str, headers: tuple[str, ...], label: str
) -> tuple[list[list[str]], list[str]]:
    problems: list[str] = []
    lines = section.splitlines()
    for index, line in enumerate(lines):
        if "|" not in line:
            continue
        if tuple(cell.lower() for cell in _cells(line)) != headers:
            continue
        if index + 1 >= len(lines) or not _separator(_cells(lines[index + 1])):
            return [], [f"{label}: invalid Markdown table separator"]
        rows: list[list[str]] = []
        for row in lines[index + 2 :]:
            if "|" not in row:
                if row.strip():
                    break
                continue
            cells = _cells(row)
            if _separator(cells):
                continue
            if len(cells) != len(headers):
                problems.append(
                    f"{label}: table row has {len(cells)} cells; expected {len(headers)}"
                )
                continue
            rows.append(cells)
        return rows, problems
    return [], [f"{label}: missing table with columns: {' | '.join(headers)}"]


def _frontmatter(path: Path, text: str) -> tuple[dict[str, str], int, list[str]]:
    lines = text.splitlines()
    problems: list[str] = []
    if not lines or lines[0] != "---":
        return {}, 0, [f"{path}: frontmatter must begin with an exact '---' delimiter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, 0, [f"{path}: frontmatter closing '---' delimiter is missing"]
    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        match = FRONTMATTER_LINE_RE.fullmatch(line)
        if not match:
            problems.append(
                f"{path}:{line_number}: frontmatter must use key: JSON-quoted-string"
            )
            continue
        key, raw = match.groups()
        if key in fields:
            problems.append(f"{path}:{line_number}: duplicate frontmatter key '{key}'")
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            problems.append(f"{path}:{line_number}: invalid JSON string: {exc.msg}")
            continue
        if not isinstance(value, str) or "\n" in value or "\r" in value:
            problems.append(f"{path}:{line_number}: frontmatter value must be one string")
            continue
        fields[key] = value
    missing = sorted(FRONTMATTER_KEYS - fields.keys())
    extra = sorted(fields.keys() - FRONTMATTER_KEYS)
    if missing:
        problems.append(f"{path}: missing frontmatter key(s): {', '.join(missing)}")
    if extra:
        problems.append(f"{path}: unknown frontmatter key(s): {', '.join(extra)}")
    return fields, end + 1, problems


def _sections(path: Path, lines: list[str], start: int) -> tuple[dict[str, str], list[str]]:
    sections: dict[str, str] = {}
    problems: list[str] = []
    headings: list[tuple[int, str]] = []
    for index in range(start, len(lines)):
        match = HEADING_RE.fullmatch(lines[index])
        if match:
            headings.append((index, match.group(1).strip()))
    for position, (index, name) in enumerate(headings):
        key = name.lower()
        if key in sections:
            problems.append(f"{path}:{index + 1}: duplicate section '## {name}'")
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        sections[key] = "\n".join(lines[index + 1 : end]).strip()
    missing = sorted(REQUIRED_SECTIONS - sections.keys())
    if missing:
        problems.append(f"{path}: missing required section(s): {', '.join(missing)}")
    return sections, problems


def _label(section: str, name: str) -> str:
    values = _labels(section, name)
    return values[-1] if values else ""


def _labels(section: str, name: str) -> list[str]:
    values: list[str] = []
    for line in section.splitlines():
        match = LABEL_RE.fullmatch(line.strip())
        if match and match.group(1).strip().lower() == name.lower():
            values.append(match.group(2).strip().strip("`"))
    return values


def _roadmap_lifecycle_authorization(
    path: Path, section: str
) -> tuple[str, list[str]]:
    """Normalize the optional exact lifecycle ADR section."""
    if not section:
        return "", []
    problems: list[str] = []
    lines = [line.strip() for line in section.splitlines() if line.strip()]
    values = _labels(section, "ADR")
    if len(lines) != 1 or len(values) != 1:
        return "", [
            f"{path}: Roadmap lifecycle authorization must contain exactly one "
            "'**ADR:** `constitution/decisions/ADR-YYYYMMDD-NN-lowercase-kebab-name.md`' line"
        ]
    value = values[0].strip()
    if _placeholder(value) or "\\" in value:
        problems.append(f"{path}: Roadmap lifecycle ADR path is empty, placeholder, or malformed")
        return "", problems
    posix = PurePosixPath(value)
    normalized = posix.as_posix()
    if (
        posix.is_absolute()
        or ".." in posix.parts
        or normalized != value
        or ROADMAP_LIFECYCLE_ADR_RE.fullmatch(normalized) is None
    ):
        problems.append(
            f"{path}: Roadmap lifecycle ADR must be a repository-relative "
            "constitution/decisions/ADR-YYYYMMDD-NN-lowercase-kebab-name.md path"
        )
        return "", problems
    return normalized, problems


def _obligations(path: Path, section: str) -> tuple[tuple[Obligation, ...], list[str]]:
    rows, problems = _table(
        section,
        ("constraint", "why activated", "expected evidence", "initial state"),
        f"{path}: Activated proof obligations",
    )
    obligations: list[Obligation] = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        constraint_id, reason, expected, initial = row
        label = f"{path}: obligation row {index}"
        if not ID_RE.fullmatch(constraint_id):
            problems.append(f"{label}: invalid constraint id '{constraint_id}'")
            continue
        if constraint_id in seen:
            problems.append(f"{label}: duplicate constraint id '{constraint_id}'")
            continue
        seen.add(constraint_id)
        if _placeholder(reason):
            problems.append(f"{label}: reason is empty or placeholder")
        if _placeholder(expected):
            problems.append(f"{label}: expected evidence is empty or placeholder")
        if not initial.strip():
            problems.append(f"{label}: initial state is empty")
        obligations.append(Obligation(constraint_id, reason, expected, initial))
    if not obligations:
        problems.append(f"{path}: activated proof obligations table has no rows")
    return tuple(obligations), problems


def _plan(path: Path, section: str) -> tuple[tuple[str, ...], list[str]]:
    steps = tuple(
        match.group(1).strip()
        for line in section.splitlines()
        if (match := NUMBERED_RE.fullmatch(line))
    )
    problems = []
    if not steps or any(_placeholder(step) for step in steps):
        problems.append(f"{path}: Short implementation plan needs a non-placeholder numbered step")
    return steps, problems


def _evidence(path: Path, section: str) -> tuple[tuple[EvidenceEntry, ...], list[str]]:
    if _placeholder(section.splitlines()[0] if section.splitlines() else ""):
        return (), []
    rows, problems = _table(
        section, ("constraint", "result", "evidence"), f"{path}: Evidence"
    )
    entries: list[EvidenceEntry] = []
    for index, (constraint_id, result, evidence) in enumerate(rows, start=1):
        label = f"{path}: evidence row {index}"
        result = result.lower()
        if not ID_RE.fullmatch(constraint_id):
            problems.append(f"{label}: invalid constraint id '{constraint_id}'")
            continue
        if result not in EVIDENCE_RESULTS:
            problems.append(f"{label}: result '{result}' is not pass, fail, or pending")
        if _placeholder(evidence):
            problems.append(f"{label}: evidence is empty or placeholder")
        entries.append(EvidenceEntry(constraint_id, result, evidence))
    return tuple(entries), problems


def _corrections(section: str) -> tuple[str, ...]:
    if _placeholder(section.splitlines()[0] if section.splitlines() else ""):
        return ()
    return tuple(line.strip() for line in section.splitlines() if line.strip())


def _attempts(path: Path, section: str) -> tuple[tuple[str, ...], list[str]]:
    lines = section.splitlines()
    starts = [index for index, line in enumerate(lines) if SUBHEADING_RE.fullmatch(line)]
    attempts: list[str] = []
    problems: list[str] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        attempt = "\n".join(lines[start:end]).strip()
        heading = SUBHEADING_RE.fullmatch(lines[start])
        expected_heading = f"Attempt {position + 1}"
        if heading is None or heading.group(1).strip() != expected_heading:
            problems.append(
                f"{path}: final review attempt heading must be '### {expected_heading}'"
            )
        labels = {
            name.lower(): value
            for name in FINAL_ATTEMPT_LABELS
            if (value := _label(attempt, name))
        }
        missing = [name for name in FINAL_ATTEMPT_LABELS if name.lower() not in labels]
        if missing:
            problems.append(
                f"{path}: {expected_heading} missing field(s): {', '.join(missing)}"
            )
        else:
            reviewer_date = labels["reviewer/date"]
            if not re.search(r"\b\d{4}-\d{2}-\d{2}\b", reviewer_date):
                problems.append(f"{path}: {expected_heading} Reviewer/date needs an ISO date")
            for name in (
                "reviewed target",
                "start local head",
                "start remote head",
                "completion local head",
                "completion remote head",
            ):
                if not FULL_SHA_RE.fullmatch(labels[name].strip("`")):
                    problems.append(
                        f"{path}: {expected_heading} {name} must be one full commit SHA"
                    )
            stability = labels["stability"].strip("`").upper()
            verdict = labels["returned verdict"].strip("`").upper()
            if stability not in {"STABLE", "STALE"}:
                problems.append(
                    f"{path}: {expected_heading} Stability must be STABLE or STALE"
                )
            if verdict not in {"PROMOTE", "BLOCK"}:
                problems.append(
                    f"{path}: {expected_heading} Returned verdict must be PROMOTE or BLOCK"
                )
            heads = {
                labels[name].strip("`")
                for name in (
                    "reviewed target",
                    "start local head",
                    "start remote head",
                    "completion local head",
                    "completion remote head",
                )
            }
            if stability == "STABLE" and len(heads) != 1:
                problems.append(
                    f"{path}: {expected_heading} cannot claim STABLE when target/head values differ"
                )
            for name in ("remote", "ref", "gates", "evidence", "summary"):
                if _placeholder(labels[name]):
                    problems.append(
                        f"{path}: {expected_heading} {name} is empty or placeholder"
                    )
        attempts.append(attempt)
    return tuple(attempts), problems


def _residual_dispositions(
    path: Path, section: str
) -> tuple[tuple[ResidualDisposition, ...], list[str]]:
    if "residual | disposition | notes" not in section.lower():
        return (), []
    rows, problems = _table(
        section,
        ("residual", "disposition", "notes"),
        f"{path}: Independent final review residual dispositions",
    )
    entries: list[ResidualDisposition] = []
    seen: set[str] = set()
    for index, (residual_id, disposition, notes) in enumerate(rows, start=1):
        label = f"{path}: residual disposition row {index}"
        disposition = disposition.lower()
        if residual_id in seen:
            problems.append(f"{label}: duplicate residual id '{residual_id}'")
            continue
        seen.add(residual_id)
        if disposition not in DISPOSITIONS:
            problems.append(f"{label}: invalid disposition '{disposition}'")
        if _placeholder(notes):
            problems.append(f"{label}: notes are empty or placeholder")
        entries.append(ResidualDisposition(residual_id, disposition, notes))
    return tuple(entries), problems


def _closeout(path: Path, section: str) -> tuple[tuple[tuple[str, str], ...], list[str]]:
    if not section:
        return (), []
    rows, problems = _table(
        section, ("disposition", "record"), f"{path}: Closeout"
    )
    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for index, (disposition, record) in enumerate(rows, start=1):
        label = f"{path}: closeout row {index}"
        disposition = disposition.lower()
        if disposition not in CLOSEOUT_DISPOSITIONS:
            problems.append(f"{label}: invalid disposition '{disposition}'")
        if disposition in seen:
            problems.append(f"{label}: duplicate disposition '{disposition}'")
        seen.add(disposition)
        if _placeholder(record):
            problems.append(f"{label}: record is empty or placeholder")
        entries.append((disposition, record))
    return tuple(entries), problems


def load_change_record(
    path: Path, constraints_path: Path | None = None
) -> ChangeRecord:
    """Parse one dated Change Record and fail closed on malformed state."""
    path = Path(path)
    text = _read(path)
    lines = text.splitlines()
    fields, body_start, problems = _frontmatter(path, text)
    sections, section_problems = _sections(path, lines, body_start)
    problems.extend(section_problems)

    filename_match = DATED_RECORD_RE.fullmatch(path.name)
    if filename_match is None:
        problems.append(
            f"{path}: filename must be changes/YYYY-MM-DD-lowercase-kebab-name.md"
        )
    else:
        try:
            date.fromisoformat(filename_match.group("date"))
        except ValueError:
            problems.append(f"{path}: filename date is not a valid calendar date")
        if fields.get("change") != filename_match.group("slug"):
            problems.append(
                f"{path}: frontmatter change must equal filename slug "
                f"'{filename_match.group('slug')}'"
            )

    status = fields.get("status", "")
    if status not in STATUSES:
        problems.append(f"{path}: status '{status}' is not draft, confirmed, or reviewed")
    roadmap = fields.get("roadmap", "")
    if _placeholder(roadmap):
        problems.append(f"{path}: roadmap anchor is empty or placeholder")

    intent = sections.get("intent and first human confirmation", "")
    outcome = _label(intent, "Observable outcome")
    confirmation = _label(intent, "Initial human confirmation")
    if _placeholder(outcome):
        problems.append(f"{path}: observable outcome is empty or placeholder")
    if status in {"confirmed", "reviewed"} and _placeholder(confirmation):
        problems.append(f"{path}: confirmed state needs a non-placeholder human attestation")
    roadmap_lifecycle_adr, lifecycle_authorization_problems = (
        _roadmap_lifecycle_authorization(
            path, sections.get("roadmap lifecycle authorization", "")
        )
    )
    problems.extend(lifecycle_authorization_problems)

    obligations, obligation_problems = _obligations(
        path, sections.get("activated proof obligations", "")
    )
    problems.extend(obligation_problems)
    plan_steps, plan_problems = _plan(
        path, sections.get("short implementation plan", "")
    )
    problems.extend(plan_problems)
    evidence, evidence_problems = _evidence(path, sections.get("evidence", ""))
    problems.extend(evidence_problems)
    corrections = _corrections(sections.get("corrections", ""))

    architecture_companion = path.with_suffix("") / "design-under-test.md"
    architecture_triggered = architecture_companion.is_file()
    architecture_section = sections.get("architecture", "")
    architecture_review = sections.get("architecture review", "")
    architecture_verdict = _label(architecture_review, "Returned verdict").upper()
    if architecture_triggered:
        if not architecture_section:
            problems.append(f"{path}: linked design companion requires '## Architecture'")
        if not architecture_review:
            problems.append(f"{path}: linked design companion requires '## Architecture review'")
        companion_reference = f"{path.stem}/design-under-test.md"
        if companion_reference not in architecture_section:
            problems.append(
                f"{path}: Architecture must link the sibling {companion_reference}"
            )
        if "trigger" not in architecture_section.lower():
            problems.append(f"{path}: Architecture must name the companion trigger")
        if architecture_verdict and architecture_verdict != "PENDING":
            for label in (
                "Reviewer/date",
                "Reviewed design target/ref",
                "Start heads",
                "Completion heads",
                "Stability",
                "Pre-check",
                "Returned verdict",
            ):
                if _placeholder(_label(architecture_review, label)):
                    problems.append(
                        f"{path}: Architecture review actual return is missing {label}"
                    )
            if architecture_verdict not in {"SOUND", "REWORK", "ESCALATE"}:
                problems.append(
                    f"{path}: Architecture review verdict must be SOUND, REWORK, or ESCALATE"
                )
            architecture_shas = re.findall(
                r"\b[0-9a-f]{40}(?:[0-9a-f]{24})?\b", architecture_review
            )
            if len(architecture_shas) < 5:
                problems.append(
                    f"{path}: Architecture review needs target plus four head observations"
                )
            if (
                _label(architecture_review, "Stability").strip("`").upper() == "STABLE"
                and len(set(architecture_shas[:5])) != 1
            ):
                problems.append(
                    f"{path}: Architecture review cannot claim STABLE when target/head values differ"
                )

    final_review = sections.get("independent final review", "")
    attempts, attempt_problems = _attempts(path, final_review)
    problems.extend(attempt_problems)
    latest_review = attempts[-1] if attempts else final_review
    final_reviewed_target = _label(latest_review, "Reviewed target").strip("`")
    final_verdict = _label(latest_review, "Returned verdict").upper()
    final_stability = _label(latest_review, "Stability").upper()
    residual_dispositions, residual_problems = _residual_dispositions(path, latest_review)
    problems.extend(residual_problems)
    closeout, closeout_problems = _closeout(path, sections.get("closeout", ""))
    problems.extend(closeout_problems)

    if constraints_path is not None:
        try:
            known = {
                block.constraint_id for block in parse_constraints(Path(constraints_path))
            }
        except ConstraintModelError as exc:
            problems.append(str(exc))
        else:
            unknown = sorted(
                obligation.constraint_id
                for obligation in obligations
                if obligation.constraint_id not in known
            )
            if unknown:
                problems.append(
                    f"{path}: unknown activated constraint id(s): {', '.join(unknown)}"
                )

    if problems:
        raise ChangeRecordError(problems)
    record = ChangeRecord(
        path=path,
        change=fields["change"],
        status=status,
        roadmap=roadmap,
        outcome=outcome,
        initial_confirmation=confirmation,
        roadmap_lifecycle_adr=roadmap_lifecycle_adr,
        obligations=obligations,
        plan_steps=plan_steps,
        evidence=evidence,
        corrections=corrections,
        architecture_triggered=architecture_triggered,
        architecture_verdict=architecture_verdict,
        final_reviewed_target=final_reviewed_target,
        final_verdict=final_verdict,
        final_stability=final_stability,
        final_attempts=attempts,
        residual_dispositions=residual_dispositions,
        closeout=closeout,
        sections=sections,
    )
    if status == "reviewed":
        state_problems = reviewable_problems(record)
        if not record.final_attempts:
            state_problems.append("reviewed state requires at least one final-review attempt")
        if record.final_stability != "STABLE":
            state_problems.append("reviewed state requires latest final-review stability STABLE")
        if record.final_verdict != "PROMOTE":
            state_problems.append("reviewed state requires latest final verdict PROMOTE")
        if constraints_path is not None:
            expected, residual_problems = expected_residuals(record, constraints_path)
            state_problems.extend(residual_problems)
            actual = record.disposition_by_residual
            missing = sorted(expected - actual.keys())
            unknown = sorted(actual.keys() - expected)
            if missing:
                state_problems.append(
                    f"reviewed state missing residual disposition(s): {', '.join(missing)}"
                )
            if unknown:
                state_problems.append(
                    f"reviewed state has unknown residual disposition(s): {', '.join(unknown)}"
                )
        if state_problems:
            raise ChangeRecordError([f"{path}: {item}" for item in state_problems])
    return record


def expected_residuals(
    record: ChangeRecord, constraints_path: Path
) -> tuple[set[str], list[str]]:
    """Resolve review-routed residuals for the record's activated hard constraints."""
    problems: list[str] = []
    try:
        blocks = parse_constraints(Path(constraints_path))
    except ConstraintModelError as exc:
        return set(), [str(exc)]
    by_id = {block.constraint_id: block for block in blocks}
    result: set[str] = set()
    for obligation in record.obligations:
        block = by_id.get(obligation.constraint_id)
        if block is None:
            problems.append(
                f"{record.path}: unknown activated constraint '{obligation.constraint_id}'"
            )
            continue
        if scalar(block, "severity") != "hard":
            continue
        try:
            residuals = json_array(block, "residual")
        except ConstraintModelError as exc:
            problems.append(str(exc))
            continue
        for residual in residuals:
            if not isinstance(residual, dict) or residual.get("route") != "review":
                continue
            residual_id = residual.get("id")
            if isinstance(residual_id, str) and residual_id.strip():
                result.add(residual_id.strip())
    return result, problems


def reviewable_problems(record: ChangeRecord) -> list[str]:
    """Return deterministic reasons the implementation target is not ready for final review."""
    problems: list[str] = []
    obligation_ids = {entry.constraint_id for entry in record.obligations}
    evidence = record.evidence_by_constraint
    missing = sorted(obligation_ids - evidence.keys())
    failed = sorted(
        constraint_id
        for constraint_id, entry in evidence.items()
        if constraint_id in obligation_ids and entry.result != "pass"
    )
    unknown = sorted(evidence.keys() - obligation_ids)
    if missing:
        problems.append(f"missing evidence for obligation(s): {', '.join(missing)}")
    if failed:
        problems.append(f"non-passing evidence for obligation(s): {', '.join(failed)}")
    if unknown:
        problems.append(f"evidence references unknown obligation(s): {', '.join(unknown)}")
    if not record.corrections:
        problems.append("Corrections is still pending")
    if record.architecture_triggered and record.architecture_verdict != "SOUND":
        problems.append("triggered architecture review has no actual SOUND verdict")
    closeout = dict(record.closeout)
    missing_closeout = sorted(CLOSEOUT_DISPOSITIONS - closeout.keys())
    if missing_closeout:
        problems.append(
            f"closeout missing disposition(s): {', '.join(missing_closeout)}"
        )
    return problems


def merge_ready_problems(
    record: ChangeRecord, constraints_path: Path
) -> list[str]:
    """Return deterministic reasons the record cannot authorize governed merge."""
    if record.status != "reviewed":
        verdict = record.final_verdict or "pending"
        return [
            f"Change Record status is '{record.status}' (expected 'reviewed')",
            f"final returned verdict is {verdict}",
        ]
    problems = reviewable_problems(record)
    if record.final_stability != "STABLE":
        problems.append(
            f"latest final review stability is '{record.final_stability or 'pending'}'"
        )
    if record.final_verdict != "PROMOTE":
        problems.append(
            f"latest final returned verdict is '{record.final_verdict or 'pending'}'"
        )
    expected, residual_problems = expected_residuals(record, constraints_path)
    problems.extend(residual_problems)
    actual = record.disposition_by_residual
    missing = sorted(expected - actual.keys())
    unknown = sorted(actual.keys() - expected)
    if missing:
        problems.append(f"missing routed residual disposition(s): {', '.join(missing)}")
    if unknown:
        problems.append(f"unknown routed residual disposition(s): {', '.join(unknown)}")
    return problems


def monotonic_problems(old: ChangeRecord, new: ChangeRecord) -> list[str]:
    """Compare two versions where the base record exists."""
    problems: list[str] = []
    if old.status == "reviewed":
        return [f"{new.path}: reviewed Change Record is terminal and cannot be modified"]
    transitions = {
        "draft": {"draft", "confirmed"},
        "confirmed": {"confirmed", "reviewed"},
    }
    if new.status not in transitions.get(old.status, set()):
        problems.append(f"{new.path}: illegal status transition {old.status} -> {new.status}")
    if old.status == "draft":
        return problems
    for label, before, after in (
        ("change", old.change, new.change),
        ("roadmap", old.roadmap, new.roadmap),
        ("observable outcome", old.outcome, new.outcome),
        ("initial confirmation", old.initial_confirmation, new.initial_confirmation),
        ("Roadmap lifecycle ADR", old.roadmap_lifecycle_adr, new.roadmap_lifecycle_adr),
        ("short implementation plan", old.plan_steps, new.plan_steps),
    ):
        if before != after:
            problems.append(f"{new.path}: confirmed {label} changed")
    for label, before, after in (
        ("obligations", old.obligations, new.obligations),
        ("evidence", old.evidence, new.evidence),
        ("corrections", old.corrections, new.corrections),
        ("final-review attempts", old.final_attempts, new.final_attempts),
    ):
        if len(after) < len(before) or after[: len(before)] != before:
            problems.append(f"{new.path}: confirmed {label} are not prefix-append-only")
    if new.status == "reviewed":
        for label, before, after in (
            ("evidence", old.evidence, new.evidence),
            ("corrections", old.corrections, new.corrections),
            ("architecture", old.sections.get("architecture", ""), new.sections.get("architecture", "")),
            (
                "architecture review",
                old.sections.get("architecture review", ""),
                new.sections.get("architecture review", ""),
            ),
            ("closeout", old.closeout, new.closeout),
        ):
            if before != after:
                problems.append(
                    f"{new.path}: protected {label} changed during final review recording"
                )
    return problems
