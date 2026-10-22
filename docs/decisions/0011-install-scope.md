# 0011. Install scope: user or project

- Status: accepted
- Date: 2026-10-22

## Context

Agents can live in the user's home (available everywhere) or inside a project (available to that project, often committed with it). The installer only supported the home. An environment that already exists in a project, with its own instructions file, needs a project-level install. The instructions file itself is outside this repository's purpose and the installer never reads or writes it.

## Decision

- `--scope user` (default) writes under the home (`--home` substitutes it); `--scope project` writes under a project root (`--project`, default: the current directory).
- `--home` is an error with `--scope project`, and `--project` an error with `--scope user`, so the destination is never ambiguous.
- Each target maps a scope to its own paths: Claude Code uses `.claude/` in both cases; Copilot CLI uses `.copilot/` for the user and `.github/` in a project.
- Everything else is unchanged: same origin mark, same refusal to overwrite an unmarked file, no deletion.

## Consequences

- Project-level files are meant to be reviewed and may be committed by the project; the installer does not touch version control.
- The `.github/` project paths for Copilot CLI come from documentation excerpts and are not verified on a real CLI.
- Two projects can hold the same agent names without conflict, since the destinations differ.
