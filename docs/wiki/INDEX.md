# Graph index

Last audited: `726b19e` (2026-08-11, incremental — plan-005 branch)

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
| `bayes-rule` | `logarithms` | delivered | `TheEvidenceRuler` re-plots `YesterdaysPosterior`'s ladder in base 3 — each head adds exactly +2, and two tails walk the marker back to exactly 0; evidence as distance, decibans named |
| `ctc-alignment` | `logarithms` | delivered | `TheUnderflowCliff` delivers `deep_learning/`'s log-space bullet: the 0.1³²⁴ hard zero, the −324 log sum, and Graves' log-add identity for the trellis's additions (2012 book, correctly attributed) |
| `ctc-alignment` | *(beam search / gradient / peaky dynamics)* | promised | `deep_learning/README.md` Ideas not yet built |
| `ctc-alignment` | *(dynamic programming as its own concept)* | promised | `deep_learning/README.md` row 5 when-useful; plan 001 gaps. A future build inherits log-space for free: `TheUnderflowCliff` already shows the recursion's additions need the log-add identity |
| `counting-rules` | *(binomial distribution — future random variables)* | promised | `combinatorics/README.md` row 3 when-useful names it; lands when `probability/` grows random variables |
| `independence` | *(softmax, likelihood, log-likelihood)* | promised | `probability/README.md` Ideas — the remaining half of the CTC bridge |
| `independence` | *(law of large numbers)* | promised | `probability/README.md` Ideas; `WhenToUseIt`'s swamping beat is the seed |
| `independence` | *(random variables)* | promised | `probability/README.md` Ideas |
| `counting-rules` | *(Pascal, stars & bars, inclusion–exclusion, binomial theorem)* | promised | `combinatorics/README.md` Ideas not yet built |
| `logarithms` | *(e and ln — a `calculus/` topic)* | promised | `algebra/README.md` Scope exclusion + Ideas; on screen ("that story waits"); root README likely-next; the compound-interest table sits verified in plan 005's anchors |
| `logarithms` | *(the log-odds inference scene in `probability/`)* | promised | `algebra/README.md` Ideas ("this series builds the ruler; that series owns the inference") — the residual of the delivered bayes→logarithms edge |
| `logarithms` | *(information as log-counting — bits, entropy)* | promised | `algebra/README.md` Ideas; `ShrinkCounts`' −log₂ = 4 is the HHTH cell's surprisal, one caption short of "4 bits" |

## Shared visual devices

Device lineage matters for consistency — a viewer who learns a picture in
one topic should meet the same picture, upgraded, in the next:

- **The outer-product grid**: `MultiplicativeRule` (counting) →
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
  progressive square subdivision. One device, three series.
- **The shrinking pool**: `PermutationRule`'s pool-that-depletes is
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
- **The quartered unit square** (`ChainsOfTrials` → `ShrinkCounts`):
  the (1/2)⁴ cell, first as a probability, then re-read as four
  halvings — negative logs fall out of a picture the viewer owns.
- **The odds ladder** (`YesterdaysPosterior` → `TheEvidenceRuler`):
  the multiplicative waterfall and the additive ruler are the same
  data — the tree/waterfall lineage extended into log space.
- **The two-slices reading** (`TwoSlicesOneSquare` → `TheOddsForm`):
  one overlap, two denominators — the geometric form of the transposed
  conditional, and the picture the odds form was built on.
- **The two-coin example** (`WhenToCondition` → `YesterdaysPosterior`):
  one pair of coins, LR 9 — first the common-cause lesson, then the
  iterated-update engine; the same factor as the prevalence test, named
  on screen ("one number, two stories").
