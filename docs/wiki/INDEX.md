# Graph index

Last audited: *(pending first audit — plan 002 branch)*

The stamp is a commit hash: the state of the repo this graph was last
reconciled against. The `connection-auditor` diffs from it instead of
crawling every page; whoever applies an audit's findings updates it.

## Nodes

| Node | Where | One line |
| --- | --- | --- |
| `counting-rules` | `combinatorics/counting_rules_manim.py` | The four elementary counting rules; the grid as outer product of stages |
| `ctc-alignment` | `deep_learning/ctc_alignment_manim.py` | CTC: collapse map, alignment counting, forward trellis |
| `independence` | `probability/independence_manim.py` | The product rule as definition; the aligned unit square |
| `conditional-probability` | *(not built — plan 003)* | Renormalized area, P(A∩B) = P(B)·P(A\|B), Bayes |

## Edges

Status: **delivered** (both ends exist and the content makes the link) or
**promised** (stated somewhere, target missing or link not yet on screen).

| From | To | Status | Stated where |
| --- | --- | --- | --- |
| `counting-rules` | `ctc-alignment` | delivered | `PartitionRule` when-useful cell promised "the counting step behind CTC"; `CountingAlignments` delivers it (3⁴ raw paths, C(T+U, T−U)) |
| `counting-rules` | `independence` | delivered | `probability/README.md` Scope: the multiplication grid reweighted from counts to areas; `ProbabilityAsArea` + `TheProductRule` |
| `ctc-alignment` | `independence` | delivered | `deep_learning/README.md` named the gap; `ChainsOfTrials` teaches the per-frame product CTC purchases |
| `independence` | `conditional-probability` | promised | `probability/README.md` Scope + Ideas; plan 002 gaps; the renormalization teaser foreshadowed in scene design |
| `ctc-alignment` | *(beam search / gradient / peaky dynamics)* | promised | `deep_learning/README.md` Ideas not yet built |
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
