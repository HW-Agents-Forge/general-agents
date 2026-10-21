# 0005. Standard library only at runtime

- Status: proposed
- Date: 2026-10-21

## Context

`install` is meant to be launched directly from a cloned repository, on varied machines, without a prepared virtual environment. The script is also copied from one repository to another (ADR 0007).

## Decision

No runtime dependency (Python ≥ 3.11: `tomllib` reads `models.toml`). The frontmatter is read by a homemade parser limited to a subset of YAML (simple keys, short lists). Development dependencies (`pytest`, `ruff`, `mypy`) remain allowed.

## Consequences

- Immediate start, no prior installation.
- The accepted YAML subset must be bounded and documented in [agent-format.md](../agent-format.md); everything else is rejected with a clear error.
- Reversible: if the parser becomes a burden, switching to PyYAML or to TOML frontmatter needs a new decision (see question 5 in [open-questions.md](../open-questions.md)).
