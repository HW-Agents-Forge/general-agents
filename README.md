# general-agents

Small sub-agents that offload token-expensive tasks from the primary agent. They run on the smallest models available and are defined once, then adapted to several agentic tools (Claude Code, Copilot CLI, VS Code, OpenCode).

## Goals

- Atomize token-expensive tasks into small sub-agents that condense large outputs into short reports.
- Use the smallest models possible for every agent.
- Describe agents once in a neutral format; the `shuttle` Python package adapts them to each tool.
- Let the primary agent know when and how to delegate, through the `atomic-tasks` skill.

## Agents

| Agent | Role |
|---|---|
| `run` | Runs the exact command given by the parent (csh), with a mandatory timeout, and reports |
| `find` | Searches the codebase and returns paths and relevant excerpts |
| `diff` | Summarizes changes between two references or files |
| `git` | Answers questions about git history and state |
| `svn` | Answers questions about Subversion history and state |

Agents that only add indirection (`read`, `write`, `list`, `glob`) or are deterministic (`backup`) are deliberately left out. See [docs/decisions/0001-keep-only-condensing-agents.md](docs/decisions/0001-keep-only-condensing-agents.md).

## Installation

```
./install --target {claude-code,copilot-cli,vscode,opencode} [--model AGENT=MODEL]... [--dry-run]
```

`install` never deletes files. To remove an agent, delete its file by hand.

## Documentation

All design documents are in [docs/](docs/README.md). Nothing is implemented yet: start with the [roadmap](docs/roadmap.md).
