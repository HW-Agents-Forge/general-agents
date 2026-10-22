#!/usr/bin/env python3
"""Check that every agent and skill has the same prompt in all tool folders.

The frontmatter may differ between tools; the body (everything after the frontmatter) must
not. Also checks that the same agents and skills exist for every tool. Read-only, stdlib only.
"""

from __future__ import annotations

import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ("claude-code", "vs-code", "copilot-cli", "opencode")
REFERENCE = TOOLS[0]


def body(path: Path) -> str:
    """The text after the closing '---' of the frontmatter."""
    text = path.read_text(encoding="utf-8")
    _, sep, rest = text[4:].partition("\n---\n") if text.startswith("---\n") else ("", "", text)
    return rest if sep else text


def collect(kind: str, tool: str) -> dict[str, Path]:
    """Map an agent or skill name to its file for one tool."""
    base = ROOT / kind / tool
    if kind == "agents":
        return {p.name.removesuffix(".agent.md").removesuffix(".md"): p for p in sorted(base.glob("*.md"))}
    return {p.parent.name: p for p in sorted(base.glob("*/SKILL.md"))}


def main() -> int:
    errors: list[str] = []
    for kind in ("agents", "skills"):
        files = {tool: collect(kind, tool) for tool in TOOLS}
        names = sorted(set().union(*files.values()))
        for name in names:
            present = [tool for tool in TOOLS if name in files[tool]]
            if len(present) != len(TOOLS):
                missing = ", ".join(t for t in TOOLS if t not in present)
                errors.append(f"{kind}/{name}: missing for {missing}")
                continue
            ref = files[REFERENCE][name]
            for tool in TOOLS[1:]:
                other = files[tool][name]
                if body(ref) != body(other):
                    diff = difflib.unified_diff(
                        body(ref).splitlines(),
                        body(other).splitlines(),
                        str(ref.relative_to(ROOT)),
                        str(other.relative_to(ROOT)),
                        lineterm="",
                        n=1,
                    )
                    errors.append(f"{kind}/{name}: {REFERENCE} and {tool} prompts differ\n" + "\n".join(diff))
    for message in errors:
        print(f"error: {message}", file=sys.stderr)
    if not errors:
        print(f"prompts in sync across {', '.join(TOOLS)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
