# 0009. Shell-agnostic `run` and the `csh-pro` skill

- Status: accepted
- Date: 2026-10-22

## Context

`run` was first written for csh, the author's shell. The agents must work in any terminal. Separately, models drift to bash syntax when asked for csh, which breaks commands handed to `run`.

## Decision

- `run` never translates the parent's command. The parent writes it in its own shell's syntax and names the shell. The prompt carries a small reference table (exit status variable, redirection to a file, read-only log filters) for csh/tcsh, bash/zsh/sh, fish, PowerShell and cmd.
- When no timeout can be enforced (PowerShell or cmd without a tool option), `run` refuses rather than running unbounded.
- A separate `csh-pro` skill documents csh and tcsh for the primary agent, which writes the commands. Its facts are verified against tcsh. It is not preloaded into `run`: preloading injects the whole skill on every call, which costs more than the table `run` already carries.
- Workplace-specific conventions stay out of this repository.

## Consequences

- No agent is tied to one shell; `git`, `svn`, `diff` and `find` already run the same commands everywhere.
- The `run` prompt grew by a table; it is still under 60 lines.
- PowerShell, fish and cmd rows follow the standard syntax but were not run here. Only csh/tcsh was tested.
- The csh skill is a primary-agent aid, not a delegation, and sits at the edge of the project's scope.
