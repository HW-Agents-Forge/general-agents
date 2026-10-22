"""Read agent and skill sources: plain Markdown, no frontmatter.

The name comes from the file (or folder) name and the description from the first paragraph.
Frontmatter is added by the targets when they render a file.
"""

from __future__ import annotations

from pathlib import Path

from .errors import SourceError
from .manifest import AgentSpec
from .model import NAME_PATTERN, REFERENCE_PATTERN, Agent, Reference, Skill

FRONTMATTER_MARKERS = ("---", "+++")


def _read(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise SourceError(f"{path}: the file is empty")
    if text.splitlines()[0].strip() in FRONTMATTER_MARKERS:
        raise SourceError(f"{path}: sources must not contain frontmatter")
    return text


def _name(name: str, path: Path) -> str:
    if not NAME_PATTERN.match(name):
        raise SourceError(f"{path}: invalid name '{name}' (lowercase letters, digits, hyphens)")
    return name


def _description(text: str, path: Path) -> str:
    """The first paragraph that is not a heading, on a single line."""
    for block in text.split("\n\n"):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines and not lines[0].startswith("#"):
            return " ".join(lines)
    raise SourceError(f"{path}: no description paragraph (the first paragraph is the description)")


def parse_agent(path: Path, spec: AgentSpec) -> Agent:
    text = _read(path)
    return Agent(
        name=_name(path.stem, path),
        description=_description(text, path),
        tier=spec.tier,
        tools=spec.tools,
        body=text,
    )


def parse_references(skill_file: Path) -> tuple[Reference, ...]:
    """Every other Markdown file next to SKILL.md, in sorted order."""
    references: list[Reference] = []
    for path in sorted(skill_file.parent.glob("*.md")):
        if path.name == skill_file.name:
            continue
        if not REFERENCE_PATTERN.match(path.name):
            raise SourceError(f"{path}: invalid file name (lowercase letters, digits, hyphens)")
        references.append(Reference(filename=path.name, body=_read(path)))
    return tuple(references)


def parse_skill(path: Path) -> Skill:
    text = _read(path)
    return Skill(
        name=_name(path.parent.name, path),
        description=_description(text, path),
        body=text,
        references=parse_references(path),
    )
