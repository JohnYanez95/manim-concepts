# Graph index

Last audited: `75e5cf9` (2026-08-11, seed audit — full crawl by design)

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
| `conditional-probability` | *(Bayes' rule series)* | promised | `probability/README.md` Scope + Ideas; `TwoSlicesOneSquare` ends at the named front door |
| `ctc-alignment` | *(beam search / gradient / peaky dynamics)* | promised | `deep_learning/README.md` Ideas not yet built |
| `ctc-alignment` | *(dynamic programming as its own concept)* | promised | `deep_learning/README.md` row 5 when-useful ("the same dynamic-programming move as the HMM forward algorithm"); plan 001 gaps |
| `counting-rules` | *(binomial distribution — future random variables)* | promised | `combinatorics/README.md` row 3 when-useful names it; lands when `probability/` grows random variables |
| `independence` | *(softmax, likelihood, log-likelihood)* | promised | `probability/README.md` Ideas — the remaining half of the CTC bridge |
| `independence` | *(law of large numbers)* | promised | `probability/README.md` Ideas; `WhenToUseIt`'s swamping beat is the seed |
| `independence` | *(random variables)* | promised | `probability/README.md` Ideas |
| `counting-rules` | *(Pascal, stars & bars, inclusion–exclusion, binomial theorem)* | promised | `combinatorics/README.md` Ideas not yet built |

## Shared visual devices

Device lineage matters for consistency — a viewer who learns a picture in
one topic should meet the same picture, upgraded, in the next:

- **The outer-product grid**: `MultiplicativeRule` (counting) →
  `CountingAlignments` (raw path space) → `TheProductRule` (2×2 and 6×6,
  reweighted to probability) → the aligned unit square.
- **"Divide out / drop what doesn't matter" in WARM**: cancelled
  orderings (combinatorics) → merged repeats and dropped blanks (CTC) →
  failed product tests (independence).
- **The closing `WhenToUseIt` mapping scene**: same layout in all three
  series — problem shapes on the left, verdicts on the right.
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
