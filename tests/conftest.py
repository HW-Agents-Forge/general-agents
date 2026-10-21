from __future__ import annotations

from pathlib import Path

import pytest

AGENT = """\
Runs a command.

Run the command and report.
"""

SKILL = """\
When to delegate.

# When to delegate

Delegate large outputs.
"""

MODELS = """\
name = "test-repo"

[defaults]
small = "tiny-model"
"""

MANIFEST = """\
[run]
tools = ["shell", "read"]
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A minimal valid content repository."""
    root = tmp_path / "repo"
    (root / "agents").mkdir(parents=True)
    (root / "skills" / "atomic-tasks").mkdir(parents=True)
    (root / "agents" / "run.md").write_text(AGENT, encoding="utf-8")
    (root / "skills" / "atomic-tasks" / "SKILL.md").write_text(SKILL, encoding="utf-8")
    (root / "models.toml").write_text(MODELS, encoding="utf-8")
    (root / "agents.toml").write_text(MANIFEST, encoding="utf-8")
    return root


@pytest.fixture
def home(tmp_path: Path) -> Path:
    path = tmp_path / "home"
    path.mkdir()
    return path
