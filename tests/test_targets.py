from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.errors import UsageError
from shuttle.manifest import load_manifest
from shuttle.mark import read_mark
from shuttle.parser import parse_agent, parse_skill
from shuttle.targets import TARGETS, get_target

GOLDEN = Path(__file__).parent / "golden"


@pytest.mark.parametrize("name", sorted(TARGETS))
def test_target_rendering_matches_golden_and_carries_the_mark(name: str, repo: Path) -> None:
    target = get_target(name)
    agent = parse_agent(repo / "agents" / "run.md", load_manifest(repo / "agents.toml")["run"])
    skill = parse_skill(repo / "skills" / "atomic-tasks" / "SKILL.md")

    rendered_agent = target.render_agent(agent, "tiny-model", "test-repo")
    rendered_skill = target.render_skill(skill, "test-repo")

    assert read_mark(rendered_agent) == "test-repo"
    assert read_mark(rendered_skill) == "test-repo"
    assert (GOLDEN / name / "run.agent.md").read_text() == rendered_agent
    assert (GOLDEN / name / "atomic-tasks.SKILL.md").read_text() == rendered_skill
    assert target.render_agent(agent, "tiny-model", "test-repo") == rendered_agent
    assert not target.agent_path(agent).is_absolute()
    assert not target.skill_path(skill).is_absolute()


def test_unknown_target() -> None:
    with pytest.raises(UsageError, match="unknown target"):
        get_target("nope")


@pytest.mark.parametrize("name", sorted(TARGETS))
def test_reference_files_sit_next_to_the_skill_and_carry_the_mark(name: str) -> None:
    from shuttle.model import Reference, Skill
    from shuttle.targets.base import reference_path, render_reference

    target = get_target(name)
    skill = Skill(name="atomic-tasks", description="d", body="b")
    reference = Reference(filename="examples-run.md", body="# Examples\n\nOne.")
    assert reference_path(target, skill, reference).parent == target.skill_path(skill).parent
    rendered = render_reference(reference, "test-repo")
    assert read_mark(rendered) == "test-repo"
    assert rendered == "<!-- managed-by: test-repo -->\n\n# Examples\n\nOne.\n"


def test_project_scope_paths() -> None:
    from shuttle.model import Agent as AgentModel
    from shuttle.model import Scope, Skill, Tier, Tool

    agent = AgentModel("run", "d", Tier.SMALL, (Tool.SHELL,), "b")
    skill = Skill(name="atomic-tasks", description="d", body="b")
    claude, copilot = get_target("claude-code"), get_target("copilot-cli")
    # Claude Code: `.claude/` at user level and in a project
    assert claude.agent_path(agent, Scope.PROJECT) == claude.agent_path(agent, Scope.USER)
    assert str(claude.agent_path(agent, Scope.PROJECT)) == ".claude/agents/run.md"
    # Copilot CLI: `.copilot/` for the user, `.github/` in a project
    assert str(copilot.agent_path(agent, Scope.USER)) == ".copilot/agents/run.agent.md"
    assert str(copilot.agent_path(agent, Scope.PROJECT)) == ".github/agents/run.agent.md"
    assert str(copilot.skill_path(skill, Scope.USER)) == ".copilot/skills/atomic-tasks/SKILL.md"
    assert str(copilot.skill_path(skill, Scope.PROJECT)) == ".github/skills/atomic-tasks/SKILL.md"
