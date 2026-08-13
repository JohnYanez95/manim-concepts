# Graph index

Last audited: `61d1f6e` (2026-08-12, incremental — plan-013 branch)

The stamp is a commit hash: the state of the repo this graph was last
reconciled against. The `connection-auditor` diffs from it instead of
crawling every page; whoever applies an audit's findings updates it.

## Nodes

| Node | Where | One line |
| --- | --- | --- |
| `counting-rules` | `combinatorics/counting_rules_manim.py` | The four elementary counting rules; the grid as outer product of stages |
| `ctc-alignment` | `deep_learning/ctc_alignment_manim.py` | CTC: collapse map, alignment counting, forward trellis |
| `dynamic-programming` | `algorithms/dynamic_programming_manim.py` | The recursion tree folded: 177 calls to 11 answers, the lattice by Pascal's sum, the trellis re-read as a stored answer, the state's price, the two-part signature |
| `ctc-gradient` | `deep_learning/ctc_gradient_manim.py` | The CTC gradient: the backward trellis, the constant column, occupancy as the truth's soft target, ∂L/∂u = y − γ, the error signal over training, peakiness as topology + weight sharing |
| `independence` | `probability/independence_manim.py` | The product rule as definition; the aligned unit square |
| `conditional-probability` | `probability/conditional_probability_manim.py` | Renormalized area, the multiplication rule, LOTP and trees, the inversion, conditional independence |
| `bayes-rule` | `probability/bayes_rule_manim.py` | The division named, whole-people counting, the odds form and waterfall, the factored prevalence pair, iterated updating, the host's protocol |
| `logarithms` | `algebra/logarithms_manim.py` | The counting strip: multiplying is adding counters; the evidence ruler; the underflow cliff and log-sum-exp |
| `e-and-ln` | `calculus/e_and_ln_manim.py` | e as the self-paced base: Bernoulli's ceiling, the mystery constants, ln as the natural counter row; the underflow identity re-read |
| `random-variables` | `probability/random_variables_manim.py` | The die as a function; the pmf as sorted area; expectation as balance point; the binomial columns; swamping quantified |
| `derivative-toolkit` | `calculus/derivatives_manim.py` | The slope as a function; nudge geometry; sum + chain rules; e^x and ln differentiated; the score finds the MLE peak; dLSE = softmax |
| `softmax-likelihood` | `probability/softmax_likelihood_manim.py` | Likelihood as the row lens on the binomial table; MLE as the peak; log as evidence's native scale; softmax forced by shift invariance; temperature and why-e; NLL as the LSE gap |
| `gradient-descent` | `calculus/gradient_descent_manim.py` | The slope becomes an update: the bowl walk and its automatic brake, the 1−2η factor's four fates, the nudge square's corner as curvature's fee, sign-change stamps on stopping places, the basin hop no ball could make, the road's 12-knob walk read off one chart |

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
| `ctc-alignment` | *(beam search)* | promised | `deep_learning/README.md` Ideas not yet built. This row's gradient and peaky-dynamics strands were delivered by `ctc-gradient` (2026-08-12); beam search over collapsed prefixes — and the new label-prior-variant idea the gradient series opened — are what remain. Second anchor since plan 013: `algorithms/` hosts the exact-DP prerequisite beam search leans on (its Scope says so), and the guide's decoding chapter already leans on it in print |
| `ctc-gradient` | `ctc-alignment` | delivered | Four strands: `TheOtherHalfOfTheTrellis` mirrors `TheForwardTrellis`'s recurrence against the arrows on the same 5×4 grid; `PathsThroughACell`'s constant column returns the trellis's 15 four times (the flagship number's third on-screen return, second series); `WhereTheTruthSpendsItsTime`'s uniform beat is "the alignment series' counting scene, reborn as a target", said on screen; and `WhyTheSpikesAppear` opens by quoting `WhenToUseIt`'s "never read spike timing as segmentation" and supplies the mechanism behind the rule |
| `ctc-gradient` | `counting-rules` | delivered | Two strands: `PathsThroughACell`'s waist — 2 prefixes × 4 suffixes = 8 of the 15 paths through cell (t=2, A), the multiplicative rule "now carrying probability", said on screen — and `WhyTheSpikesAppear`'s dominance totals (A 21, B 21, ε 18 at T=4, "the input never entered this count"), pure counting delivering the peakiness mechanism |
| `ctc-gradient` | `conditional-probability` | delivered | `WhereTheTruthSpendsItsTime` says it on screen: "the renormalized slice again — this time conditioned on the transcript" — γ_t is the conditional series' renormalization run on a trellis column, P(state at t given Y and X) |
| `ctc-gradient` | `random-variables` | delivered | `WhereTheTruthSpendsItsTime` reads γ's rows as expected dwell times — `TheBalancePoint`'s expectation under new weights, with rows summing past 1 disposing of the rows-are-probabilities misreading |
| `softmax-likelihood` | `ctc-gradient` | delivered | `TheLossThatTrains`' closer promised "softmax output minus how often the truth used each cell — is the next series"; `WhereTheTruthSpendsItsTime` names that exact phrase as γ on screen, and `SoftmaxMinusOccupancy` lands the identity with Bridle's "one-from-N target" gone soft; the reuse is also named on screen — scene 1's real weights arrive as "the matrix the softmax series scored" |
| `ctc-alignment` | `dynamic-programming` | delivered | The graph's oldest standing promise (plan 001 gaps; `deep_learning/README.md` row 5 when-useful), closed: `TheTrellisWasAMemo` re-reads the forward trellis on screen — "α_t(s) was a stored answer all along" — with the mini trellis landing 3 + 3 = 6 and the flagship 81/15/20 returning. Both recorded anchors spent in `TheSignatureInTheWild`'s horizon: the recurrence's additions inherit log-space (`TheUnderflowCliff`), and the constant column is the law of total probability over the frame's states (`TotalProbabilityAndTrees`, performed by `PathsThroughACell`); and the third pointer — the same grid swept backward, a second dynamic program over suffixes — names content already delivered (`TheOtherHalfOfTheTrellis`), use-case framing pointing at a built scene |
| `dynamic-programming` | `counting-rules` | delivered | `TheLatticeRecounted` recounts the walker's 15 = C(6,2) by Pascal addition and checks it against the counting series' answer on screen — the queued fifth `WhenToUseIt` problem shape now has its screen precedent (that re-render stays batched in combinatorics' Ideas) |
| `dynamic-programming` | *(divide and conquer as its own concept)* | promised | `algorithms/README.md` Ideas, and on screen: `WhatBreaksIt` names "divide and conquer is the tree-shaped sibling" — a merge-sort recurrence module would contrast scene 5's shape table from the tree side |
| `dynamic-programming` | *(edit distance worked in full)* | promised | `algorithms/README.md` Ideas; the closer names the Wagner–Fischer table, and the KITTEN→SITTING 7×8 grid is already pinned in plan 013 (anchors K/L, distance 3) — the cheapest promise on the board |
| `derivative-toolkit` | `gradient-descent` | delivered | The derivatives series' row-5 when-useful cell promised "the sign-change check is the habit that survives every optimizer" — `WhereTheWalkStops` runs that check on every stopping place (valley, hilltop, shelf) with the optimizer inheriting the toolkit's blindness; and the update itself is rebuilt from owned objects on screen: `TheSlopeBecomesAStep` derives w ← w − ηL′ from the toolkit's nudge algebra (ΔL ≈ L′·Δw), `TheCornerChargesTheFee` re-runs `NudgeInNudgeOut`'s square with a finite step |
| `gradient-descent` | `ctc-gradient` | delivered | The gradient series' `TheErrorSignalLearns` ran "plain gradient descent" on screen (loss 0.7181 → 0.1602 → 0.0356, README row 6) with the rule itself untaught; `TheRoadsOwnWalk` teaches the mechanism and re-reads the same pinned anchor-M trajectory (0.7181 → 0.0003, ×0.86 vs ×0.9993 per step), restating frame 3's mixed (0.032, 0.218, 0.750) convergence — y matches γ out of indifference — with the walk that produced it now explained |
| `counting-rules` | `random-variables` | delivered | The graph's oldest promise (`combinatorics/README.md` row 3 when-useful), closed: `TheBinomialColumns` counts the sorted columns' cells as C(4,k) — "counted exactly the way the combinations series counts them" — and assembles C(n,k)p^k q^(n−k) from cell count times cell area |
| `independence` | `softmax-likelihood` | delivered | The CTC bridge's remaining half, closed: the product-becomes-sum arithmetic is independence's own delivery — `AddToSurvive` multiplies five per-frame factors to 0.27216 and `TheLossThatTrains` says "independent frames: losses add" on screen (takeaway included); the promise itself was spoken by `ProportionsConverge` ("likelihood is next") and answered by `TheLikelihoodLens` |
| `conditional-probability` | `softmax-likelihood` | delivered | `TheLossThatTrains` quotes the license verbatim on screen: "multiplying is licensed: the frames are independent given the input — the conditioning series said when" — `WhenToCondition`'s exact lesson, used where it was always headed |
| `ctc-alignment` | `softmax-likelihood` | delivered | The first-delivered strand of the bundle (its gradient sibling now delivered too, by `ctc-gradient`): `TheLossThatTrains` scores a {A, B, ε} per-frame matrix one column at a time and its closer sums the path products into P(transcript given input) — "the trellis's sum" — and names the CTC loss as its negative log (a 29-way softmax per frame in Deep Speech; 50,257-way per token in GPT-2), closing `deep_learning/`'s queued softmax-and-log-likelihood Scope line |
| `independence` | *(law of large numbers — the theorem, with variance)* | promised | `probability/README.md` Ideas and Scope exclusion; `ProportionsConverge` computes the weak law's instances exactly and names it on screen via Bernoulli, proved ~1689 / printed 1713 (G&S Thm. 8.2 is the anchors' source, not the screen citation) — what remains promised is the theorem and the variance machinery, together; plan 007's anchors already carry variance three routes (npq; die 35/12; two-dice 35/6) and the Chebyshev-vs-exact 1/4-vs-0.0569 comparison, so the future series starts with its numbers done |
| `independence` | `random-variables` | delivered | `TheStampedSquare` and `SortTheSquare` run on `ChainsOfTrials`' quartered square (its third 16-cell appearance, after `ShrinkCounts`); `TheBalancePoint` reuses the biased die (E moves to 27/7 — "the balance point belongs to the measure", echoing `OneDieTwoEvents`); `SameOutcomesAdd` re-reads `TheProductRule`'s 6×6 grid ("the two-dice grid you already own"); `ProportionsConverge` quantifies `WhenToUseIt`'s swamping beat |
| `random-variables` | `e-and-ln` | delivered | `TheBinomialColumns`' closer: zero successes in n trials of chance 1/n is (1−1/n)ⁿ → 1/e ≈ 0.3679 — "the split year, mirrored"; the plan-006 audit's possible-connection, made |
| `random-variables` | `softmax-likelihood` | delivered | `TheLikelihoodLens`' two-lens table is three sorted-square pmfs side by side (the p = 1/4 re-cut from `TheBinomialColumns` flanking the fair columns); `TheBestExplanation` reuses the owned double-weight die (4/343 vs 1/216) and reads `ProportionsConverge` backwards ("the proportion is the best guess") |
| `logarithms` | `softmax-likelihood` | delivered | `AddToSurvive` says "multiplying is adding counters — the strip carries likelihood now" and "the evidence ruler was a log-likelihood-ratio ruler all along", then re-runs the cliff (float32 dead at 0.1⁴⁶, 0.1³²⁴ = 0.0 exactly); `TheLossThatTrains` re-uses log-sum-exp as "the smooth max — the log-sum-exp ruler, again" |
| `e-and-ln` | `softmax-likelihood` | delivered | `TurningTheDial` pays the debt `calculus/README.md`'s Scope stated ("why e appears in every probability machine" — Scope prose, not a rendered caption): base 2 is exactly (4/7, 2/7, 1/7), b^z = e^(z ln b), "no base above 1 is forced — each is e at another T; e is the convention because ln is the natural counter" |
| `bayes-rule` | `softmax-likelihood` | delivered | `TheBestExplanation` names the dice ratio "a likelihood ratio — one rung of the posterior ladder: the update factor, not a verdict about the die", and points the not-a-density guard at the prior-and-renormalize move ("that is the Bayes move, and it is not this move") |
| `softmax-likelihood` | `derivative-toolkit` | delivered | `ZeroSlopeFindsThePeak` finds `TheBestExplanation`'s grid peak analytically (the score 3/p − 1/(1−p) zeroes at p̂ = 3/4, and the general line derives p̂ = k/n — "the observed proportion … now derived"); `TheSmoothMaxsShares` differentiates the NLL gap into (−0.3348, 0.2447, 0.0900) = p − one-hot and makes "the gap grows roughly linearly" a theorem (slope → −1) |
| `logarithms` | `derivative-toolkit` | delivered | `ZeroSlopeFindsThePeak` names the score "the counting strip differentiated — under ln, products become sums of relative rates"; `TheSmoothMaxsShares` differentiates the log-sum-exp ruler itself, its sensitivities landing as the softmax shares |
| `derivative-toolkit` | `ctc-gradient` | delivered | `TheSmoothMaxsShares`' on-screen closer answered: `TheSensitivityOfTheSum` generalizes the shares reading to path scale (many paths share one cell, so shares add into occupancy) and `SoftmaxMinusOccupancy`'s degeneration beat receives p − one-hot as the one-path special case. Both riders resolved: the bare product rule was **not needed** — the log-sensitivity route replaced it (plan 010 decision 2, the rectangle stays in the drawer) — and occupancy-as-expectation grounds in `TheBalancePoint` (A's dwell row, 1.7578 of 4 frames, on screen; the uniform beat's on-screen sum is 1.4 + 1.4 + 1.2 = 4 = T) |
| `counting-rules` | *(Pascal, stars & bars, inclusion–exclusion, binomial theorem)* | promised | `combinatorics/README.md` Ideas not yet built. The Pascal strand now has a screen precedent: `TheLatticeRecounted`'s R(i,j) = R(i−1,j) + R(i,j−1) is Pascal's identity in block-walking form, and `TheSignatureInTheWild` restates the queue on screen ("queued back home in counting") |
| `logarithms` | `e-and-ln` | delivered | `TheSplitYear` replays `MultiplyIsAdd`'s deferral caption on screen ("the wait ends here"); `TheNaturalStride` names the mystery constants as ln and re-rules the strip in natural units; `TheDebtRepaid` re-reads `TheUnderflowCliff`'s identity symbol by symbol — the graph's only on-screen debt, closed; and since the plan-011 refactor the promise side is on screen too: the underflow scene's loan note ("ln and e are names on loan from calculus … it earns them, then re-reads this exact line" — the MathTex is character-identical in both modules) |
| `logarithms` | *(the log-odds inference scene in `probability/`)* | promised | `algebra/README.md` Ideas ("this series builds the ruler; that series owns the inference") — the residual of the delivered bayes→logarithms edge. `TheBestExplanation` grew it a second passenger: the 864/343 rung stops exactly where a prior would enter, so MLE→MAP (the ratio through a 1:1 prior) rides the same future scene — its numbers already verified in plan 008 addendum A1 |
| `logarithms` | *(information as log-counting — bits, entropy)* | promised | `algebra/README.md` Ideas; `ShrinkCounts`' −log₂ = 4 is the HHTH cell's surprisal. Both halves now exist: `ProportionsConverge` says "average surprisal over the 16 equal cells is exactly 4 bits" on screen — entropy is one series away — H = E[surprisal] is `TheBalancePoint`'s fulcrum under `ShrinkCounts`' stamps, averaged the sorted-square way — with nats vs bits a unit change on `TheNaturalStride`'s device. The freight grew on the plan-008 branch: `probability/README.md` Scope queues KL and soft-target cross-entropy behind this row, and `TheLossThatTrains` names the alias on screen ('the negative log-likelihood (its alias: "cross-entropy loss")') — the one-beat payoff waiting for entropy to exist. Third hook, from the gradient series: `WhyTheSpikesAppear`'s family portrait puts "distillation — the teacher's soft outputs" on screen — soft-target cross-entropy, named before entropy exists |
| `e-and-ln` | `derivative-toolkit` | delivered | `TheSlopeIsAFunction` generalizes `ZoomUntilStraight` and says so on screen (d/dx names the settling ratio); `TheCurveThatIsItsOwnSlope` re-reads `TheMysteryConstants` in d/dx notation (Euler §186/§188 anchored) and differentiates `TheDebtRepaid`'s undo pair into ln′ = 1/x |
| `e-and-ln` | *(ln as area under 1/t, Euler's formula, growth in the wild)* | promised | `calculus/README.md` Ideas not yet built; the derivative-toolkit entry was struck delivered by the derivatives series |

## Shared visual devices

Device lineage matters for consistency — a viewer who learns a picture in
one topic should meet the same picture, upgraded, in the next:

- **Zoom until straight** (`ZoomUntilStraight` → `TheSlopeIsAFunction`,
  which runs the device at many points and plots the read-offs as a
  second curve — the derivative born as a function; the number-line
  stretch view in `NudgeInNudgeOut` is the same zoom in transformation
  clothing, and the chain rule composes it).
- **The counting strip, re-ruled** (`TheCountingStrip` →
  `MultiplyIsAdd` → `TheNaturalStride`): the same two-row strip running
  through three scenes — first the definition, then base-as-unit, and
  finally the counter row disclosed as ln in nature's units; the
  mystery constants obey the strip's laws before they are named.
  Fourth stop: `AddToSurvive` — "multiplying is adding counters — the
  strip carries likelihood now". Fifth: `ZeroSlopeFindsThePeak`
  differentiates it — the score d ln f = f′/f is the strip's own
  derivative, products becoming sums of relative rates. Sixth:
  `TheSensitivityOfTheSum` — "the move that found the likelihood's
  peak now reads the trellis", the score at path scale.
- **The outer-product grid** (now also `SameOutcomesAdd`'s two-dice
  diagonals — level sets on the owned picture):
  `MultiplicativeRule` (counting) →
  `CountingAlignments` (raw path space) → `TheProductRule` (2×2 and 6×6,
  reweighted to probability) → the aligned unit square →
  `PathsThroughACell`'s prefix-bundle × suffix-bundle waist (ways in ×
  ways out, on the trellis) → `TheTrellisWasAMemo`'s waist ring, the
  same picture renamed a stored answer.
