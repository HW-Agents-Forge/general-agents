from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.errors import SourceError
from shuttle.model import Tier, Tool
from shuttle.parser import parse_agent, parse_skill

from .conftest import AGENT, SKILL


def write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_agent(tmp_path: Path) -> None:
    agent = parse_agent(write(tmp_path, "run.md", AGENT))
    assert agent.name == "run"
    assert agent.tier is Tier.SMALL
    assert agent.tools == (Tool.SHELL, Tool.READ)
    assert agent.max_output_lines == 40
    assert agent.body == "Run the command and report."


def test_max_output_lines_defaults(tmp_path: Path) -> None:
    text = AGENT.replace("max_output_lines = 40\n", "")
    assert parse_agent(write(tmp_path, "run.md", text)).max_output_lines == 40


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('name = "run"\n', "", "'name' is required"),
        ('name = "run"', 'name = "other"', "must match"),
        ('name = "run"', 'name = "Run_It"', "invalid name"),
        ('description = "Runs a command."\n', "", "'description' is required"),
        ('tier = "small"', 'tier = "medium"', "'tier' must be one of"),
        ('tools = ["shell", "read"]', "tools = []", "non-empty list"),
        ('tools = ["shell", "read"]', 'tools = ["write"]', "unknown tool"),
        ('tools = ["shell", "read"]', 'tools = ["shell", "shell"]', "duplicate tool"),
        ("max_output_lines = 40", "max_output_lines = 0", "positive integer"),
        ("max_output_lines = 40", 'max_output_lines = "40"', "positive integer"),
        ("tier = ", 'model = "x"\ntier = ', "unknown frontmatter key"),
    ],
)
def test_invalid_agent(tmp_path: Path, old: str, new: str, message: str) -> None:
    with pytest.raises(SourceError, match=message):
        parse_agent(write(tmp_path, "run.md", AGENT.replace(old, new)))


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("no frontmatter\n", "must start with"),
        ("+++\nname = 'run'\n", "not closed"),
        ("+++\nname = \n+++\nbody\n", "invalid TOML"),
        (AGENT.split("+++\n\n")[0] + "+++\n", "body is empty"),
    ],
)
def test_invalid_document(tmp_path: Path, text: str, message: str) -> None:
    with pytest.raises(SourceError, match=message):
        parse_agent(write(tmp_path, "run.md", text))


def test_valid_skill(tmp_path: Path) -> None:
    folder = tmp_path / "atomic-tasks"
    folder.mkdir()
    skill = parse_skill(write(folder, "SKILL.md", SKILL))
    assert skill.name == "atomic-tasks"
    assert skill.body.startswith("# When to delegate")


def test_skill_name_must_match_folder(tmp_path: Path) -> None:
    folder = tmp_path / "other"
    folder.mkdir()
    with pytest.raises(SourceError, match="must match"):
        parse_skill(write(folder, "SKILL.md", SKILL))
