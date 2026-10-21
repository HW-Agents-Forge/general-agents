"""Registry of the available targets."""

from __future__ import annotations

from ..errors import UsageError
from .base import Target
from .copilot_cli import CopilotCliTarget

# VS Code and OpenCode targets are added once their formats are verified (docs/targets.md).
TARGETS: dict[str, Target] = {target.name: target for target in (CopilotCliTarget(),)}


def get_target(name: str) -> Target:
    try:
        return TARGETS[name]
    except KeyError:
        raise UsageError(f"unknown target {name!r} (available: {', '.join(TARGETS)})") from None
