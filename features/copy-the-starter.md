# Copy the starter onto an application repo

## What the person does

They want the same finish-check loop in a repository they actually ship, opened in Claude Code.

## How the agent reaches it

Copy the contents of `starter/` onto the root of that repository. Overwrite only files the person agrees to overwrite. Then replace the sample lines in `scripts/verify.commands` with commands that prove that application.

Read [starter/README.md](../starter/README.md) before copying.

## What proves it works

In the application repo, `python3 scripts/verify.py` prints `ok:` and exits 0. The commands in `scripts/verify.commands` are real checks for that repo, not the commented sample.

## Gotcha

Copying the files without a real `scripts/verify.commands` leaves the Stop hook blocking every session. That block is intentional. A comment-only command file does not count as a check.
