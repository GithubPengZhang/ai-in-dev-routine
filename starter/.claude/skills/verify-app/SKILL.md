---
name: verify-app
description: Drive this application and collect proof that the changed behavior works. Use before claiming a task is done, and when a change touches a user-facing flow.
---

# Verify this application

## Launch

Run the start command recorded in `CLAUDE.md`. Record the signal that shows the process is ready, and the command that stops it.

## Doctor

Confirm you are driving the build under test, not a stale process. Use a read-only check (port, version, health URL, or the binary's `--version`) and write down what you observed.

## Drive

Open `features/README.md` and the file for the flow this change touches. Follow that file's path. Prefer the commands or stable labels written there. If the flow has no feature file yet, add one before claiming success: what the person does, how to reach it, what proves it, and the gotcha that looks like a pass.

## Evidence

Run:

```bash
python3 scripts/verify.py
```

Paste the `ok:` line. For a UI change, also save a screenshot of the flow after the action. For a saved value, reload and show the stored value, not only the success toast. For a CLI change, paste the command output. For a performance change, paste a before and an after taken the same way.

## Cleanup

Stop only what this run started. Leave the evidence in place.

## Gotcha

`scripts/verify.commands` must contain real commands. A missing file, or a file that is only comments, exits 2. That is a failed finish, not a skipped step.
