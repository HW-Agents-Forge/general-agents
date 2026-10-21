# 0001. Keep only agents that condense

- Status: accepted
- Date: 2026-10-21

## Context

The initial list contained `run`, `read`, `write`, `list`, `diff`, `backup`, `glob`, `find`, `git`, `svn`. Delegating has a fixed cost (system prompt, transmitted context, round trip).

## Decision

An agent is kept only if it condenses a large output into a short answer. Kept: `run`, `find`, `diff`, `git`, `svn`. Dropped:
- `read`, `list`, `glob`: redundant with the primary agent's native tools;
- `write`: the content to write must already be supplied by the primary agent, so the cost is doubled;
- `backup`: deterministic operation, a job for a script.

## Consequences

- Smaller and more coherent catalog, with clear boundaries (see [agents-catalog.md](../agents-catalog.md)).
- Each agent must prove its gain by measurement ([evaluation.md](../evaluation.md)).
- No agent writes a file.
