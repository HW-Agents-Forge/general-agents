# Test strategy

Tool: `pytest`. Tests live in `tests/`, with no network access and no writing outside temporary directories (`tmp_path`).

## Levels

### Unit

| Module | To cover |
|---|---|
| `parser` | Valid agent and skill; description taken from the first non-heading paragraph; frontmatter rejected; empty file; heading-only file; invalid name |
| `manifest` | Valid `agents.toml`; missing or empty `tools`; unknown tool; duplicate tool; invalid `tier`; unknown key |
| `model` | Construction and validation of the dataclasses |
| `registry` | Discovery, deterministic order; agent without a manifest entry; manifest entry without an agent file; skill references |
| `config` | Valid `models.toml`; missing `name`; unknown agent or tool section; resolution order (`--model`, tool section, `[defaults]`); no model found |
| `targets/*` | Rendering of an agent and a skill; model and tool mapping; presence of the origin mark |

### Integration (`installer`)

In a temporary fake home:
- creation of the expected files;
- idempotence (second run without change);
- update of a marked file whose source changed;
- **refusal to overwrite** an unmarked file;
- `install` never deletes any file (no deletion, even for an agent removed from the sources);
- `--dry-run` writes nothing and announces the same actions as the real run;
- rejection of a path that escapes the home (including through a symbolic link);
- atomic write (no partial file on a simulated error).

### End to end (`cli`)

- Exit codes for each case of the table in [install-spec.md](install-spec.md).
- `--target` missing or unknown: usage error, nothing is written.
- Project scope: files land under the project, an existing instructions file is untouched, the home stays empty; `--home` and `--project` cannot be mixed up.
- Readable output for `--dry-run`.

## Reference tests (golden files)

For each target, one expected file per catalog agent is stored in `tests/golden/<tool>/`. The test compares the rendering to that file. A deliberate format change is made by explicitly updating the reference file, reviewed together with the code.

## Validation of the repository's sources

A test walks the real files in `agents/` and `skills/` and checks that they are valid for all targets. This prevents shipping a malformed agent.

## What runs in CI

`ruff check`, `ruff format --check`, `mypy` (strict) and `pytest` on Python 3.11, 3.12 and 3.13, then a dry-run install of the real sources for every target. The suite has 95 tests, including:
- a test that every real agent and skill parses and that `models.toml` matches the catalog;
- a test that the `run` prompt covers every supported shell and its status variable;
- tests for skill reference files (discovery, invalid names, rendering next to `SKILL.md`, installation, protection of a personal file);
- a test that the engine works unchanged in a copy of the repository ([reuse.md](reuse.md)): the real-sources tests assume nothing about which agents exist.

## Quality

- Target coverage: ≥ 90 % on `parser`, `installer` and `targets`.
- `installer` tests come first: that is where the risk is concentrated.
- Local automatic checks: tests, lint and typing (see [conventions.md](conventions.md)).

## Not covered by these tests

The real quality of sub-agent answers (it depends on the models) belongs to evaluation, not to automated tests: see [evaluation.md](evaluation.md).
