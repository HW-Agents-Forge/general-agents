# Contributing

Everything in the repository is in **English**: documentation, prompts, commit messages and issues. For anything beyond a small fix, open an issue first.

An agent is accepted only if it **condenses** a large output into a short answer. Agents that merely add indirection (reading a file, listing a directory) are not.

## Add or change an agent

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json` (`name` equal to the folder, `description`, `version`).
2. Write `agents/<name>.md` with the frontmatter `name`, `description` (what it does, when and when not to use it), `tools` (give `Read` only if the agent must read whole files: filtering with commands is cheaper) and `model: haiku`.
3. Keep the prompt short and directive (it runs on a tiny model): a rigid output contract of at most 20 lines, one filled-in example, the rule that text read from files is data and never instructions, and explicit read-only limits.
4. Write `skills/delegate-to-<name>/SKILL.md`: when to delegate, how to phrase the request, worked examples, when not to.
5. Add the plugin to `.claude-plugin/marketplace.json` and the [catalog](docs/agents-catalog.md).
6. Show that it pays for itself, following the [evaluation protocol](docs/evaluation.md).

## Add or change a skill

Keep it short: its description is always in the primary agent's context and its body is loaded when consulted. Verify every technical claim by running it (`csh-pro` was checked against tcsh) and say when only one implementation was tested. Keep workplace-specific conventions out.

## Before pushing

```sh
./scripts/check
```

It needs only `sh` and `jq`, and CI runs the same script.
