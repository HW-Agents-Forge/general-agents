---
name: delegate-to-diff
description: "When and how to delegate the summary of a large change to the diff sub-agent. Consult before reading a long diff."
---

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. The sub-agent runs on a small model: do not give it work that needs delicate reasoning.

| Situation | Decision |
|---|---|
| Size and nature of a change between two files, directories or revisions | Delegate to `diff` |
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

**Two directories.** Ask `diff`: "Compare `release_1.2/` and `release_1.3/`." Reply: number of files, a line each, risks such as "interface of `fifo` changed". Next: read the risky files yourself.

**Two revisions.** Ask `diff`: "Summarize `git diff v1.2 v1.3` for `rtl/`." Reply: groups by directory and any removed test. Next: ask `git` who removed that test.

**Before a review.** Ask `diff`: "Summarize the uncommitted changes in the working copy." Reply: files and a one-line summary. Next: decide what to commit or revert yourself.

# Do not delegate

- A change of a few lines: read the diff yourself.
- A file you will edit: read the exact lines yourself.
- "Is this change correct?": it needs reasoning, so keep it.
