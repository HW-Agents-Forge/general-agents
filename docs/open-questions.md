# Open questions

## Resolved

| # | Question | Answer |
|---|---|---|
| 1 | Which target tool first? | All three, all through a GitHub Copilot subscription. Order of work to be set (see [roadmap.md](roadmap.md)). |
| 2 | Which is the smallest model (`small`)? | Haiku 5.5 (`claude-haiku-5-5`). Announced as available in Copilot (VS Code, Copilot CLI) by the GitHub changelog of 2026-10-07; its exact identifier in each tool, notably OpenCode through its Copilot provider, remains to be confirmed. |
| 3 | Default value of `--target`? | None. `--target` is required and names a single tool. |
| 6 | Deletion by the script? | None, ever (ADR 0004). |
| 7 | `run`: allow-list or confirmation? | The parent agent supplies the exact command; `run` executes it as is and launches nothing else. Safety rests on the parent agent and the tool. |
| 8 | Minimum Python? | 3.11 (`tomllib` without dependency). |
| 10 | `run` timeout? | Mandatory, set by the parent agent, no default. |
| 11 | Interactive prompt? | `run` reports `blocked` and never answers. |

## Open

| # | Question | Leads |
|---|---|---|
| 4 | Merge `git` and `svn` into one `vcs` agent? | One agent that detects the repository (less overlap, a single prompt) versus two specialized agents (more targeted prompts) |
| 5 | Homemade frontmatter parser (YAML subset) or PyYAML? | Homemade: zero dependency but scope to bound. PyYAML: simple but a dependency. Alternative: TOML frontmatter for the sources, readable with `tomllib` |
| 9 | Evaluation acceptance thresholds (30 % gain) | To adjust after the first measurements |
| 12 | `run`: how to monitor a long job (periodic reading of the output or of a log file) and what each tool's terminal expiry mechanism is | Depends on what each tool's terminal allows |

## To verify in the official documentation

Partial findings and conflicts are listed in [tool-differences.md](tool-differences.md). Highest priority:

- Does Copilot CLI honor the `model` property? (Otherwise agents silently run on the primary model.)
- Exact model identifier format of Haiku 5.5 in each tool, notably OpenCode through its Copilot provider.
- Installed OpenCode version: `permission` map (stable) or `permissions` list (v2).
- Whether the VS Code sub-agent settings are still required, and which user-level agent path applies to the installed VS Code version (`~/.copilot/agents` or the profile folder).
- Shell command timeout behavior in Copilot CLI and VS Code, and OpenCode's reported 2-minute default (`run` may need to pass an explicit timeout).
- Token usage reporting for sub-agents in VS Code and OpenCode.
- Exact OpenCode identifier of Haiku 5.5: run `opencode models github-copilot` (guess: `github-copilot/claude-haiku-5.5`).


- Agent formats, locations and tool names of each target (see [targets.md](targets.md)).
- `SKILL.md` support and skill location in each tool.
- Whether a free key is allowed in the frontmatter for the origin mark.
- How to read the token consumption of the primary agent and sub-agents in each tool.
- Terminal timeout mechanism of each tool.
