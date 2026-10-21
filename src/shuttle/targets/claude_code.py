"""Claude Code target.

Sub-agents are Markdown files with YAML frontmatter in `~/.claude/agents/`; skills are
`~/.claude/skills/<name>/SKILL.md`. Claude Code ignores frontmatter fields it does not know,
so the origin mark is a plain `managed-by` key in the agent frontmatter.
"""

from __future__ import annotations

import json
from pathlib import PurePath

from ..mark import MARK_KEY
from ..model import Agent, Skill, Tool

TOOL_NAMES: dict[Tool, tuple[str, ...]] = {
    Tool.READ: ("Read",),
    Tool.SEARCH: ("Grep", "Glob"),
    Tool.SHELL: ("Bash",),
}


def _quote(value: str) -> str:
    """A JSON string is a valid YAML double-quoted scalar."""
    return json.dumps(value, ensure_ascii=False)


class ClaudeCodeTarget:
    name = "claude-code"

    def agent_path(self, agent: Agent) -> PurePath:
        return PurePath(".claude", "agents", f"{agent.name}.md")

    def skill_path(self, skill: Skill) -> PurePath:
        return PurePath(".claude", "skills", skill.name, "SKILL.md")

    def render_agent(self, agent: Agent, model: str, mark_name: str) -> str:
        tools = ", ".join(name for tool in agent.tools for name in TOOL_NAMES[tool])
        return (
            "---\n"
            f"name: {agent.name}\n"
            f"description: {_quote(agent.description)}\n"
            f"tools: {tools}\n"
            f"model: {_quote(model)}\n"
            f"{MARK_KEY}: {mark_name}\n"
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
