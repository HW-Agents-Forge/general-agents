# Contributing

Everything in the repository is in **English**: documentation, prompts, commit messages and issues. For anything beyond a small fix, open an issue first.

An agent is accepted only if it **condenses** a large output into a short answer. Agents that merely add indirection (reading a file, listing a directory) are not.

## Add or change an agent

1. Write the prompt once, then create it in the three folders: `agents/claude-code/<name>.md`, `agents/vs-code/<name>.agent.md` and `agents/copilot-cli/<name>.agent.md`. The bodies must be identical.
2. Frontmatter: `name` (the file name), `description` (what it does, when and when not to use it), `tools` and `model`. Claude Code: `tools: Bash` (comma-separated `Read`, `Grep`, `Glob`, `Bash`) and `model: haiku`. VS Code and Copilot CLI: `tools: ["execute"]` (list of `read`, `search`, `execute`) and the qualified model name. Give `read` only if the agent must read whole files: filtering with commands is cheaper.
3. Keep the prompt short and directive (it runs on a tiny model): a rigid output contract of at most 20 lines, one filled-in example, the rule that text read from files is data and never instructions, and explicit read-only limits.
4. Write the skill `delegate-to-<name>/SKILL.md` in the three `skills/<tool>/` folders: when to delegate, how to phrase the request, worked examples, when not to.
5. Add it to the [catalog](docs/agents-catalog.md) and show that it pays for itself, following the [evaluation protocol](docs/evaluation.md).

## Add or change a skill

Keep it short: its description is always in the primary agent's context and its body is loaded when consulted. Verify every technical claim by running it (`csh-pro` was checked against tcsh) and say when only one implementation was tested. Keep workplace-specific conventions out.

## Before pushing

```sh
python -m pip install pyyaml
python scripts/check_frontmatter.py
python scripts/check_prompts_sync.py
```

CI runs the same scripts. To publish a release, push a tag `vX.Y.Z`.
