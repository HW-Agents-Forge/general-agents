When and how to delegate voluminous tasks (command execution, search, diff, history) to small sub-agents. Consult before running a command with long output or a wide search.

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. Do not delegate when you need the exact content, when the operation is trivial, or when it requires delicate reasoning: the sub-agents run on tiny models.

# Decision table

| Situation | Decision |
|---|---|
| Command with long or lengthy output (simulation, build, regression) | Delegate to `run` with the exact command in your shell's syntax writing to a log file, and a timeout |
| Finding where something appears in a large repository | Delegate to `find` |
| Size and nature of a change between two revisions | Delegate to `diff` |
| Who or what introduced a change | Delegate to `git` or `svn` |
| Reading a small file or a few lines | Read directly |
| Writing or modifying a file | Do it yourself |
| Short command whose output fits in a few lines | Run it yourself |

# How to phrase the request

1. Ask a precise question ("which tests fail and why?"), not a vague instruction.
2. Give the minimal context: paths, references. For `run`: the exact command written for YOUR shell (name it: csh, bash, zsh, fish, PowerShell, cmd), redirecting its output to a log file (`command >& job.log` in csh, `command > job.log 2>&1` in bash or zsh), AND a timeout in seconds chosen from the expected duration. `run` filters the log instead of reading it whole, and refuses to start without the command and the timeout.
3. State the expected format only if it differs from the default report.
4. Do not paste large content into the request.

# After the answer

- Trust the report, but verify before any irreversible action.
- If it says `truncated: yes`, or lists uncertainties, ask a narrower question instead of rereading the raw content.
- Do not ask a sub-agent the same question again without new information.

# Example sequences

Each line starting with "Ask" is the request to send, written the way you should write it. Replies are summarized. Redirections are shown for csh (`>&`); in bash or zsh write `> file 2>&1` instead.

## `run`: commands with long output

**Failing simulation.** Ask `run`: "Run `make sim TEST=smoke >& sim.log`, timeout 1800 s." Reply: `failed`, `errors=3`, "scoreboard mismatch at 1250 ns (3 times)". Next: ask `find` where the scoreboard is, read those lines yourself, fix.

**Regression with many tests.** Ask `run`: "Run `./run_regression.csh >& reg.log`, timeout 7200 s. Which tests failed?" Reply lists the failing test names and the first error of each. Next: pick one failing test and rerun only that test through `run`.

**Build that must succeed.** Ask `run`: "Run `make all >& build.log`, timeout 900 s." Reply: `finished`, `errors=0 warnings=12`. Next: continue; do not read the log.

**Lint or CDC check.** Ask `run`: "Run `lint_run.csh top >& lint.log`, timeout 1200 s. List the distinct error rules and their counts." Reply: three rules with counts. Next: fix the most frequent rule first.

**Job cut short.** Reply: `timeout`, last line "simulating at 40 us". The job was not wrong, only slow. Ask `run` again with a timeout twice as long, or run it yourself in the background.

**Command that needs input.** Reply: `blocked`, last line "Enter license server:". `run` never answers. Fix the environment (set the variable, source the setup script), then ask again.

**Command with a pipe.** Ask `run`: "Run `cat list.txt | xargs -n1 check.csh >& chk.log`, timeout 600 s." `run` wraps it in `timeout 600 <your shell> -c '...'` itself. If the command contains a single quote, `run` refuses: add the timeout yourself.

## `find`: searching the code

**Where is it defined?** Ask `find`: "Where is the entity `uart_tx` declared and where is it instantiated?" Reply: the declaring file and each instance with `label : entity work.uart_tx`. Next: read the instance you care about.

**Who drives this signal?** Ask `find`: "Which processes or assignments drive `tx_busy` in `rtl/`?" Reply: lines with `<=`, `assign` and port-map connections. Next: read the one that matters; ask again in the parent module if the signal is renamed.

**Hierarchy of a block.** Ask `find`: "List the modules instantiated directly in `soc_top.sv`, with their instance names." Reply: a short list. Next: repeat for a child only if needed.

**Where is this parameter used?** Ask `find`: "Where is the generic `DATA_WIDTH` set or overridden?" Reply: the default value and each override with its file and line.

**What does this big file say?** Ask `find`: "In `doc/spec.md`, what does it say about reset behavior?" Reply: the relevant lines, with line numbers. Next: read those lines if the answer is not enough.

**Nothing found.** Reply: `no match found for uart_rx`. Do not conclude the code is absent: try other spellings, a different directory, or ask `git` or `svn` whether it was renamed.

## `diff`: sizing up a change

**Two directories.** Ask `diff`: "Compare `release_1.2/` and `release_1.3/`." Reply: number of files, a line each, risks such as "interface of `fifo` changed". Next: read the risky files yourself.

**Two revisions.** Ask `diff`: "Summarize `git diff v1.2 v1.3` for `rtl/`." Reply: groups by directory and any removed test. Next: ask `git` who removed that test.

**Before a review.** Ask `diff`: "Summarize the uncommitted changes in the working copy." Reply: files and a one-line summary. Next: decide what to commit or revert yourself.

## `git`: history and state

**Who changed this line?** Ask `git`: "Who last changed line 88 of `rtl/uart_tx.vhd` and in which commit?" Reply: one commit, author, date, message.

**When did it break?** Ask `git`: "Which commits touched `rtl/uart_tx.vhd` since 2026-09-01?" Reply: a short list. Next: ask `diff` for the most suspicious commit.

**State of the tree.** Ask `git`: "Is the working copy clean? List modified files." Reply: `state: modified` and the files.

## `svn`: history and state

**What changed in a revision?** Ask `svn`: "What did revision 4521 change?" Reply: files and the log message. Next: ask `diff` for details if needed.

**Who touched this file recently?** Ask `svn`: "Last five revisions of `rtl/top.vhd`, with authors." Reply: five lines.

**Working copy state.** Ask `svn`: "Status of the working copy: modified, missing and conflicted files." Reply: `state: conflict` and the conflicted files. Next: resolve them yourself; sub-agents never change the copy.

## Combining agents

**New failure after a merge.** `run` (rerun the test, get the error) then `svn` or `git` (who touched the failing file) then `diff` (what that change did) then read and fix yourself.

**Understanding unknown code.** `find` (where is the block and who instantiates it) then read the two or three files it points to. Do not ask `find` to explain the design.

**Checking before a release.** `run` (build and smoke tests, one request each, in parallel if your tool allows) then `diff` (changes since the last release) then `git` or `svn` (state is clean).

## Do not delegate

- `ls rtl/`, `git status`, `cat` of a short file: the output is shorter than the request.
- "Is this design correct?" or "why does this fail?": it needs reasoning, so keep it.
- A command you must follow interactively: sub-agents never answer prompts.
- A file you will edit: read the exact lines yourself, a summary is not enough to edit safely.
- The same question again with no new information.
