# 0002. Neutral source format and shuttle package

- Status: accepted
- Date: 2026-10-21

## Context

Several agentic tools are used (VS Code, Copilot CLI, OpenCode), with different formats, locations, tool names and model identifiers.

## Decision

- Agents are described once, neutrally, in `agents/` (model tiers and abstract tools).
- A real Python package, `shuttle`, adapts these sources to each tool. The `install` executable is only its entry point.
- One target class per tool, behind a common interface.

## Consequences

- Adding a tool = adding a target module.
- Tool mappings are isolated in the targets and can evolve without touching the sources. Model identifiers live in `models.toml` (ADR 0007).
- The project has a package structure (tests, typing, lint) rather than that of a script.
