# Neutral source format for agents

Each agent is a Markdown file in `agents/`, made of a **frontmatter** and a **body** (the system prompt).

## Example

```markdown
---
name: run
description: Runs the exact command given (build, tests, scripts), watches it and returns a short report with the useful errors. Use it when the raw output would be large.
tier: small
tools: [shell]
max_output_lines: 40
---

You run the requested command and summarize the result.
...
```

## Frontmatter fields

| Field | Required | Type | Description |
|---|---|---|---|
| `name` | yes | string | Identifier, lowercase letters, digits and hyphens. Unique. Must match the file name. |
| `description` | yes | string | One to three sentences. States **when** the primary agent should invoke it. This is the text the tool shows to the primary model. |
| `tier` | yes | `small` | Desired model tier. The only accepted value is `small` (see ADR 0006). Never a model identifier. |
| `tools` | yes | list | Allowed abstract tools (see below). Empty list not allowed. |
| `max_output_lines` | no | integer | Maximum response size, repeated in the body as an instruction. Default: 40. |

Any unknown key is a validation error.

## Abstract tools

| Abstract tool | Meaning | Risk |
|---|---|---|
| `read` | Read files | Low |
| `search` | Search by pattern or name in the tree | Low |
| `shell` | Run commands | High |

File writing does not exist on the source side: no agent in the catalog needs it (see [vision.md](vision.md)). Each target converts these tools into platform-specific names.

## Model tiers

| `tier` | Intent |
|---|---|
| `small` | The smallest model available in the target tool. The only tier that exists: no agent uses a larger model by default. |

Consequence for writing: prompts must stay very short and very directive, with a rigid output contract and, if needed, an example answer. A task requiring delicate reasoning must not be given to an agent; it stays with the primary agent.

The identifier actually used is not in the sources. It comes from `models.toml` or from `--model` at install time (see [install-spec.md](install-spec.md)).

## Body

The body is the system prompt. Recommended structure:

1. **Role** in one sentence.
2. **Procedure**, short and ordered.
3. **Output contract**: exact format and maximum size.
4. **Limits**: what the agent must not do.

Rules:
- No reference to a particular tool (no platform tool names in the body).
- The output contract is imperative and testable.
- Stay under about 60 lines: the system prompt is paid for on every call.

## Origin mark

**Generated** files receive, in their frontmatter, the mark `managed-by: <name>` (or an equivalent comment if the tool does not accept free keys), where `<name>` is the `name` field of `models.toml`. It does not appear in the sources. See [install-spec.md](install-spec.md).

## Skills

A skill is a folder `skills/<name>/SKILL.md` with a `name` and `description` frontmatter, followed by a Markdown body. Specification of this project's skill: [skill-atomic-tasks.md](skill-atomic-tasks.md).
