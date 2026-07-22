#!/usr/bin/env python3
"""Shared parser for Control Tower constraint blocks.

Constraint metadata lives in fenced YAML, but collection-valued fields use JSON inline
values so the deterministic gates remain standard-library only.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

KEY_VALUE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")


class ConstraintModelError(ValueError):
    """A malformed constraint artifact."""


@dataclass(frozen=True)
class ConstraintBlock:
    path: Path
    line: int
    fields: dict[str, str]

    @property
    def constraint_id(self) -> str:
        return _strip_scalar(self.fields.get("id", "")) or f"line {self.line}"


def _strip_scalar(value: str) -> str:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.strip()


def _yaml_blocks(text: str) -> list[tuple[int, list[str]]]:
    blocks: list[tuple[int, list[str]]] = []
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
        raise ConstraintModelError(f"unclosed yaml fence opened at line {start_line}")
    return blocks


def parse_constraints(path: Path) -> list[ConstraintBlock]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ConstraintModelError(f"{path}: cannot read UTF-8 constraint artifact: {exc}") from exc

    result: list[ConstraintBlock] = []
    for start_line, lines in _yaml_blocks(text):
        if not any(re.match(r"^\s*constraint\s*:\s*$", line) for line in lines):
            continue
        fields: dict[str, str] = {}
        for offset, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = KEY_VALUE.match(line)
            if not match:
                raise ConstraintModelError(
                    f"{path}: constraint at line {start_line}: malformed line "
                    f"{start_line + offset}: {stripped}"
                )
            key, value = match.groups()
            if key == "constraint":
                continue
            if key in fields:
                raise ConstraintModelError(
                    f"{path}: constraint at line {start_line}: duplicate key '{key}'"
                )
            fields[key] = value.strip()
        if not _strip_scalar(fields.get("id", "")):
            raise ConstraintModelError(
                f"{path}: constraint at line {start_line}: missing non-empty key 'id'"
            )
        result.append(ConstraintBlock(path=path, line=start_line, fields=fields))
    if not result:
        raise ConstraintModelError(f"{path}: no fenced constraint blocks found")
    return result


def scalar(block: ConstraintBlock, key: str) -> str:
    return _strip_scalar(block.fields.get(key, ""))


def json_array(block: ConstraintBlock, key: str) -> list[Any]:
    raw = block.fields.get(key)
    if raw is None:
        raise ConstraintModelError(
            f"{block.path}: constraint {block.constraint_id}: missing key '{key}'"
        )
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConstraintModelError(
            f"{block.path}: constraint {block.constraint_id}: '{key}' is not valid inline JSON: "
            f"{exc.msg}"
        ) from exc
    if not isinstance(value, list):
        raise ConstraintModelError(
            f"{block.path}: constraint {block.constraint_id}: '{key}' must be a JSON array"
        )
    return value