- **"Divide out / drop what doesn't matter" in WARM**: cancelled
  orderings (combinatorics) → merged repeats and dropped blanks (CTC) →
  failed product tests (independence) → duplicate subtrees greyed into
  lookups (`WriteTheAnswersDown`'s fold — the fourth thing WARM
  removes: repeated work).
- **The closing `WhenToUseIt` mapping scene**: same layout in five
  series (including `WhenToCondition` and `algorithms/`'s
  `TheSignatureInTheWild`, whose verdicts are the states) — problem
  shapes left, verdicts right. `TheHostsProtocol` deliberately breaks
  the pattern: its close is a caption trio, since the protocol table
  already did the mapping.
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
  deferred — three forms of one object, named on screen. Fourth
  stop, from `algorithms/`: `WriteTheAnswersDown` sets the call tree
  over a six-cell memo row — first computations write down GOOD,
  duplicate copies grey WARM into lookups (the tree stays drawn; the
  fold is the greying, not a merge).
- **The fold** (`WriteTheAnswersDown`, new in `algorithms/`): first
  computations write GOOD into a memo row, every later copy greys
  WARM into a lookup — 15 calls to 6 computations on screen, 177 to
  11 by ticker. The device the whole DP series stands on, and the
  counter to the documented "DP = filling tables" misconception (the
  table is the residue of a correct recurrence).
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
- **The softmax bars, reborn** (`TheProbabilityMachine` →
  `TurningTheDial` → `TheLossThatTrains` → `TheSmoothMaxsShares`, where
  the same bars — same values, order, colors — return as a *gradient*
  read-out → the gradient series delivers the promised different
  target: `WhereTheTruthSpendsItsTime` pulls a γ column out of the
  grid and stands it beside the one-hot bar, and
  `TheErrorSignalLearns`' output panels are the bars four frames
  wide).
