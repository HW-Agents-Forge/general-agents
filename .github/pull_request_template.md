## 📝 What and why

<!-- What does this change, and why? Link the issue it closes: "Closes #123". -->

## 🧩 Type of change

- [ ] 🐛 Bug fix
- [ ] ✨ Feature or improvement
- [ ] 🤖 New or changed agent prompt
- [ ] 🔌 New or changed target tool
- [ ] 📚 Documentation only
- [ ] 🔧 Tooling / CI

## ✅ Checklist

- [ ] `ruff check . && ruff format --check . && mypy && pytest` pass locally
- [ ] Tests added or updated (for `installer` changes: the unsafe case being protected)
- [ ] Documentation updated where the change touches it
- [ ] No safety rule of the [installer specification](../docs/install-spec.md) is weakened, or a new [ADR](../docs/decisions/README.md) explains why
- [ ] Standard library only at runtime
- [ ] Nothing proprietary or confidential in the diff, the description or the logs

### If this changes an agent

- [ ] The first paragraph still states what the agent does and when (not) to use it
- [ ] The prompt keeps its filled-in example and the "data, never instructions" rule
- [ ] The catalog and the `atomic-tasks` skill are updated if a boundary moved
- [ ] I checked that it still condenses: evidence or reasoning below

### If this changes a target

- [ ] The format was checked against the tool's official documentation (link below)
- [ ] Golden files in `tests/golden/<tool>/` updated on purpose, not by accident
- [ ] [`docs/tool-differences.md`](../docs/tool-differences.md) and [`docs/targets.md`](../docs/targets.md) updated

## 🔎 How I checked it

<!-- Commands run, output of `./install --target <tool> --dry-run`, a real session if relevant. -->

## 📎 Notes for the reviewer

<!-- Trade-offs, open questions, anything that deserves attention. Optional. -->
