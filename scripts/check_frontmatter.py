#!/usr/bin/env python3
"""Check the frontmatter of every agent and skill, per tool. Read-only; needs PyYAML.

That the prompts match across tools is checked by check_prompts_sync.py."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ("claude-code", "vs-code", "copilot-cli")

# Per tool: agent file suffix, allowed tool names, how `tools` is written, accepted models.
AGENT_RULES = {
    "claude-code": {
        "suffix": ".md",
        "tools": {"Read", "Grep", "Glob", "Bash"},
        "tools_type": "csv",
        "models": {"haiku"},
    },
    "vs-code": {
        "suffix": ".agent.md",
        "tools": {"read", "search", "execute"},
        "tools_type": "list",
        "models": None,
    },
    "copilot-cli": {
        "suffix": ".agent.md",
        "tools": {"read", "search", "execute"},
        "tools_type": "list",
        "models": None,
    },
}
AGENT_KEYS = {"name", "description", "tools", "model"}
SKILL_KEYS = {"name", "description"}
errors: list[str] = []


def err(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def split(path: Path) -> tuple[dict, str] | None:
    """Return (frontmatter, body), or None after recording an error."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        err(path, "must start with a '---' frontmatter line")
        return None
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        err(path, "frontmatter is not closed by a '---' line")
        return None
    try:
        data = yaml.safe_load(head)
    except yaml.YAMLError as exc:
        err(path, f"invalid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        err(path, "frontmatter must be a mapping")
        return None
    return data, body


def check_common(path: Path, data: dict, allowed: set[str], name: str) -> None:
    for key in sorted(set(data) - allowed):
        err(path, f"unknown key '{key}'")
    for key in sorted(allowed - set(data)):
        err(path, f"missing key '{key}'")
    if data.get("name") != name:
        err(path, f"name must be '{name}', got {data.get('name')!r}")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        err(path, "description must be a non-empty string")
    elif len(description) > 1024:
        err(path, "description is longer than 1024 characters")


def check_agent(tool: str, path: Path) -> tuple[dict, str] | None:
    rules = AGENT_RULES[tool]
    name = path.name.removesuffix(rules["suffix"])
    parsed = split(path)
    if parsed is None:
        return None
    data, body = parsed
    check_common(path, data, AGENT_KEYS, name)
    tools = data.get("tools")
    if rules["tools_type"] == "csv":
        names = [t.strip() for t in tools.split(",")] if isinstance(tools, str) else None
    else:
        ok = isinstance(tools, list) and all(isinstance(t, str) for t in tools)
        names = tools if ok else None
    if not names:
        kind = "comma-separated string" if rules["tools_type"] == "csv" else "list of strings"
        err(path, f"tools must be a non-empty {kind}")
    else:
        for t in names:
            if t not in rules["tools"]:
                err(path, f"unknown tool '{t}' (allowed: {', '.join(sorted(rules['tools']))})")
    model = data.get("model")
    if not isinstance(model, str) or not model.strip():
        err(path, "model must be a non-empty string")
    elif rules["models"] and model not in rules["models"]:
        err(path, f"model must be one of {sorted(rules['models'])}, got {model!r}")
    if not body.strip():
        err(path, "empty prompt")
    return data, body


def check_skill(path: Path) -> tuple[dict, str] | None:
    parsed = split(path)
    if parsed is not None:
        check_common(path, parsed[0], SKILL_KEYS, path.parent.name)
    return parsed


def main() -> int:
    agents: dict[str, dict[str, tuple[dict, str]]] = {}
    skills: dict[str, dict[str, tuple[dict, str]]] = {}
    for tool in TOOLS:
        suffix = AGENT_RULES[tool]["suffix"]
        adir, sdir = ROOT / "agents" / tool, ROOT / "skills" / tool
        if not adir.is_dir() or not sdir.is_dir():
            errors.append(f"agents/{tool} or skills/{tool}: folder is missing")
            continue
        for path in sorted(adir.glob("*.md")):
            if not path.name.endswith(suffix):
                err(path, f"agent file name must end with '{suffix}'")
            elif (parsed := check_agent(tool, path)) is not None:
                agents.setdefault(tool, {})[path.name.removesuffix(suffix)] = parsed
        for path in sorted(sdir.glob("*/SKILL.md")):
            if (parsed := check_skill(path)) is not None:
                skills.setdefault(tool, {})[path.parent.name] = parsed
        for stray in sorted(p for p in sdir.iterdir() if p.is_dir() and not (p / "SKILL.md").exists()):
            err(stray, "skill folder has no SKILL.md")

    for message in errors:
        print(f"error: {message}", file=sys.stderr)
    if not errors:
        n_agents = sum(len(v) for v in agents.values())
        n_skills = sum(len(v) for v in skills.values())
        print(f"frontmatter OK ({n_agents} agent files, {n_skills} skill files)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
