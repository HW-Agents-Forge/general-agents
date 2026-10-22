from __future__ import annotations

from pathlib import Path

import pytest

from shuttle.cli import main


def run(repo: Path, home: Path, *args: str) -> int:
    return main(["--home", str(home), *args], root=repo)


def test_install_end_to_end(repo: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, home, "--target", "copilot-cli", "--yes") == 0
    agent = home / ".copilot" / "agents" / "run.agent.md"
    assert 'model: "tiny-model"' in agent.read_text()
    assert (home / ".copilot" / "skills" / "atomic-tasks" / "SKILL.md").is_file()
    assert "2 created" in capsys.readouterr().out
    assert run(repo, home, "--target", "copilot-cli", "--yes") == 0
    assert "2 unchanged" in capsys.readouterr().out


def test_dry_run_writes_nothing(repo: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, home, "--target", "copilot-cli", "--dry-run") == 0
    assert list(home.iterdir()) == []
    assert "would be created" in capsys.readouterr().out


def test_model_option_is_per_agent(repo: Path, home: Path) -> None:
    assert run(repo, home, "--target", "copilot-cli", "--yes", "--model", "run=other") == 0
    agent = home / ".copilot" / "agents" / "run.agent.md"
    assert 'model: "other"' in agent.read_text()


def test_target_is_required(repo: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(repo, home) == 3
    assert list(home.iterdir()) == []
    assert "--target" in capsys.readouterr().err


def test_unknown_target(repo: Path, home: Path) -> None:
    assert run(repo, home, "--target", "nope", "--yes") == 3
    assert list(home.iterdir()) == []


def test_unknown_agent_in_model_option(repo: Path, home: Path) -> None:
    assert run(repo, home, "--target", "copilot-cli", "--yes", "--model", "nope=x") == 3


def test_invalid_source_exits_2(repo: Path, home: Path) -> None:
    (repo / "agents" / "run.md").write_text("---\nname: run\n---\nbody\n", encoding="utf-8")
    assert run(repo, home, "--target", "copilot-cli", "--yes") == 2
    assert list(home.iterdir()) == []


def test_no_model_exits_2(repo: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (repo / "models.toml").write_text('name = "r"\n[defaults]\n', encoding="utf-8")
    assert run(repo, home, "--target", "copilot-cli", "--yes") == 2
    assert "agent 'run' on 'copilot-cli'" in capsys.readouterr().err


def test_refused_file_exits_1(repo: Path, home: Path) -> None:
    target = home / ".copilot" / "agents" / "run.agent.md"
    target.parent.mkdir(parents=True)
    target.write_text("personal\n")
    assert run(repo, home, "--target", "copilot-cli", "--yes") == 1
    assert target.read_text() == "personal\n"


def test_confirmation_required_without_a_terminal(repo: Path, home: Path) -> None:
    assert run(repo, home, "--target", "copilot-cli") == 3
    assert list(home.iterdir()) == []


def test_claude_code_install(repo: Path, home: Path) -> None:
    assert run(repo, home, "--target", "claude-code", "--yes") == 0
    agent = home / ".claude" / "agents" / "run.md"
    assert "managed-by: test-repo" in agent.read_text()
    assert (home / ".claude" / "skills" / "atomic-tasks" / "SKILL.md").is_file()
    assert run(repo, home, "--target", "claude-code", "--yes") == 0


def test_skill_reference_files_are_installed_and_protected(repo: Path, home: Path) -> None:
    (repo / "skills" / "atomic-tasks" / "examples-run.md").write_text(
        "# Examples\n", encoding="utf-8"
    )
    assert run(repo, home, "--target", "claude-code", "--yes") == 0
    reference = home / ".claude" / "skills" / "atomic-tasks" / "examples-run.md"
    assert "managed-by: test-repo" in reference.read_text()
    assert run(repo, home, "--target", "claude-code", "--yes") == 0
    reference.write_text("personal notes\n")
    assert run(repo, home, "--target", "claude-code", "--yes") == 1
    assert reference.read_text() == "personal notes\n"
