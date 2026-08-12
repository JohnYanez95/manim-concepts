# Graph index

Last audited: `e517c09` (2026-08-11, incremental — plan-008 branch)

The stamp is a commit hash: the state of the repo this graph was last
reconciled against. The `connection-auditor` diffs from it instead of
crawling every page; whoever applies an audit's findings updates it.

## Nodes

| Node | Where | One line |
| --- | --- | --- |
| `counting-rules` | `combinatorics/counting_rules_manim.py` | The four elementary counting rules; the grid as outer product of stages |
| `ctc-alignment` | `deep_learning/ctc_alignment_manim.py` | CTC: collapse map, alignment counting, forward trellis |
| `independence` | `probability/independence_manim.py` | The product rule as definition; the aligned unit square |
| `conditional-probability` | `probability/conditional_probability_manim.py` | Renormalized area, the multiplication rule, LOTP and trees, the inversion, conditional independence |
| `bayes-rule` | `probability/bayes_rule_manim.py` | The division named, whole-people counting, the odds form and waterfall, the factored prevalence pair, iterated updating, the host's protocol |
| `logarithms` | `algebra/logarithms_manim.py` | The counting strip: multiplying is adding counters; the evidence ruler; the underflow cliff and log-sum-exp |
| `e-and-ln` | `calculus/e_and_ln_manim.py` | e as the self-paced base: Bernoulli's ceiling, the mystery constants, ln as the natural counter row; the underflow identity re-read |
| `random-variables` | `probability/random_variables_manim.py` | The die as a function; the pmf as sorted area; expectation as balance point; the binomial columns; swamping quantified |
| `softmax-likelihood` | `probability/softmax_likelihood_manim.py` | Likelihood as the row lens on the binomial table; MLE as the peak; log as evidence's native scale; softmax forced by shift invariance; temperature and why-e; NLL as the LSE gap |

## Edges

Status: **delivered** (both ends exist and the content makes the link) or
**promised** (stated somewhere, target missing or link not yet on screen).

