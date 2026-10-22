# Contributing

Thanks for your interest in general-agents. This guide covers how to set up, what a good change looks like, and how to propose one.

Everything in the repository is in **English**: code, documentation, agent prompts, commit messages and issues.

## Before you start

- For anything beyond a small fix, **open an issue first** to discuss it.
- Read the [vision](docs/vision.md) and [ADR 0001](docs/decisions/0001-keep-only-condensing-agents.md): an agent is accepted only if it *condenses* a large output into a short answer.
- Structural decisions are recorded as [ADRs](docs/decisions/README.md). A change that goes against one needs a new ADR.

## Setup

Python 3.11 or newer.

```sh
git clone https://github.com/chabrioche/general-agents.git
cd general-agents
python -m pip install -e '.[dev]'
```

Run the same checks as CI before every push:

```sh
ruff check . && ruff format --check . && mypy && pytest
```

## Ground rules

- **Standard library only at runtime** ([ADR 0005](docs/decisions/0005-stdlib-only.md)). Development tools (`pytest`, `ruff`, `mypy`) are fine.
- **All disk writes go through `installer.py`**, and the installer never deletes anything ([ADR 0004](docs/decisions/0004-no-deletion-by-the-script.md)). Do not weaken a safety rule from the [installer specification](docs/install-spec.md) without an ADR.
- Type annotations everywhere in `src/`; frozen dataclasses for the data model; no global state.
- Details: [docs/conventions.md](docs/conventions.md).

## Common contributions

### Add or change an agent

1. Create `agents/<name>.md` as plain Markdown, **no frontmatter**. The first paragraph says what the agent does and when to use it: it becomes the description ([format](docs/agent-format.md)).
2. Add a table for it in `agents.toml` with its `tools`.
3. Keep the prompt short and directive (it runs on a tiny model), with a rigid output contract of at most 40 lines.
4. Update the [catalog](docs/agents-catalog.md) and the `atomic-tasks` skill if a boundary between agents changes.
5. Show that it pays for itself, following the [evaluation protocol](docs/evaluation.md).

### Add or change a skill

1. Create `skills/<name>/SKILL.md` as plain Markdown, **no frontmatter**. The folder name is the skill name and the first paragraph is its description: say when to consult it.
2. Keep it short, since its description is always in the primary agent's context and its body is loaded when consulted.
3. **Verify every technical claim by running it** (the `csh-pro` skill was checked against tcsh), and say when only one implementation was tested.
4. Keep workplace-specific conventions out of this repository.

### Add a target tool

1. Fill in the tool's column in [docs/targets.md](docs/targets.md) from its **official documentation**, and note the verification date.
2. Implement `Target` in `src/shuttle/targets/<tool>.py` and register it in `targets/__init__.py`.
3. Add golden files in `tests/golden/<tool>/` and a CLI test.
4. Record what you learned in [docs/tool-differences.md](docs/tool-differences.md).

### Fix a bug

Add a failing test first, then the fix. `installer` changes need tests for the unsafe case they protect against.

## Pull requests

- Branch from `main`: `feature/<topic>`, `fix/<topic>` or `docs/<topic>`.
- One idea per pull request, with imperative commit messages and a short first line.
- CI must be green: lint, format, types, tests and the installer smoke test.
- Update the documentation your change touches, and the golden files if a target's output changes on purpose.
- Fill in the pull request template: what changed and why, the checklist, and how you checked it.

## Reporting problems

Open an issue and pick the matching template (bug report, feature request, new agent proposal or new target tool). For a bug, give the command you ran, the target tool and its version, and the output (`--dry-run` output is ideal). **Do not include proprietary code or logs** in issues or pull requests.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
