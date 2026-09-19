# Plan 018: the CodeRabbit review budget — one local pass, two bot reviews

Branch: `chore/coderabbit-review-budget`, cut from updated `main`
(f350d3b, the plan-017 merge). Started: 2026-09-19.

The maintainer's ask (2026-09-19): before the next series, read how
`~/Repos/job-search` uses CodeRabbit — its `.coderabbit.yaml`, its
local-plugin loop before a PR, its conservative spending — and bring the
learnings here, revising `docs/workflow.mmd` and the documentation where
the loop changes. No scene, README table or study guide is touched; this
is a process change, so phases 1–3 of the series table collapse.

## What job-search does (observed, 2026-09-19)

Sources: its `.coderabbit.yaml`, `.claude/rules/orchestrator.md` (flow
steps 7–9, delivery discipline), `.claude/rules/coderabbit-checklist.md`,
`docs/diagrams/agent-flow.mmd`.

1. **The allowance is a budget, and it is written down.** The bot's
   allowance is a rolling per-developer window that the fair-usage policy
   lowers with trailing-week volume (five per hour under thirty reviews
   in seven days, one per hour at sixty or more). The local CLI has its
   own five per hour. The allowance is per developer, so **this repo and
   job-search draw on the same one.**
2. **`auto_pause_after_reviewed_commits: 1`.** The bot reviews once
   automatically, then pauses; every later push costs nothing until an
   explicit `@coderabbitai review`. At most two bot reviews per PR: the
   automatic one, and one request only when a finding required a change.
3. **Read every thread, batch every fix into one push, then one
   request** — posted inside the rate-limit window, never before it.
4. **The local pass runs once on the committed branch, and again only
   when code changed after it.** It comes last among the pre-PR reviews
   (after the reviewer and the critic), so it sees the diff the PR will
   carry.
5. **The same-function stop rule.** Two consecutive local passes each
   finding a new edge in the same function stops the loop; a
   whole-output invariant test is written before the next pass (seven
   passes were once spent on one function).
6. **A cheap self-check before the expensive one**: the builder checks
   its diff against the recurring-findings checklist before the local
   pass runs "the same list more expensively".
7. **Declined findings reach the model.** The declined list lives in
   `.claude/rules/*.md`, which `knowledge_base.code_guidelines
   .filePatterns` feeds to the reviewer on every run.
8. Draft-first PRs: the PR opens as a draft (no review), the close
   narrative lands with the real PR number, one push, then "ready" is
   the one automatic review of code and narrative together.

## What this repo does today (measured, PRs #15–#19)

