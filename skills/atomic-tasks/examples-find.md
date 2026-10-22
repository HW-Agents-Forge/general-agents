# Examples for `find`

**Where is it defined?** Ask `find`: "Where is the entity `uart_tx` declared and where is it instantiated?" Reply: the declaring file and each instance with `label : entity work.uart_tx`. Next: read the instance you care about.

**Who drives this signal?** Ask `find`: "Which processes or assignments drive `tx_busy` in `rtl/`?" Reply: lines with `<=`, `assign` and port-map connections. Next: read the one that matters; ask again in the parent module if the signal is renamed.

**Hierarchy of a block.** Ask `find`: "List the modules instantiated directly in `soc_top.sv`, with their instance names." Reply: a short list. Next: repeat for a child only if needed.

**Where is this parameter used?** Ask `find`: "Where is the generic `DATA_WIDTH` set or overridden?" Reply: the default value and each override with its file and line.

**What does this big file say?** Ask `find`: "In `doc/spec.md`, what does it say about reset behavior?" Reply: the relevant lines, with line numbers. Next: read those lines if the answer is not enough.

**Nothing found.** Reply: `no match found for uart_rx`. Do not conclude the code is absent: try other spellings, a different directory, or ask `git` or `svn` whether it was renamed.
