# AI in the Development Routine

A living collection of AI-for-development learnings, focused on practical application in day-to-day software engineering.

This repository is a place to record things learned online about using AI in routine software development, and to note how that knowledge applies to real software engineering work.

Open this repo in Claude Code. [CLAUDE.md](CLAUDE.md) is the short fact sheet. A Stop hook runs `python3 scripts/check_collection.py` and will not let a session finish while the index or a relative link is wrong.

To use the same loop on an application you ship, copy [starter/](starter/README.md) onto that repo and put real commands in `scripts/verify.commands`.

## Notes

| Date | Note |
| --- | --- |
| 2026-11-16 | [Escalate models only when stuck](notes/2026-11-16-escalate-models-only-when-stuck.md). Keep the strong model for plan, second failure, and hard judgment—not a pasted multi-agent zoo. |
| 2026-11-16 | [Spec first, then a diff you understand](notes/2026-11-16-spec-first-then-diff-you-understand.md). Human decides, AI executes: Spec → plan → verified slices → no blind Accept All. |
| 2026-11-13 | [Enforce the correction, then automate](notes/2026-11-13-enforce-corrections-before-automation.md). Lauren Tan's SpaceXAI method, adapted to a Claude Code workday. |

## Layout

| Path | What it is |
| --- | --- |
| [CLAUDE.md](CLAUDE.md) | Facts Claude Code loads every session. |
| [verify-notes](.claude/skills/verify-notes/SKILL.md) | How to prove a change to this collection. |
| [features/](features/README.md) | What a person does here, and what proves it. |
| [starter/](starter/README.md) | The same loop to copy onto an application repo. |
| [check_collection.py](scripts/check_collection.py) | The check the Stop hook runs. |
