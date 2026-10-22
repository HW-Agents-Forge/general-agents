# Combining agents

**New failure after a merge.** `run` (rerun the test, get the error) then `svn` or `git` (who touched the failing file) then `diff` (what that change did) then read and fix yourself.

**Understanding unknown code.** `find` (where is the block and who instantiates it) then read the two or three files it points to. Do not ask `find` to explain the design.

**Checking before a release.** `run` (build and smoke tests, one request each, in parallel if your tool allows) then `diff` (changes since the last release) then `git` or `svn` (state is clean).
