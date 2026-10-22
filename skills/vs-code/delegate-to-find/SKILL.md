---
name: delegate-to-find
description: "When and how to delegate a wide codebase search to the find sub-agent. Consult before a search across many files."
---

# When to delegate

Delegate when the raw output would be large AND you only need a conclusion. The sub-agent runs on a small model: do not give it work that needs delicate reasoning.

| Situation | Decision |
|---|---|
| Finding where something is defined or used in a large repository | Delegate to `find` |
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

**Where is it defined?** Ask `find`: "Where is the entity `uart_tx` declared and where is it instantiated?" Reply: the declaring file and each instance with `label : entity work.uart_tx`. Next: read the instance you care about.

**Who drives this signal?** Ask `find`: "Which processes or assignments drive `tx_busy` in `rtl/`?" Reply: lines with `<=`, `assign` and port-map connections. Next: read the one that matters; ask again in the parent module if the signal is renamed.

**Hierarchy of a block.** Ask `find`: "List the modules instantiated directly in `soc_top.sv`, with their instance names." Reply: a short list. Next: repeat for a child only if needed.

**Where is this parameter used?** Ask `find`: "Where is the generic `DATA_WIDTH` set or overridden?" Reply: the default value and each override with its file and line.

**What does this big file say?** Ask `find`: "In `doc/spec.md`, what does it say about reset behavior?" Reply: the relevant lines, with line numbers. Next: read those lines if the answer is not enough.

**Nothing found.** Reply: `no match found for uart_rx`. Do not conclude the code is absent: try other spellings, a different directory, or ask `git` or `svn` whether it was renamed.

# Do not delegate

- A file you will edit: read the exact lines yourself, a summary is not enough to edit safely.
- A small file or a known path: read it directly.
- "Is this design correct?": it needs reasoning, so keep it.
