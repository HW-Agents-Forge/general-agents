# 0004. No deletion by the script

- Status: accepted (replaces the initial version, which planned `--remove`)
- Date: 2026-10-21

## Context

A script that deletes files in the home is risky: a path or filter mistake can destroy files that do not belong to the project. A first version of this decision accepted a `--remove` limited to marked files.

## Decision

The script deletes **no** file: no `uninstall`, no `--remove`, and `installer` exposes no deletion operation. To remove an agent, the user deletes the file by hand.

## Consequences

- Destruction risk removed at the source; the origin mark now only decides whether a file may be updated (see [install-spec.md](../install-spec.md)).
- An agent removed from the sources stays installed until it is deleted by hand; `install` does not report it.
- Less code and fewer tests in `installer` ([testing.md](../testing.md)).
