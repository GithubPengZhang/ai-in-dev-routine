# Escalate models only when stuck

Recorded 2026-11-16 from Chinese posts that paste a Claude Code “org chart”: Sonnet for the main session, Haiku sub-agents for search/grep/audit, Opus as consultant, worktree-isolated audit, and “show the diff before you touch files.”

**Source.** Screenshots collected 2026-11-16 (芃臣说生活 / related carousels). Related install noise: Leo Lab’s pstack copy-paste table and `/setup-pstack` then `/poteto-mode`. The durable encode/evidence order remains [enforce the correction, then automate](2026-11-13-enforce-corrections-before-automation.md).

## What is sound

- **Do not burn the strongest model’s context on grunt work.** Search dumps and test log spam belong in a cheaper pass when your tool supports it.
- **Escalate on purpose.** Useful moments for a stronger model (or a second session): before the plan is locked, when the *same* error appears a second time, and for a hard final judgment—not for every file write.
- **Isolate the judge when you can.** An audit in another worktree or session is the same idea as “the author is a poor judge of the patch.”
- **Diff before large writes** when the plan is still soft. That is human control, not a model brand.

## What to skip as week-one ritual

- A fixed three-Haiku zoo (`search` / `grep` / `audit`) hard-coded into [CLAUDE.md](../CLAUDE.md). That file is for facts; model nicknames and vendor version strings go stale.
- “Hand every small choice to JEV” (or any named router) as a universal rule. Deterministic retries are fine; opaque auto-choosing of paths is not a substitute for Spec acceptance.
- Installing pstack / poteto-mode *before* you have a finish-line check and one verification skill. The plugin does not invent reliability; it packages a loop.
- Treating “adversarial review wastes tokens” as permission to skip review. Skip theatrical roast-of-the-diff when independent evidence already exists. Keep humans on irreversible actions.

## How to run this without the zoo

1. One main agent implements against a named proof ([spec-first note](2026-11-16-spec-first-then-diff-you-understand.md)).
2. On first failure: fix in-session, re-run the proof.
3. On second identical failure: new session and/or stronger model, with the failing evidence pasted in. Prefer encode (lint/test/type) over a third chat debate.
4. Before merge: run the project check yourself or via a verify skill. Here that is `python3 scripts/check_collection.py` and the `ok:` line.

## How to tell it is working

- Stuck loops end after one escalation, not five same-model retries.
- CLAUDE.md stays short; skills and scripts hold procedures and enforcement.
- Token spend shifts toward verification evidence, not toward more authoring agents.
