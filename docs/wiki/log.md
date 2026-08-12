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
  delivered, one opened (label-prior variant); eight references
  landed unchecked for the maintainer's pass
