# general-agents

[![CI](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Status: early development](https://img.shields.io/badge/status-early%20development-orange)

**A marketplace of small sub-agents that take the token-expensive chores off your primary coding agent.**

Reading a 20,000-line simulation log, sweeping a repository for every usage of a signal, digesting a long `svn log`: your primary agent only needs the *conclusion*. Each agent here does the heavy reading on the **smallest model** (Haiku) and hands back a short, structured report.

There is no installer and no generator. This repository is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces): you pick the plugins you need, each one ships an agent together with the skill that teaches your primary agent when and how to delegate to it, and the files are plain Markdown you can read, edit or copy wherever you like.

## Use it

```
/plugin marketplace add chabrioche/general-agents
/plugin install run@general-agents
/plugin install git@general-agents
```

| Plugin | Contains | What it does |
|---|---|---|
| [`run`](plugins/run) | agent `run`, skill `delegate-to-run` | Runs the exact command you give it (any shell) under a mandatory timeout and reports status, exit code and key lines |
| [`find`](plugins/find) | agent `find`, skill `delegate-to-find` | Searches the codebase and returns paths, lines and a short answer |
| [`diff`](plugins/diff) | agent `diff`, skill `delegate-to-diff` | Summarizes the changes between two files, directories or revisions |
| [`git`](plugins/git) | agent `git`, skill `delegate-to-git` | Answers questions about git history and state, read-only |
| [`svn`](plugins/svn) | agent `svn`, skill `delegate-to-svn` | Answers questions about Subversion history and state, read-only |
| [`csh-pro`](plugins/csh-pro) | skill `csh-pro` | Verified csh and tcsh reference: bash-to-csh translation and pitfalls |

Every agent replies in a fixed, short format (at most 20 lines); contracts are in the [agent catalog](docs/agents-catalog.md).

## Not using Claude Code, or want to adapt them?

Nothing is hidden behind a script. Copy the files you want:

- `plugins/<name>/agents/<name>.md`: a sub-agent. The frontmatter is Claude Code's (`name`, `description`, `tools`, `model`); the body is the prompt and works in any tool that supports Markdown agents. Change `model: haiku` to whatever your tool calls its smallest model.
- `plugins/<name>/skills/*/SKILL.md`: a skill, the open `SKILL.md` format.

Put them in `~/.claude/agents/` and `~/.claude/skills/` (or `.claude/` in a project), or in the equivalent folders of your tool. Updates are yours to take: `git pull` and copy again.

## Why these agents

Delegation has a fixed cost, so an agent earns its place only if it *condenses* a large output into a short answer. That is why there is no `read`, `write` or `list` agent: your primary agent already does those cheaply. Whether each agent pays for itself is checked with the [evaluation protocol](docs/evaluation.md).

## Repository layout

```
.claude-plugin/marketplace.json   the catalog of plugins
plugins/<name>/                   one plugin: .claude-plugin/plugin.json, agents/, skills/
scripts/check                     static validation of the marketplace (sh and jq)
docs/                             agent catalog and evaluation protocol
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Early development. The agents have not yet been exercised in a real session, and **the token savings have not been measured yet**: an agent that does not pay for itself will be reworked or removed.

Released under the [MIT License](LICENSE).
