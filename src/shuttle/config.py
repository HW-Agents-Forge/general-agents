"""Read `models.toml` and resolve the model of each agent for a tool."""

from __future__ import annotations

import re
import tomllib
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ConfigError, UsageError
from .model import Tier

CONFIG_FILE = "models.toml"
MARK_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MODEL_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/# ()+-]*$")


@dataclass(frozen=True)
class Config:
    name: str
    defaults: Mapping[str, str]
    tools: Mapping[str, Mapping[str, str]]


def check_model(model: str, origin: str) -> str:
    """Only the form of a model identifier can be checked, not its existence."""
    if not MODEL_PATTERN.match(model) or model != model.strip():
        raise ConfigError(f"{origin}: invalid model identifier {model!r}")
    return model


def _table(value: Any, origin: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ConfigError(f"{origin}: must be a table")
    result: dict[str, str] = {}
    for key, model in value.items():
        if not isinstance(model, str):
            raise ConfigError(f"{origin}.{key}: must be a string")
        result[key] = check_model(model, f"{origin}.{key}")
    return result


def load_config(path: Path, known_targets: Collection[str]) -> Config:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ConfigError(f"{path}: file not found") from None
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"{path}: invalid TOML: {error}") from error

    name = data.pop("name", None)
    if not isinstance(name, str) or not MARK_NAME_PATTERN.match(name):
        raise ConfigError(f"{path}: 'name' is required (letters, digits, '.', '_', '-')")

    defaults = _table(data.pop("defaults", None), f"{path} [defaults]")
    unknown_tiers = sorted(set(defaults) - {tier.value for tier in Tier})
    if unknown_tiers:
        raise ConfigError(f"{path}: unknown tier(s) in [defaults]: {', '.join(unknown_tiers)}")

    tools: dict[str, dict[str, str]] = {}
    for section, table in data.items():
        if section not in known_targets:
            allowed = ", ".join(sorted(known_targets))
            raise ConfigError(f"{path}: unknown section [{section}] (known tools: {allowed})")
        tools[section] = _table(table, f"{path} [{section}]")
    return Config(name=name, defaults=defaults, tools=tools)


def check_agents(config: Config, agent_names: Collection[str]) -> None:
    """Every agent named in a tool section must exist in the catalog."""
    for tool, table in config.tools.items():
        unknown = sorted(set(table) - set(agent_names))
        if unknown:
            names = ", ".join(unknown)
            raise ConfigError(f"[{tool}] in models.toml names unknown agent(s): {names}")


def parse_overrides(options: list[str], agent_names: Collection[str]) -> dict[str, str]:
    """Parse repeated `--model AGENT=MODEL` options."""
    overrides: dict[str, str] = {}
    for option in options:
        agent, separator, model = option.partition("=")
        if not separator or not agent or not model:
            raise UsageError(f"--model expects AGENT=MODEL, got {option!r}")
        if agent not in agent_names:
            raise UsageError(f"--model names an unknown agent: {agent!r}")
        if agent in overrides:
            raise UsageError(f"--model given twice for agent {agent!r}")
        try:
            overrides[agent] = check_model(model, f"--model {agent}")
        except ConfigError as error:
            raise UsageError(str(error)) from error
    return overrides


def resolve_model(
    config: Config, target: str, agent: str, tier: Tier, overrides: Mapping[str, str]
) -> str:
    """`--model` first, then the tool section, then `[defaults]` for the agent's tier."""
    if agent in overrides:
        return overrides[agent]
    section = config.tools.get(target, {})
    if agent in section:
        return section[agent]
    if tier.value in config.defaults:
        return config.defaults[tier.value]
    raise ConfigError(
        f"no model for agent '{agent}' on '{target}': set it with --model {agent}=MODEL, "
        f"in [{target}] or via [defaults] {tier.value} in models.toml"
    )
