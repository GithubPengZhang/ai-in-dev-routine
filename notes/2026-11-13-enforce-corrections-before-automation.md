# Enforce the correction, then automate

Recorded 2026-11-13 from a Chinese carousel of Lauren Tan's talk, checked against the talk transcript.

**Source.** Lauren Tan (`@poteto`), Principal Engineer at SpaceXAI, on the Grok Bot client. Talk: *All Code Is Slop (Except Mine)*, AI Engineer Code Summit, 11 November 2026. The carousel is a Chinese summary by 老王的 AI 工坊 (整理 @leo_xiaolei). Public write-ups that fill in the method: [desty](https://desty.github.io/en/blog/81-pstack-merge-without-review/) and the [session transcript](https://agents.conffab.com/aie-code-26/live/keynotes/sessions/1794420600.md). Her plugin is [pstack](https://github.com/cursor/plugins/tree/main/pstack). The PR counts below are her team's own figures, not an independent benchmark.

**Setup this note assumes.** "Cloud Code" here means Claude Code, the CLI agent. The same order applies to a Cursor cloud agent; only the filenames change (`AGENTS.md` and project skills, instead of `CLAUDE.md` and `.claude/skills`).

## What she is actually doing

The carousel's seven points are one loop, in this order:

1. **Clean the code the agent will copy.** Agents imitate the surrounding code. A leftover hack, a `setTimeout` "fix it later," or a comment that says "never do this" becomes the template for the next change. In her codebase, comments fell from about 65,800 (31 July) to about 1,200, because comments go stale, people do not read them, and an agent will cite them as a reason to skip the real fix. Comments are the weakest place to store a rule.

2. **Make the correction enforceable.** Each time she corrects an agent she asks whether that mistake can become a lint, a type, a test, or a better API that makes the bad path unrepresentable. A longer instruction file does not do this. Lint and the compiler fail CI. A prompt can be forgotten, and the first time it is forgotten the bad code is back in the repo for the next agent to copy. Lint messages should say what to do instead, because that message is the instruction the agent actually reads.

3. **Close the habitual bugs in the architecture.** Dune, their agent-oriented app framework, is the example, not a recipe to copy. Product code cannot call React `useEffect` (only framework internals). One folder per feature. Import boundaries between Electron main and renderer fail CI, so a 16 ms frame budget cannot be broken by a stray import. No comments in code. The design goal is that the shortcut is the correct path. Those bans are *their* repeated failures. A Java service, a Python pipeline, or a robot repo has different habitual bugs. Encode those, not hers.

4. **Give the agent a way to run and look.** Runtime verification means the agent drives the real product with the same tools a person would use. Two pieces make that cheap to repeat:
   - A **feature map**: for each user-facing feature, what it is, how a person reaches it, and what observable result proves it works. That is shared vocabulary. "The thing in the left sidebar" stops being a guess.
   - A **small CLI** the agent reuses (`doctor`, open the feature, snapshot, screenshot, cleanup). Reuse cuts tokens and is itself testable. pstack's `/create-verification-skill` generates this as Launch, Doctor, Drive, Evidence, and Cleanup, and the skill has to be run once before it counts.

5. **Demand evidence of behavior, not a polished explanation.** Screenshots, short videos, and state diagrams (her `/statechart` skill). A clear write-up is easy for a model to produce and does not show that the feature works. For UI they are also trying property-based testing with [Bombadil](https://github.com/antithesisha/bombadil). A final screenshot is weak if it does not show the path taken and the resulting state (reload after save, the row in the database, the command's real output).

6. **Spend the tokens on verification.** She agrees with Cindy Sridharan that most daily tokens now go to verification (Sridharan put hers near 70%). The layers she named, from ordinary to expensive: unit and functional tests, runtime checks, fuzzing, UI property tests, and formal models (TLA+ for multi-device flows, Lean for a virtualization algorithm). None of these are new. They used to cost too much to write and maintain. Agents make them affordable. Review then shrinks to looking at the evidence, not at every line before merge. Formal methods are a later layer, not step one.

7. **Automate only after the inner loop is reliable.** The low-trust trap is: the agent writes slop, a person checks it, bugs come back, and more agents only make more slop, faster and more expensively. She spent on the order of six months making the environment good before agents ran new builds, found bugs, opened fixes, and auto-merged. The slide in the carousel shows her own monthly PR count rising to about 3,100. In the 11 November talk she said the Grok Bot team merged about 11,000 PRs in October, with a revert rate around half a percent, and that startup and chat-switching got faster over that period. Earlier public figures (about 1,000 in July, about 2,500 in August) are also self-reported. The useful claim is the order, not the count. She still reads code *after* it lands, and turns what she finds into a lint or a redesign. Human review moved; it did not vanish. Irreversible actions still stop for a person.

Trust, in her framing, is something you earn one agent at a time: watch it, then let it drive the app, then encode failures, then run several, then auto-merge the low-risk ones. Parallel agents are a result of trust.

## What a normal job should not copy

- Do not ban `useEffect`, delete every comment, or split Electron processes unless those are *your* repeated incidents.
- Do not turn on auto-merge, scheduled cloud agents, or "ship whatever CI accepts" in week one. Her budget is an AI lab's (she has said on the order of 15 billion tokens a day). A product team pays for a bad loop.
- Do not paste pstack into the repo and hope. The durable part is the order: evidence, then CI for repeated mistakes, then more agents.
- Do not grow `CLAUDE.md` every time the agent misbehaves. That file is the weak layer. It is for facts: how to build, where things live, what the shared names are.

## How to run this in Claude Code

Rank a rule by how hard it is to ignore. Use the strongest one that fits.

| Strength | Where it lives in Claude Code | Survives a forgetful model? |
| --- | --- | --- |
| Bad state cannot be represented | Types, API shape | Yes |
| CI fails | Lint, typecheck, tests, import boundaries | Yes |
| The tool refuses to finish | A `Stop` hook that reruns the check and sends the agent back | Yes, until the hook itself is wrong |
| A procedure the agent can load | `.claude/skills/<name>/SKILL.md` | Only if it invokes the skill |
| A reminder in context | `CLAUDE.md` | No |

### This week

1. **Write the finish line as a pass/fail check** in the prompt, before any code. Example: "Add JSON output. Text output stays byte-identical. Both modes run against `samples/demo`. Paste the two outputs." "Make it better" is not a task.
2. **Keep `CLAUDE.md` short.** Build command, test command, directory map, and the names of the features a user would recognize. When you notice a sentence that says "never do X," that sentence is a candidate to delete after a lint or a test exists.
3. **Add one verification skill for the surface you actually ship.** Path: `.claude/skills/verify-<app>/SKILL.md`. Sections:
   - Launch: the exact command, the ready signal, how to stop it.
   - Doctor: a read-only check that the running app is the one you think it is.
   - Drive: commands or selectors for the three to five flows that break most often. Prefer stable labels over pixel coordinates.
   - Evidence: what to save (command output, screenshot, a row, a log line) and where.
   - Cleanup: stop what this run started. Leave the evidence.

   Run the skill once yourself. A skill that has never been executed is a draft.
4. **Add a feature map only for those same flows.** One short file each: what the user does, how the agent reaches it, what proves it worked, and the gotcha that makes a fake pass (a toast that says "saved" while a reload shows the old value).
5. **On the second correction of the same mistake, encode it before the session ends.** Lint with a message that names the replacement. A failing test. A type that will not compile the bad call. Then remove the nag from `CLAUDE.md`.
6. **Block "I'm done" without a check.** A project `Stop` hook in `.claude/settings.json` can run the test or lint command. Exit code 2, or JSON `{"decision":"block","reason":"..."}`, sends Claude back to keep working. Claude Code already stops after a run of continuations, so a broken hook cannot loop forever. The hook should check a real command, not the wording of the reply.

### This month

7. **Separate the author from the judge.** A second session, preferably a different model, runs the verification skill against the parent and the branch and posts pass or fail. CI being green is not that verdict. The agent that wrote the patch is a poor judge of it.
8. **Read what landed, once a week.** Pick one smell. Turn it into a lint, a type, or a deletion. That post-merge reading is the review she kept.
9. **Match the evidence to the change.** A CLI change runs the command. A UI change walks the flow and saves a screenshot. A migration replays a saved input. A performance change compares a before and an after taken the same way. A persistence change reloads.

### Not yet

10. **Property tests and formal models** for the one flow that keeps escaping ordinary tests (a retry state machine, a permissions matrix, a multi-step sync). TLA+ and Lean are optional tools for that flow, not a new platform.
11. **Outer-loop automation** (a cloud agent that opens fix PRs, any auto-merge) only after, for a few weeks: reverts are rare, the same review comment is not returning, and the independent check fails in public when the change is wrong. Start with small, easy-to-revert patches. Deploys, data deletion, and force-push stay manual.

## A workday shape

- Start the task by naming the command or click that will prove it, and the artifact you expect to see.
- Let Claude Code implement in a small diff.
- Make it run that proof. If your app has a UI, it uses the verification skill. If it is a library or service, it runs the tests and one real invocation, and pastes the output.
- If you correct it, the same session adds the lint, type, or test. The chat agreement is not the end of the correction.
- Merge when the evidence is in the PR. The explanation is optional. The output is not.

## How to tell it is working

Count these for a few weeks. They are cheaper than counting PRs.

- Repeated review comments on the same kind of mistake. If they continue, the rule is still a sentence.
- Reverts and incidents after merge.
- Tasks where the agent claimed success without running the real path.
- Token cost per change. Verification should be most of the spend. A second and third agent should wait until the first one stops lying.

## Sources

- Session transcript, 11 November 2026: https://agents.conffab.com/aie-code-26/live/keynotes/sessions/1794420600.md
- Carousel summarized in the images attached on 13 November 2026 (slides 02–07 and the seven-point recap).
- Adoption order and Dune's rules, as reported from her talks and pstack: https://desty.github.io/en/blog/81-pstack-merge-without-review/
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code hooks (`Stop` continues the agent on exit code 2): https://code.claude.com/docs/en/hooks