- **The sign-change ribbon** (`ZeroSlopeFindsThePeak`: + / 0 / − under
  the likelihood curve, with the x³ cameo and the p = 0 valley floor
  disposing of the converse error) — inherited as promised:
  `TheErrorSignalLearns`' push bars balance about the axis (every
  column sums to zero in both signs), the sign pinned on screen the
  moment the first axis appears.
- **The y = x flip** (`TheDebtRepaid` earns the inverse graph →
  `TheCurveThatIsItsOwnSlope` differentiates it: rise and run swap, so
  slopes reciprocate — 1/e at x = e).
- **Factor out the max**: `TheUnderflowCliff`/`TheDebtRepaid`'s a ≥ b
  convention in the log-add identity → `TheProbabilityMachine`'s
  subtract-the-max rescue (the invariance, used) → `TheLossThatTrains`'
  LSE gap. One move — pull the max out so the remainder is tame —
  three appearances; differentiated as promised:
  `SoftmaxMinusOccupancy` pushes the loss through the log-softmax
  Jacobian, `TheSmoothMaxsShares`' ∂LSE = softmax doing the one line.
- **The constant column** (`PathsThroughACell` →
  `SoftmaxMinusOccupancy`; Eisner's classroom checksum, new in the
  gradient series): sum α·β down any trellis column and get the same
  P(Y|X) — proved by "every path crosses every column exactly once",
  and load-bearing twice: the emission-ledger self-check, and
  Σ_j γ_t(j) = 1 collapsing the softmax Jacobian into y − γ.
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
