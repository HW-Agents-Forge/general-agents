Reference for writing and fixing csh and tcsh commands, one-liners and scripts: the bash habits that fail in csh, their exact replacements, and the pitfalls that cost time. Consult it before writing or editing any csh or tcsh command or script, and when a command for the `run` agent must be written for csh.

# Bash habit to csh

| Bash | csh / tcsh |
|---|---|
| `export A=1` | `setenv A 1` |
| `A=1` | `set A = 1` (shell-local: a child process sees it only after `setenv`) |
| `$?` (exit status) | `$status` (works in csh and tcsh; `$?` only in tcsh) |
| `cmd > f 2>&1` | `cmd >& f` (append: `>>& f`) |
| `cmd 2> f` | no direct form: `( cmd > /dev/null ) >& f` |
| `$(cmd)` | `` `cmd` `` (`$(...)` fails with "Illegal variable name") |
| `f() { ...; }` | not available: use an `alias` or a separate script ("Badly placed ()'s") |
| `for x in a b; do ...; done` | `foreach x (a b)` ... `end` |
| `if [ "$a" = b ]; then` | `if ("$a" == b) then` ... `else` ... `endif` |
| `[ -e f ]`, `-d`, `-f` | `if (-e f)`, `-d`, `-f`, `-r`, `-w`, `-x`, `-z`; negate with `! -e f` |
| `a=(1 2)`, `${a[1]}`, `${#a}` | `set a = (1 2)`, `$a[1]`, `$#a` |
| `$#`, `$@` | `$#argv`, `$argv` (`$1` also works; `$0` is the script name) |
| `read x` | `set x = $<` |
| `$((1+2))` | `@ x = 1 + 2` |
| `case` | `switch (w)` / `case a*:` / `breaksw` / `endsw` |
| `trap ... INT`, `set -e` | `onintr label`; no `set -e`: test `$status` yourself |

Unchanged: `source f`, `exit N`, `&&`, `||`, pipes, `<< EOF` here-documents (variables are expanded), `cd`, `alias n "cmd"`.

# Pitfalls

1. **A glob with no match is an error.** `echo *.zzz` prints "No match." and aborts the command or the script. Use `set nonomatch` to get the literal text, or test with `ls` first.
2. **Loops start their own line.** Put `foreach`, `while`, `if ... then` and `switch` first on their line. csh re-reads the line holding `while`, so `set i = 0; while ($i < 2)` on one line can loop forever, and in `csh -c '...'` a `foreach` after another command may run only once. Write a script file instead of a long one-liner.
3. **`@` needs spaces.** `@ i = 2 + 3` works, `@ i=2+3` fails ("Badly formed number").
4. **An undefined variable is an error** ("x: Undefined variable."). Test first: `if ($?x) then`.
5. **`\$` does not escape inside double quotes.** `"\$Q"` expands `$Q` and keeps the backslash. To pass a literal `$` to another program, use single quotes: `sh -c 'echo $Q'`.
6. **Pipeline status is not portable.** tcsh reports failure when any stage fails, classic csh uses the last stage. When the status matters, redirect to a file instead of piping.
7. **`2>` is not stderr.** csh reads `2` as an argument and `>file` as stdout.
8. **Shebang:** `#!/bin/csh -f`. The `-f` skips `~/.cshrc`, which is faster and predictable.

# When not to use csh

Beyond about 20 lines, or as soon as you need functions, real error handling or string processing, write the logic in Python or bash and call that script from csh. csh is fine for environment setup and short launchers.

# Skeleton

```csh
#!/bin/csh -f
if ($#argv != 1) then
  echo "usage: $0 test_name" >&2
  exit 2
endif
set test = $argv[1]
set log = ${test}.log
make sim TEST=$test >& $log
set rc = $status
if ($rc != 0) then
  echo "FAILED: $test (status $rc), see $log" >&2
  exit $rc
endif
echo "PASSED: $test"
```

# With the `run` agent

Give `run` the command in csh syntax, naming the shell, with the output redirected to a log and a timeout: `make sim TEST=smoke >& smoke.log`, timeout 1800 s. For a long chain, put it in a script file and run `./script.csh test_name >& log`.
