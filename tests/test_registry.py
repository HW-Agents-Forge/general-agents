from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.errors import SourceError
from shuttle.registry import discover

from .conftest import AGENT


def test_discover(repo: Path) -> None:
    (repo / "agents" / "find.md").write_text(AGENT.replace('"run"', '"find"'), encoding="utf-8")
    catalog = discover(repo)
    assert [agent.name for agent in catalog.agents] == ["find", "run"]
    assert [skill.name for skill in catalog.skills] == ["atomic-tasks"]
    assert catalog.agent_names() == {"find", "run"}


def test_skills_are_optional(repo: Path) -> None:
    (repo / "skills" / "atomic-tasks" / "SKILL.md").unlink()
    (repo / "skills" / "atomic-tasks").rmdir()
    (repo / "skills").rmdir()
    assert discover(repo).skills == ()


def test_missing_agents_directory(tmp_path: Path) -> None:
    with pytest.raises(SourceError, match="agents directory"):
        discover(tmp_path)


def test_skill_folder_without_skill_file(repo: Path) -> None:
    (repo / "skills" / "empty").mkdir()
    with pytest.raises(SourceError, match="missing SKILL.md"):
        discover(repo)
