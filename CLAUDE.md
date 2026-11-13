# AI in the development routine

Facts for Claude Code in this repository.

## What this repo is

A living collection of notes on using AI in day-to-day software engineering. One note per learning, under `notes/`.

## Commands

- Check the collection: `python3 scripts/check_collection.py`
- Run the harness checks: `python3 scripts/test_harness.py`

The Stop hook in `.claude/settings.json` runs `scripts/stop_hook.sh`. A session is not finished while that check exits 2.

## When you add or change a note

1. Write `notes/YYYY-MM-DD-short-title.md`.
2. Add a row to the Notes table in `README.md` that links to that file.
3. Keep relative links inside this repo resolvable.
4. Run `python3 scripts/check_collection.py` and include its `ok:` line as the evidence.

## Layout

- `notes/` holds the learnings.
- `features/` says what a person does here and what proves it.
- `starter/` is copied onto an application repo. The collection check does not read inside it, except for links that point at it from `README.md`.
- `.claude/skills/verify-notes/` is how to prove a change here.

When the same mistake shows up twice, encode the fix in `scripts/check_collection.py`. Do not add a "never do X" line to this file.
