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

## [2026-08-11] series | plan 006 finalised (PR #7)

- final 1080p60 render verified: 7 files — the six e-and-ln scenes
  (1841-2273 frames, native 0.75x pace) plus the re-rendered algebra
  06_TheUnderflowCliff, whose final beat was spot-checked at full
  resolution: the lingering log-sum-exp box is gone, the render claim
  the finalisation-audit correction flagged is true again
- bot round: 2 findings, both accepted — rounded decimals now display
  with approx signs (the iff between two rounded computations removed)
  and "every CTC implementation" softened to match algebra/'s own
  attribution (2006 rescaled; log space is the 2012 book)
- the calculus/ topic lands with all sixteen references
  maintainer-verified and ticked
- next per the roadmap: random variables & distributions in
  probability/ (binomial via the quartered square), then the
  softmax/likelihood bridge — the linear_algebra/ front-page call is
  still open

## [2026-08-11] series | plan 007, random variables (in progress)

- node built: `random-variables` (probability/random_variables_manim.py,
  six scenes; probability/'s fourth series)
- the graph's OLDEST promise closed: counting-rules -> random-variables
  (TheBinomialColumns counts the sorted columns as C(4,k) and assembles
  the pmf from cell count times cell area); independence ->
  random-variables closed in the same landing (quartered square's
  fifth series, the biased die's balance point, swamping quantified)
- one possible-connection made: random-variables -> e-and-ln ((1-1/n)^n
  -> 1/e in the binomial closer — a backward reference, per the new
  narrative rule)
- softmax row fully ungated: both halves of its double gate are now
  delivered; ProportionsConverge's closer names it as next
- LLN row narrowed: instances computed exactly on screen; the theorem
  and variance stay promised together
- bits/entropy row: the expectation half arrived ("average surprisal
  = 4 bits" on screen) — entropy is one series away
- device recorded: sort the square; the quartered square's lineage
  extended to a fifth series
- narrative rule in force from this plan on: levels 1-2 point backward
  at owned devices; forward pointers live only in when-useful beats
  and closers (this series' closer carries all of them)

## [2026-08-11] audit | incremental, plan 007 branch

- scope: diffed fef9ebb..74c4fe2 (plan-006 finalisation segment + 4
  plan-007 commits); changed files plus cited far ends, no full crawl
- findings: 6 promised-not-delivered, 3 delivered-not-recorded,
  4 possible-not-yet-made, 6 graph-health — applied alongside the
  local CodeRabbit round (the balance axis now underlines all six
  bars) in one phase-4 commit
- all four flipped-edge citations verified verbatim against scene
  code (the C(4,k) count, the 27/7 balance, the swamping tables to
  the addendum's digits, the 1/e mirror); narrative rule clean in
  scenes and README cells
- top finding: the plan-007 research pass had never landed in
  probability/README's References — sixteen entries added unchecked;
  the phase-3 claim was false until this commit
- stale-at-delivery occurrence 7: combinatorics row 3 — the closed
  oldest promise's own origin cell still read as future; now points
  at TheBinomialColumns
- prose trued to build: fraction-axis bars, the G&S caption, the HHTH
  callout, the LLN naming vehicle; "bars visibly summing to 1" built
  instead (the 16/16 = 1 beat added to SortTheSquare)
- README Scope gains the Galton-board / continuous / Pascal-ownership
  exclusions the plan promised it
- recorded: the 6x6 grid re-read as the edge's third strand; the aces
  boundary as the shrinking pool's fourth stop; the calculus far end
  now mirrors the 1/e connection; entropy's fully-assembled device
  noted on its row
- linear_algebra/ maintainer call still open
- stamp: advance to 74c4fe2

## [2026-08-11] series | softmax-likelihood lands (plan 008, phase 3)

- node `softmax-likelihood` added: six scenes in
  `probability/softmax_likelihood_manim.py`
- flipped: independence → softmax-likelihood (the CTC bridge's
  remaining half — "likelihood is next" answered, the conditional
  license quoted on screen in the join)
- new delivered edges: random-variables → (two-lens table on the
  sorted-square pmfs; the owned die; ProportionsConverge read
  backwards), logarithms → (the strip carries likelihood; the
  evidence ruler named a log-likelihood-ratio ruler; the cliff rerun;
  the LSE ruler as smooth max), e-and-ln → (calculus/'s "why e in
  every probability machine" debt paid via base-2 = (4/7, 2/7, 1/7)),
  bayes-rule → (the ratio as a posterior-ladder rung; the guard
  pointing at the prior-and-renormalize move)
- new promised edge: softmax-likelihood → the CTC gradient identity
  (the closer's on-screen foreshadow); the ctc-alignment gradient row
  narrowed accordingly — only the derivative toolkit and the identity
  remain ungated
- device: sort-the-square lineage extended to TheLikelihoodLens (pmf
  columns become the two-lens table)
- mid-phase interlude recorded in plan 008: two maintainer-reported
  collisions in shipped random-variables scenes fixed and re-rendered;
  layout linter + placement guards added repo-wide

## [2026-08-11] audit | incremental, plan 008 branch

- scope: diffed 74c4fe2..e517c09 (13 commits — plan-007 finalisation +
  PR #8 merge, full plan-008 branch, layout interlude, --jobs); changed
  files plus cited far ends, no full crawl
- findings: 3 promised-not-delivered, 4 delivered-not-recorded,
  4 possible-not-yet-made, 7 graph-health — applied alongside the
  local CodeRabbit round in the phase-4 commit
- all five new/flipped edge citations verified verbatim against scene
  code (the workhorse softmax, the 4/343 vs 1/216 ratio, the 23/32 row
  sum, the 0.294/−1.2242 join, the (4/7, 2/7, 1/7) base-2 reading)
- new delivered edges recorded: conditional-probability →
  softmax-likelihood (the license quoted on screen had been filed
  under the independence row, now re-grounded on its own delivery) and
  ctc-alignment → softmax-likelihood (the CTC loss named on the
  per-frame matrix — the delivered strand beside the promised
  gradient)
- the CTC gradient identity is the strongest open promise (on screen +
  two documents), and the derivative toolkit is now the single gate
  behind three rows — anchor M already carries its verified numbers
- stale-at-delivery occurrences 8 and 9 fixed: deep_learning Scope no
  longer queues softmax/log-likelihood; calculus Scope calls the
  likelihood series delivered; also trued: root README's topic row and
  likely-next, and ProportionsConverge's origin cell
- row 49's "on-screen debt" corrected: calculus's promise was Scope
  prose, not a rendered caption
- devices grown a stop each, now recorded: chain product (fourth
  stop), counting strip (fourth stop), evidence ruler (named its true
  identity), quartered square (the HHTH lift re-read); new bullet:
  factor out the max (three appearances)
- possible, recorded on rows: cross-entropy alias as the entropy
  series' hook (row grown); MLE→MAP riding the queued log-odds scene
  (row grown); T = 1/ln b as the base-is-a-unit lesson noted in the
  plan only
- plan-008 design prose trued to the build (naive-normalizer example,
  the summed log line, chips not bars)
- CodeRabbit precision fixes folded in: the forcing claim scoped to
  per-score recipes; base = temperature restricted to b > 1 (scene
  captions, README cells, plan, and the row-49 quote all updated
  together)
- linear_algebra/ maintainer call still open (fifth entry)
- stamp: advance to e517c09

## [2026-08-12] series | derivative-toolkit lands (plan 009, phase 3)

- node `derivative-toolkit` added: six scenes in
  calculus/derivatives_manim.py
- flipped: e-and-ln → derivative toolkit (the Ideas entry delivered;
  the residual promises — ln as area, Euler's formula, growth in the
  wild — keep their own promised row)
- new delivered edges: softmax-likelihood → (the grid peak found
  analytically; the NLL gap differentiated to p − one-hot, "roughly
  linearly" made a theorem) and logarithms → (the score as the
  counting strip differentiated; the LSE ruler differentiated into
  the softmax shares)
- the CTC gradient rows narrowed: every gate is now open — only the
  identity itself and the training-dynamics scenes remain
- devices: zoom-until-straight lineage recorded (the derivative born
  as a function; the stretch view; the chain rule composing it);
  counting strip fifth stop (the score is the strip's derivative)

## [2026-08-12] audit | incremental, plan 009 branch

- scope: diffed e517c09..5615507 (12 commits — plan-008 finalisation
  tail + PR #9 merge, LICENSE fill, full plan-009 branch, maintainer
  source pass); changed files plus cited far ends, no full crawl
- findings: 3 promised-not-delivered, 4 delivered-not-recorded,
  4 possible-not-yet-made, 7 graph-health — applied in the phase-4
  commit (the local CodeRabbit round returned zero findings, a repo
  first)
- top finding: the "grid search" claim was a beat no scene contains —
  TheBestExplanation swept the whole curve; reworded in the scene,
  README cell, INDEX quote and plan, caught before finals exist
- built on the audit's recommendation: the general line
  k/p − (n−k)/(1−p) = 0 ⟹ p̂ = k/n — ProportionsConverge's claim,
  now derived on screen
- the new node's out-promise recorded: derivative-toolkit → the CTC
  gradient identity (the promise's third on-screen strand), carrying
  two riders — the bare-product-rule decision and occupancy-as-
  expectation (TheBalancePoint is the owned picture)
- stale-at-delivery occurrences 10 and 11 fixed: probability Scope
  and deep_learning's gradient bullet now say only the identity
  remains
- root README's likely-next and calculus topic row trued; algebra
  README points at the strip's fifth stop (symmetry restored)
- the welcome row was three series behind: now two rows of five,
  gif re-rendered, and the re-render rule reworded to fire on series
- devices recorded: the softmax bars reborn, the sign-change ribbon,
  the y = x flip differentiated
- possible, recorded: the product rule's owned picture
  (TheProductRule's rectangle, noted in calculus Scope); the stretch
  factor as the 1-D Jacobian feeds the still-open linear_algebra/
  maintainer call (sixth entry)
- plan-009 design prose trued: the sliding dot, collapse-at-0 and
  stacked-heights beats marked cut-at-build
- stamp: advance to 5615507

## [2026-08-12] series | ctc-gradient lands (plan 010, phase 3)

- the roadmap's end target: the series plans 006–009 existed to gate,
  now built — seven scenes in `deep_learning/ctc_gradient_manim.py`
- node added; all three converging promise rows flipped delivered:
  softmax-likelihood's on-screen closer ("how often the truth used
  each cell" — now γ, named on screen), derivative-toolkit's closer
  (p − one-hot received as the one-path degeneration), and the
  alignment bundle's gradient + peaky strands (the row narrows to
  beam search, plus the new label-prior-variant idea)
- both derivative-toolkit riders resolved: the bare product rule was
  not needed (log-sensitivity route, plan 010 decision 2);
  occupancy-as-expectation grounds in TheBalancePoint (dwell rows)
- three new backward edges delivered: the trellis returns
  (ctc-alignment), the waist is the multiplicative rule
  (counting-rules), dwell rows are the balance point
  (random-variables)
- devices: the constant column recorded as a new device (checksum,
  load-bearing twice); the softmax bars' promised different target
  delivered; the sign-change ribbon inherited as promised; factor-
  out-the-max differentiated as promised; the outer-product grid
  gains the waist as its fifth stop
- deep_learning Scope grown to two series; Ideas: two entries struck
  delivered, one opened (label-prior variant); seven references
  landed unchecked and were maintainer-verified and ticked the same
  day (column 4 of the worked matrix confirmed in the same pass)

## [2026-08-12] audit | incremental, plan 010 branch

- scope: diffed 5615507..9058d19 (plan-009 finalisation segment
  through the ebcf856 merge, then the six plan-010 branch commits);
  changed files plus cited far ends, no full crawl
- findings: 3 promised-not-delivered, 5 delivered-not-recorded,
  4 possible-not-yet-made, 10 graph-health — applied in the phase-4
  commit (the local CodeRabbit round returned one minor plan-prose
  finding, also applied)
- top finding: the γ-column-beside-one-hot-bar beat was claimed by
  the softmax-bars device bullet and the plan's scene-3 design, but
  no scene contained a one-hot bar — BUILT: scene 3's closer now
  stands γ at t=2 beside the one-from-N trio
- built on the strongest possible edge: γ's divide-by-P named on
  screen as "the renormalized slice again — this time conditioned on
  the transcript" — ctc-gradient → conditional-probability delivered;
  constant column = LOTP recorded as a second anchor on the promised
  DP row
- the welcome row missed its first series-triggered re-render: row
  rebuilt as 6 + 5, gif re-rendered; CLAUDE.md's phase-3 gate reworded
  from "topic" to "series" (the rule's second occurrence)
- unrecorded strands recorded: scene 7 quotes WhenToUseIt's spike
  rule, the uniform-γ beat is CountingAlignments reborn, dominance
  counts are a second counting-rules strand, the score device's sixth
  stop, "the matrix the softmax series scored"
- correction to the series entry above: its "dwell rows 1.7578 +
  1.1220 + 1.1202 = 4" overstates the screen — only 1.7578 is on
  screen; the on-screen sum is the uniform beat's 1.4 + 1.4 + 1.2 = 4
- stale-at-delivery occurrences 12–15 fixed: probability row 6 +
  Scope + Ideas, calculus row 6 + product-rule rider (resolution
  recorded), root README topic row and likely-next, INDEX row 50
- "three series promised on screen" trued to two (module docstring +
  README intro; the third strand was documents-only); "third series"
  → "third on-screen return, second series"; the mirror caveat moved
  on screen ("this palindrome's mirror"); the β recurrence formula
  redrawn with per-successor weights
- entropy row gains its third hook (the family portrait's
  distillation line); the label-prior Ideas entry cross-referenced as
  a Bayes move
- linear_algebra/ maintainer call still open (seventh entry)
- stamp: advance to 9058d19

## [2026-08-12] audit | incremental, plan 011 branch

- scope: diffed f2cfec6..aeb25f6 (the three narrative-refactor
  commits) from the 9058d19 stamp; changed files plus cited far ends
  (TheDebtRepaid, the aces row, INDEX rows 37/63/114, the
  shrinking-pool device), no full crawl
- findings: 0 promised-not-delivered, 2 delivered-not-recorded,
  1 possible-not-yet-made, 4 graph-health — applied in the phase-3
  commit (local CodeRabbit: zero findings)
- no stale quotes of the old lines anywhere; the debt premise
  survives — the loan note's "re-reads this exact line" is
  character-true (identical MathTex in both modules), and
  TheDebtRepaid's "rendered before ln meant anything" stays valid in
  the viewing-order reading (pre-ruled by plan 011; recorded so it
  is not re-litigated)
- applied: INDEX row 63 now records the promise side on screen (the
  graph's flagship edge, symmetric at last); calculus Scope's
  two-promises sentence trued (both are captions now); algebra
  Scope's antecedent slip fixed ("the identity behind the second");
  the "by counting alone" residual softened to "with no license
  shown" in both the cell and the caption (the scene was already in
  the re-render set, so strictness was free)
- possible, recorded: TheDebtRepaid quoting the loan note back
  verbatim (second instance of the replayed-deferral device) — out
  of this plan's render scope, future touch
- 9058d19..f2cfec6 (audit application + PR #11 bot fixes) never
  formally re-diffed; absorbed by this stamp advance
- stamp: advance to aeb25f6

## [2026-08-12] audit | incremental, plan 012 branch

- scope: diffed aeb25f6..d9eb601; the head segment is the plan-011
  audit's own application (verified as logged, absorbed); the
  study-guides branch read in full plus cited far ends (both scene
  modules, both topic READMEs, plans 001/009/010, wiki rows 32/47),
  no full crawl
- findings: 4 promised-not-delivered, 2 sub-graph nits, 4
  possible-not-yet-made, 5 graph-health — applied in the phase-3
  commit alongside local CodeRabbit's nine
- the wiki is untouched by the branch — plan 012's screen-shaped rule
  respected and now stated in the wiki README's scope boundary; row
  47's DP promise stays promised, print delivery recorded in the plan
- all 8 anchors byte-exact vs their plan sources; trellis columns,
  both answer scripts, C(150,50) and the 0.36/0.64 construction
  re-verified by computation — zero numeric findings
- top gap BUILT: per-document sourcing (the maintainer's directive) —
  biblatex, \cite in both primitives, the guide's bibliography,
  an undefined-citation structure test (checkcites was tried and
  rejected in the bot round — its bcf parsing fails relative paths)
- prose-vs-scene: the counting primitive attributed to WhenToUseIt
  the phrasing its code comment rejects — trued in the primitive AND
  the combinatorics README cell that seeded it
- root README now names the print track and make study
- possible, recorded: the walker's-lattice beat pre-drafts the queued
  fifth WhenToUseIt shape (noted on that Ideas bullet); the T=3
  mini-trellis seeds the DP series; the greedy construction seeds
  ctc-decoding
- open maintainer call: the digit-literal lint's scoping (R1) —
  deferred to the next batch
- stamp: advance to d9eb601 (the audited HEAD; findings applied in
  the commit after it)

## [2026-08-12] series | dynamic-programming lands (plan 013, phase 3)

- the graph's OLDEST promise closed: ctc-alignment → dynamic
  programming (promised since plan 001), delivered by
  TheTrellisWasAMemo ("α_t(s) was a stored answer all along") with
  both recorded anchors spent in the closer's horizon (log-space
  inheritance; the constant column as LOTP)
- the first series built under ADR 008's inverted pipeline: the
  guide-first DP chapter was the seed; the book drafted, the screen
  animated
- new topic `algorithms/` (scope: counting/sum DP only; no
  optimization zoo, no "optimal substructure" vocabulary, no MDPs)
- new delivered edge: dynamic-programming → counting-rules (the
  lattice recounted, checked against C(6,2) on screen — the queued
  fifth WhenToUseIt shape's screen precedent)
- devices: the fold recorded as a new device; tree↔grid gains its
  fourth direction; the WhenToUseIt mapping close reaches five series
- naming history kept honest on screen: the Bellman/Wilson story told
  as Bellman's story (the verifier pinned the contradicting
  chronology); "memo functions (Michie 1968)", never "memoization"
- seventeen references landed unchecked for the maintainer's pass

## [2026-08-12] audit | incremental, plan 013 branch

- scope: diffed bb2abce (plan-012 merge, PR #14)..61d1f6e; the
  d9eb601..bb2abce segment (plan-012 audit application + ADR
  stitching) absorbed per direction, not re-diffed; branch files
  read in full plus cited far ends, no full crawl
- findings: 2 promised-not-delivered (both now recorded as promised
  rows: divide & conquer, edit distance worked), 6
  delivered-not-recorded, 1 possible-not-yet-made, 8 graph-health —
  applied in the phase-4 commit alongside local CodeRabbit's three
  (all residuals of the cut merge animation)
- prose-vs-scene: the flipped row's claims all verified against the
  built scenes; C(150,50), the call tables and the mini trellis
  re-verified by computation — zero numeric findings
- top gap applied: the promise's home cell (deep_learning row 5)
  now points at algorithms/; the closer's backward-sweep horizon
  recorded as row 48's third strand; the WARM lineage's fourth
  removal and the waist ring's rename recorded; the Pascal-queue
  row gains its screen precedent; beam search gains its second
  anchor
- stale trio fixed: root README (algorithms/ row added; likely-next
  trimmed; the gif alt text now says rows), study-guides INDEX
  graduated dynamic-programming to series-backed
- "in-degree" softened to what the screen shows ("shared children");
  Scope's "shortest routes" corrected to "routes on grids"; row 48
  now says "oldest standing promise" (row 50 keeps the elder title)
- stamp: advance to 61d1f6e

## [2026-08-12] series | plan 014, gradient descent

- node added: `gradient-descent` (six scenes, calculus/ — third
  series in the topic; second ADR-008 graduation, book-to-screen
  from the guide's formerly guide-first chapter)
- edge delivered: `derivative-toolkit` → `gradient-descent` (the
  row-5 "habit that survives every optimizer" promise, closed by
  `WhereTheWalkStops`; the update derived from the toolkit's own
  nudge algebra)
- edge delivered: `gradient-descent` → `ctc-gradient` (the
  training beats' "plain gradient descent", named on screen since
  plan 010, now taught; the anchor-M walk re-read with its
  mechanism)
- no new promises opened: SGD/momentum/schedules, Newton, contours
  and gradient flow are Scope exclusions, not queued ideas
- note: the verifier's F3 (double-well basin boundary √11 at
  η = 0.1) promoted to scene 5's payoff; the guide chapter's
  overclaiming sentence trued in the same change

## [2026-08-12] audit | plan-014 branch

- scope: diffed 61d1f6e..9226fdf — the plan-013 finalisation segment
  (phase-4 application verified as logged, PR #15 bot round, merge)
  absorbed; the four plan-014 commits read in full plus cited far
  ends (ctc-gradient scene 6, deep_learning README, anchors.yaml,
  root README); no full crawl
- findings: 0 promised-not-delivered, 3 delivered-not-recorded,
  3 possible-not-yet-made, 5 prose-vs-scene, 5 graph-health;
  numerics all pass (factor table, ledger, √11, anchor-M
  byte-checked)
- both new edges verified against scene code; no new promises
  opened, as the plan claimed
- top drift: the plan's "loss-vs-step inset trained on the bowl" and
  "WhenToUseIt mapping close (sixth series)" claim beats no scene
  contains — scene 2 carries the identical-losses beat as captions,
  scene 6 closes on a caption stack
- unrecorded strand: TheRoadsOwnWalk opens on "the alignment table —
  twelve knobs" (ctc-alignment's object, on screen)
- none of the five device lineages the plan says the series extends
  reached INDEX's device section (ribbon third stop, nudge square,
  stretch factor, bars, loss-vs-step readout)
- stale-at-delivery occurrence 16: root README's calculus row missed
  the descent series; derivatives row 5's origin cell unstruck;
  deep_learning never pointed back
- study INDEX's seed-anchor note was stale (all three cited) and the
  gradient-descent row omitted 010.K.NLL; √11 in print carried no
  anchor macro or answer-script assertion
- possible: the log-axis replot is MultiplyIsAdd unnamed; the bowl
  walk pre-draws half-life; softmax parameterisation named in print
  only
- applied (same change): all sixteen findings — new edges
  gradient-descent → ctc-alignment (with the softmax rider) and,
  via one added caption ("× per step: a straight march on the log
  ruler"), logarithms → gradient-descent DELIVERED, promoting the
  audit's own top possible; the plan trued to as-built; the √11
  boundary anchored (014.basin.sqrt11) and asserted in the answer
  script; the three stale far ends fixed
- stamp: advance to 9226fdf

## [2026-08-12] series | plan 015, CTC decoding

- node added: `ctc-decoding` (seven scenes, deep_learning/ — third
  series in the topic; third and final ADR-008 graduation: the
  guide-first set empties)
- edge delivered: `ctc-alignment` → `ctc-decoding` (row 42's
  beam-search strand, the graph's oldest remaining promised strand —
  sum-vs-max in deployment costume, the collapsed-prefix beam, the
  two ledgers beside the trellis's final column). The label-prior
  variant stays promised on the row
- edges delivered: `dynamic-programming` → `ctc-decoding` (the
  Scope-promised exact-DP prerequisite, named on screen);
  `ctc-gradient` → `ctc-decoding` (peakiness excusing greedy;
  spikes-not-timestamps restated at deployment);
  `logarithms` → `ctc-decoding` (the log-add in the production
  ledgers, named on screen — never max)
- branch note: cut from main at 9d0c86a while PR #16 (plan 014) was
  open; the plan-014 rows are absent from this branch's view of the
  graph and reconcile on merge

## [2026-08-12] audit | incremental, plan 015 branch

- scope: diffed 61d1f6e..ca95076 (plan-013 finalisation tail absorbed
  as the previous audit's application; the four plan-015 commits read
  in full plus cited far ends — alignment scene 3, algorithms README,
  root README); plan-014's absent rows excluded per branch context,
  none reported
- findings: 3 promised-not-delivered, 5 delivered-not-recorded,
  2 possible-not-yet-made, 8 graph-health (3 stale, 5 prose-vs-scene);
  zero numeric findings — every on-screen number re-derived in exact
  fractions against the pinned digest
- top finding: the digest's flagship side-by-side (ledgers beside the
  trellis's final column) was built as a caption, not a juxtaposition
  — and TheForwardTrellis' rendered column holds different numbers;
  row 43, the plan design and this log's series entry all overstated
- root README untouched despite the phase-3 claim: topics row and
  likely-next both stale (beam search still "backlog")
- forced alignment was promised on screen with no graph row; the
  label-prior residue moved to its own promised row from ctc-gradient
- devices recorded: the mapping close's sixth stop (TheLoopClosed),
  the per-frame matrix lineage, the pooled-bar sum-vs-max (cited to
  the guide chapter's construction, not alignment scene 3), the WARM
  lineage's fifth stop (the one-ledger overcount chip)
- row 72 gained a queued third passenger: Q(c) is the MAP move
  deployed
- applied (same change): all findings — the α-column juxtaposition
  BUILT in scene 5 (chips α₂(A)=0.40 / α₂(ε)=0.24 beside the
  ledgers); the max-reverts-to-path-search clause added on screen;
  the fifth-of-mass caption trued to half-with-a-fifth-A-bound; the
  leaderboard title bounded ("top transcript masses", CodeRabbit's
  finding too); root README, algorithms README (both spots) and the
  alignment rows 3/6 pointed at the delivered series; the plan's
  false root-README claim corrected in place
- stamp: advance to ca95076

## [2026-08-29] series | plan 016, inclusion–exclusion

- node added: `inclusion-exclusion` (seven scenes, probability/ — the
  topic's sixth series; the first new authored study-guide primitive
  since v1, solve gate 8/8)
- edge delivered: `counting-rules` → `inclusion-exclusion` (row 79's
  inclusion–exclusion strand — the "two and three overlapping sets"
  bullet, re-homed from `combinatorics/README.md` Ideas with a pointer;
  Pascal, stars & bars and the binomial theorem stay promised on the
  row, the binomial theorem now restated on screen a second time)
- edges delivered: `independence` → `inclusion-exclusion` (the
  Bernstein coins' device reuse the seed audit recorded, acted on:
  the empty centre and the mutual-independence licence);
  `random-variables` → `inclusion-exclusion` (the 4, 6, 4, 1 row as
  the sorted square's columns; D(n)/n! beside (1 − 1/n)ⁿ);
  `e-and-ln` → `inclusion-exclusion` (e cited as the compound-interest
  ceiling)
- edges promised: `inclusion-exclusion` → the exponential series
  (named unbuilt on screen; home calculus/), → the sieve for exactly
  m of n (named not built on screen)
- devices recorded: the per-cell ledger, the WARM overcount's sixth
  stop, the mapping close's seventh stop
- branch note: cut from main at 18d4cbb (clean, level with origin)

## [2026-08-29] audit | incremental, plan 016 branch

- scope: diffed 18d4cbb..d59000d (the four plan-016 commits read in
  full plus the cited far ends — independence scenes 2/3/4/5's
  inset, random-variables scenes 2/5, calculus scene 1, combinatorics
  scene 3; root README working tree; every other README and the
  study INDEX grepped for stale queue wording)
- findings: 3 promised-not-delivered, 3 delivered-not-recorded,
  5 possible-not-yet-made, 11 graph-health (1 structural, 10
  prose-vs-scene); zero numeric discrepancies — every on-screen
  number re-derived in exact fractions against anchors A–R; 3
  provenance/print nits
- top finding: the designed counter to the headline misconception
  ("disjoint and independent are opposite ends of the overlap" —
  scene 1 L3, plan design) was not built; the primitive stated it as
  taught and row 86's "re-reads NotMutualExclusivity" leaned on it
- row 80's hybrid status buried the counting residue (Pascal, stars &
  bars, binomial theorem): no promised row from counting-rules
  remained — split per the plan-015 label-prior precedent
- both new promised rows lacked a home-queue entry: the exponential
  series was absent from calculus/ Ideas, the sieve from probability/
  Ideas
- "removed once" was said, not shown: the unit-square overlap was
  outlined WARM and never removed (README row 1, plan design)
- unrecorded reuse: TheProductRule's 6×6 grid and 2×2 coin grid
  rebuilt verbatim (scene 1 closer, Bernstein); the indicator pointer
  leans on SameOutcomesAdd's linearity
- far ends all verified; no stale queue mentions anywhere; the
  mapping-close lineage still said "six series"
- applied (same change): the "two ends of the overlap" caption BUILT
  under scene 1's three rows; the overlap filled WARM and faded out
  as the −P(A∩B) term writes; the 24 outside cells stamped 0; the
  ellipse caption reworded (Venn stopped at four, five took Grünbaum);
  "de Moivre stated" (Montmort's was the one solved); the indicator
  caption names SameOutcomesAdd; row 80 split into delivered + the
  promised counting residue; rows 86/87 grew the grid-reuse and
  linearity strands; the outer-product-grid and WARM bullets gained
  their inclusion–exclusion stops, the mapping close counts seven;
  the exponential series queued in calculus/ Ideas, the sieve in
  probability/ Ideas; README row 5 trued (decimals on screen; 1/e
  "as a probability limit"); plan design trued (ChainsOfTrials is
  named, not quoted; Ross's aside lives in the takeaway); primitive
  nits (n ≥ 2; about four per cent). Not made, recorded here: the
  Pascal-row bill as a picture, the Bonferroni truncation on the
  ledger grid, de Méré's complement named as the chain's product
  measure, the missing 1/8 drawn as a cell
- stamp: advance to d59000d

## [2026-09-06] series | plan 017, Cantor's diagonal

- node added: `cantor-diagonal` (seven scenes, probability/ — the
  topic's seventh series; the first whose result is a negative claim;
  study-guide primitive authored, solve gate recorded in the plan)
- edges delivered: `counting-rules` → `cantor-diagonal` (the grid
  zigzagged — stamped 1..15, relabelled p/q, four cells skipped);
  `independence` → `cantor-diagonal` (the unit segment as sample
  space; the halving cover; finite additivity re-read as Axiom 2's
  first clause); `inclusion-exclusion` → `cantor-diagonal` (the union
  rule's additivity as the finite case of the axiom stated for
  sequences); `e-and-ln` → `cantor-diagonal` (1/e and e − 2 as digit
  rows)
- edges promised: `cantor-diagonal` → undecidability by the diagonal
  (Turing 1936 §8, named on screen; home algorithms/, queue entry
  added); → length as a probability law, existence (Lebesgue, named
  on screen as B&T's "more advanced treatment"; home probability/
  Ideas, waits on integration)
- devices recorded: the outer-product grid's plan-017 stop (read as a
  sequence); stacked lists with pairing arrows (`ArrangedInASequence`,
  never side-by-side sets — Tsamir & Tirosh); the digit table with its
  diagonal boxed cell by cell (`TheDiagonalRule`, `WhyOneOrTwo`)
- branch note: cut from main at ce317e5 (PR #18 merged, clean, level
  with origin)

## [2026-09-06] audit | incremental, plan 017 branch

- scope: diffed d59000d..14e3f65 (the plan-016 finalisation tail and
  PR #18 merge absorbed as the previous audit's application; the four
  plan-017 commits read in full plus cited far ends — ProbabilityAsArea,
  ChainsOfTrials, MultiplicativeRule, TheMysteryConstants, the 1/e
  captions in random-variables and inclusion–exclusion); no full crawl
- findings: 6 promised-not-delivered, 5 delivered-not-recorded,
  6 possible-not-yet-made, 8 graph-health; zero numeric discrepancies —
  every on-screen and README number re-derived (Decimal at 80 digits,
  exact Fractions) against anchors A–T; 2 precision items (E¹/E²/E³
  broke the subscript-is-which-number convention; "the reals came
  afterwards" read as post-1891)
- top finding, BUILT: the "first clause" strand — the finite additivity
  every earlier series used — was README-only and rows 94/95 hung on
  it; `AreaNotSums` now says it on screen. Also built: `TheDiagonalRule`
  names calculus/'s constants as rows 5 and 6 (row 96 had no citable
  statement anywhere) and says the rows beyond the screen obey the same
  rule (the plan's flag 7 had claimed this was on screen); the cover
  caption names the coin square's halving; scene 1 closes the shifted
  row with "…"; Cantor's rows relabelled E₁, E₂, E₃; the history caption
  now says the reals were 1874, by nesting; the names caption grounds
  itself in the zigzag; the re-run caption says why d′₁ = 3 − d₁; the
  two names of 1/2 recoloured categorical (they are two distinct
  things, not an overcount)
- plan design trued to the built scenes: boxes not sliding rows; the
  axiom condensed, the footnote verbatim; WARM strikes not MUTED tints;
  a caption not a chip; B&T's closing sentence pinned under anchor A
- correction to the series entry above: only the outer-product grid's
  stop had reached INDEX's device section; the pairing-arrows and
  boxed-cell bullets it claimed are now written
- row 94 re-cited (ProbabilityAsArea draws the square; the segment is
  new furniture — recorded as such; the on-screen strand is "probability
  is area — the interval is not a sum over points"); row 93 gained the
  tokens strand; row 96 the 1/e strand; row 98 the calculus/ cross-ref
  and the segment-helper intent
- possible, recorded in README cells: the anti-diagonal walk as the DP
  wavefront (row 2); the yes/no table as an indicator table (row 6);
  scene 7's covered points are scene 4's rows with the duplicate
  dropped (row 7)
- far ends: combinatorics/ (MultiplicativeRule row) and calculus/ (the
  ln-as-area bullet) now point back; algorithms/' queue entry no longer
  says "§8 on screen" and notes the Scope sentence it will need; root
  README's probability row updated; linear_algebra/ maintainer call
  still open (ninth entry)
- local CodeRabbit pass: one minor finding (the same "§8 on screen"
  overstatement), applied
- stamp: advance to 14e3f65 (the audited HEAD; findings applied in the
  commit after it)

## [2026-09-19] series | plan 019, the spectrum

- node added: `spectrum` (seven scenes, signal_processing/ — a new
  topic's first series, the first of four on the road from sound to
  log-mel)
- edges delivered: `random-variables` → `spectrum` (the weighted sum
  re-used with signed weights, its differences from expectation said
  on screen; linearity "owned since dice"); `logarithms` → `spectrum`
  (the log ruler named on screen; −20 × 0.301 = −6.02 dB; log 0 = −∞
  behind the floor — the dB strand of algebra/'s log-scales Idea
  delivered, the essay itself narrowed, not closed);
  `counting-rules` → `spectrum` (C(8, 2) = 28 pairs on screen, sizing
  the exhaustive check)
- edges promised: `spectrum` → convolution (the closing map's first
  unbuilt line, on screen; README road table and Ideas); → windowing → STFT → spectrogram
  (leakage and "filterbank" named on screen in `WhatSetsTheSpacing`,
  the window behind the trumpet's levels in `TheSpectrumInDecibels`,
  the closing map); → mel (201 rows into 80, on screen; the closing
  map); → the inverse ("a promise, not shown here", on screen). Home
  for all four: signal_processing/ Ideas
- rows amended, no new row: `e-and-ln` → *(ln as area, Euler's
  formula, growth in the wild)* gains its first waiting customer for
  the Euler strand (real probe pairs, orthogonality "computed, not
  proved" at N = 8; the complex form and the every-N reason wait —
  calculus/ Ideas updated); `dynamic-programming` → *(divide and
  conquer)* gains the FFT as its second waiting example (README Scope
  and Ideas only; algorithms/ Ideas updated). algebra/ Ideas'
  log-scales bullet records the dB strand as built
- devices recorded: the outer-product grid's plan-019 stop
  (`NoDoubleCounting`'s probe-against-probe table — a measurement per
  cell; drawn, not named on screen)
- linear_algebra/: parked, to be returned to (maintainer, 2026-09-19).
  Its first concrete on-ramp is recorded in signal_processing/README.md
  Ideas — the bank as a projection onto probes, the mel filterbank as a
  matrix. No promised row: nothing on screen names it, and the README
  states an on-ramp, not a promise
- not made, recorded here: `spectrum` ↔ the deep_learning/ CTC nodes
  (the scenes say "speech models" and Whisper, never CTC; no statement
  links the bank to the per-frame matrix, and deep_learning/'s Scope
  puts the encoder out of scope); a graph row for the log-scales essay
  (it never had one; the narrowing rides the `logarithms` → `spectrum`
  row and algebra/'s Ideas — whether it earns its own promised row is
  left to the audit);
  quantization and the source–filter model (Ideas only, no on-screen
  statement); `TheFoldAtNyquist`'s closing map as the mapping close's
  eighth stop, and device bullets for the series' new pictures — the
  sampled rotation, the bank (both left to the audit); the plan's
  scene-7 `np.fft.fft`/`rfft` beat and the Gauss/Fourier
  history credits (designed, not built — nothing cites them)
- stamp: unchanged (14e3f65) — the audit advances it
- branch note: cut from main at 9277a9c (PR #20 merged, clean, level
  with origin)

## [2026-09-19] audit | incremental, plan 019 branch

- scope: diffed 14e3f65..94c3c10 (the plan-017 finalisation tail and
  PR #19 merge absorbed as the previous audit's application; plan 018's
  review-budget PR #20 is process only; the four plan-019 commits read
  in full plus cited far ends — TheBalancePoint, SameOutcomesAdd,
  MultiplyIsAdd, ShrinkCounts, TheUnderflowCliff, CombinationRule,
  deep_learning/ Scope, TheRoadsOwnWalk); no full crawl
- findings: 3 promised-not-delivered, 6 delivered-not-recorded,
  5 possible-not-yet-made, 8 graph-health; zero numeric discrepancies —
  the 28 pairs, the teaser bars, the fold cells and the 96.33 dB
  recomputed
- top finding, BUILT: `NoDoubleCounting`'s "reading of (A + B) =
  reading of A + reading of B" was false where "reading" is the
  distance — the series' own 12, 16, 20. The scene now says "a probe's
  sum on (tone A + tone B)" / "= its sum on A + its sum on B", then "the
  pair adds, sum by sum — the distance is taken last (12 and 16 made
  20)"; README row 4, the guide chapter's lead-in sentence and the
  plan's scene-4 row follow it
- second finding, BUILT in part: `WhatSetsTheSpacing`'s 1500 Hz leakage
  chart now stands beside its 8 samples, under a new first caption ("a
  1500 Hz sine: one and a half laps in the window — not a whole
  number"); `TheSpectrumInDecibels`' charts still stand alone (no room),
  so "never a spectrum without its waveform" was narrowed to the bank
  scenes — signal_processing/README.md's Wage reference and plan D8
- correction to the series entry above: the scene-7 numpy beat WAS
  built ("in numpy, the upper half of fft's output is this mirror — rfft
  returns the bank"); only the on-screen Gauss/Fourier credit is unbuilt
  (the guide chapter prints Gauss c. 1805). Row 59's tail narrowed
  accordingly — READMEs and print state the FFT, the screen names
  numpy's functions and never the algorithm; row 88's README quote
  trued ("needs Euler's formula, and the screen says so") and its
  doubled tail removed
- asymmetry closed: signal_processing/README.md Scope gained a
  paragraph naming the far-end scenes (TheBalancePoint,
  SameOutcomesAdd, MultiplyIsAdd, ShrinkCounts, TheUnderflowCliff,
  CombinationRule, and deep_learning/ from the other side); three
  far-end when-useful cells now point back — probability/
  (TheBalancePoint, SameOutcomesAdd) and combinatorics/
  (CombinationRule)
- "appears once" was false — the trumpet is a second off-row tone:
  README Scope and the guide chapter (its header comment too) now say
  twice, one computed and one measured; the guide's "two curves" →
  "two cosines"; scene 7 now quotes scene 1 accurately ("at least two…
  strictly, more than two"), and README row 7, the guide and the plan's
  scene-1 and scene-7 rows follow
- devices: the mapping close counts eight series, `TheFoldAtNyquist`'s
  map the first whose verdicts include unbuilt series (two GOOD, four
  MUTED); WARM's seventh stop (`TheProbe`'s cancelled mismatch products,
  `TheFoldAtNyquist`'s impostor); three new bullets — the sampled
  rotation (scenes 1, 2, 7; the picture the Euler series should
  inherit), stems never staircases (`_Stems`, scenes 1, 2, 3, 5, 7),
  the linear-then-log replot (`TheRoadsOwnWalk` →
  `TheSpectrumInDecibels`, a reuse stated nowhere on screen)
- row added: `logarithms` → *(log scales in the wild — the visual
  essay)*, promised — `TheUnderflowCliff`'s closer lists the scales on
  screen; placed as row 102, under the `logarithms` → `spectrum` row
  that narrows it (the series entry had left the question to the
  audit). Row 101 gained the pH strand (`ShrinkCounts`' concentration,
  `TheSpectrumInDecibels`' activity — IUPAC's wording) and the
  005.log10two print splice; rows 100 and 103 gained their `\primref`
  print citations, row 100 the new on-screen linearity lines
- riders, not rows: row 88 — the Euler series can open on the sampled
  circle (the shadow a quarter-turn ahead is sin′ = cos in picture
  form; `TheProbe`'s pair plane is already the complex plane's picture;
  calculus/ has no trig yet); row 105 (windowing) — the new leakage
  caption, and the honest joint to the CTC nodes when the STFT series
  lands: the STFT hop becoming `TheAlignmentProblem`'s frames, the
  encoder out of scope on both sides and Whisper not a CTC model, so
  the source-verifier pins that first
- not made, recorded here: `spectrum` ↔ the CTC nodes (the rider
  above, nothing more); orthogonality as disjointness
  (`NoDoubleCounting` ↔ `TwoSetsOneOverlap`, leakage as the overlap — a
  candidate level-3 beat for the windowing series); the shadow as
  sin′ = cos and the sampled rotation as the Euler series' opening
  picture (recorded as the rider and the device bullet, no edge)
- plan design trued to the built scenes: D4's "shown here for four";
  D8 narrowed; scene 1's planted line, scene 4's linearity beat, scene
  5's samples-beside-the-teaser, scene 7's quote, numpy line and
  six-line closing map (convolution included); "the bank is drawn in
  scene 3"
- linear_algebra/: parked, to be returned to (maintainer, 2026-09-19).
  No live text frames it otherwise — README Ideas' Mel bullet and row
  106 now say "on-ramp", not "customer" or "no promise opened"; earlier
  log entries stand unedited
- stamp: advance to 94c3c10 (the audited HEAD; findings applied in the
  commit after it)

## [2026-09-24] series | plan 020, convolution

- node added: `convolution` (seven scenes, signal_processing/ — the
  road's second series, after the spectrum and before windowing)
- edge closed: `spectrum` → *(convolution)* flipped to `spectrum` →
  `convolution`, delivered, the row kept in place (the
  `counting-rules` → `inclusion-exclusion` precedent) — four strands on
  screen: `TheSlidingWeightedSum`'s "the probe's multiply-and-sum, now
  walking: one output at every stop" and the boxed "a filter turns a
  signal into a signal"; `AMovingAverageIsALowPass` reading "the bank
  from the spectrum series … before and after the window";
  `TheKernelsOwnReading`'s "recall: delaying a tone by one sample turns
  its pair — by 45° × the row number" on `TheProbe`'s pair plane;
  `MultiplyingInTime` re-showing `WhatSetsTheSpacing`'s 1500 Hz bars
  under "leakage — by the theorem"
- edges delivered: `random-variables` → `convolution`
  (`WhatOneClickBecomes`' "sums pass through — the response of a sum is
  the sum of the responses" and "two owned facts: the weighted sum is
  linear (the dice); the window never changes" — `SameOutcomesAdd`'s
  move, spent on the spectrum side by `NoDoubleCounting` and again here
  on the pair plane; the series named on screen, the scene in README
  row 2). One row per prerequisite, as for `spectrum`: the `spectrum` →
  `convolution` row above carries both the closure and the delivered
  edge — no reverse-direction row
- rows amended, no new row: `spectrum` → *(windowing → STFT →
  spectrogram)* gains its mechanism, stated on screen by
  `MultiplyingInTime` ("every frame is a multiplication: an endless
  tone × a rectangle of eight ones"; "a window with quieter lines
  copies less: the windowing series' whole subject") and the filterbank
  move by `WhereConvolutionLives` ("the bank becomes a filterbank — its
  kernels the probes, reversed") — the row stays from `spectrum`, the
  convolution series restating the promise it inherited; `e-and-ln` →
  *(… Euler's formula …)* gains its second customer
  (`TheKernelsOwnReading`: "checked on one kernel and four rows; for
  every kernel and N, the proof needs Euler"; the takeaway's "checked
  here, proved with Euler's formula"; calculus/ Ideas updated);
  `dynamic-programming` → *(divide and conquer)* gains the FFT's second
  reason and its first on-screen naming (`WhereConvolutionLives`:
  "100 000 multiply-adds for every output sample" / "— which is why
  long kernels are applied by multiplying spectra" / "the fast way to
  those spectra is the FFT — an algorithm story, parked elsewhere" —
  the screen says "parked elsewhere", the README says `algorithms/`;
  algorithms/ Ideas updated); `spectrum` → *(mel)* notes the closing
  map's MUTED repeat, unchanged
- edge promised: `convolution` → *(the source–filter model of speech)*
  — `WhereConvolutionLives` on screen: "speech: a 115 Hz buzz from the
  glottis is a comb of lines — 230, 345, 460 Hz …", "the vocal tract is
  a filter: its own reading, drawn over the comb, makes the vowel", the
  tag "the source–filter model (a picture, not to scale)"; home
  signal_processing/ Ideas (the plan-019 entry had it as Ideas-only,
  no on-screen statement)
- devices recorded: WARM's eighth stop (`TheFlip`'s "a pre-echo?", the
  sign-flipped tones of `AMovingAverageIsALowPass` and the negative
  readings of `TheKernelsOwnReading` — a sign not hidden rather than an
  overcount, the sense widened); the mapping close's ninth stop
  (`WhereConvolutionLives`' six lines, three GOOD, three MUTED —
  verified in code); a new bullet, the walking window (`_Window`'s
  tokens and ACCENT frame with an arrow dropping one stem into a second
  strip — no Σ node is drawn, whatever `_Window`'s docstring says); the
  sampled rotation's fourth stop (`TheKernelsOwnReading`'s turned-arrow
  sum — the theorem as a picture); stems-never-staircases gains the
  edge-neighbour ghost stems (scenes 1–3) and the endless wave
  (scene 6)
- planned but not stated, recorded here: the plan's scene-7 closing
  map had a seventh line, "harmonics under formants → source–filter" —
  the built map has six, so the source–filter row cites the comb beat
  alone; the plan's scene-6 source–filter pointer moved wholly to scene
  7 (the design's open call 2, taken); the plan's "(the FFT, parked in
  `algorithms/`)" reached the screen as "parked elsewhere"
- not made, recorded here: convolutional layers — a level-3 pointer
  with no home node (`WhereConvolutionLives`: "a convolutional layer:
  kernels slid over the input —" / "their weights learned, not
  designed", the caption "the kernel of the convolution is the set of
  connection weights — LeCun, 1998"; `TheFlip`'s aside "conv layers
  slide unflipped yet say "convolution" — a learned kernel does not
  mind"; deep_learning/ is CTC and has no CNN node, no Ideas bullet
  queues one, so no promised row — the audit may say whether one is
  owed); the two-dice diagonals as a convolution of two pmfs (the
  design allowed a one-caption aside; the build says only "the dice" —
  not stated, not recorded, probability/ Ideas untouched); circular vs
  linear convolution as a concept (met, not taught — README Scope's
  exclusion; the windowing series owns the case where they differ)
- stamp: unchanged (94c3c10) — the audit advances it
- branch note: cut from main at fdf2672 (PR #21 merged, clean, level
  with origin)

## [2026-09-24] audit | incremental, plan 020 branch

- scope: diffed 94c3c10..ce6ea65 (the plan-019 finalisation tail and
  PR #21 merge absorbed as the previous audit's application; the six
  plan-020 commits read in full plus cited far ends — SameOutcomesAdd,
  NoDoubleCounting, TheProbe, WhatSetsTheSpacing, TheSpectrumInDecibels,
  TheFoldAtNyquist, TheSlopeIsAFunction, deep_learning/ Scope,
  probability/ row 4); no full crawl
- findings: 5 promised-not-delivered (4 standing, 1 ruled a Scope
  exclusion), 3 delivered-not-recorded, 7 possible-not-yet-made
  (1 declined), 6 graph-health; zero numeric discrepancies — the
  moving-average gains (1, 0.80, ⅓, 0.14, ⅓ and 3.22, 1.33, 0.55, 2.67),
  the ½ ½ window's 0.71 at 45°, the 0.5, 1.5, 1, 1.5, 1.5 both ways, the
  step's 0, ⅓, ⅔, 1, the product's 4 × 4 ÷ 8 = 2, the 1500 Hz bars, the
  100 000 taps and the 115 Hz comb recomputed
- top finding, FIXED: signal_processing/README.md's Scope said a tone
  between detectors appears twice, "each time as an honest pointer and
  never explained" — contradicted by `MultiplyingInTime`, which re-shows
  the 1500 Hz bars under "leakage — by the theorem" and explains the
  smear (the rectangle's lines copied onto the tone's) without taming
  it. The bullet now says three times, explained but not tamed; the
  window's shape stays the windowing series'
- second finding, BUILT (scene 7): the closing map's line "built here —
  next on the road…" sat over three GOOD lines of which only the
  kernel's own reading is built — reverb and convolutional layers are
  named as where the walk lives, not built. The caption now reads "met
  here — next on the road: the window behind every frame, then the
  spectrogram"; README row 7 ("met here — one built, two named as where
  the walk lives") and both wiki quotes (row 107, the mapping-close
  bullet) follow
- BUILT (scene 4): the 3000 Hz reading 0.55 was on the bank and in the
  plan's anchors but not in the caption; it now reads "3000 Hz: 0.14 as
  tall, upside down — 4 became 0.55, the sign flipped" — README row 4
  and the WARM device bullet quote it
- convolutional layers: ruled a Scope exclusion, not a row. The map
  colours the line GOOD, there is no home node, and deep_learning/'s
  Scope excludes the encoder — so no promise stands to record.
  signal_processing/ Scope gained the bullet (`WhereConvolutionLives`'
  LeCun caption, `TheFlip`'s unflipped aside; "named, not promised: no
  series is queued"), and deep_learning/'s encoder bullet now says the
  same from its side
- windowing bookkeeping confirmed: one row (107, `spectrum` → windowing)
  carrying the spectrum's promise and convolution's mechanism, per the
  series entry; the row now states its closure rule — at closure it
  flips delivered in place (the `spectrum` → `convolution` precedent)
  and `convolution` → the windowing node gets its own delivered row
- asymmetries closed: probability/README.md row 4's when-useful cell
  now points at `WhatOneClickBecomes` ("the weighted sum is linear (the
  dice)") beside `NoDoubleCounting`; signal_processing/ Scope's
  three-series paragraph now says which prior scenes the convolution
  series stands on (`SameOutcomesAdd` once more, then the spectrum
  series alone — `TheSlidingWeightedSum`, `AMovingAverageIsALowPass`,
  `TheKernelsOwnReading`); deep_learning/'s encoder bullet names
  signal_processing/ stopping at the same encoder
- plan design trued to the built scenes: scene 1's "Σ node" (the
  window's frame drops the stem; no Σ node is drawn), scene 7's
  "restated" (the source–filter model is stated in scene 7 only, scene
  6 no longer carrying it) and the map's "met here"
- README row 6's unsourced sentence cut: "Modulation, mixing and every
  'multiply by a carrier' in radio is this same copying of lines" — no
  anchor in plan 020 and nothing on screen supports it
- riders, not rows: row 106 (`random-variables` → `convolution`) — the
  two-dice diagonals are the die's pmf slid against itself,
  `SameOutcomesAdd`'s level sets as a convolution, not stated on either
  side, a candidate beat for the variance series (row 73);
  signal_processing/ Ideas' "Other kernels" — the first difference's
  far end is `TheSlopeIsAFunction` (calculus/), S. W. Smith's discrete
  derivative as the slope born as a signal, and [1, 2, 1]/4 re-checks
  the theorem (gains multiply); pinned, not on screen
- not made, recorded here: a trellis/DP reading of the sliding sum
  (`dynamic-programming`) — declined, the weights are input-dependent
  there and fixed here, so the shapes only look alike; the bank
  diagonalising a circulant matrix (`TheKernelsOwnReading`'s readings
  as eigenvalues, the probes as eigenvectors) — the strongest on-ramp
  yet for the parked `linear_algebra/`, recorded as an on-ramp only;
  Whisper's two convolutional layers as the fact-bridge from
  `WhereConvolutionLives` to `TheAlignmentProblem`'s frames — encoder,
  out of scope on both sides, not opened
- linear_algebra/: parked, to be returned to (maintainer, 2026-09-19).
  No live text frames it otherwise — the circulant on-ramp above is
  recorded as an on-ramp, not a customer
- stamp: advance to ce6ea65 (the audited HEAD; findings applied in the
  commit after it)
