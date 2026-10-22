---
name: delegate-to-svn
description: "When and how to delegate a Subversion history or state question to the svn sub-agent. Consult before reading long svn output."
---

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. The sub-agent runs on a small model: do not give it work that needs delicate reasoning.

| Situation | Decision |
|---|---|
| Who or what changed something, when it broke, state of the working copy (svn) | Delegate to `svn` |
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

**What changed in a revision?** Ask `svn`: "What did revision 4521 change?" Reply: files and the log message. Next: ask `diff` for details if needed.

**Who touched this file recently?** Ask `svn`: "Last five revisions of `rtl/top.vhd`, with authors." Reply: five lines.

**Working copy state.** Ask `svn`: "Status of the working copy: modified, missing and conflicted files." Reply: `state: conflict` and the conflicted files. Next: resolve them yourself; sub-agents never change the copy.

# Do not delegate

- `svn status` on a small tree: the output is shorter than the request.
- Any change to the working copy: sub-agents only read.
- The same question again with no new information.
