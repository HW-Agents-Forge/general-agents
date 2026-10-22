---
name: delegate-to-git
description: "When and how to delegate a git history or state question to the git sub-agent. Consult before reading long git output."
---

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. The sub-agent runs on a small model: do not give it work that needs delicate reasoning.

| Situation | Decision |
|---|---|
| Who or what changed something, when it broke, state of the tree (git) | Delegate to `git` |
| The output fits in a few lines, or you need the exact content | Do it yourself |

# How to phrase the request

1. Ask a precise question, not a vague instruction.
2. Give the minimal context: paths, revisions, a directory to restrict the search.
3. State the expected format only if it differs from the default report.
4. Do not paste large content into the request.

# After the answer

- Trust the report, but verify before any irreversible action.
- If it lists uncertainties or says the result was truncated, ask a narrower question instead of rereading the raw content.
- Do not ask the same question again without new information.

# Examples

**Who changed this line?** Ask `git`: "Who last changed line 88 of `rtl/uart_tx.vhd` and in which commit?" Reply: one commit, author, date, message.

**When did it break?** Ask `git`: "Which commits touched `rtl/uart_tx.vhd` since 2026-09-01?" Reply: a short list. Next: ask `diff` for the most suspicious commit.

**State of the tree.** Ask `git`: "Is the working copy clean? List modified files." Reply: `state: modified` and the files.

# Do not delegate

- `git status` or `git log -3`: the output is shorter than the request.
- Any change to the repository: sub-agents only read.
- The same question again with no new information.
