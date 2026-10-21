# 0003. Installation by transformed copy

- Status: accepted
- Date: 2026-10-21

## Context

Agents installed in the home could be symbolic links to the repository, or generated files.

## Decision

Copy of files **generated** by the target, carrying an origin mark.

## Consequences

- Required because the content depends on the tool (a symbolic link cannot transform).
- A change in the repository is only visible after rerunning `install` (idempotent, see [install-spec.md](../install-spec.md)).
- The origin mark makes it possible to tell managed files from personal ones.
