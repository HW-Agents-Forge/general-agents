# general-agents

[![CI](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Status: early development](https://img.shields.io/badge/status-early%20development-orange)

**A marketplace of small sub-agents that take the token-expensive chores off your primary coding agent.**

Reading a 20,000-line simulation log, sweeping a repository for every usage of a signal, digesting a long `svn log`: your primary agent only needs the *conclusion*. Each agent here does the heavy reading on the **smallest model** (Haiku) and hands back a short, structured report.

There is no installer and no generator. This repository is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces): you pick the plugins you need, each one ships an agent together with the skill that teaches your primary agent when and how to delegate to it, and the files are plain Markdown you can read, edit or copy wherever you like.

## Use it

**Claude Code**

```
/plugin marketplace add chabrioche/general-agents
/plugin install run@general-agents
```

**GitHub Copilot CLI**

```
copilot plugin marketplace add chabrioche/general-agents
copilot plugin install run@general-agents
```

**VS Code (GitHub Copilot)**: add `chabrioche/general-agents` to the setting `chat.plugins.marketplaces`, then install the plugins from the Extensions view (agent plugins). Or copy the files by hand, see below.

| Plugin | Contains | What it does |
|---|---|---|
| [`run`](plugins/run) | agent `run`, skill `delegate-to-run` | Runs the exact command you give it (any shell) under a mandatory timeout and reports status, exit code and key lines |
| [`find`](plugins/find) | agent `find`, skill `delegate-to-find` | Searches the codebase and returns paths, lines and a short answer |
| [`diff`](plugins/diff) | agent `diff`, skill `delegate-to-diff` | Summarizes the changes between two files, directories or revisions |
| [`git`](plugins/git) | agent `git`, skill `delegate-to-git` | Answers questions about git history and state, read-only |
| [`svn`](plugins/svn) | agent `svn`, skill `delegate-to-svn` | Answers questions about Subversion history and state, read-only |
| [`csh-pro`](plugins/csh-pro) | skill `csh-pro` | Verified csh and tcsh reference: bash-to-csh translation and pitfalls |

Every agent replies in a fixed, short format (at most 20 lines); contracts are in the [agent catalog](docs/agents-catalog.md).

## Two formats, one prompt

The agent frontmatter differs between the tools (tool names, model names), so each plugin carries two copies of the same prompt:

- `plugins/<name>/agents/<name>.md`: Claude Code (`tools: Bash`, `model: haiku`).
- `plugins/<name>/copilot/agents/<name>.agent.md`: Copilot CLI and VS Code (`tools: ["execute"]`, `model: "Claude Haiku 5.5 (copilot)"`).
- `plugins/<name>/skills/*/SKILL.md`: the skills, one shared copy.

Each plugin has a manifest for each tool (`.claude-plugin/plugin.json`, `.github/plugin/plugin.json`), and so does the marketplace. `scripts/check` fails if the two prompts or the two marketplace files drift apart; there is no generator, you edit both files.

To use the files without plugins, copy them: `agents/*.md` to `~/.claude/agents/`, `copilot/agents/*.agent.md` to `~/.copilot/agents/` (user) or `.github/agents/` (project), skills to `~/.claude/skills/`, `~/.copilot/skills/` or `.github/skills/`.

> **Not yet verified on the real tools.** I could not read the Copilot and VS Code documentation from the development environment, so these points come from search excerpts: the exact Copilot model identifier (a wrong one makes the agent fall back silently to the default model), whether Copilot CLI honors `model`, the `agents`/`skills` fields of `.github/plugin/plugin.json`, and the VS Code marketplace setting. Please test and tell me what breaks.

## Why these agents

Delegation has a fixed cost, so an agent earns its place only if it *condenses* a large output into a short answer. That is why there is no `read`, `write` or `list` agent: your primary agent already does those cheaply. Whether each agent pays for itself is checked with the [evaluation protocol](docs/evaluation.md).

## Repository layout

```
.claude-plugin/marketplace.json   the catalog of plugins
.github/plugin/marketplace.json  the same catalog, for Copilot
plugins/<name>/                   one plugin: agents/, copilot/agents/, skills/, two manifests
scripts/check                     static validation of the marketplace (sh and jq)
docs/                             agent catalog and evaluation protocol
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Early development. The agents have not yet been exercised in a real session, and **the token savings have not been measured yet**: an agent that does not pay for itself will be reworked or removed.

Released under the [MIT License](LICENSE).
