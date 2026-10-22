# Examples for `diff`

**Two directories.** Ask `diff`: "Compare `release_1.2/` and `release_1.3/`." Reply: number of files, a line each, risks such as "interface of `fifo` changed". Next: read the risky files yourself.

**Two revisions.** Ask `diff`: "Summarize `git diff v1.2 v1.3` for `rtl/`." Reply: groups by directory and any removed test. Next: ask `git` who removed that test.

**Before a review.** Ask `diff`: "Summarize the uncommitted changes in the working copy." Reply: files and a one-line summary. Next: decide what to commit or revert yourself.
