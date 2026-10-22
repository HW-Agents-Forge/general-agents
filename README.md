# general-agents

[![CI](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Status: early development](https://img.shields.io/badge/status-early%20development-orange)

**A marketplace of small sub-agents that take the token-expensive chores off your primary coding agent.**

Reading a 20,000-line simulation log, sweeping a repository for every usage of a signal, digesting a long `svn log`: your primary agent only needs the *conclusion*. Each agent here does the heavy reading on the **smallest model** (Haiku) and hands back a short, structured report.

There is no installer and no generator. This repository is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces): you pick the plugins you need, each one ships an agent together with the skill that teaches your primary agent when and how to delegate to it, and the files are plain Markdown you can read, edit or copy wherever you like.

## Use it

There is no installer: you take the files you want and put them where your tool reads them. Get them either way:

- **Clone** this repository, or
- **Download a release** and unzip the archive for your tool (`general-agents-claude-code-*.zip`, `general-agents-vs-code-*.zip`, `general-agents-copilot-cli-*.zip`). Each contains `agents/<tool>/` and `skills/<tool>/`.

Then copy what you need:

| Tool | Agents (`agents/<tool>/`) go to | Skills (`skills/<tool>/`) go to |
|---|---|---|
| Claude Code | `~/.claude/agents/` or `<project>/.claude/agents/` | `~/.claude/skills/` or `<project>/.claude/skills/` |
| Copilot CLI | `~/.copilot/agents/` or `<project>/.github/agents/` | `~/.copilot/skills/` or `<project>/.github/skills/` |
| VS Code (Copilot) | `<project>/.github/agents/` | `<project>/.github/skills/` |

Take an agent **and** its skill together: `delegate-to-run` teaches your primary agent when and how to call `run`.

| Agent | Skill | What it does |
|---|---|---|
| `run` | `delegate-to-run` | Runs the exact command you give it (any shell) under a mandatory timeout and reports status, exit code and key lines |
| `find` | `delegate-to-find` | Searches the codebase and returns paths, lines and a short answer |
| `diff` | `delegate-to-diff` | Summarizes the changes between two files, directories or revisions |
| `git` | `delegate-to-git` | Answers questions about git history and state, read-only |
| `svn` | `delegate-to-svn` | Answers questions about Subversion history and state, read-only |
| none | `csh-pro` | Verified csh and tcsh reference: bash-to-csh translation and pitfalls |

Every agent replies in a fixed, short format (at most 20 lines); contracts are in the [agent catalog](docs/agents-catalog.md).

## Layout: one folder per tool

```
agents/claude-code/   run.md, find.md, ...             tools: Bash, model: haiku
agents/vs-code/       run.agent.md, ...                tools: ["execute"], qualified model name
agents/copilot-cli/   run.agent.md, ...                same format, kept separate on purpose
skills/<tool>/        delegate-to-run/SKILL.md, csh-pro/SKILL.md, ...
```

The prompts are the same everywhere; only the frontmatter differs. There is no generator: you edit each copy, and CI fails when they drift apart.

> **Not yet verified on the real tools.** The documentation of Copilot and VS Code could not be read from the development environment, so these frontmatters come from search excerpts: the exact model identifier (`Claude Haiku 5.5 (copilot)`; a wrong one makes the agent fall back silently to the default model), whether Copilot CLI honors `model`, and the tool names. Test them and report what breaks.

## Why these agents

Delegation has a fixed cost, so an agent earns its place only if it *condenses* a large output into a short answer. That is why there is no `read`, `write` or `list` agent: your primary agent already does those cheaply. Whether each agent pays for itself is checked with the [evaluation protocol](docs/evaluation.md).

## Checks and releases

CI runs `scripts/check_frontmatter.py` (needs PyYAML) on every push: valid YAML, the keys, tool and model values each tool expects, and the same agents, skills, prompts and descriptions in all three folders. Pushing a tag `vX.Y.Z` publishes a release with one zip per tool.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Early development. The agents have not yet been exercised in a real session, and **the token savings have not been measured yet**: an agent that does not pay for itself will be reworked or removed.

Released under the [MIT License](LICENSE).
