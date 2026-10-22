"""Discover the agents and skills of a repository."""

from __future__ import annotations

from pathlib import Path

from .errors import SourceError
from .manifest import MANIFEST_FILE, load_manifest
from .model import Agent, Catalog, Skill
from .parser import parse_agent, parse_common, parse_skill

AGENTS_DIR = "agents"
SKILLS_DIR = "skills"
SKILL_FILE = "SKILL.md"
COMMON_FILE = "_common.md"


def _discover_agents(root: Path) -> tuple[Agent, ...]:
    agents_dir = root / AGENTS_DIR
    if not agents_dir.is_dir():
        raise SourceError(f"{agents_dir}: the agents directory does not exist")
    specs = load_manifest(root / MANIFEST_FILE)
    common_file = agents_dir / COMMON_FILE
    common = parse_common(common_file) if common_file.is_file() else ""
    paths = sorted(path for path in agents_dir.glob("*.md") if path != common_file)
    missing = sorted(path.stem for path in paths if path.stem not in specs)
    if missing:
        raise SourceError(f"{MANIFEST_FILE}: no entry for agent(s): {', '.join(missing)}")
    orphans = sorted(set(specs) - {path.stem for path in paths})
    if orphans:
        raise SourceError(f"{MANIFEST_FILE}: entry without an agent file: {', '.join(orphans)}")
    return tuple(parse_agent(path, specs[path.stem], common) for path in paths)


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
