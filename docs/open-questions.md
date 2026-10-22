# Open questions

## Resolved

| # | Question | Answer |
|---|---|---|
| 1 | Which target tool first? | Claude Code (implemented) and Copilot CLI (draft); VS Code and OpenCode later. All through a GitHub Copilot subscription except Claude Code. See [roadmap.md](roadmap.md). |
| 2 | Which is the smallest model (`small`)? | Haiku 5.5 (`claude-haiku-5-5`). Announced as available in Copilot (VS Code, Copilot CLI) by the GitHub changelog of 2026-10-07; its exact identifier in each tool, notably OpenCode through its Copilot provider, remains to be confirmed. |
| 3 | Default value of `--target`? | None. `--target` is required and names a single tool. |
| 5 | Source frontmatter format? | None: sources are plain Markdown and the script adds the frontmatter (ADR 0008). |
| 6 | Deletion by the script? | None, ever (ADR 0004). |
| 7 | `run`: allow-list or confirmation? | The parent agent supplies the exact command; `run` executes it as is and launches nothing else. |
| 8 | Minimum Python? | 3.11 (`tomllib` without dependency). |
| 10 | `run` timeout? | Mandatory, set by the parent agent, no default. |
| 11 | Interactive prompt? | `run` reports `blocked` and never answers. |
| 15 | Reuse in other repositories? | The script is copied, never shared as a package; see [reuse.md](reuse.md) and ADR 0007. |
| 16 | Which shells does `run` support? | Any: csh/tcsh, bash/zsh/sh, fish, PowerShell and cmd, through a table in the prompt (ADR 0009). Only csh/tcsh was tested. |
| 17 | A skill per shell or language? | Only `csh-pro`, because models are weakest there. It is not preloaded into `run` (ADR 0009). |
| 18 | How does `run` avoid reading a whole log? | The parent redirects output to a log file; `run` runs only read-only filters on it. |

## Open

| # | Question | Leads |
|---|---|---|
| 4 | Merge `git` and `svn` into one `vcs` agent? | One agent that detects the repository (less overlap, a single prompt) versus two specialized agents (more targeted prompts) |
| 9 | Evaluation acceptance thresholds (30 % gain) | To adjust after the first measurements |
| 12 | Terminal timeout mechanism of each tool | Unknown for Copilot CLI and VS Code; OpenCode's bash tool reportedly defaults to 2 minutes, so `run` may need to pass an explicit timeout |
| 13 | Per-command enforcement of read-only limits | Deferred until the OpenCode target; see [tool-differences.md](tool-differences.md) |
| 14 | EDA error markers in `run` are generic | Provide the real tools' messages (simulator, lint, synthesis) to tune them |
| 19 | Timeout on PowerShell and cmd | `run` refuses when the tool has no timeout option; look for a portable wrapper |
| 20 | PowerShell, fish and cmd rows of the shell table | Untested; check them on a real shell |

## To verify in the official documentation

Partial findings and conflicts are listed in [tool-differences.md](tool-differences.md). Highest priority:

- Does Copilot CLI honor the `model` property? (Otherwise agents silently run on the primary model.)
- Exact model identifier format of Haiku 5.5 in each tool; for OpenCode run `opencode models github-copilot` (guess: `github-copilot/claude-haiku-5.5`).
- Installed OpenCode version: `permission` map (stable) or `permissions` list (v2).
- Whether the VS Code sub-agent settings are still required, and which user-level agent path applies to the installed VS Code version (`~/.copilot/agents` or the profile folder).
- Shell command timeout behavior in Copilot CLI and VS Code.
- Token usage reporting for sub-agents in VS Code and OpenCode.
- Agent formats, locations and tool names of each remaining target (see [targets.md](targets.md)).
- `SKILL.md` support and skill location in each tool.
- Whether a free key is allowed in the frontmatter for the origin mark.
- Whether the installed skills are actually loaded and consulted by each tool (not tested in a real session).
