# ADR 009: CodeRabbit reviews are a budget — one local pass, two bot reviews

Status: accepted — adopts a practice from the maintainer's `job-search`
repo, and declines three parts of it.

## Context

The bot's allowance is a rolling per-developer window that CodeRabbit's
fair-usage policy lowers with trailing-week volume (five reviews per hour
under thirty reviews in seven days, one per hour at sixty or more); the
local CLI has its own five per hour. The allowance is per developer, so
this repo and every other repo the maintainer runs draw on the same one.

Measured on PRs #15–#19 (plan 018): every PR opened non-draft and drew
its automatic review, and then the phase-5 fix push drew a **second
automatic review nobody asked for**; PR #17 spent a third through an
explicit request. Rate-limit notices appeared on PRs #15, #16 and #17.
Phase 4 ran the local pass and the `connection-auditor` side by side, so
the auditor's findings — which routinely build things — changed the diff
after the local pass had read it. And `docs/adr/` reached the reviewer
only through a path instruction that applies when an ADR file is in the
diff, which is how a declined finding came back for three rounds.

## Decision

Adopted, from `job-search`'s loop:

- `auto_pause_after_reviewed_commits: 1`. The bot reviews when the PR
  opens, then pauses; later pushes cost nothing until a review is asked
  for.
- **At most two bot reviews per PR**: the automatic one, and one
  `@coderabbitai review` only when a finding required a change. Every
  thread is read first; every fix is batched into one push; the request
  is posted inside the rate-limit window. The 1080p render waits until
  the bot round is closed — a late finding would stale it — and the
  plan's phase-5 closure then pushes free under the pause. A third
  review is the maintainer's call.
- **Phase 4 is a sequence**: `connection-auditor`, its findings applied
  and committed, a self-check of the diff against CLAUDE.md, then **one**
  local CodeRabbit pass on the diff the PR will carry. It reruns only
  when code changed after it.
- **The same-spot stop rule**: two consecutive local passes each finding
  a new edge in the same function or scene stop the loop; the check that
  would have caught both (a test, or a layout-linter rule) is written
  before the next pass.
- `docs/adr/*.md` joins `CLAUDE.md` in `code_guidelines.filePatterns`, so
  the declined record is in front of the reviewer on every run.

Declined:

- **Draft-first PRs.** `job-search` opens a draft so its close narrative
  can carry the real PR number and still be reviewed with the code. Here
  the plan's phase-5 entry records the bot round itself, so it
  necessarily follows the review; there is no CI to wait on; and the
  pause already makes the later pushes free. The draft step would be
  ceremony.
- **A separate recurring-findings checklist.** CLAUDE.md already is one —
  "rules derived from failures that actually happened here" — with most
  of it mechanised (`make check`, `tests/test_text_markup.py`, the layout
  linter), and the declined record is this directory. A second list
  would drift from the first.
- **Squash merges and the builder / reviewer / critic split.** Not
  review-budget questions; this repo's merge commits and phase gates
  stand.

## Consequences

A plan's phase-5 checklist entry records the bot reviews spent (one or
two). A PR that needs a third is a signal, not a routine — either the
local pass was skipped or run on a diff that later changed, or a finding
class is recurring and wants a rule. If the pause proves too loose,
`auto_review.enabled: false` (fully on demand) is the next lever; if
draft-first ever earns its keep — CI arrives, or a narrative must be
reviewed with its PR number — edit this entry to say so.
