# Roadmap

Principle: validate early, on a single agent and a single tool, before generalizing.

```mermaid
flowchart LR
    M0["0 Preparation"] --> M1["1 Vertical slice"] --> M2["2 First evaluation"] --> M3["3 Full catalog"] --> M4["4 Multi-tool"] --> M5["5 Finishing"]
    classDef done fill:#2da44e,stroke:#1a7f37,color:#ffffff
    classDef partial fill:#bf8700,stroke:#9a6700,color:#ffffff
    classDef todo fill:#6e7781,stroke:#57606a,color:#ffffff
    class M1 done
    class M0,M3,M4,M5 partial
    class M2 todo
```

Green: done. Amber: in progress. Grey: not started. The first real evaluation (milestone 2) decides how much to invest in the rest.

## Milestone 0: preparation

- [x] Answer the blocking points of [open-questions.md](open-questions.md) (smallest model, first targets, `--target` behavior).
- [ ] Confirm the exact model identifier of Haiku 5.5 in each tool.
- [x] Claude Code format checked against the official documentation excerpts.
- [ ] Check the other tools' formats in their official documentation and fill in [targets.md](targets.md).
- [x] `pyproject.toml`, `src/shuttle/` skeleton, `tests/`, lint and typing tools.

## Milestone 1: minimal vertical slice

Goal: `agents/run.md` installed end to end for **one** tool.

- [x] `model.py` and `errors.py`.
- [x] `parser.py` and `manifest.py` with tests.
- [x] `config.py` and `models.toml` with tests.
- [x] `registry.py`.
- [x] First target in `targets/` (Copilot CLI draft; format to be verified).
- [x] `installer.py` with all the safety rules and their tests.
- [x] `cli.py` and `install` executable (`--dry-run` included).
- [x] `run` agent written.

Exit criterion: `install --dry-run` then `install` produce the right file in a test home; the agent is usable in the tool. Met in a test home for Claude Code; use in a real session is still to be confirmed.

## Milestone 2: first evaluation

- [ ] Evaluate `run` as described in [evaluation.md](evaluation.md) on at least one real scenario.
- [ ] Decide: continue, adjust the prompt, or rethink the approach.

This milestone conditions what follows: if the gain is not demonstrated, review the catalog before investing further.

## Milestone 3: full catalog

- [x] `find`, `diff`, `git`, `svn` written as first drafts (kept separate, no `vcs` merge); evaluation pending.
- [x] `atomic-tasks` skill, with example sequences for every agent.
- [x] `csh-pro` skill (facts verified against tcsh).
- [x] `run` is shell-agnostic (ADR 0009); agents hardened (injection guard, filled-in examples, log filtering).
- [ ] Evaluation of each agent.

## Milestone 4: multi-tool

- [x] Claude Code target.
- [ ] Verify the Copilot CLI draft against a real CLI.
- [ ] VS Code and OpenCode targets, one at a time, each preceded by checking its format.
- [x] Reference tests for the existing targets.
- [x] Skills installed at each implemented tool's location.

## Milestone 5: finishing

- [x] README, LICENSE (MIT), CONTRIBUTING, issue and pull request templates, CI workflow and Dependabot.
- [x] Guide for reusing the script in other repositories ([reuse.md](reuse.md)).
- [ ] Security review of `installer`.

## Out of the roadmap (to reconsider later)

- Additional agents, based on measured need.
- Automating the evaluation.
- Publishing the package.
