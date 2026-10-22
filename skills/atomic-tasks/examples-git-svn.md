# Examples for `git` and `svn`

The two agents work the same way; replace one by the other according to the repository.

## `git`

**Who changed this line?** Ask `git`: "Who last changed line 88 of `rtl/uart_tx.vhd` and in which commit?" Reply: one commit, author, date, message.

**When did it break?** Ask `git`: "Which commits touched `rtl/uart_tx.vhd` since 2026-09-01?" Reply: a short list. Next: ask `diff` for the most suspicious commit.

**State of the tree.** Ask `git`: "Is the working copy clean? List modified files." Reply: `state: modified` and the files.

## `svn`

**What changed in a revision?** Ask `svn`: "What did revision 4521 change?" Reply: files and the log message. Next: ask `diff` for details if needed.

**Who touched this file recently?** Ask `svn`: "Last five revisions of `rtl/top.vhd`, with authors." Reply: five lines.

**Working copy state.** Ask `svn`: "Status of the working copy: modified, missing and conflicted files." Reply: `state: conflict` and the conflicted files. Next: resolve them yourself; sub-agents never change the copy.
