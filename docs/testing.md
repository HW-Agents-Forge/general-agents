# Test strategy

Tool: `pytest`. Tests live in `tests/`, with no network access and no writing outside temporary directories (`tmp_path`).

## Levels

### Unit

| Module | To cover |
|---|---|
| `parser` | Valid frontmatter; missing required field; unknown key; `name` different from the file name; invalid `tier`; empty `tools`; empty body |
| `model` | Construction and validation of the dataclasses |
| `registry` | Discovery, deterministic order, duplicate names |
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
- Readable output for `--dry-run`.

## Reference tests (golden files)

For each target, one expected file per catalog agent is stored in `tests/golden/<tool>/`. The test compares the rendering to that file. A deliberate format change is made by explicitly updating the reference file, reviewed together with the code.

## Validation of the repository's sources

A test walks the real files in `agents/` and `skills/` and checks that they are valid for all targets. This prevents shipping a malformed agent.

## Quality

- Target coverage: ≥ 90 % on `parser`, `installer` and `targets`.
- `installer` tests come first: that is where the risk is concentrated.
- Local automatic checks: tests, lint and typing (see [conventions.md](conventions.md)).

## Not covered by these tests

The real quality of sub-agent answers (it depends on the models) belongs to evaluation, not to automated tests: see [evaluation.md](evaluation.md).
