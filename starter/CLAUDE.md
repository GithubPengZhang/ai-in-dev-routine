# Application facts

Replace this file after you copy `starter/` onto your repository. Keep it short. This file is for facts the agent cannot get from a failing command.

## Commands

- Finish check: `python3 scripts/verify.py`
- The commands that check runs live in `scripts/verify.commands`, one per line.

The Stop hook runs `scripts/stop_hook.sh`. A session is not finished while that exits 2.

## Layout

- `features/` maps each user-facing flow: how a person reaches it, how to drive it, what proves it, and the fake-pass gotcha.
- `.claude/skills/verify-app/` is the procedure for collecting that proof.

Name the build command, the test command, and the directories a person would recognize. When the same mistake happens twice, encode it in a lint, a type, a test, or `scripts/verify.commands`, and delete the nag from this file.
