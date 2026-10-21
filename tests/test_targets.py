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
