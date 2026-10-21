from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.config import Config, check_agents, load_config, parse_overrides, resolve_model
from shuttle.errors import ConfigError, UsageError
from shuttle.model import Tier

TARGETS = ("copilot-cli", "vscode")


def config_file(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "models.toml"
    path.write_text(text, encoding="utf-8")
    return path


GOOD = """\
name = "repo"

[defaults]
small = "tiny"

[copilot-cli]
run = "special"
"""


def test_load(tmp_path: Path) -> None:
    config = load_config(config_file(tmp_path, GOOD), TARGETS)
    assert config.name == "repo"
    assert config.defaults == {"small": "tiny"}
    assert config.tools == {"copilot-cli": {"run": "special"}}


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ('[defaults]\nsmall = "x"\n', "'name' is required"),
        ('name = "a b"\n[defaults]\nsmall = "x"\n', "'name' is required"),
        ('name = "r"\n', "must be a table"),
        ('name = "r"\n[defaults]\nlarge = "x"\n', "unknown tier"),
        ('name = "r"\n[defaults]\nsmall = 3\n', "must be a string"),
        ('name = "r"\n[defaults]\nsmall = "bad;id"\n', "invalid model identifier"),
        ('name = "r"\n[defaults]\nsmall = "x"\n[nope]\n', "unknown section"),
        ("name = ", "invalid TOML"),
    ],
)
def test_invalid(tmp_path: Path, text: str, message: str) -> None:
    with pytest.raises(ConfigError, match=message):
        load_config(config_file(tmp_path, text), TARGETS)


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="file not found"):
        load_config(tmp_path / "models.toml", TARGETS)


def test_vscode_style_model_with_spaces_is_accepted(tmp_path: Path) -> None:
    text = 'name = "r"\n[defaults]\nsmall = "Claude Haiku 5.5 (copilot)"\n'
    assert load_config(config_file(tmp_path, text), TARGETS).defaults["small"].endswith("(copilot)")


def test_check_agents(tmp_path: Path) -> None:
    config = load_config(config_file(tmp_path, GOOD), TARGETS)
    check_agents(config, {"run"})
    with pytest.raises(ConfigError, match="unknown agent"):
        check_agents(config, {"find"})


def make(**tools: dict[str, str]) -> Config:
    return Config(name="r", defaults={"small": "tiny"}, tools=tools)


def test_resolution_order() -> None:
    config = make(**{"copilot-cli": {"run": "section"}})
    assert resolve_model(config, "copilot-cli", "run", Tier.SMALL, {"run": "cli"}) == "cli"
    assert resolve_model(config, "copilot-cli", "run", Tier.SMALL, {}) == "section"
    assert resolve_model(config, "copilot-cli", "find", Tier.SMALL, {}) == "tiny"
    assert resolve_model(config, "vscode", "run", Tier.SMALL, {}) == "tiny"


def test_no_model_found_names_agent_and_tool() -> None:
    config = Config(name="r", defaults={}, tools={})
    with pytest.raises(ConfigError, match="agent 'run' on 'vscode'"):
        resolve_model(config, "vscode", "run", Tier.SMALL, {})


def test_parse_overrides() -> None:
    assert parse_overrides(["run=a", "find=b"], {"run", "find"}) == {"run": "a", "find": "b"}


@pytest.mark.parametrize(
    ("options", "message"),
    [
        (["run"], "AGENT=MODEL"),
        (["=x"], "AGENT=MODEL"),
        (["run="], "AGENT=MODEL"),
        (["nope=x"], "unknown agent"),
        (["run=a", "run=b"], "twice"),
        (["run=bad;id"], "invalid model identifier"),
    ],
)
def test_parse_overrides_errors(options: list[str], message: str) -> None:
    with pytest.raises(UsageError, match=message):
        parse_overrides(options, {"run"})
