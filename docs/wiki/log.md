# Wiki log

Chronological, append-only record of graph operations — series landing,
audits, schema changes. One `## [date] kind | slug` entry per operation,
terse bullets, newest at the bottom; entries are never edited or
reordered.

## [2026-08-11] series | plan 001, CTC alignment (merged as PR #2)

- node added: `ctc-alignment` (six scenes, deep_learning/)
- edge delivered: `counting-rules` → `ctc-alignment` (PartitionRule's
  promise, closed by `CountingAlignments`)
- edges promised: → probability foundations (PR body named it the next
  branch), → beam search / gradient / peaky dynamics (Ideas queue)
- note: predates the wiki; recorded retroactively from plan 001 and the
  PR body

## [2026-08-11] scaffold | wiki bootstrap + repo agents

- created docs/wiki/ (README, INDEX) on branch
  feat/probability-independence, plan 002
- INDEX seeded by hand: 4 nodes, 3 delivered edges, 5 promised
- agents added: pedagogy-researcher, source-verifier, connection-auditor
  (.claude/agents/); wired into CLAUDE.md Step 0 and Phase 4

## [2026-08-11] schema fix | graph-first auditing

- connection-auditor now reads INDEX.md and its `Last audited:` stamp
  first, then diffs from the stamp (`git diff --name-only stamp..HEAD`)
  — no naive full crawls; full crawl is a flagged fallback
- trigger: maintainer feedback while the seed audit was in flight
- INDEX.md gained the stamp; whoever applies audit findings updates it

## [2026-08-11] series | plan 002, independence (in progress)

- node added: `independence` (six scenes, probability/)
- edges delivered: `counting-rules` → `independence` (grid reweighted to
  areas), `ctc-alignment` → `independence` (`ChainsOfTrials` teaches the
  per-frame product CTC purchases)
- edge promised: `independence` → `conditional-probability` (plan 003,
  next branch per maintainer)
- pending: seed audit report, then first `Last audited:` stamp

## [2026-08-11] audit | seed audit applied (full crawl)

- scope: entire repo (seed verification of the hand-built graph; full
  crawl by design, per the graph-first rule's fallback)
- findings: 5 promised-not-delivered, 3 delivered-not-recorded,
  5 possible-not-yet-made, 5 graph-health
- fixed: stale `deep_learning/` Scope ("does not exist yet" → links to
  `probability/`, names the remaining queue); combinatorics → CTC link
  made explicit; the phantom "renormalization teaser" claim removed
  from three documents (no scene contains it)
- edges corrected: ctc→independence narrowed to "delivered
  (unconditional half)"; promised rows added for ctc→conditional,
  ctc→dynamic-programming, counting→binomial-distribution,
  independence→softmax/log-likelihood
- new connections made (README cells): shrinking pool = sampling
  without replacement (combinatorics ↔ probability); the word as
  common cause = why LMs help CTC (probability ↔ deep_learning)
- deferred: alignment-counting shape in combinatorics `WhenToUseIt`
  (re-render; queued in its Ideas); Bernstein ↔ inclusion–exclusion
  device reuse (recorded, acts at build time)
- stamp: set to `75e5cf9`

## [2026-08-11] series | plan 002 finalised (PR #3)

- corrects the plan-002 entry's "pending" line: seed audit applied and
  stamped (see previous entry)
- two CodeRabbit rounds resolved; declines recorded (ADR 006, ADR 007)
- final 1080p60 render verified: 6 files, native 0.75× pace
- next: plan 003, conditional probability — fresh branch after merge;
  carries ctc→conditional residual and the renormalized-slice picture

## [2026-08-11] series | plan 003, conditional probability (in progress)

- node built: `conditional-probability`
  (probability/conditional_probability_manim.py, six scenes; closer is
  `WhenToCondition` — sibling module owns the `WhenToUseIt` name)
- edges closed: `independence` → `conditional-probability` (renormalized
  slice delivered; stepped cut named as P(A|B));
  `ctc-alignment` → `conditional-probability` (conditional independence
  taught with the two-coin example; "given the input" named)
- edge promised: `conditional-probability` → Bayes series (the series
  ends at the named front door)
- devices extended: stepped-cut lineage named; shrinking pool's factors
  licensed as conditional probabilities
- also this branch: CodeRabbit tuned for the bookkeeping (see plan 003)

## [2026-08-11] audit | incremental, plan 003 branch

- scope: diffed 75e5cf9..23c47f2 (11 commits — seed-audit application,
  PR #3 merge, full plan-003 branch); changed files only, no full crawl
- findings: 3 promised-not-delivered, 3 delivered-not-recorded,
  4 possible-not-yet-made, 3 graph-health
- both edges into conditional-probability verified delivered against
  scene content, not just the README
- Bayes is now promised on screen twice plus four documents — the
  strongest open promise; INDEX row's citation undersells it
- new delivered edge to record: counting-rules → conditional-probability
  (TheMultiplicationRule speaks the rule of product back; C(13,3) check)
- devices to record: square-drawn-as-tree, natural-frequency chips,
  two-slices reading — all inherited by the promised Bayes series
- stale: deep_learning Scope still queues conditional independence,
  which WhenToCondition delivered; plan 003 gaps section still blank
- possible: LOTP ↔ forward trellis (anchors the promised DP edge);
  tree↔grid inversion; 1/16 is ChainsOfTrials' cell; explaining-away
  verified but unbuilt
- stamp: advance to 23c47f2

## [2026-08-11] series | plan 003 finalised (PR #4)

- final 1080p60 render verified: 6 files, native 0.75x pace
- review round: one finding (tuned config's first trial — zero
  bookkeeping churn), the stepped-A geometry fix, applied
- maintainer caught a frame-sampling blind spot (scene 1 overlap);
  lesson recorded in plan 003's review notes
- next: Bayes' rule — the repo's strongest open promise, seeded by
  the front door, the cohort chips, the protocol lesson, and Rosenthal

## [2026-08-11] series | plan 004, Bayes' rule (in progress)

- node built: `bayes-rule` (probability/bayes_rule_manim.py, six scenes)
- edge closed: `conditional-probability` -> `bayes-rule` — the repo's
  strongest open promise (on screen twice + four documents), delivered
  through the front door, the factored prevalence pair, and the host's
  protocol
- edge promised: `bayes-rule` -> log-odds (blocked on logarithms)
- Monty Small's 1/(1+p) enumerated in the phase-2 verification script
  (five values of p) — graduated from verify-first caption to on-screen
  beat; its Ideas bullet retired
- device note: the waterfall is the square-drawn-as-tree with the
  division deferred — the three inherited devices named as one object
  on screen in TheOddsForm

## [2026-08-11] audit | incremental, plan 004 branch

- scope: diffed 23c47f2..67713b8 (9 commits — plan-003 finalisation and
  PR #4 merge, full plan-004 branch); changed files only, no full crawl
- findings: 3 promised-not-delivered, 4 delivered-not-recorded,
  4 possible-not-yet-made, 4 graph-health
- conditional→bayes verified delivered against scene content; the
  Monty/Fall/Crawl arithmetic and the 1/(1+p) endpoints re-checked
- Monty Small bookkeeping was incoherent (anchors said "NOT enumerated"
  while the docstring claimed verification): fixed by writing the
  record into the anchors — five p values with exact results
- INDEX device bullets still called the Bayes series "promised" — the
  watch-every-series staleness, third occurrence; fixed
- one logarithms concept closes two promises (bayes→log-odds and
  deep_learning's log-space bullet) — both queues now cross-reference
- plan 004 known-gaps placeholder filled (same genre, second time)
- stamp: advance to 67713b8
