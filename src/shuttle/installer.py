"""The only module that writes to disk.

Rules (docs/install-spec.md): never overwrite a file without our mark, never delete anything,
write only under the home, atomically, and make the dry-run decide exactly like the real run.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePath

from .errors import UsageError
from .mark import read_mark


class Action(StrEnum):
    CREATE = "created"
    UPDATE = "updated"
    UNCHANGED = "unchanged"
    REFUSED = "refused"


@dataclass(frozen=True)
class PlannedFile:
    relative: PurePath
    content: str


@dataclass(frozen=True)
class Outcome:
    path: Path
    action: Action
    reason: str = ""


@dataclass(frozen=True)
class _Decision:
    outcome: Outcome
    content: str


def _destination(home: Path, relative: PurePath) -> Path | None:
    """Resolve the destination; None if it would escape the home (even via a symlink)."""
    if relative.is_absolute() or ".." in relative.parts:
        return None
    destination = (home / relative).resolve()
    return destination if destination.is_relative_to(home) else None


def _decide(home: Path, planned: PlannedFile, mark_name: str) -> _Decision:
    destination = _destination(home, planned.relative)
    if destination is None:
        refused = Outcome(home / planned.relative, Action.REFUSED, "path escapes the home")
        return _Decision(refused, planned.content)
    if not destination.exists():
        return _Decision(Outcome(destination, Action.CREATE), planned.content)
    if not destination.is_file():
        refused = Outcome(destination, Action.REFUSED, "destination is not a regular file")
        return _Decision(refused, planned.content)
    existing = destination.read_text(encoding="utf-8", errors="replace")
    found = read_mark(existing)
    if found != mark_name:
        reason = "exists without a mark" if found is None else f"marked by '{found}'"
        return _Decision(Outcome(destination, Action.REFUSED, reason), planned.content)
    if existing == planned.content:
        return _Decision(Outcome(destination, Action.UNCHANGED), planned.content)
    return _Decision(Outcome(destination, Action.UPDATE), planned.content)


def _write_atomically(destination: Path, content: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=destination.parent, prefix=".shuttle-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(content)
        os.replace(temporary, destination)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def plan(home: Path, files: list[PlannedFile], mark_name: str) -> list[Outcome]:
    """What `install` would do. No side effects."""
    return [_decide(home.resolve(), planned, mark_name).outcome for planned in files]


def install(
    home: Path, files: list[PlannedFile], mark_name: str, *, dry_run: bool = False
) -> list[Outcome]:
    """Apply the plan (or only report it with `dry_run`). Refused files are skipped."""
    if not home.is_dir():
        raise UsageError(f"{home}: the destination directory does not exist")
    root = home.resolve()
    decisions = [_decide(root, planned, mark_name) for planned in files]
    if not dry_run:
        for decision in decisions:
            if decision.outcome.action in (Action.CREATE, Action.UPDATE):
                _write_atomically(decision.outcome.path, decision.content)
    return [decision.outcome for decision in decisions]
