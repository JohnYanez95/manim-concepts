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

## [2026-08-11] series | plan 004 finalised (PR #5)

- final 1080p60 render verified: 6 files, native 0.75x pace
- review round: bot and auditor converged on Monty Small from opposite
  sides; the record won over the claim — anchors carry the enumeration
- transition-window rule's first live catch: the rate-label crossfade
- next: logarithms — one series, two promises closed (bayes→log-odds
  and deep_learning's log-space bullet)

## [2026-08-11] series | plan 005, logarithms (in progress)

- node built: `logarithms` (algebra/logarithms_manim.py, six scenes;
  new algebra/ topic)
- the double-unlock closed: bayes-rule -> logarithms (the evidence
  ruler, +2 per head exactly) and ctc-alignment -> logarithms (the
  underflow cliff, log-sum-exp, Graves 2012 correctly attributed)
- also on this branch: workflow sequence diagram + welcome gif on the
  front page; Apache 2.0 license; repo made public
- branch note: first cut sat on a stale main (PR #5 was still open);
  pull-and-verify caught it, merge completed, branch re-cut

## [2026-08-11] audit | incremental, plan 005 branch

- scope: diffed 67713b8..726b19e (9 commits); changed files only
- findings: 4 promised-not-delivered, 5 delivered-not-recorded,
  3 possible-not-yet-made, 4 graph-health — all applied
- the picture-is-a-claim rule caught on the flipped edge itself: three
  documents promised a return-to-zero the ruler never walked; fixed in
  the scene's favour (H, H, T, T — the marker comes home)
- stale-at-delivery occurrences 4 and 5 (probability Scope, the
  deep_learning log-space bullet) repaired; logarithms gains its three
  out-promise rows; calculus/e is the new strongest open promise
- devices recorded: the quartered square's fourth series; the odds
  ladder into log space
- structural fix: phase 3 now includes re-rendering the welcome gif
  when a topic lands (the hand-listed topic row is a staleness surface)
- stamp: advance to 726b19e

## [2026-08-11] series | plan 005 finalised (PR #6)

- final 1080p60 render verified: 6 files, native 0.75x pace; the
  ruler's walk-home confirmed at full resolution
- review round: 2 CodeRabbit findings (the a >= b convention, the gif
  exception) + 16 audit findings, all applied
- the repo is public, licensed Apache 2.0, and its front page explains
  itself (welcome gif + workflow diagram)
- next: calculus/ (unlocks e and ln), or the log-odds inference scene

## [2026-08-11] audit | plan-005 finalisation + box-leak fix

- scope: diffed 726b19e..344f4f1 (PR #6 bot round, merge, post-merge
  box-leak fix); changed files only, no full crawl
- findings: 0 new promised (queue stands at 10 rows),
  1 delivered-not-recorded, 3 possible-not-yet-made, 4 graph-health
- correction: the plan-005 finalisation entry's render claim is stale
  for one scene — scene 6's verified 1080p60 render predates the
  box-leak fix (the log-sum-exp box never faded out). Decision: the fix
  rides the next topic branch (`feat/calculus-e-ln`) as a pre-phase
  commit, no separate fix PR; scene 6 re-renders at that branch's
  finalise gate
- ShrinkCounts' zero-prior beat recorded as a second delivered strand
  of bayes -> logarithms (INDEX row updated)
- noted for the next builds: bits/entropy silently depends on
  expectation (random variables); the binomial pmf already sits in the
  quartered square (group ChainsOfTrials' cells by head count); the
  base-is-a-unit stride device is the natural opening for calculus/
- open maintainer call: root README's likely-next names linear_algebra/,
  which no graph row carries — promise it properly or drop it
- next build: calculus/ (strongest open promise, on-screen ln debt,
  anchors part-verified in plan 005) over random variables
- stamp: unchanged at 726b19e; advance to plan 006's merge commit when
  `feat/calculus-e-ln` lands

## [2026-08-11] series | plan 006, e and ln (in progress)

- node built: `e-and-ln` (calculus/e_and_ln_manim.py, six scenes; new
  calculus/ topic)
- the strongest open promise closed: logarithms -> e-and-ln.
  TheSplitYear replays the deferral caption, TheNaturalStride names
  the mystery constants as ln, and TheDebtRepaid re-reads the
  underflow identity — the graph's only on-screen debt, repaid
- independence -> softmax row updated: the e-half of its double gate
  is delivered; the row now waits on random variables alone
- calculus/ opens one batched out-promise row (derivative toolkit,
  ln as area, Euler's formula, growth in the wild)
- device recorded: the counting strip re-ruled — definition ->
  base-as-unit -> natural units, across algebra/ and calculus/
- root README likely-next updated: random variables leads (per the
  CTC roadmap), linear_algebra/ still listed pending the maintainer
  call the finalisation audit raised
- riding this branch as pre-phase: the box-leak fix + audit
  bookkeeping; algebra scene 6 re-renders at this branch's finalise

## [2026-08-11] audit | incremental, plan 006 branch

- scope: diffed 344f4f1..fef9ebb (5 commits — audit bookkeeping, full
  plan-006 branch); 726b19e..344f4f1 already covered by the previous
  entry; changed files plus cited algebra/probability content, no
  full crawl
- findings: 3 promised-not-delivered, 2 delivered-not-recorded,
  4 possible-not-yet-made, 5 graph-health — applied alongside the
  local CodeRabbit round (log1p attribution, the dropped a >= b) in
  one phase-4 commit
- the flipped logarithms -> e-and-ln edge verified against scene
  content: the deferral replay is verbatim, the strip re-rules, the
  debt is read; the re-read identity regained the (a >= b) the
  original carries, with the max convention now named in its captions
- picture-is-a-claim: scene 1's hops were prose-claimed "on the
  strip" (no strip is drawn — README cell and plan design fixed to
  the built scene); the plan's scene-3 bisection prose replaced by
  the built settling-rows beat
- stale-at-delivery occurrence 6: algebra/README's Scope, e/ln Ideas
  bullet, and inverse-graph deferral all still called this branch's
  content future — all three updated with pointers to calculus/
- rows polished: ctc gradient row cross-referenced (e-half exists),
  bits/entropy row notes nats-vs-bits as a stretched-unit change,
  batched calculus row says "first three", softmax bullet states its
  remaining random-variables gate
- future connections recorded here for the next builds: Bernoulli's
  table re-read as a binomial sum (counting-rules <-> e-and-ln);
  half-life as ShrinkCounts in continuous time; doubling time
  answering TheCountingStrip's halving-times promise
- linear_algebra/ remains promised nowhere — maintainer call still
  open
- stamp: advance to fef9ebb
