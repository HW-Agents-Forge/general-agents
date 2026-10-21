from __future__ import annotations

import os
from pathlib import Path, PurePath

import pytest

from shuttle.errors import UsageError
from shuttle.installer import Action, PlannedFile, install, plan

MARKED = "---\nmetadata:\n  managed-by: me\n---\nold\n"


def planned(content: str = "new\n", relative: str = "a/b.md") -> PlannedFile:
    return PlannedFile(PurePath(relative), content)


def test_create_then_idempotent(home: Path) -> None:
    files = [planned("<!-- managed-by: me -->\n")]
    assert [o.action for o in install(home, files, "me")] == [Action.CREATE]
    assert (home / "a" / "b.md").read_text() == "<!-- managed-by: me -->\n"
    assert [o.action for o in install(home, files, "me")] == [Action.UNCHANGED]


def test_update_marked_file(home: Path) -> None:
    target = home / "a" / "b.md"
    target.parent.mkdir()
    target.write_text(MARKED)
    outcome = install(home, [planned("---\nmetadata:\n  managed-by: me\n---\nnew\n")], "me")[0]
    assert outcome.action is Action.UPDATE
    assert target.read_text().endswith("new\n")


def test_never_overwrites_unmarked_file(home: Path) -> None:
    target = home / "a" / "b.md"
    target.parent.mkdir()
    target.write_text("personal\n")
    outcome = install(home, [planned()], "me")[0]
    assert outcome.action is Action.REFUSED
    assert "without a mark" in outcome.reason
    assert target.read_text() == "personal\n"


def test_never_overwrites_file_marked_by_another_repository(home: Path) -> None:
    target = home / "a" / "b.md"
    target.parent.mkdir()
    target.write_text(MARKED)
    outcome = install(home, [planned()], "someone-else")[0]
    assert outcome.action is Action.REFUSED
    assert "marked by 'me'" in outcome.reason
    assert target.read_text() == MARKED


def test_never_deletes(home: Path) -> None:
    stale = home / "a" / "old.md"
    stale.parent.mkdir()
    stale.write_text(MARKED)
    install(home, [planned("<!-- managed-by: me -->\n")], "me")
    assert stale.read_text() == MARKED


def test_dry_run_writes_nothing_and_matches_real_run(home: Path) -> None:
    existing = home / "a" / "keep.md"
    existing.parent.mkdir()
    existing.write_text("personal\n")
    files = [
        planned("<!-- managed-by: me -->\n"),
        planned("x\n", "a/keep.md"),
    ]
    dry = install(home, files, "me", dry_run=True)
    assert not (home / "a" / "b.md").exists()
    assert dry == plan(home, files, "me")
    assert install(home, files, "me") == dry


@pytest.mark.parametrize("relative", ["../escape.md", "/etc/escape.md", "a/../../escape.md"])
def test_rejects_paths_outside_home(home: Path, relative: str) -> None:
    outcome = install(home, [planned(relative=relative)], "me")[0]
    assert outcome.action is Action.REFUSED
    assert not (home.parent / "escape.md").exists()


def test_rejects_symlink_escaping_home(home: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(outside, home / "link")
    outcome = install(home, [planned(relative="link/b.md")], "me")[0]
    assert outcome.action is Action.REFUSED
    assert not (outside / "b.md").exists()


def test_refuses_directory_destination(home: Path) -> None:
    (home / "a" / "b.md").mkdir(parents=True)
    assert install(home, [planned()], "me")[0].action is Action.REFUSED


def test_atomic_write_leaves_no_partial_file(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*_: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(os, "replace", fail)
    with pytest.raises(OSError, match="disk full"):
        install(home, [planned("<!-- managed-by: me -->\n")], "me")
    assert list((home / "a").iterdir()) == []


def test_missing_home(tmp_path: Path) -> None:
    with pytest.raises(UsageError, match="does not exist"):
        install(tmp_path / "nope", [planned()], "me")