- Non-draft PR opens → automatic review. The phase-5 fix push →
  **a second automatic review nobody asked for** (PR #19: push at
  19:34:51Z, the bot's summary re-processed at 19:36:24Z). PR #17 spent
  a third through an explicit request. Rate-limit notices appeared on
  PRs #15, #16 and #17 — three of the last five.
- Phase 4 runs the local CodeRabbit pass and the `connection-auditor`
  **side by side**, then applies both sets of findings. The auditor's
  findings routinely build things (plan 017's top finding built a beat
  in `AreaNotSums`), so the local pass reviews a diff that then changes,
  and the changed code goes to the PR unreviewed locally — or costs a
  second local pass.
- Local findings are already low (one per pass on plans 015–017): the
  local loop is healthy; the waste is on the bot side and in the
  phase-4 ordering.
- `docs/adr/` reaches the reviewer only through a `path_instructions`
  entry on `docs/adr/**`, which applies when an ADR file is *in the
  diff*. On an ordinary series PR the declined record is not in front of
  the model — the config's own header records a declined finding
  recurring for three rounds.

## Decisions

Adopt:

- **A1. The pause.** `auto_pause_after_reviewed_commits: 1`, with the
  budget stated in the config header.
- **A2. Two bot reviews per PR, by budget.** The PR-open review, and one
  `@coderabbitai review` only when a finding required a change. Read
  every thread first; every fix is batched into **one** push; the
  request goes inside the window. The 1080p render waits until the bot
  round is closed (a late finding would stale it), and the plan's
  phase-5 closure then pushes free under the pause — refined in phase 1
  from "one commit carries fixes, closure and render", which would have
  rendered finals before the re-review could still change a scene. A
  third review is the maintainer's call, not the loop's.
- **A3. Phase 4 becomes a sequence**: `connection-auditor` first, its
  findings applied and committed; then a cheap self-check of the diff
  against CLAUDE.md's Colour / Structure / `Text` rules; then **one**
  local CodeRabbit pass (`--base main`, committed branch) on the diff
  the PR will carry. Rerun only when code changed after it.
- **A4. The same-spot stop rule.** Two consecutive local passes finding
  a new edge in the same function or scene: stop, and write the check
  that would have caught both (a test in `tests/`, or a layout-linter
  rule) before the next pass. This is the repo's existing "add a rule
  when something goes wrong twice", applied to the review loop.
- **A5. ADRs become code guidelines.** `code_guidelines.filePatterns`
  lists `CLAUDE.md` and `docs/adr/*.md`, so declined findings are in
  front of the reviewer on every run, not only when an ADR is in the
  diff.
- **A6. Tone tightened** toward job-search's: terse, cite the CLAUDE.md
  section a finding rests on.

Decline (recorded in the ADR with reasons):

- **D1. Draft-first PRs.** job-search needs the draft because its close
  narrative must carry the PR number *and* be reviewed with the code.
  Here the phase-5 entry records the bot round itself, so it necessarily
  follows the review; there is no CI to wait for; and A1 already makes
  the later pushes free. The draft step would be ceremony.
- **D2. A separate recurring-findings checklist file.** CLAUDE.md is
  already "rules derived from failures that actually happened here",
  most of it mechanised (`make check`, `test_text_markup`, the layout
  linter), and the declined record is `docs/adr/`. A second list would
  drift from the first.
- **D3. Squash merges, the builder/reviewer/critic split, Dependabot
  rules.** Not review-budget questions; this repo's merge commits and
  single-agent phases stand.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Branch; observation of job-search and measurement of PRs #15–#19 pinned above | **John approves decisions A1–A6 / D1–D3** |
| 1 | `.coderabbit.yaml` (A1, A5, A6, header); ADR 009 + index row; CLAUDE.md (phase table rows 4–5, the workflow paragraph, a short "Review budget" section); README "Working on a scene" steps 3–4 and the diagram's alt text | `make check`; the config validated against CodeRabbit's schema (key names checked by computation, not by eye) |
| 2 | `docs/workflow.mmd` — phase 4 as a sequence (auditor → apply → self-check → one local pass, the stop rule as a note), phase 5 with the pause, the one batched push and the conditional single request; `docs/workflow.png` re-rendered | Diagram renders; PNG opened and read against the CLAUDE.md text — every arrow cites a rule that exists |
| 3 | One local CodeRabbit pass on this branch (the new loop, used on itself); no auditor — the change touches no topic or wiki edge | Review clean |
| 4 | PR; the bot's automatic review; batched fixes in one push; one request only if a finding required a change | Bot round closed within budget; the count recorded here |

## Checklist

- [x] Phase 0: decisions A1–A6 / D1–D3 approved by the maintainer as
  proposed, 2026-09-19
- [x] Phase 1: `.coderabbit.yaml` carries the pause, the ADR file pattern,
  the terser tone (229 of 250 characters) and the budget in its header;
  ADR 009 recorded; CLAUDE.md's phase rows 4–5, workflow paragraph and
  "Review budget" section; README steps 3–5 and alt text. Config checked
  against CodeRabbit's published schema by script — and the check
  checked: a copy with an overlong tone fails the schema, a misspelt
  pause key fails the explicit key read (the schema tolerates unknown
  keys, so the key read is what pins the name). `make check` green (285)
- [x] Phase 2: `docs/workflow.mmd` splits CodeRabbit into the local CLI
  and the bot; phase 4 reads auditor → applied → self-check → one local
  pass with the rerun and stop rules as a note; phase 5 reads review 1 +
  pause, an `opt` block for the batched push and single request, finals
  only after the bot round closes. First render failed — a `;` in a
  message is a mermaid statement separator — fixed; PNG re-rendered at
  the committed 2× scale (the README's command now says `-s 2`; it did
  not reproduce the committed file before) on mermaid's default white
  background (the old file was transparent — dark text over whatever
  the page behind it is; not checked on a dark page, a judgement call);
  PNG opened and each new arrow read against CLAUDE.md's Review budget
- [x] Phase 3: one local pass on the committed branch (`--base main`),
  one minor finding: "regenerate `docs/workflow.png` from the updated
  diagram". Not valid, and not a decision (so no ADR) — the PNG was
  regenerated in the phase-2 commit; the reviewer cannot read a binary.
  Checked by computation, not by assertion: a fresh render of the
  committed `.mmd` is pixel-identical to the committed PNG (1568×1730).
  Nothing changed after the pass, so no rerun: local passes spent, 1
- [x] Phase 4: PR #20 opened. The bot's automatic review: no actionable
  comments, and the summary then read "Reviews paused …
  `auto_pause_after_reviewed_commits`" — the pause is read from the PR
  branch's own config and took effect on its first PR. No finding, so no
  request: **bot reviews spent, 1 of 2**; local passes, 1. The bot
  reported the allowance at 4 reviews per hour on the trailing week, 3
  available after this one. This closure pushes under the pause.
  Merge authorized by the maintainer, 2026-09-19
