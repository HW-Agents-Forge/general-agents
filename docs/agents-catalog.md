# Agent catalog

Entry criterion: the agent **condenses** a large output into a short answer. Agents that only add indirection are excluded (see [vision.md](vision.md)).

All agents are `tier: small` to start with. None writes a file by itself; the side effects of `run` are only those of the command supplied by the parent agent.

## Overview

| Agent | Tools | Typical input | Output |
|---|---|---|---|
| `run` | `shell` | The exact command to run (csh syntax) and its timeout | Report: status, exit code, key points |
| `find` | `search`, `read` | A question about the repository | Relevant paths and excerpts |
| `diff` | `shell`, `read` | Two references or files to compare | Structured summary of the changes |
| `git` | `shell` | A question about history or state | Digested answer |
| `svn` | `shell` | A question about history or state | Digested answer |

## Boundaries (no overlap)

| Question | Agent |
|---|---|
| "Where is X defined? Which files mention Y?" | `find` |
| "What does this big file say about Z?" | `find` |
| "What changed between A and B?" | `diff` |
| "Who changed this line? When did this bug appear?" | `git` / `svn` |
| "What is the state of the working copy?" | `git` / `svn` |
| "Run exactly this command, watch it and tell me what fails" | `run` |

Tie-breaking rules:
- `diff` compares content. `git` and `svn` query a repository's history and state. If a comparison concerns two revisions, `diff` does it; if it asks **who** or **why**, it is `git` or `svn`.
- `find` runs no command; `run` only runs the command it receives and does not search the code.
- Open question: merge `git` and `svn` into one `vcs` agent (see [open-questions.md](open-questions.md)).

## Output contracts

Every answer fits in `max_output_lines` lines, with no preamble and no chatty conclusion. Contract keys are in English.

### `run`

Role: run in the terminal the **exact** command supplied by the parent agent, watch it while it runs and return a report. The shell is `csh`.

Responsibilities:
- The parent agent supplies the full command, already written for `csh`, **and a timeout in seconds**. `run` does not rewrite the command, complete it, or add options or redirections on its own initiative.
- The **timeout is mandatory** and decided by the parent agent. `run` always applies it (see "Timeout" below); there is no default duration.
- `run` launches **no command other than the one received** (no investigation command, no retry). It may read the terminal output and the log file designated by the parent agent.
- It monitors progress (output produced, process end, exit code) and returns its report at the end, or when blocked.
- It does not diagnose beyond what the output shows: analysis and the next decision belong to the parent agent.

```
command: <command received, copied verbatim>
status: finished | failed | blocked | timeout
exit_code: <integer, or "unknown" if not finished>
duration: <approximate>
key_points:
- <useful error or warning, one line>
excerpt: |
  <at most a few decisive lines of raw output>
truncated: yes | no
```

Instructions: never return the full log; deduplicate repeated errors; `blocked` if the process waits for input (interactive prompt, password, confirmation): `run` never answers, it reports and gives the last line seen; `timeout` if the allotted time is exceeded: the process is stopped and the report states what had been produced; set `truncated: yes` if the analysis was limited.
Limits: run the command as is (responsibility for its content lies with the parent agent); if the exact command **or the timeout** is missing, run nothing and say so.

Timeout:
- It is expressed in seconds and supplied by the parent agent, which knows the reasonable duration of the job (short simulation, long regression).
- `run` uses the tool terminal's expiry mechanism if there is one; otherwise it prefixes the command with `timeout <seconds>`. This is the only modification of the command it is allowed to make.
- On expiry, `run` stops the process it launched (and only that one), reports `status: timeout` and relaunches nothing. The parent agent decides whether to retry with another duration.

### `find`

```
results:
- path:line — <why relevant, one line>
answer: <direct answer to the question, 1 to 3 sentences>
uncertainties: <what could not be confirmed>
```

Instructions: rank by relevance, cap the number of results, quote verified lines rather than assumed ones.

### `diff`

```
files_changed: <number>
summary: <2 to 4 sentences on the intent of the changes>
details:
- path — <nature of the change>
risks: <points of attention, or "none spotted">
```

### `git` and `svn`

```
answer: <direct answer>
evidence:
- <revision or commit> — <author>, <date> — <why relevant>
state: <clean | modified | conflict> (if requested)
```

Instructions: read-only commands only (`log`, `blame`/`annotate`, `status`, `show`, `diff`); never commit, reset, checkout or merge.

## Adding an agent

A new agent is accepted if it:
1. really condenses an output (the gain must be measured as in [evaluation.md](evaluation.md));
2. has a clear boundary with the existing agents;
3. has a short, verifiable output contract;
4. requires the minimum number of tools.
