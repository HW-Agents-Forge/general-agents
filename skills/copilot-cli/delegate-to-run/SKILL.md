---
name: delegate-to-run
description: "When and how to delegate a long-output command (simulation, build, regression) to the run sub-agent. Consult before running such a command."
---

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. The sub-agent runs on a small model: do not give it work that needs delicate reasoning.

| Situation | Decision |
|---|---|
| Command with long output (simulation, build, regression, lint) | Delegate to `run`: the exact command in your shell's syntax, output redirected to a log file, and a timeout in seconds |
| The output fits in a few lines, or you need the exact content | Do it yourself |

# How to phrase the request

1. Ask a precise question, not a vague instruction.
2. Give the minimal context: the exact command written for YOUR shell (name it: csh, bash, zsh, fish, PowerShell, cmd), redirecting its output to a log file (`command >& job.log` in csh, `command > job.log 2>&1` in bash or zsh), AND a timeout in seconds chosen from the expected duration. `run` filters the log instead of reading it whole, and refuses to start without the command and the timeout.
3. State the expected format only if it differs from the default report.
4. Do not paste large content into the request.

# After the answer

- Trust the report, but verify before any irreversible action.
- If it lists uncertainties or says the result was truncated, ask a narrower question instead of rereading the raw content.
- Do not ask the same question again without new information.

# Examples

Redirections are shown for csh (`>&`); in bash or zsh write `> file 2>&1`. Each "Ask" is the request to send.

**Failing simulation.** Ask `run`: "Run `make sim TEST=smoke >& sim.log`, timeout 1800 s." Reply: `failed`, `errors=3`, "scoreboard mismatch at 1250 ns (3 times)". Next: ask `find` where the scoreboard is, read those lines yourself, fix.

**Regression with many tests.** Ask `run`: "Run `./run_regression.csh >& reg.log`, timeout 7200 s. Which tests failed?" Reply lists the failing test names and the first error of each. Next: pick one failing test and rerun only that test through `run`.

**Build that must succeed.** Ask `run`: "Run `make all >& build.log`, timeout 900 s." Reply: `finished`, `errors=0 warnings=12`. Next: continue; do not read the log.

**Lint or CDC check.** Ask `run`: "Run `lint_run.csh top >& lint.log`, timeout 1200 s. List the distinct error rules and their counts." Reply: three rules with counts. Next: fix the most frequent rule first.

**Job cut short.** Reply: `timeout`, last line "simulating at 40 us". The job was not wrong, only slow. Ask `run` again with a timeout twice as long, or run it yourself in the background.

**Command that needs input.** Reply: `blocked`, last line "Enter license server:". `run` never answers. Fix the environment (set the variable, source the setup script), then ask again.

**Command with a pipe.** Ask `run`: "Run `cat list.txt | xargs -n1 check.csh >& chk.log`, timeout 600 s." `run` wraps it in `timeout 600 <your shell> -c '...'` itself. If the command contains a single quote, `run` refuses: add the timeout yourself.

# Do not delegate

- A short command whose output fits in a few lines: run it yourself.
- A command you must follow interactively: sub-agents never answer prompts.
- "Why does this fail?": it needs reasoning, so keep it.
