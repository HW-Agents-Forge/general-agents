from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.errors import SourceError
from shuttle.manifest import load_manifest
from shuttle.model import Tier, Tool


def manifest(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "agents.toml"
    path.write_text(text, encoding="utf-8")
    return path


def test_load(tmp_path: Path) -> None:
    specs = load_manifest(manifest(tmp_path, '[run]\ntools = ["shell", "read"]\n'))
    assert specs["run"].tools == (Tool.SHELL, Tool.READ)
    assert specs["run"].tier is Tier.SMALL


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("[run]\n", "'tools' is required"),
        ("[run]\ntools = []\n", "non-empty list"),
        ('[run]\ntools = ["write"]\n', "unknown tool"),
        ('[run]\ntools = ["shell", "shell"]\n', "duplicate tool"),
        ('[run]\ntools = ["shell"]\ntier = "medium"\n', "'tier' must be one of"),
        ('[run]\ntools = ["shell"]\nmodel = "x"\n', "unknown key"),
        ("run = 3\n", "must be a table"),
        ("[run\n", "invalid TOML"),
    ],
)
def test_invalid(tmp_path: Path, text: str, message: str) -> None:
    with pytest.raises(SourceError, match=message):
        load_manifest(manifest(tmp_path, text))


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(SourceError, match="file not found"):
        load_manifest(tmp_path / "agents.toml")
