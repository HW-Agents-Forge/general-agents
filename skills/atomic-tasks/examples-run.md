# Examples for `run`

Redirections are shown for csh (`>&`); in bash or zsh write `> file 2>&1`. Each "Ask" is the request to send.

**Failing simulation.** Ask `run`: "Run `make sim TEST=smoke >& sim.log`, timeout 1800 s." Reply: `failed`, `errors=3`, "scoreboard mismatch at 1250 ns (3 times)". Next: ask `find` where the scoreboard is, read those lines yourself, fix.

**Regression with many tests.** Ask `run`: "Run `./run_regression.csh >& reg.log`, timeout 7200 s. Which tests failed?" Reply lists the failing test names and the first error of each. Next: pick one failing test and rerun only that test through `run`.

**Build that must succeed.** Ask `run`: "Run `make all >& build.log`, timeout 900 s." Reply: `finished`, `errors=0 warnings=12`. Next: continue; do not read the log.

**Lint or CDC check.** Ask `run`: "Run `lint_run.csh top >& lint.log`, timeout 1200 s. List the distinct error rules and their counts." Reply: three rules with counts. Next: fix the most frequent rule first.

**Job cut short.** Reply: `timeout`, last line "simulating at 40 us". The job was not wrong, only slow. Ask `run` again with a timeout twice as long, or run it yourself in the background.

**Command that needs input.** Reply: `blocked`, last line "Enter license server:". `run` never answers. Fix the environment (set the variable, source the setup script), then ask again.

**Command with a pipe.** Ask `run`: "Run `cat list.txt | xargs -n1 check.csh >& chk.log`, timeout 600 s." `run` wraps it in `timeout 600 <your shell> -c '...'` itself. If the command contains a single quote, `run` refuses: add the timeout yourself.
