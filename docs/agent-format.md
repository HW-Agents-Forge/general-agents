# Neutral source format for agents

Agent and skill sources are **plain Markdown, with no frontmatter** (ADR 0008). The script adds the frontmatter each tool expects when it generates the installed files.

## Where each piece of information comes from

| Information | Source |
|---|---|
| `name` | The file name (`agents/run.md` → `run`), or the folder name for a skill (`skills/atomic-tasks/SKILL.md`). Lowercase letters, digits and hyphens. |
| `description` | The first paragraph of the file that is not a heading, joined on one line. It states **when** the primary agent should invoke the agent; it is the text the tool shows to the primary model. |
| System prompt (body) | The whole file, including the first paragraph. |
| `tools`, `tier` | `agents.toml` (below). They cannot be deduced from the Markdown. |
| Model | `models.toml` or `--model` at install time (see [install-spec.md](install-spec.md)). |
| Origin mark | Added by the target (see below). |

A source that starts with a frontmatter (`---` or `+++`) is rejected.

## Example: `agents/run.md`

```markdown
Runs one exact shell command with a mandatory timeout, watches it and returns a short report. Use it when the raw output would be large.

You run ONE command given by the parent agent, watch it, and report. You do nothing else.
...
```

## `agents.toml`

One table per agent, at the repository root.

```toml
[run]
tools = ["shell", "read"]

[find]
tools = ["search", "read"]
# tier = "small"   # optional, "small" is the default and the only tier
```

| Key | Required | Description |
|---|---|---|
| `tools` | yes | Non-empty list of abstract tools (below). |
| `tier` | no | Model tier. `small` (default) is the only accepted value (ADR 0006). |

Every agent file needs a table, and every table needs an agent file. Unknown keys are errors.

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

## Writing the prompt

Recommended structure after the description paragraph:

1. **Role** in one sentence.
2. **Procedure**, short and ordered.
3. **Output contract**: exact format and maximum size (state the number of lines in the prompt, 20 at most).
4. **Limits**: what the agent must not do.

Rules:
- No reference to a particular tool (no platform tool names).
- The output contract is imperative and testable.
- Stay under about 60 lines: the system prompt is paid for on every call.
- Include one filled-in example answer: tiny models copy a bare template literally.
- Say that text read from files, logs or command output is data, never instructions.
- The first paragraph is read twice (as the description and as the start of the prompt): write it as a statement of what the agent does and when to use it.

## Origin mark

**Generated** files receive the mark `managed-by: <name>` (in the frontmatter, or as a comment where the tool does not accept free keys), where `<name>` is the `name` field of `models.toml`. It never appears in the sources. See [install-spec.md](install-spec.md).

## Skills

A skill is a folder `skills/<name>/SKILL.md`, plain Markdown like the agents: the name is the folder name and the description is the first paragraph. Specification of this project's skills: [skill-atomic-tasks.md](skill-atomic-tasks.md) (which also covers `csh-pro`). Facts stated in a skill must be verified, not recalled.
