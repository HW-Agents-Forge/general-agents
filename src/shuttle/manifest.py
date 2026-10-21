"""Read `agents.toml`: the per-agent settings that cannot be deduced from the Markdown source."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import SourceError
from .model import Tier, Tool

MANIFEST_FILE = "agents.toml"
_KEYS = frozenset({"tools", "tier"})


@dataclass(frozen=True)
class AgentSpec:
    tools: tuple[Tool, ...]
    tier: Tier


def _tools(value: Any, origin: str) -> tuple[Tool, ...]:
    if not isinstance(value, list) or not value:
        raise SourceError(f"{origin}: 'tools' is required and must be a non-empty list")
    tools: list[Tool] = []
    for item in value:
        try:
            tool = Tool(item)
        except ValueError:
            allowed = ", ".join(t.value for t in Tool)
            raise SourceError(f"{origin}: unknown tool {item!r} (allowed: {allowed})") from None
        if tool in tools:
            raise SourceError(f"{origin}: duplicate tool '{tool.value}'")
        tools.append(tool)
    return tuple(tools)


def _tier(value: Any, origin: str) -> Tier:
    try:
        return Tier(str(value))
    except ValueError:
        allowed = ", ".join(tier.value for tier in Tier)
        raise SourceError(f"{origin}: 'tier' must be one of: {allowed}") from None


def load_manifest(path: Path) -> dict[str, AgentSpec]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SourceError(f"{path}: file not found") from None
    except tomllib.TOMLDecodeError as error:
        raise SourceError(f"{path}: invalid TOML: {error}") from error

    specs: dict[str, AgentSpec] = {}
    for name, table in data.items():
        origin = f"{path} [{name}]"
        if not isinstance(table, dict):
            raise SourceError(f"{origin}: must be a table")
        unknown = sorted(set(table) - _KEYS)
        if unknown:
            raise SourceError(f"{origin}: unknown key(s): {', '.join(unknown)}")
        specs[name] = AgentSpec(
            tools=_tools(table.get("tools"), origin),
            tier=_tier(table.get("tier", Tier.SMALL.value), origin),
        )
    return specs
