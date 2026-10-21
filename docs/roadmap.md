# Roadmap

Principle: validate early, on a single agent and a single tool, before generalizing.

## Milestone 0: preparation

- [ ] Answer the blocking points of [open-questions.md](open-questions.md) (exact model identifiers per tool).
- [ ] Check each target tool's format in its official documentation and fill in [targets.md](targets.md).
- [x] `pyproject.toml`, `src/shuttle/` skeleton, `tests/`, lint and typing tools.

## Milestone 1: minimal vertical slice

Goal: `agents/run.md` installed end to end for **one** tool.

- [x] `model.py` and `errors.py`.
- [x] `parser.py` with tests.
- [x] `config.py` and `models.toml` with tests.
- [x] `registry.py`.
- [x] First target in `targets/` (Copilot CLI draft; format to be verified).
- [x] `installer.py` with all the safety rules and their tests.
- [x] `cli.py` and `install` executable (`--dry-run` included).
- [x] `run` agent written.

Exit criterion: `install --dry-run` then `install` produce the right file in a test home; the agent is usable in the tool.

## Milestone 2: first evaluation

- [ ] Evaluate `run` as described in [evaluation.md](evaluation.md) on at least one real scenario.
- [ ] Decide: continue, adjust the prompt, or rethink the approach.

This milestone conditions what follows: if the gain is not demonstrated, review the catalog before investing further.

## Milestone 3: full catalog

- [ ] `find`, `diff`, `git`, `svn` agents (or `vcs`, depending on the decision).
- [ ] `atomic-tasks` skill.
- [ ] Evaluation of each agent.

## Milestone 4: multi-tool

- [ ] Remaining targets (VS Code, Copilot CLI, OpenCode), one at a time, each preceded by checking its format.
- [ ] Reference tests per target.
- [ ] Skill installation at each tool's locations.

## Milestone 5: finishing

- [ ] Repository README updated (usage, installation).
- [ ] Security review of `installer`.

## Out of the roadmap (to reconsider later)

- Additional agents, based on measured need.
- Automating the evaluation.
- Publishing the package.
