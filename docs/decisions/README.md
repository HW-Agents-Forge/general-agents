# Architecture decision records (ADR)

Each structural decision is recorded in a numbered file `NNNN-title.md`.

## Template

```markdown
# NNNN. Title

- Status: proposed | accepted | superseded by NNNN
- Date: YYYY-MM-DD

## Context
## Decision
## Consequences
```

## Index

| No. | Title | Status |
|---|---|---|
| [0001](0001-keep-only-condensing-agents.md) | Keep only agents that condense | accepted |
| [0002](0002-neutral-source-format-and-shuttle.md) | Neutral source format and shuttle package | accepted |
| [0003](0003-install-by-transformed-copy.md) | Installation by transformed copy | accepted |
| [0004](0004-no-deletion-by-the-script.md) | No deletion by the script | accepted |
| [0005](0005-stdlib-only.md) | Standard library only at runtime | accepted |
| [0006](0006-smallest-models-only.md) | Tiny models only by default | accepted |
| [0007](0007-per-agent-models-in-models-toml.md) | Per-agent models in models.toml, copied script | accepted |
| [0008](0008-no-frontmatter-in-sources.md) | No frontmatter in the sources | accepted |
| [0009](0009-shell-agnostic-run-and-csh-skill.md) | Shell-agnostic run and the csh-pro skill | accepted |
| [0010](0010-skill-references-and-shared-agent-rules.md) | Skill reference files and lighter agents | accepted |
| [0011](0011-install-scope.md) | Install scope: user or project | accepted |
