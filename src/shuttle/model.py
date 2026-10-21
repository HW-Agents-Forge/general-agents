"""Typed representation of agents and skills. No I/O here."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Tier(StrEnum):
    """Model tiers. `small` is the only one (ADR 0006)."""

    SMALL = "small"


class Tool(StrEnum):
    """Abstract tools an agent may use."""

    READ = "read"
    SEARCH = "search"
    SHELL = "shell"


@dataclass(frozen=True)
class Agent:
    name: str
    description: str
    tier: Tier
    tools: tuple[Tool, ...]
    body: str


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    body: str


@dataclass(frozen=True)
class Catalog:
    agents: tuple[Agent, ...]
    skills: tuple[Skill, ...]

    def agent_names(self) -> frozenset[str]:
        return frozenset(agent.name for agent in self.agents)
