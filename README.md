# general-agents

[![CI](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Status: early development](https://img.shields.io/badge/status-early%20development-orange)

**A catalog of small sub-agents that take the token-expensive chores off your primary coding agent.**

Reading a 20,000-line simulation log, sweeping a repository for every usage of a signal, digesting a long `svn log`: your primary agent only needs the *conclusion*. Each agent here does the heavy reading on the **smallest model** (Haiku) and hands back a short, structured report.

This repository is a plain catalog for Claude Code, VS Code (GitHub Copilot), Copilot CLI and OpenCode. Each agent comes with the skill that teaches your primary agent when and how to delegate to it. No installer, no generator: the files are Markdown you can read, edit and copy wherever you like.

## Use it

There is no installer: you take the files you want and put them where your tool reads them. Get them either way:

- **Clone** this repository, or
- **Download a release** and unzip the archive for your tool (`general-agents-claude-code-*.zip`, `-vs-code-`, `-copilot-cli-`, `-opencode-`). Each contains `agents/<tool>/` and `skills/<tool>/`.

Then copy what you need:

| Tool | Agents (`agents/<tool>/`) go to | Skills (`skills/<tool>/`) go to |
|---|---|---|
| Claude Code | `~/.claude/agents/` or `<project>/.claude/agents/` | `~/.claude/skills/` or `<project>/.claude/skills/` |
| Copilot CLI | `~/.copilot/agents/` or `<project>/.github/agents/` | `~/.copilot/skills/` or `<project>/.github/skills/` |
| VS Code (Copilot) | `<project>/.github/agents/` | `<project>/.github/skills/` |
| OpenCode | `~/.config/opencode/agents/` or `<project>/.opencode/agents/` | `~/.config/opencode/skills/` or `<project>/.opencode/skills/` |

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
agents/opencode/      run.md, ...                      mode: subagent, permission map, provider/model
skills/<tool>/        delegate-to-run/SKILL.md, csh-pro/SKILL.md, ...
```

The prompts are the same everywhere; only the frontmatter differs. There is no generator: you edit each copy, and CI fails when the prompts drift apart.

> **Not yet verified on the real tools.** The documentation of Copilot and VS Code could not be read from the development environment, so these frontmatters come from search excerpts: the exact model identifier (`Claude Haiku 5.5 (copilot)`; a wrong one makes the agent fall back silently to the default model), whether Copilot CLI honors `model`, and the tool names. For OpenCode: the `permission` map (stable docs; v2 uses an ordered rule list), the skills location, and the model `anthropic/claude-haiku-5-5` (change the provider, e.g. `github-copilot/...`, to match yours). Test them and report what breaks.

## Why these agents

Delegation has a fixed cost, so an agent earns its place only if it *condenses* a large output into a short answer. That is why there is no `read`, `write` or `list` agent: your primary agent already does those cheaply. Whether each agent pays for itself is checked with the [evaluation protocol](docs/evaluation.md).

## Checks and releases

CI runs two independent jobs on every push: `scripts/check_frontmatter.py` (needs PyYAML) checks the YAML, the keys and the tool and model values each tool expects; `scripts/check_prompts_sync.py` (stdlib only) checks that every agent and skill exists in every tool folder with an identical prompt, and prints a diff when one drifts. Pushing a tag `vX.Y.Z` publishes a release with one zip per tool.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Early development. The agents have not yet been exercised in a real session, and **the token savings have not been measured yet**: an agent that does not pay for itself will be reworked or removed.

Released under the [MIT License](LICENSE).
