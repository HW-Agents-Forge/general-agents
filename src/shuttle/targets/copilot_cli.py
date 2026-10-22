"""Copilot CLI target.

DRAFT: derived from search excerpts of the official documentation, not yet checked against
the full pages or a running CLI. See docs/tool-differences.md for the open points (notably
whether the CLI honors the `model` property).
"""

from __future__ import annotations

import json
from pathlib import PurePath

from ..mark import MARK_KEY
from ..model import Agent, Scope, Skill, Tool

TOOL_NAMES = {
    Tool.READ: "read",
    Tool.SEARCH: "search",
    Tool.SHELL: "execute",
}


def _quote(value: str) -> str:
    """A JSON string is a valid YAML double-quoted scalar."""
    return json.dumps(value, ensure_ascii=False)


class CopilotCliTarget:
    name = "copilot-cli"

    # User level lives in `~/.copilot/`, project level in `<project>/.github/`.
    @staticmethod
    def _base(scope: Scope) -> str:
        return ".copilot" if scope is Scope.USER else ".github"

    def agent_path(self, agent: Agent, scope: Scope = Scope.USER) -> PurePath:
        return PurePath(self._base(scope), "agents", f"{agent.name}.agent.md")

    def skill_path(self, skill: Skill, scope: Scope = Scope.USER) -> PurePath:
        return PurePath(self._base(scope), "skills", skill.name, "SKILL.md")

    def render_agent(self, agent: Agent, model: str, mark_name: str) -> str:
        tools = ", ".join(_quote(TOOL_NAMES[tool]) for tool in agent.tools)
        return (
            "---\n"
            f"name: {agent.name}\n"
            f"description: {_quote(agent.description)}\n"
            f"model: {_quote(model)}\n"
            f"tools: [{tools}]\n"
            "metadata:\n"
            f"  {MARK_KEY}: {mark_name}\n"
            "---\n\n"
            f"{agent.body}\n"
        )

    def render_skill(self, skill: Skill, mark_name: str) -> str:
        return (
            "---\n"
            f"name: {skill.name}\n"
            f"description: {_quote(skill.description)}\n"
            "---\n\n"
            f"<!-- {MARK_KEY}: {mark_name} -->\n\n"
            f"{skill.body}\n"
        )
