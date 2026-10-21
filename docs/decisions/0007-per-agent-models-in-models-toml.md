# 0007. Per-agent models in models.toml, copied script

- Status: accepted
- Date: 2026-10-21

## Context

Model identifiers depend on the tool and on the user's Copilot plan. The script will be copied as is into other repositories, with other agents.

## Decision

- The model is chosen at install time, **agent by agent**, never in bulk.
- It comes, in order of priority, from `--model AGENT=MODEL`, the tool's section in `models.toml`, then `[defaults]` according to the `tier`.
- `models.toml` sits at the repository root and carries the `name` field, used in the origin mark `managed-by: <name>`.
- The script is copied from one repository to another: no `--source` parameter, no package publication. Python ≥ 3.11.
- No model is ever chosen by default in the absence of configuration: the error is explicit.

## Consequences

- The targets no longer contain model identifiers; they keep their tool-name mapping table.
- The identifier is not checked against the tool (no reliable offline way); only its form is.
- Each copy of the script has its own `name`, which avoids confusing the files of two repositories writing to the same home.
