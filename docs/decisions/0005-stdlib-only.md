# 0005. Standard library only at runtime

- Status: accepted
- Date: 2026-10-21

## Context

`install` is meant to be launched directly from a cloned repository, on varied machines, without a prepared virtual environment. The script is also copied from one repository to another (ADR 0007).

## Decision

No runtime dependency (Python ≥ 3.11: `tomllib` reads `models.toml`). Source frontmatter is TOML between `+++` lines, read with `tomllib`: no homemade YAML parser. Development dependencies (`pytest`, `ruff`, `mypy`) remain allowed.

## Consequences

- Immediate start, no prior installation.
- Sources use TOML frontmatter ([agent-format.md](../agent-format.md)); invalid TOML is rejected with a clear error.
- Generated files are plain strings rendered by each target, so no YAML library is needed to write them either.
