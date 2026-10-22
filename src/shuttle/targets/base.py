"""The interface every target tool implements."""

from __future__ import annotations

from pathlib import PurePath
from typing import Protocol

from ..mark import MARK_KEY
from ..model import Agent, Reference, Scope, Skill


class Target(Protocol):
    """Tool-specific paths and rendering. Targets never write to disk."""

    name: str

    def agent_path(self, agent: Agent, scope: Scope = Scope.USER) -> PurePath:
        """Install location of an agent, relative to the home (user) or the project root."""
        ...

    def skill_path(self, skill: Skill, scope: Scope = Scope.USER) -> PurePath:
        """Install location of a skill, relative to the home (user) or the project root."""
        ...

    def render_agent(self, agent: Agent, model: str, mark_name: str) -> str: ...

    def render_skill(self, skill: Skill, mark_name: str) -> str: ...


def reference_path(
    target: Target, skill: Skill, reference: Reference, scope: Scope = Scope.USER
) -> PurePath:
    """A reference file sits next to the skill's SKILL.md, whatever the tool."""
    return target.skill_path(skill, scope).parent / reference.filename


def render_reference(reference: Reference, mark_name: str) -> str:
    """References are plain Markdown for every tool; only the origin mark is added."""
    return f"<!-- {MARK_KEY}: {mark_name} -->\n\n{reference.body}\n"