| From | To | Status | Stated where |
| --- | --- | --- | --- |
| `counting-rules` | `ctc-alignment` | delivered | `PartitionRule` when-useful cell promised "the counting step behind CTC"; `CountingAlignments` delivers it (3⁴ raw paths, C(T+U, T−U)) |
| `counting-rules` | `independence` | delivered | `probability/README.md` Scope: the multiplication grid reweighted from counts to areas; `ProbabilityAsArea` + `TheProductRule` |
| `ctc-alignment` | `independence` | delivered (unconditional half) | `deep_learning/README.md` Scope names the split; `ChainsOfTrials` teaches the unconditional per-frame product |
| `ctc-alignment` | `conditional-probability` | delivered | `WhenToCondition` teaches conditional independence with the exact two-coin example and names "independent given the input" — the conditional half of PR #2's bridge, closed |
| `independence` | `conditional-probability` | delivered | `TheRestrictedSquare` delivers the deferred renormalized slice; `IndependenceRevisited` re-reads the stepped cut as P(A\|B) and rederives P(A\|B) = P(A) |
| `counting-rules` | `conditional-probability` | delivered | `TheMultiplicationRule` speaks the rule of product back ("the counting rule of product, carrying probabilities") and checks the chain against C(13,3)/C(52,3) |
| `conditional-probability` | `bayes-rule` | delivered | `ThroughTheFrontDoor` divides the exact identity `TwoSlicesOneSquare` left on screen; `OneTestTwoPatients` factors the counted prevalence pair; `YesterdaysPosterior` repeats the CI license verbatim; `TheHostsProtocol` closes the Monty deferral with Rosenthal's variants |
| `bayes-rule` | `logarithms` | delivered | `TheEvidenceRuler` re-plots `YesterdaysPosterior`'s ladder in base 3 — each head adds exactly +2, and two tails walk the marker back to exactly 0; evidence as distance, decibans named. Second strand: `ShrinkCounts`' zero-prior beat (log 0 = −∞, infinitely far away), read back from `probability/README.md`'s zero-prior sentence |
| `ctc-alignment` | `logarithms` | delivered | `TheUnderflowCliff` delivers `deep_learning/`'s log-space bullet: the 0.1³²⁴ hard zero, the −324 log sum, and Graves' log-add identity for the trellis's additions (2012 book, correctly attributed) |
| `ctc-alignment` | *(beam search / gradient / peaky dynamics)* | promised | `deep_learning/README.md` Ideas not yet built. The gradient story's e-half (`e-and-ln`) and softmax/NLL half (`softmax-likelihood`) both now exist; what remains is the derivative toolkit and the identity itself |
| `softmax-likelihood` | *(the CTC gradient identity)* | promised | `TheLossThatTrains`' closer, on screen: "its gradient — softmax output minus how often the truth used each cell — is the next series"; the same identity waits in `deep_learning/README.md` Ideas, with Bridle 1989's "output minus a one-from-N target" pinned in plan 008 anchor M |
| `ctc-alignment` | *(dynamic programming as its own concept)* | promised | `deep_learning/README.md` row 5 when-useful; plan 001 gaps. A future build inherits log-space for free: `TheUnderflowCliff` already shows the recursion's additions need the log-add identity |
| `counting-rules` | `random-variables` | delivered | The graph's oldest promise (`combinatorics/README.md` row 3 when-useful), closed: `TheBinomialColumns` counts the sorted columns' cells as C(4,k) — "counted exactly the way the combinations series counts them" — and assembles C(n,k)p^k q^(n−k) from cell count times cell area |
| `independence` | `softmax-likelihood` | delivered | The CTC bridge's remaining half, closed: the product-becomes-sum arithmetic is independence's own delivery — `AddToSurvive` multiplies five per-frame factors to 0.27216 and `TheLossThatTrains` says "independent frames: losses add" on screen (takeaway included); the promise itself was spoken by `ProportionsConverge` ("likelihood is next") and answered by `TheLikelihoodLens` |
| `conditional-probability` | `softmax-likelihood` | delivered | `TheLossThatTrains` quotes the license verbatim on screen: "multiplying is licensed: the frames are independent given the input — the conditioning series said when" — `WhenToCondition`'s exact lesson, used where it was always headed |
| `ctc-alignment` | `softmax-likelihood` | delivered | The delivered strand beside the promised gradient: `TheLossThatTrains` scores a {A, B, ε} per-frame matrix one column at a time and its closer sums the path products into P(transcript given input) — "the trellis's sum" — and names the CTC loss as its negative log (a 29-way softmax per frame in Deep Speech; 50,257-way per token in GPT-2), closing `deep_learning/`'s queued softmax-and-log-likelihood Scope line |
| `independence` | *(law of large numbers — the theorem, with variance)* | promised | `probability/README.md` Ideas and Scope exclusion; `ProportionsConverge` computes the weak law's instances exactly and names it on screen via Bernoulli, proved ~1689 / printed 1713 (G&S Thm. 8.2 is the anchors' source, not the screen citation) — what remains promised is the theorem and the variance machinery, together; plan 007's anchors already carry variance three routes (npq; die 35/12; two-dice 35/6) and the Chebyshev-vs-exact 1/4-vs-0.0569 comparison, so the future series starts with its numbers done |
| `independence` | `random-variables` | delivered | `TheStampedSquare` and `SortTheSquare` run on `ChainsOfTrials`' quartered square (its third 16-cell appearance, after `ShrinkCounts`); `TheBalancePoint` reuses the biased die (E moves to 27/7 — "the balance point belongs to the measure", echoing `OneDieTwoEvents`); `SameOutcomesAdd` re-reads `TheProductRule`'s 6×6 grid ("the two-dice grid you already own"); `ProportionsConverge` quantifies `WhenToUseIt`'s swamping beat |
| `random-variables` | `e-and-ln` | delivered | `TheBinomialColumns`' closer: zero successes in n trials of chance 1/n is (1−1/n)ⁿ → 1/e ≈ 0.3679 — "the split year, mirrored"; the plan-006 audit's possible-connection, made |
| `random-variables` | `softmax-likelihood` | delivered | `TheLikelihoodLens`' two-lens table is three sorted-square pmfs side by side (the p = 1/4 re-cut from `TheBinomialColumns` flanking the fair columns); `TheBestExplanation` reuses the owned double-weight die (4/343 vs 1/216) and reads `ProportionsConverge` backwards ("the proportion is the best guess") |
| `logarithms` | `softmax-likelihood` | delivered | `AddToSurvive` says "multiplying is adding counters — the strip carries likelihood now" and "the evidence ruler was a log-likelihood-ratio ruler all along", then re-runs the cliff (float32 dead at 0.1⁴⁶, 0.1³²⁴ = 0.0 exactly); `TheLossThatTrains` re-uses log-sum-exp as "the smooth max — the log-sum-exp ruler, again" |
| `e-and-ln` | `softmax-likelihood` | delivered | `TurningTheDial` pays the debt `calculus/README.md`'s Scope stated ("why e appears in every probability machine" — Scope prose, not a rendered caption): base 2 is exactly (4/7, 2/7, 1/7), b^z = e^(z ln b), "no base above 1 is forced — each is e at another T; e is the convention because ln is the natural counter" |
| `bayes-rule` | `softmax-likelihood` | delivered | `TheBestExplanation` names the dice ratio "a likelihood ratio — one rung of the posterior ladder: the update factor, not a verdict about the die", and points the not-a-density guard at the prior-and-renormalize move ("that is the Bayes move, and it is not this move") |
| `counting-rules` | *(Pascal, stars & bars, inclusion–exclusion, binomial theorem)* | promised | `combinatorics/README.md` Ideas not yet built |
| `logarithms` | `e-and-ln` | delivered | `TheSplitYear` replays `MultiplyIsAdd`'s deferral caption on screen ("the wait ends here"); `TheNaturalStride` names the mystery constants as ln and re-rules the strip in natural units; `TheDebtRepaid` re-reads `TheUnderflowCliff`'s identity symbol by symbol — the graph's only on-screen debt, closed |
| `logarithms` | *(the log-odds inference scene in `probability/`)* | promised | `algebra/README.md` Ideas ("this series builds the ruler; that series owns the inference") — the residual of the delivered bayes→logarithms edge. `TheBestExplanation` grew it a second passenger: the 864/343 rung stops exactly where a prior would enter, so MLE→MAP (the ratio through a 1:1 prior) rides the same future scene — its numbers already verified in plan 008 addendum A1 |
| `logarithms` | *(information as log-counting — bits, entropy)* | promised | `algebra/README.md` Ideas; `ShrinkCounts`' −log₂ = 4 is the HHTH cell's surprisal. Both halves now exist: `ProportionsConverge` says "average surprisal over the 16 equal cells is exactly 4 bits" on screen — entropy is one series away — H = E[surprisal] is `TheBalancePoint`'s fulcrum under `ShrinkCounts`' stamps, averaged the sorted-square way — with nats vs bits a unit change on `TheNaturalStride`'s device. The freight grew on the plan-008 branch: `probability/README.md` Scope queues KL and soft-target cross-entropy behind this row, and `TheLossThatTrains` names the alias on screen ('the negative log-likelihood (its alias: "cross-entropy loss")') — the one-beat payoff waiting for entropy to exist |
| `e-and-ln` | *(derivative toolkit, ln as area under 1/t, Euler's formula, growth in the wild)* | promised | `calculus/README.md` Ideas not yet built; the first three are also Scope exclusions stated with their reasons |

## Shared visual devices

Device lineage matters for consistency — a viewer who learns a picture in
one topic should meet the same picture, upgraded, in the next:

- **The counting strip, re-ruled** (`TheCountingStrip` →
  `MultiplyIsAdd` → `TheNaturalStride`): the same two-row strip running
  through three scenes — first the definition, then base-as-unit, and
  finally the counter row disclosed as ln in nature's units; the
  mystery constants obey the strip's laws before they are named.
  Fourth stop: `AddToSurvive` — "multiplying is adding counters — the
  strip carries likelihood now".
- **The outer-product grid** (now also `SameOutcomesAdd`'s two-dice
  diagonals — level sets on the owned picture):
  `MultiplicativeRule` (counting) →
  `CountingAlignments` (raw path space) → `TheProductRule` (2×2 and 6×6,
  reweighted to probability) → the aligned unit square.
- **"Divide out / drop what doesn't matter" in WARM**: cancelled
  orderings (combinatorics) → merged repeats and dropped blanks (CTC) →
  failed product tests (independence).
- **The closing `WhenToUseIt` mapping scene**: same layout in four
  series (including `WhenToCondition`) — problem shapes left, verdicts
  right. `TheHostsProtocol` deliberately breaks the pattern: its close
  is a caption trio, since the protocol table already did the mapping.
- **The chain product**: `PermutationRule`'s slot chain →
  `ManyPathsOneWord`'s per-frame product annotation → `ChainsOfTrials`'
  progressive square subdivision → `TheLossThatTrains`' column-highlighted
  matrix product (0.7 × 0.6 × 0.7 = 0.294), the per-frame annotation come
  home. One device, four series.
- **The shrinking pool** (fourth stop: `TheBinomialColumns`' "no
  replacement → no binomial" boundary): `PermutationRule`'s pool-that-depletes is
  sampling without replacement — the same picture that breaks
  independence in `WhenToUseIt` (probability, the aces row), and whose
  per-draw factors `TheMultiplicationRule` finally names as conditional
  probabilities (the 1/221 license).
- **The stepped cut**: dependence as the cut that steps
  (`NotMutualExclusivity`) → named as conditional probability itself in
  `IndependenceRevisited` — the step's height inside the band *is*
  P(A\|B), and flattening is independence.
- **Tree ↔ grid, both directions**: `MultiplicativeRule` recasts a tree
  *as* a grid; `TotalProbabilityAndTrees` draws the square *as* a tree;
  `TheOddsForm`'s waterfall is that tree with the final division
  deferred — three forms of one object, named on screen.
- **Natural-frequency cohort chips** (`TwoSlicesOneSquare` →
  `CountingItOut`): whole-people counts carrying the prior in the
  numbers themselves — completed by the Bayes series' Diseasitis count
  (18/42 = 3/7).
- **Sort the square** (`SortTheSquare` → `TheBinomialColumns` →
  `TheLikelihoodLens`, which stands three of its pmfs side by side and
  reads the pinned row *across* them — the columns become a table, the
  table grows a second lens): the
  stamped cells slide into columns grouped by value — the pmf born as
  conserved, rearranged area; re-cut at p, the same columns are argued
  (highlight plus formula, not a second slide) to weigh
  C(n,k)·p^k q^(n−k). The device that makes "induced weights" a move
  you watched instead of a definition.
- **The quartered unit square** (`ChainsOfTrials` → `ShrinkCounts` →
  `TheStampedSquare`/`SortTheSquare`):
  the (1/2)⁴ cell, first as a probability, then re-read as four
  halvings — negative logs fall out of a picture the viewer owns;
  `AddToSurvive`'s lift beat re-reads the HHTH cell once more as the
  exact-sequence likelihood, ln 4 below the count curve.
- **Factor out the max**: `TheUnderflowCliff`/`TheDebtRepaid`'s a ≥ b
  convention in the log-add identity → `TheProbabilityMachine`'s
  subtract-the-max rescue (the invariance, used) → `TheLossThatTrains`'
  LSE gap. One move — pull the max out so the remainder is tame —
  three appearances; the future gradient series differentiates it.
- **The odds ladder** (`YesterdaysPosterior` → `TheEvidenceRuler` →
  `AddToSurvive`, which names the ruler's true identity on screen:
  "the evidence ruler was a log-likelihood-ratio ruler all along"):
  the multiplicative waterfall and the additive ruler are the same
  data — the tree/waterfall lineage extended into log space.
- **The two-slices reading** (`TwoSlicesOneSquare` → `TheOddsForm`):
  one overlap, two denominators — the geometric form of the transposed
  conditional, and the picture the odds form was built on.
- **The two-coin example** (`WhenToCondition` → `YesterdaysPosterior`):
  one pair of coins, LR 9 — first the common-cause lesson, then the
  iterated-update engine; the same factor as the prevalence test, named
  on screen ("one number, two stories").
