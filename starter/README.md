# Starter for an application repo

Copy the contents of this folder onto the root of a repository you open in Claude Code. This folder is the week-one loop from the 2026-11-13 note: a short `CLAUDE.md`, one verification skill, a feature map, and a Stop hook that runs a real check.

## Copy

From the application repo root, copy these paths and keep them at those paths:

| Path | Role |
| --- | --- |
| `CLAUDE.md` | Facts only: how to build, how to test, where things live. |
| `.claude/settings.json` | Stop hook. Exit 2 from the check sends Claude Code back to work. |
| `.claude/skills/verify-app/SKILL.md` | Launch, doctor, drive, evidence, cleanup. |
| `features/README.md` | Index of user-facing flows. |
| `features/example-flow.md` | Replace with a real flow. |
| `scripts/verify.py` | Runs `scripts/verify.commands`. |
| `scripts/stop_hook.sh` | What the Stop hook executes. |
| `scripts/verify.commands.example` | Sample. Do not leave this as the only command file. |

Then create `scripts/verify.commands` with one finish command per line. `verify.commands.example` shows the shape. A comment-only file fails the check.

## Prove the copy

```bash
python3 scripts/verify.py
```

`ok:` and exit 0 means every command passed. Exit 2 means the session is not finished.

## After the first repeated correction

Put the correction in a lint, a type, a test, or a line in `scripts/verify.commands`. Delete the matching "never do X" sentence from `CLAUDE.md` once the check enforces it.

Fill `features/` with the three to five flows that actually break. For each one, write how a person reaches it, how the agent drives it, what observable result proves it, and the gotcha that makes a fake pass.
