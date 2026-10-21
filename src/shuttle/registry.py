"""Discover the agents and skills of a repository."""

from __future__ import annotations

from pathlib import Path

from .errors import SourceError
from .model import Agent, Catalog, Skill
from .parser import parse_agent, parse_skill

AGENTS_DIR = "agents"
SKILLS_DIR = "skills"
SKILL_FILE = "SKILL.md"


def _discover_agents(root: Path) -> tuple[Agent, ...]:
    agents_dir = root / AGENTS_DIR
    if not agents_dir.is_dir():
        raise SourceError(f"{agents_dir}: the agents directory does not exist")
    return tuple(parse_agent(path) for path in sorted(agents_dir.glob("*.md")))


def _discover_skills(root: Path) -> tuple[Skill, ...]:
    skills_dir = root / SKILLS_DIR
    if not skills_dir.is_dir():
        return ()
    skills: list[Skill] = []
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        skill_file = skill_dir / SKILL_FILE
        if not skill_file.is_file():
            raise SourceError(f"{skill_dir}: missing {SKILL_FILE}")
        skills.append(parse_skill(skill_file))
    return tuple(skills)


def discover(root: Path) -> Catalog:
    """Parse every agent and skill under `root`, in a deterministic (sorted) order."""
    return Catalog(agents=_discover_agents(root), skills=_discover_skills(root))
