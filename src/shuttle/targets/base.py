"""The interface every target tool implements."""

from __future__ import annotations

from pathlib import PurePath
from typing import Protocol

from ..model import Agent, Skill


class Target(Protocol):
    """Tool-specific paths and rendering. Targets never write to disk."""

    name: str

    def agent_path(self, agent: Agent) -> PurePath:
        """Install location of an agent, relative to the home."""
        ...

    def skill_path(self, skill: Skill) -> PurePath:
        """Install location of a skill, relative to the home."""
        ...

    def render_agent(self, agent: Agent, model: str, mark_name: str) -> str: ...

    def render_skill(self, skill: Skill, mark_name: str) -> str: ...
