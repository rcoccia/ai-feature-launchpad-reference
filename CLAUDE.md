# Control Tower — agent bootstrap

This repository uses the **Control Tower** method. The canonical, always-current instructions live
in **[`.github/copilot-instructions.md`](.github/copilot-instructions.md)** — read that file and
follow it.

This file is a **pointer only** (Claude Code auto-reads `CLAUDE.md`): the canonical file is the
single source of truth, so the method's activation is described in exactly one place and cannot
drift. In short, it tells you to check the repository state first — if there is no `constitution/`,
run inception (`bootstrap-tower`) before any code; if there is, read the loop, rules, and roadmap
and run `plan-slice`. The human commands; you propose.
