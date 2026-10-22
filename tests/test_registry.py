from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.errors import SourceError
from shuttle.registry import discover

from .conftest import AGENT


def test_discover(repo: Path) -> None:
    (repo / "agents" / "find.md").write_text(AGENT, encoding="utf-8")
    (repo / "agents.toml").write_text(
        '[run]\ntools = ["shell"]\n[find]\ntools = ["search"]\n', encoding="utf-8"
    )
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


def test_agent_without_manifest_entry(repo: Path) -> None:
    (repo / "agents" / "find.md").write_text(AGENT, encoding="utf-8")
    with pytest.raises(SourceError, match="no entry for agent.*find"):
        discover(repo)


def test_manifest_entry_without_agent_file(repo: Path) -> None:
    (repo / "agents.toml").write_text(
        '[run]\ntools = ["shell"]\n[ghost]\ntools = ["shell"]\n', encoding="utf-8"
    )
    with pytest.raises(SourceError, match="entry without an agent file.*ghost"):
        discover(repo)


def test_skill_folder_without_skill_file(repo: Path) -> None:
    (repo / "skills" / "empty").mkdir()
    with pytest.raises(SourceError, match="missing SKILL.md"):
        discover(repo)


def test_real_repository_sources_are_valid() -> None:
    """Every real agent and skill must parse, and models.toml must match the catalog."""
    from shuttle.config import check_agents, load_config
    from shuttle.targets import TARGETS

    root = Path(__file__).resolve().parent.parent
    catalog = discover(root)
    assert catalog.agents, "the repository has no agent"
    check_agents(load_config(root / "models.toml", TARGETS), catalog.agent_names())


def test_run_prompt_is_not_tied_to_one_shell() -> None:
    """`run` must cover every supported shell, not only the one used where it was written."""
    prompt = (Path(__file__).resolve().parent.parent / "agents" / "run.md").read_text()
    for shell in ("csh", "bash", "zsh", "fish", "PowerShell", "cmd"):
        assert shell in prompt, shell
    for status_variable in ("$status", "$?", "$LASTEXITCODE", "%ERRORLEVEL%"):
        assert status_variable in prompt, status_variable


def test_common_file_is_not_an_agent_and_is_appended(repo: Path) -> None:
    (repo / "agents" / "_common.md").write_text("Shared rule.\n", encoding="utf-8")
    catalog = discover(repo)
    assert catalog.agent_names() == {"run"}
    assert catalog.agents[0].body.endswith("\n\nShared rule.")
    assert catalog.agents[0].description == "Runs a command."


def test_skill_references_are_discovered(repo: Path) -> None:
    (repo / "skills" / "atomic-tasks" / "examples-run.md").write_text(
        "# Examples\n", encoding="utf-8"
    )
    (skill,) = discover(repo).skills
    assert [reference.filename for reference in skill.references] == ["examples-run.md"]
