# 0010. Skill reference files and lighter agents

- Status: accepted
- Date: 2026-10-22

## Context

Token cost has three parts: what the primary agent always carries (agent and skill descriptions), what it loads when it consults a skill, and what a sub-agent's prompt costs on every call. A review of the prompts found three avoidable costs: the `atomic-tasks` skill (about 1,900 tokens) was loaded whole even though a consultation concerns one agent; `run` and `diff` had a `read` tool that let a tiny model read a whole log or file, against the prompt's own filtering rule; and the same three rules were copied into five prompts (a shared file was tried for those and rejected, see below).

## Decision

- **Skill reference files.** Any `*.md` file next to a skill's `SKILL.md` is a reference: plain Markdown, no frontmatter, no description. `SKILL.md` stays short and links to them; the tool loads a reference only when the model follows the link. `atomic-tasks` keeps its decision table in `SKILL.md` and has one examples file per agent. Targets install references next to the skill with the origin mark as a first-line comment.
- **No shared rules file.** An `agents/_common.md` appended to every prompt was implemented, then rejected as unusable by the maintainer. The three rules stay in each prompt, in a `Rules` section.
- **No `read` tool where filtering is the rule.** `run` and `diff` use `shell` only. `find` keeps `read`, limited by its prompt to about 20 lines around a match.
- **Lighter reports.** `run` no longer echoes the command and the log path; it adds `shell:` only when the parent did not name it.
- **Shorter descriptions.** One action sentence and one "not for" sentence, since descriptions are always in the primary agent's context.

## Consequences

- The saving is in the primary agent's context, where `atomic-tasks` drops from about 1,900 to about 730 tokens per consultation.
- References rely on the tool following a relative link to a file in the skill folder. That is the documented progressive-disclosure pattern for skills, but it was not verified in a real session for every tool.
- The installer writes more files per skill, with the same safety rules (never overwrite an unmarked file, never delete).
- Removing `read` makes the filtering rule binding for `run` and `diff` instead of advisory.
