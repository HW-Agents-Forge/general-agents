# Differences between the target tools

Reference for the `targets/*` modules: how VS Code, Copilot CLI and OpenCode differ for custom agents and skills.

> **Verification status (2026-10-21).** Gathered from search-result excerpts of the official documentation and a few third-party sources. The documentation sites could not be fetched directly from the development environment (network policy), so full pages were not read. Items marked **unverified** or **conflict** must be checked against the live documentation before the corresponding target is written. Copilot and VS Code documentation evolves quickly (several pages mention features still behind settings).

## Summary

| Aspect | VS Code | Copilot CLI | OpenCode |
|---|---|---|---|
| Agent file | `<name>.agent.md` | Markdown with YAML frontmatter (`*.agent.md` convention, unverified) | `<name>.md` |
| User-level location | `~/.copilot/agents/` in the newest docs (older docs: the VS Code profile folder) | `~/.copilot/agents/` | `~/.config/opencode/agents/` |
| Project-level location | `.github/agents/` (also `.claude/agents/`) | `.github/agents/` | `.opencode/agents/` |
| Required frontmatter | Unverified | `description` | `description` (per stable docs) |
| Tools field | `tools`: list of tools or tool sets | `tools`: list; omitted or `["*"]` = all, `[]` = none | `permission` map (the `tools` option is deprecated) |
| Model field | `model`: string or preference-ordered array, qualified `Model Name (vendor)` | `model`: documented; behavior in the CLI unclear | `model`: `provider/model-id` |
| Model if unset | The currently selected model | Inherits the default model | Sub-agents use the model of the invoking primary agent |
| Can a primary agent call it? | Via the `agent` tool and the `agents` field | Via the `agent` tool alias; controls `disable-model-invocation`, `user-invocable` | `mode: subagent`, invoked through the Task tool |
| Skills (`SKILL.md`) | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.copilot/skills/`, `.github/skills/` (also `.claude/skills/`) | `.opencode/skills/` (project; personal path unverified) |
| Shell command timeout | Unverified | Unverified | Bash tool default 2 minutes (from a repository mirror; may have changed) |
| Token usage reporting | Unverified | `/usage` (per-model breakdown; sub-agent split unverified) | Unverified |
| Free key for the origin mark | Unverified (`metadata` is ignored per GitHub docs) | `metadata` property exists | Unverified |

## VS Code

- **Format:** `.agent.md` files with an optional YAML header between `---` delimiters and a Markdown body of instructions.
- **Frontmatter fields listed in the reference:** `name`, `description`, `tools`, `agents`, `model`, `argument-hint`, `reasoning-effort`, `user-invocable`, `disable-model-invocation`, `target`, `handoffs`. The older `infer` property is deprecated in favor of `user-invocable` and `disable-model-invocation`.
- **Tools:** if a `tools` list is given, only those tools (or tool sets) are available. Tool names depend on the harness. The `agent` tool set must be included for an agent to call sub-agents.
- **Model:** in the Copilot harness a single model or an array in preference order (first available wins). The value is a qualified name, for example `GPT-5 (copilot)`. The exact qualified name of Haiku 5.5 must be checked in the model picker.
- **Sub-agents:** the `agents` field limits which custom agents a coordinator may call (`['*']` or omitted = all, `[]` = none; names are case-sensitive). Listing an agent explicitly overrides its `disable-model-invocation: true`. Release notes of January 2026 mention that custom agents as sub-agents were behind the setting `chat.customAgentInSubagent.enabled`, and that nested delegation needs `chat.subagents.allowInvocationsFromSubagents`. **Unverified** whether these settings are still required.
- **Claude format:** files in `.claude/agents` are read with a different schema (`tools` comma-separated, `model` among `sonnet`, `opus`, `haiku`, `inherit`). Not used by this project.
- **Locations:** workspace default `.github/agents/` (`.claude/agents/` also read; any `.md` file in `.github/agents/` is reported to be detected); user level `~/.copilot/agents/` in the newest documentation, whereas older pages pointed to the profile's user data folder, so check the installed version. The setting `chat.agentFilesLocations` adds locations but is deprecated and only applies to the Local agent. For sessions running on an Agent Host, user-level agents are read from the host's folder (`~/.copilot/agents` or `~/.claude/agents`). `chat.useCustomizationsInParentRepositories` lets VS Code find agents in a parent repository root.
- **Model if omitted:** the currently selected model is used.
- **Skills:** workspace skills are picked up from `.github/skills/`, `.claude/skills/` and `.agents/skills/`. The personal location `~/.copilot/skills/` is documented for Copilot CLI and the cloud agent, not for stable VS Code.

## Copilot CLI

- **Locations and precedence:** user level `~/.copilot/agents/`; repository level `.github/agents/`; organization and enterprise level in the `/agents` directory of the `.github-private` repository. On a name conflict a more local definition wins (the personal agent overrides the repository one when identifiers are equal). File names are used for deduplication across levels.
- **Frontmatter properties:** `name` (optional display name), `description` (required), `model`, `tools`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `target`, `metadata`, and `include-custom-instructions` (so that a sub-agent follows the repository's conventions).
- **Tools:** omitted or `["*"]` enables all tools; `[]` disables all. Aliases: `execute` (also accepts `shell`, `Bash`, `powershell`), `read`, `edit`, `search`, `agent`, `web`, `todo`.
- **Model:** documented as "the model to use when this custom agent executes; if unset, it inherits the default model". Documentation excerpts are inconsistent on whether the property is honored in the CLI itself (one guide mentions it for IDEs). The VS Code reference says the selected harness decides which fields take effect, and a GitHub page states that `model`, `argument-hint` and `handoffs` are ignored by the cloud agent on GitHub.com (not necessarily by the CLI). **Conflict / unverified**: check that the CLI honors `model`, since otherwise an agent would silently run on the primary model and lose its purpose.
- **Sub-agent restrictions:** a changelog mirror states that sub-agents inherit the tool restrictions of the parent agent throughout the delegation chain.
- **Usage:** `/usage` shows premium requests, session duration and a token breakdown per model; local telemetry is reportedly stored in `~/.copilot/session-store.db` (table `assistant_usage_events`), in billing units rather than raw tokens (third-party source).
- **Invocation:** `/agent` interactively, a mention in the prompt, or `copilot --agent=<id>`.
- **Skills:** personal `~/.copilot/skills/`, project `.github/skills/` (also `.claude/skills/`).

## OpenCode

- **Locations:** global `~/.config/opencode/agents/`, per project `.opencode/agents/`. The file name is the agent name.
- **Frontmatter (stable documentation):** `description`, `mode` (`primary`, `subagent` or `all`; default `all`), `model`, `temperature`, `permission`; the body is the prompt. The `tools` option is deprecated in favor of `permission`.
- **Permissions:** keys such as `read`, `edit`, `glob`, `grep`, a shell key, `task`, `webfetch`; each takes `ask`, `allow` or `deny`, and several accept glob-pattern rules (for example per-command shell rules). Rules are evaluated in order and the last matching rule wins. Anything not allowed should be explicitly denied.
- **Model:** `provider/model-id`. If unset, a primary agent uses the global model and a **sub-agent uses the model of the primary agent that invoked it**. A tiny-model sub-agent therefore needs an explicit `model`. Through the GitHub Copilot provider, model identifiers look like `github-copilot/claude-haiku-4.5` (dotted version numbers). By analogy Haiku 5.5 would be `github-copilot/claude-haiku-5.5`, but this is a **guess**; confirm with `opencode models github-copilot`.
- **Shell timeout:** the bash tool's default timeout is reported to be 2 minutes (repository mirror, possibly outdated), with no maximum. A long simulation launched through `run` could therefore be cut short unless a longer timeout is passed per call; this affects the `run` design (see [agents-catalog.md](agents-catalog.md)).
- **Sub-agents:** `permission.task` controls which sub-agents an agent can invoke through the Task tool. A hidden sub-agent is only hidden from the `@` menu; the model can still invoke it if permissions allow.
- **Version conflict:** the stable documentation uses a `permission` map; the v2 development documentation uses an ordered `permissions` list of action/resource/effect rules, renames `prompt` to `system`, `bash` to `shell`, `task` to `subagent`, and `write`/`patch` to `edit`. Stable pages also disagree with themselves on the shell key name (`bash` vs `shell`). **Conflict**: determine the installed OpenCode version before writing the target.
- **Skills:** `.opencode/skills/` appears in third-party descriptions of scanned directories; no official personal path was found.
- **Creation helper:** `opencode agent create` generates an agent file interactively.

## Consequences for the design

1. **Model pinning is the critical difference.** OpenCode sub-agents and Copilot CLI agents inherit a model when none is set. Targets must always write an explicit model, and the installer's "no model found" error (see [install-spec.md](install-spec.md)) is therefore essential, never a silent fallback.
2. **Model identifier formats differ**: `Model Name (vendor)` in VS Code, an identifier in Copilot CLI (format unverified), `provider/model-id` in OpenCode. `models.toml` holds one string per agent and tool, so each value follows its tool's format.
3. **Tools versus permissions.** VS Code and Copilot CLI use a `tools` allow-list; OpenCode uses a `permission` map with `deny` for the rest. The mapping `read` / `search` / `shell` is different in nature, not only in naming, so `render_agent` in the OpenCode target generates a permission map.
4. **Sub-agent invocability is controlled differently** (`agent` tool and `disable-model-invocation` versus `mode: subagent`). Each target must make the agent invocable by the primary agent and hidden from nothing it needs.
5. **Origin mark.** Copilot CLI has a `metadata` property that could carry `managed-by`; VS Code reportedly ignores it. Where no free key is accepted, use a first-line comment in the body (see [targets.md](targets.md)).
6. **Skills share the `SKILL.md` format** but not the locations. The skill target path depends on the tool, and OpenCode's personal path remains to be found.
7. **Timeouts are a tool-level concern.** OpenCode's reported 2-minute default means `run` must request an explicit timeout from the terminal tool when the parent asks for a longer one, rather than relying only on a `timeout` prefix. Copilot CLI and VS Code timeout behavior is undocumented in what could be found.
8. **Measuring savings** (see [evaluation.md](evaluation.md)): only Copilot CLI has a known reporting command (`/usage`); VS Code and OpenCode need to be checked.
9. **Shared locations across tools.** `.github/skills/`, `.claude/skills/` and `.agents/skills/` are read by several tools: installing the same skill for two targets may create duplicates. Choose one location per tool and document it.

## Sources

- VS Code: [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents), [Custom agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference), [Subagents](https://code.visualstudio.com/docs/copilot/agents/subagents), [January 2026 release notes (1.109)](https://code.visualstudio.com/updates/v1_109).
- GitHub Copilot: [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration), [Creating and using custom agents for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli), [About custom agents (CLI)](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents), [About Agent Skills](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/about-agent-skills), [Claude Haiku 5.5 in GitHub Copilot](https://github.blog/changelog/2026-10-07-claude-haiku-5-5-in-github-copilot/).
- Other: [Claude Haiku 5.5 in GitHub Copilot](https://github.blog/changelog/2026-10-07-claude-haiku-5-5-in-github-copilot), [OpenCode model list through Copilot (third party)](https://lasy.readthedocs.io/ai/opencode.html), [OpenCode troubleshooting (timeout)](https://mintlify.com/opencode-ai/opencode/advanced/troubleshooting).
- OpenCode: [Agents](https://opencode.ai/docs/agents/), [Permissions](https://opencode.ai/docs/permissions/), [Config](https://opencode.ai/docs/config/), [v2 Agents](https://dev.opencode.ai/v2/docs/agents), [Migrate from V1](https://dev.opencode.ai/v2/docs/migrate-v1).
