# Spec first, then a diff you understand

Recorded 2026-11-16 from a Chinese carousel by 阿尔法灵 AI arguing against vibe coding (Karpathy’s term): one-sentence apps feel fast, then the third week’s permission change lands in 800 lines nobody owns.

**Source.** Xiaohongshu-style carousel screenshots collected 2026-11-16 (five-step loop: Spec → plan → piece-by-piece verify → merge understood diffs → AI finishes docs/commits while the human still decides). Pair with [enforce the correction, then automate](2026-11-13-enforce-corrections-before-automation.md): that note is the encode/evidence/scale order; this note is the *start* of a single task.

## The loop worth keeping

1. **Spec, no code.** Goals, inputs, outputs, edges, errors, acceptance. One page is enough. The first message should stop the agent from writing files.
2. **Plan, no code.** Module split, file responsibilities, order, dependencies. You review architecture; the agent waits.
3. **One module at a time + immediate proof.** Tests, typecheck, or the project’s real verify command after each slice. Fix failures before the next module.
4. **Merge only diffs you understand.** No blind Accept All. Unclear chunks get rewritten until a person can own them.
5. **AI drafts the paperwork; you own the irreversible step.** Docs, commit text, release notes are cheap to draft. Merge and push stay human until the evidence is real.

## How this maps here

| Step | In this collection |
| --- | --- |
| Acceptance in the Spec | Same job as naming the pass/fail line before coding ([CLAUDE.md](../CLAUDE.md) + feature map) |
| Immediate proof per module | `python3 scripts/check_collection.py` (or starter `verify.commands` on an app) |
| Understood diffs | Review still happens; it moves toward evidence, not away from judgment |
| Encode later | Second instance of the same mistake → lint/test/type, not another CLAUDE.md “never” |

## A workday shape

- **Feature:** Spec → plan → small diffs → paste check/`ok:` or app output in the PR.
- **Bug:** Name the failing repro first; skip the full Spec if the proof is already a red test. Still refuse Accept All on a mysterious patch.
- **Review:** If you cannot explain a hunk, send it back. Spec compliance is not a substitute for a readable diff.
- **Learning:** “Ask why for every line” is a drill for unfamiliar generated code, not a permanent merge tax when checks already cover the path.

## What not to copy from the carousel

- A fixed “ten minutes on I/O” ritual for every chat.
- Running the full five steps on a one-line fix.
- Treating docs/commits as unsupervised: the agent drafts; you still read before push.

## How to tell it is working

- Fewer “third week” surprises where nobody knows which block owns a behavior.
- PRs where the acceptance command or click was named before the first file write.
- Lower rate of Accept All followed by immediate revert or rewrite.
