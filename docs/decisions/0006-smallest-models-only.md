# 0006. Tiny models only by default

- Status: accepted (amended by ADR 0007)
- Date: 2026-10-21

## Context

The first version of the format planned two tiers, `small` and `medium`. The project's purpose is to reduce token cost; an intermediate model reduces that advantage.

## Decision

All agents use the smallest model available in the target tool. The `medium` tier is removed: `tier` only accepts `small`.

## Consequences

- Very short and directive prompts, rigid output contracts, example answers if needed ([agent-format.md](../agent-format.md)).
- Tasks requiring delicate reasoning are not delegated: they stay with the primary agent, and the `atomic-tasks` skill must say so.
- The most exposed agents (`diff` to judge the intent of a change, `git`/`svn` to trace a cause) may produce less reliable answers. They must favor facts (lines, revisions, authors) over interpretation, and the evaluation ([evaluation.md](../evaluation.md)) must check quality explicitly.
- If an agent durably fails to reach the required quality with the smallest model, it is removed from the catalog or its role is reduced, not switched to a larger model without a new decision.

## Amendment (ADR 0007)

`tier` remains limited to `small`, but the model identifier is no longer imposed: it comes from `models.toml` and can be replaced agent by agent. The "small models only" rule becomes the default, under the user's responsibility.
