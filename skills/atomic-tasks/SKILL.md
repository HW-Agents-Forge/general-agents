When and how to delegate voluminous tasks (command execution, search, diff, history) to small sub-agents. Consult before running a command with long output or a wide search.

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. Do not delegate when you need the exact content, when the operation is trivial, or when it requires delicate reasoning: the sub-agents run on tiny models.

# Decision table

| Situation | Decision |
|---|---|
| Command with long or lengthy output (simulation, build, regression) | Delegate to `run` with the exact `csh` command writing to a log file, and a timeout |
| Finding where something appears in a large repository | Delegate to `find` |
| Size and nature of a change between two revisions | Delegate to `diff` |
| Who or what introduced a change | Delegate to `git` or `svn` |
| Reading a small file or a few lines | Read directly |
| Writing or modifying a file | Do it yourself |
| Short command whose output fits in a few lines | Run it yourself |

# How to phrase the request

1. Ask a precise question ("which tests fail and why?"), not a vague instruction.
2. Give the minimal context: paths, references. For `run`: the exact command written for `csh`, redirecting its output to a log file (`command >& job.log`), AND a timeout in seconds chosen from the expected duration. `run` filters the log instead of reading it whole, and refuses to start without the command and the timeout.
3. State the expected format only if it differs from the default report.
4. Do not paste large content into the request.

# After the answer

- Trust the report, but verify before any irreversible action.
- If it says `truncated: yes`, or lists uncertainties, ask a narrower question instead of rereading the raw content.
- Do not ask a sub-agent the same question again without new information.
