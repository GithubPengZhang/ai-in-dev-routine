---
name: verify-notes
description: Prove a change to this learning collection by running the index and link check. Use when adding a note, editing the README, or before claiming the work is done.
---

# Verify this collection

## Launch

There is no server. The product is the markdown collection. From the repository root:

```bash
python3 scripts/check_collection.py
```

Ready means the process prints a line that starts with `ok:` and exits 0.

## Doctor

Confirm the command you ran is `scripts/check_collection.py` in this repo, and that the `ok:` line counts the notes you expect. A check run in a different directory does not count.

## Drive

For a new or edited note:

1. Open `notes/YYYY-MM-DD-short-title.md` and the Notes table in `README.md`.
2. Confirm the table links to that file.
3. Run the check.

## Evidence

Paste the `ok:` line. If the check exits 2, paste the bullet list and fix those items. A summary of what you changed is not evidence.

## Cleanup

Nothing to stop. Do not delete the note or the check output.

## Gotcha

A note file with no README row looks finished in the chat and is missing from the index. The check fails that case on purpose.
