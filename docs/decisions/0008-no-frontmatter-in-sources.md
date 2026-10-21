# 0008. No frontmatter in the sources

- Status: accepted (supersedes the TOML frontmatter of ADR 0005)
- Date: 2026-10-21

## Context

Sources first carried a YAML-like frontmatter, then a TOML one. Either way, the sources contained tool-flavored syntax, and the script already has to generate each tool's own frontmatter.

## Decision

Agent and skill sources are plain Markdown with no frontmatter. The script produces all frontmatter itself:
- `name` from the file or folder name;
- `description` from the first non-heading paragraph;
- the body is the whole file;
- `tools` and `tier` come from `agents.toml`, because they cannot be deduced from the text;
- the model comes from `models.toml` or `--model`;
- the origin mark is added by the target.

A source that starts with a frontmatter is rejected, so the two sources of truth cannot disagree.

## Consequences

- Sources read as ordinary documents and are easy to write.
- Adding an agent means adding a Markdown file and a table in `agents.toml`.
- The first paragraph does double duty (description and start of the prompt) and must be written accordingly.
- `max_output_lines` is gone: the line limit is part of the prompt text.
- `agents.toml` is one more file to keep in sync with `agents/`; the registry checks that both match.
