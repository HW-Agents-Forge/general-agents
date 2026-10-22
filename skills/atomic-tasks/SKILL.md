When and how to delegate voluminous tasks (commands, search, diff, history) to small sub-agents. Consult before a long-output command or a wide search.

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

Read only the file for the agent you are about to use:

- [`run`](examples-run.md): simulation, regression, build, lint, timeout, blocked command, pipe.
- [`find`](examples-find.md): where something is defined, who drives a signal, hierarchy, no result.
- [`diff`](examples-diff.md): two directories, two revisions, uncommitted changes.
- [`git` and `svn`](examples-git-svn.md): who changed a line, when it broke, state of the tree.
- [Combining agents](examples-combined.md): chains such as `run` then `svn` then `diff`.

# Do not delegate

- `ls rtl/`, `git status`, `cat` of a short file: the output is shorter than the request.
- "Is this design correct?" or "why does this fail?": it needs reasoning, so keep it.
- A command you must follow interactively: sub-agents never answer prompts.
- A file you will edit: read the exact lines yourself, a summary is not enough to edit safely.
- The same question again with no new information.
