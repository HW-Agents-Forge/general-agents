# Target tools

> **TO VERIFY.** The formats below are working hypotheses. Before writing each target, check this document against the tool's official documentation and record the verification date in the dedicated row. Rendering tests then serve as the reference.

See [tool-differences.md](tool-differences.md) for what is already known, with sources and verification status.

## Implementation status

| Target | Status |
|---|---|
| `claude-code` | Implemented (`src/shuttle/targets/claude_code.py`), format confirmed by the official docs excerpts; install location `~/.claude/` |
| `copilot-cli` | Draft implemented (`src/shuttle/targets/copilot_cli.py`), unverified against a running CLI |
| `vscode` | Not started |
| `opencode` | Not started |

## Information to establish for each tool

Claude Code is filled in from the official documentation excerpts (2026-10-21); the other columns are still to verify (see [tool-differences.md](tool-differences.md)).

| Information | Claude Code | VS Code | Copilot CLI | OpenCode |
|---|---|---|---|---|
| Agent location (user level) | `~/.claude/agents/` | To verify | To verify | To verify |
| File extension and name | `<name>.md` | To verify | To verify | To verify |
| Frontmatter keys | `name`, `description`, `tools`, `model`; unknown keys ignored | To verify | To verify | To verify |
| Identifier of the smallest model (`small`) | Alias (`haiku`) or full ID (`claude-haiku-5-5`) | To verify | To verify | To verify |
| Tool names for `read`, `search`, `shell` | `Read`, `Grep` + `Glob`, `Bash` | To verify | To verify | To verify |
| Sub-agent mode (invocable by the primary agent) | By description; to confirm in a session | To verify | To verify | To verify |
| Skill location and `SKILL.md` support | `~/.claude/skills/<name>/SKILL.md` | To verify | To verify | To verify |
| Accepts a free key for the origin mark | Yes (unknown keys ignored) | To verify | To verify | To verify |
| Terminal timeout mechanism (for `run`) | To verify | To verify | To verify | Reported 2-minute default |
| Verification date | 2026-10-21 (documentation excerpts) | — | — | — |

## Expected mapping table

Each target expresses these mappings in its module.

| Abstract | Concrete target |
|---|---|
| `tier: small` | Model from `models.toml` or `--model` (never in the sources) |
| `tools: [read]` | Platform read tool name(s): `Read` in Claude Code |
| `tools: [search]` | Search tool name(s): `Grep`, `Glob` in Claude Code |
| `tools: [shell]` | Execution tool name(s): `Bash` in Claude Code |

## Origin mark handling

If the tool tolerates a free key in the frontmatter, use `managed-by: <name>` (`name` read from `models.toml`). Otherwise add a first-line comment in the body. Detection by `installer` must work in both cases (see [install-spec.md](install-spec.md)).

## Adding a tool

1. Fill in the corresponding column above from the official documentation.
2. Create `src/shuttle/targets/<tool>.py` implementing `Target`.
3. Register the target in the target registry.
4. Add the rendering tests (see [testing.md](testing.md)).
5. Update this document with the verification date.
