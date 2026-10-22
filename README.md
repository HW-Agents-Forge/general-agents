# general-agents

[![CI](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/chabrioche/general-agents/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Runtime dependencies: none](https://img.shields.io/badge/runtime%20dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Status: early development](https://img.shields.io/badge/status-early%20development-orange)

**Small sub-agents that take the token-expensive chores off your primary coding agent.**

Reading a 20,000-line simulation log, sweeping a repository for every usage of a signal, digesting a long `svn log`: your primary agent only needs the *conclusion*. general-agents defines a handful of focused sub-agents that do the heavy reading on the **smallest model available** and hand back a short, structured report.

You write each agent once, as plain Markdown. A small Python tool, `shuttle`, adapts it to every agentic tool you use.

## Contents

- [How it works](#how-it-works)
- [Agents](#agents)
- [Skills](#skills)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Supported tools](#supported-tools)
- [Reusing it elsewhere](#reusing-it-elsewhere)
- [Safety guarantees](#safety-guarantees)
- [Development](#development)
- [Repository layout](#repository-layout)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Status](#status)

## How it works

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"ui-sans-serif, system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif","fontSize":"15px","textColor":"#1e293b","lineColor":"#64748b","primaryColor":"#dbeafe","primaryBorderColor":"#3b82f6","primaryTextColor":"#1e3a8a","secondaryColor":"#ede9fe","tertiaryColor":"#f8fafc","edgeLabelBackground":"#f8fafc","clusterBkg":"#f8fafc","clusterBorder":"#cbd5e1","titleColor":"#334155"},"flowchart":{"curve":"basis","padding":14,"nodeSpacing":36,"rankSpacing":48,"htmlLabels":true}}}%%
flowchart LR
    subgraph src["📂 Sources"]
        A("agents/*.md<br/>one prompt per agent")
        S("skills/*/SKILL.md<br/>and example files")
        T("agents.toml<br/>tools per agent")
        M("models.toml<br/>model per agent")
    end
    subgraph sh["⚙️ shuttle"]
        P("parse and<br/>validate") --> R("resolve<br/>the model") --> X("render for<br/>the tool")
    end
    subgraph out["📦 Installed files"]
        C("Claude Code<br/>.claude/agents<br/>.claude/skills")
        G("Copilot CLI<br/>.copilot or .github<br/>agents and skills")
    end
    A & S & T & M --> P
    X --> C & G

    classDef src fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a
    classDef eng fill:#ede9fe,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95
    classDef out fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#14532d
    classDef agent fill:#fef3c7,stroke:#f59e0b,stroke-width:1.5px,color:#78350f
    classDef bad fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#7f1d1d
    classDef quiet fill:#f1f5f9,stroke:#94a3b8,stroke-width:1.5px,color:#0f172a

    class A,S,T,M src
    class P,R,X eng
    class C,G out
```

The primary agent never reads the raw log. A delegation looks like this:

```mermaid
sequenceDiagram
    autonumber
    actor You
    participant P as Primary agent<br/>(large model)
    participant R as run<br/>(tiny model)
    participant T as Terminal
    You->>P: Run the smoke test and tell me what fails
    P->>R: exact command, log file, timeout
    activate R
    R->>T: run the command under the timeout
    T-->>R: process ends, log written
    R->>T: grep and tail on the log only
    Note over R,T: the raw log never reaches a model
    R-->>P: status, error count, key points
    deactivate R
    Note over P,R: about 10 lines instead of thousands
    P-->>You: the cause and the fix
```

- **Sources are plain Markdown.** No frontmatter: the file name is the agent name, the first paragraph is its description, and the whole file is its prompt.
- **`agents.toml`** lists each agent's abstract tools (`read`, `search`, `shell`).
- **`models.toml`** picks the model, agent by agent, per tool.
- **`shuttle`** generates each tool's own format, frontmatter included, and installs it.
- The **skills** are installed alongside: `atomic-tasks` tells your primary agent when delegating is worth it and how to phrase the request, with worked example sequences for every agent; `csh-pro` is a verified csh and tcsh reference.

Delegation has a fixed cost, so an agent earns its place only if it *condenses*. That is why this repository has no `read`, `write` or `list` agent: your primary agent already does those cheaply. See [ADR 0001](docs/decisions/0001-keep-only-condensing-agents.md).

## Agents

| Agent | What it does | Tools |
|---|---|---|
| [`run`](agents/run.md) | Runs the exact command you give it (any shell: csh, bash, zsh, fish, PowerShell, cmd), with a mandatory timeout, watches it and reports status, exit code and key lines | `shell` |
| [`find`](agents/find.md) | Searches the codebase and returns paths, lines and a short answer | `search`, `read` |
| [`diff`](agents/diff.md) | Summarizes the changes between two files, directories or revisions | `shell` |
| [`git`](agents/git.md) | Answers questions about git history and state, read-only | `shell` |
| [`svn`](agents/svn.md) | Answers questions about Subversion history and state, read-only | `shell` |

Every agent replies in a fixed, short format (at most 20 lines). Contracts are in the [agent catalog](docs/agents-catalog.md).

## Skills

| Skill | What it is for |
|---|---|
| [`atomic-tasks`](skills/atomic-tasks/SKILL.md) | When to delegate to a sub-agent and when not to, how to phrase the request, and worked sequences for `run`, `find`, `diff`, `git` and `svn` |
| [`csh-pro`](skills/csh-pro/SKILL.md) | Writing csh and tcsh correctly: bash-to-csh translation, verified pitfalls, when to switch to Python or bash |

Skills are plain Markdown too and are installed with the agents. `atomic-tasks` keeps its decision table short and puts the worked examples in one file per agent next to it, so the tool loads only the examples you need.

## Quick start

Requirements: Python 3.11 or newer. No other dependency.

```sh
git clone https://github.com/chabrioche/general-agents.git
cd general-agents

# See exactly what would be written, without writing anything
./install --target claude-code --dry-run

# Install for real (asks for confirmation; use --yes to skip it)
./install --target claude-code
```

`--target` is required and takes one tool per run. By default agents go in your home; to install inside a project (next to its own configuration), use `--scope project`:

```sh
./install --target claude-code --scope project --project /path/to/project
```

Choose a model for one agent without touching any file:

```sh
./install --target claude-code --model run=claude-haiku-5-5 --model find=claude-haiku-5-5
```

## Configuration

**`models.toml`** at the repository root:

```toml
name = "general-agents"      # written in the origin mark of every generated file

[defaults]
small = "claude-haiku-5-5"   # model for every agent of tier "small"

[claude-code]
# run = "haiku"              # per-tool, per-agent override
```

For each agent and tool, the model is the first match of: `--model AGENT=MODEL`, then the tool's section, then `[defaults]`. If nothing matches, `install` fails and names the agent and the tool. It never falls back silently to a larger model.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"ui-sans-serif, system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif","fontSize":"15px","textColor":"#1e293b","lineColor":"#64748b","primaryColor":"#dbeafe","primaryBorderColor":"#3b82f6","primaryTextColor":"#1e3a8a","secondaryColor":"#ede9fe","tertiaryColor":"#f8fafc","edgeLabelBackground":"#f8fafc","clusterBkg":"#f8fafc","clusterBorder":"#cbd5e1","titleColor":"#334155"},"flowchart":{"curve":"basis","padding":14,"nodeSpacing":36,"rankSpacing":48,"htmlLabels":true}}}%%
flowchart LR
    Q(["model for<br/>agent A on tool T"]) --> O["1 · --model A=…"]
    O -- "not given" --> S["2 · tool section<br/>of models.toml"]
    S -- "not listed" --> D["3 · tier default<br/>in [defaults]"]
    D -- "missing" --> E["❌ error naming<br/>the agent and the tool"]
    O -- "given" --> U(["✅ model written<br/>into the file"])
    S -- "listed" --> U
    D -- "found" --> U

    classDef src fill:#dbeafe,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a
    classDef eng fill:#ede9fe,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95
    classDef out fill:#dcfce7,stroke:#22c55e,stroke-width:1.5px,color:#14532d
    classDef agent fill:#fef3c7,stroke:#f59e0b,stroke-width:1.5px,color:#78350f
    classDef bad fill:#fee2e2,stroke:#ef4444,stroke-width:1.5px,color:#7f1d1d
    classDef quiet fill:#f1f5f9,stroke:#94a3b8,stroke-width:1.5px,color:#0f172a

    class O,S,D src
    class U out
    class E bad
    class Q quiet
```

**Adding an agent** takes two steps:

1. Create `agents/<name>.md`. Start with a paragraph saying what the agent does and when to use it.
2. Add a table to `agents.toml`:

   ```toml
   [<name>]
   tools = ["read", "search"]
   ```

Details: [agent format](docs/agent-format.md), [installer specification](docs/install-spec.md).

## Supported tools

| Tool | `--target` | Status |
|---|---|---|
| Claude Code | `claude-code` | Implemented |
| GitHub Copilot CLI | `copilot-cli` | Draft, to be checked against a real CLI |
| VS Code (Copilot) | `vscode` | Planned |
| OpenCode | `opencode` | Planned |

How the tools differ, with sources: [tool differences](docs/tool-differences.md).

## Reusing it elsewhere

`shuttle` is meant to be **copied** into other repositories, each with its own agents. Copy `install` and `src/shuttle/`, write your own `agents/`, `agents.toml` and `models.toml`, and give `models.toml` a different `name`. The checklist and the way to keep the engine in sync are in [docs/reuse.md](docs/reuse.md).

## Safety guarantees

The installer is the only code that writes to disk, and it is deliberately conservative:

- **It never deletes anything.** To remove an agent, delete its file by hand.
- **It never overwrites a file it did not create.** Generated files carry a `managed-by: <name>` mark; a file without it, or marked by another repository, is refused.
- **It writes only under the home directory**, rejecting `..` and symbolic links that escape it, and writes atomically.
- **`--dry-run` decides exactly like a real run.**
- **Re-running changes nothing** when the sources have not changed.

## Development

```sh
python -m pip install -e '.[dev]'
pytest && ruff check . && ruff format --check . && mypy
```

CI runs the same checks on Python 3.11, 3.12 and 3.13, plus a dry-run install of the real sources. Conventions are in [docs/conventions.md](docs/conventions.md); structural decisions are recorded as [ADRs](docs/decisions/README.md).

## Repository layout

```
agents/          one Markdown prompt per agent
skills/          the atomic-tasks and csh-pro skills (plain Markdown)
agents.toml      tools and tier of each agent
models.toml      repository name and models
install          thin executable calling shuttle
src/shuttle/     the Python package (parser, config, installer, targets, CLI)
tests/           pytest suite with golden files per target
docs/            design documents and decision records
.github/         CI workflow, issue forms, pull request template, Dependabot
```

## Documentation

Start with the [documentation index](docs/README.md): [vision](docs/vision.md), [architecture](docs/architecture.md), [agent catalog](docs/agents-catalog.md), [evaluation protocol](docs/evaluation.md), [roadmap](docs/roadmap.md) and [open questions](docs/open-questions.md).

## Contributing

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md) for setup, ground rules and how to add an agent or a target tool.

## Status

Early development. The engine, the Claude Code target, a draft Copilot CLI target, five agents and two skills exist and are tested (95 tests, CI on Python 3.11 to 3.13); the agents have not yet been exercised in a real session. **The token savings have not been measured yet**: the first evaluation, on `run`, is the next milestone (see the [roadmap](docs/roadmap.md)), and an agent that does not pay for itself will be reworked or removed.

Released under the [MIT License](LICENSE).
