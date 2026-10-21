# Conventions

## Language

- Everything in the repository is in English: documentation, code, agent prompts, skills, commit messages and messages displayed by `install`.

## Python

- Minimum version: 3.11 (`tomllib` to read `models.toml`).
- Standard library only at runtime. Allowed development dependencies: `pytest`, a lint/format tool (`ruff`), a type checker (`mypy`).
- Type annotations everywhere in `src/`.
- Frozen dataclasses (`frozen=True`) for the data model.
- No global state. Paths and the home are passed as parameters.
- Business errors raise exceptions from `errors.py`, never `sys.exit` outside `cli`.
- Short functions; one module, one responsibility (see [architecture.md](architecture.md)).

## Disk writes

All writing goes through `installer`. No other module opens a file for writing.

## Agents and skills

- Agent name: lowercase letters, digits, hyphens; identical to the file name.
- Description: states **when** to use the agent.
- Short body, explicit output contract (see [agent-format.md](agent-format.md)).
- Any change of boundary between agents updates the catalog and the `atomic-tasks` skill.

## Git

- Branches: `feature/<topic>`, `fix/<topic>`, `docs/<topic>`.
- Imperative commit messages, one idea per commit, short first line.
- A change to a target's output format includes updating the test reference files.

## Review

A change is ready to merge if:
- tests, lint and typing pass;
- the relevant documentation is up to date;
- no safety rule of [install-spec.md](install-spec.md) is weakened without an ADR.

## Decisions

Every structural decision (format, safety, dependency, scope) is recorded in `docs/decisions/` following the template in [decisions/README.md](decisions/README.md).
