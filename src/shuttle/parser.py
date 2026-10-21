"""Read agent and skill sources: TOML frontmatter between `+++` lines, then a Markdown body."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from .errors import SourceError
from .model import (
    DEFAULT_MAX_OUTPUT_LINES,
    NAME_PATTERN,
    Agent,
    Skill,
    Tier,
    Tool,
)

DELIMITER = "+++"
AGENT_KEYS = frozenset({"name", "description", "tier", "tools", "max_output_lines"})
SKILL_KEYS = frozenset({"name", "description"})


def split_document(text: str, path: Path) -> tuple[dict[str, Any], str]:
    """Split a source into its parsed TOML frontmatter and its body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != DELIMITER:
        raise SourceError(f"{path}: the file must start with a '{DELIMITER}' frontmatter line")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == DELIMITER)
    except StopIteration:
        raise SourceError(f"{path}: the frontmatter is not closed by '{DELIMITER}'") from None
    try:
        meta = tomllib.loads("\n".join(lines[1:end]))
    except tomllib.TOMLDecodeError as error:
        raise SourceError(f"{path}: invalid TOML frontmatter: {error}") from error
    body = "\n".join(lines[end + 1 :]).strip()
    if not body:
        raise SourceError(f"{path}: the body is empty")
    return meta, body


def _check_keys(meta: dict[str, Any], allowed: frozenset[str], path: Path) -> None:
    unknown = sorted(set(meta) - allowed)
    if unknown:
        raise SourceError(f"{path}: unknown frontmatter key(s): {', '.join(unknown)}")


def _text(meta: dict[str, Any], key: str, path: Path) -> str:
    value = meta.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SourceError(f"{path}: '{key}' is required and must be a non-empty string")
    return value.strip()


def _name(meta: dict[str, Any], expected: str, path: Path) -> str:
    name = _text(meta, "name", path)
    if not NAME_PATTERN.match(name):
        raise SourceError(f"{path}: invalid name '{name}' (lowercase letters, digits, hyphens)")
    if name != expected:
        raise SourceError(f"{path}: name '{name}' must match '{expected}'")
    return name


def _tier(meta: dict[str, Any], path: Path) -> Tier:
    value = meta.get("tier")
    try:
        return Tier(str(value))
    except ValueError:
        allowed = ", ".join(tier.value for tier in Tier)
        raise SourceError(f"{path}: 'tier' must be one of: {allowed}") from None


def _tools(meta: dict[str, Any], path: Path) -> tuple[Tool, ...]:
    value = meta.get("tools")
    if not isinstance(value, list) or not value:
        raise SourceError(f"{path}: 'tools' is required and must be a non-empty list")
    tools: list[Tool] = []
    for item in value:
        try:
            tool = Tool(item)
        except ValueError:
            allowed = ", ".join(t.value for t in Tool)
            raise SourceError(f"{path}: unknown tool {item!r} (allowed: {allowed})") from None
        if tool in tools:
            raise SourceError(f"{path}: duplicate tool '{tool.value}'")
        tools.append(tool)
    return tuple(tools)


def _max_output_lines(meta: dict[str, Any], path: Path) -> int:
    value = meta.get("max_output_lines", DEFAULT_MAX_OUTPUT_LINES)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise SourceError(f"{path}: 'max_output_lines' must be a positive integer")
    return value


def parse_agent(path: Path) -> Agent:
    meta, body = split_document(path.read_text(encoding="utf-8"), path)
    _check_keys(meta, AGENT_KEYS, path)
    return Agent(
        name=_name(meta, path.stem, path),
        description=_text(meta, "description", path),
        tier=_tier(meta, path),
        tools=_tools(meta, path),
        max_output_lines=_max_output_lines(meta, path),
        body=body,
    )


def parse_skill(path: Path) -> Skill:
    meta, body = split_document(path.read_text(encoding="utf-8"), path)
    _check_keys(meta, SKILL_KEYS, path)
    return Skill(
        name=_name(meta, path.parent.name, path),
        description=_text(meta, "description", path),
        body=body,
    )
