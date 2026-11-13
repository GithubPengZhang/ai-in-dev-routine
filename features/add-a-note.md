# Add a learning note

## What the person does

They share something they learned about using AI in software work and ask for it to be recorded, with how it applies to a normal engineering job.

## How the agent reaches it

1. Add `notes/YYYY-MM-DD-short-title.md`.
2. Add a row to the Notes table in `README.md`. The link target is the new file.

## What proves it works

`python3 scripts/check_collection.py` prints `ok:` and exits 0. The new file is one of the linked notes.

## Gotcha

A note that is not linked from `README.md` is invisible from the index. Saying the note was added is not a pass.
