from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.errors import SourceError
from shuttle.manifest import AgentSpec
from shuttle.model import Tier, Tool
from shuttle.parser import parse_agent, parse_skill

from .conftest import AGENT, SKILL

SPEC = AgentSpec(tools=(Tool.SHELL, Tool.READ), tier=Tier.SMALL)


def write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_agent(tmp_path: Path) -> None:
    agent = parse_agent(write(tmp_path, "run.md", AGENT), SPEC)
    assert agent.name == "run"
    assert agent.description == "Runs a command."
    assert agent.tier is Tier.SMALL
    assert agent.tools == (Tool.SHELL, Tool.READ)
    assert agent.body == AGENT.strip()


def test_description_is_the_first_paragraph_on_one_line(tmp_path: Path) -> None:
    text = "# Title\n\nFirst line\nsecond line.\n\nOther paragraph.\n"
    agent = parse_agent(write(tmp_path, "run.md", text), SPEC)
    assert agent.description == "First line second line."


@pytest.mark.parametrize("text", ["+++\nname = 'run'\n+++\nbody\n", "---\nname: run\n---\nbody\n"])
def test_frontmatter_is_rejected(tmp_path: Path, text: str) -> None:
    with pytest.raises(SourceError, match="must not contain frontmatter"):
        parse_agent(write(tmp_path, "run.md", text), SPEC)


@pytest.mark.parametrize(
    ("name", "text", "message"),
    [
        ("run.md", "", "file is empty"),
        ("run.md", "   \n\n", "file is empty"),
        ("run.md", "# Only a heading\n", "no description paragraph"),
        ("Run_It.md", AGENT, "invalid name"),
    ],
)
def test_invalid_agent(tmp_path: Path, name: str, text: str, message: str) -> None:
    with pytest.raises(SourceError, match=message):
        parse_agent(write(tmp_path, name, text), SPEC)


def test_valid_skill(tmp_path: Path) -> None:
    folder = tmp_path / "atomic-tasks"
    folder.mkdir()
    skill = parse_skill(write(folder, "SKILL.md", SKILL))
    assert skill.name == "atomic-tasks"
    assert skill.description == "When to delegate."
    assert "# When to delegate" in skill.body


def test_skill_rejects_frontmatter(tmp_path: Path) -> None:
    folder = tmp_path / "atomic-tasks"
    folder.mkdir()
    with pytest.raises(SourceError, match="frontmatter"):
        parse_skill(write(folder, "SKILL.md", "---\nname: x\n---\nbody\n"))


def test_common_rules_are_appended_to_the_prompt_not_the_description(tmp_path: Path) -> None:
    agent = parse_agent(write(tmp_path, "run.md", AGENT), SPEC, common="Rules for every agent.")
    assert agent.description == "Runs a command."
    assert agent.body == AGENT.strip() + "\n\nRules for every agent."


def test_skill_references(tmp_path: Path) -> None:
    folder = tmp_path / "atomic-tasks"
    folder.mkdir()
    write(folder, "examples-run.md", "# Run examples\n\nOne.\n")
    write(folder, "examples-find.md", "# Find examples\n")
    skill = parse_skill(write(folder, "SKILL.md", SKILL))
    assert [reference.filename for reference in skill.references] == [
        "examples-find.md",
        "examples-run.md",
    ]
    assert skill.references[1].body.startswith("# Run examples")


@pytest.mark.parametrize(
    ("filename", "text", "message"),
    [
        ("Bad_Name.md", "# x\n", "invalid file name"),
        ("examples.md", "---\nname: x\n---\nbody\n", "must not contain frontmatter"),
        ("examples.md", "", "file is empty"),
    ],
)
def test_invalid_reference(tmp_path: Path, filename: str, text: str, message: str) -> None:
    folder = tmp_path / "atomic-tasks"
    folder.mkdir()
    write(folder, filename, text)
    with pytest.raises(SourceError, match=message):
        parse_skill(write(folder, "SKILL.md", SKILL))
