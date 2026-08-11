# Probability

## Scope

Probability as proportion, built visually: the sample space as a unit
square, events as regions, probability as area. The first series covers
**independence** — the product rule P(A∩B) = P(A)·P(B) as the *primary*
definition, why it is the probability-weighted upgrade of the counting
grid, the confusions it attracts, and the product over a chain of trials.

This topic exists because two earlier ones promised it: the
[multiplicative rule](../combinatorics/README.md) counts pairs as
|A|·|B|, and independence is the same rectangle with cells reweighted
from counts to areas; and the CTC series in
[`deep_learning/`](../deep_learning/README.md) multiplies per-frame
probabilities — a move that is legitimate exactly when the model's
measure factorizes, which is what this series teaches.

Deliberately **not** covered here:

- Conditional probability. P(A|B), the equivalent definition of
  independence via P(A|B) = P(A), and Bayes' rule are the next series on
  their own branch — this one teaches the product form first precisely
  because it needs no conditioning (and survives zero-probability
  events). One renormalization teaser is foreshadowed, not defined.
- Random variables, distributions, and expectation. Events only.
- Measure-theoretic formality. "Probability is area" is used as a
  faithful picture, not developed as measure theory.
- Counting itself — that is `combinatorics/`'s job; this topic starts
  where counting hands over to proportion.

## Concepts

### independence_manim.py

Watch in order. The first two scenes build the visual language and the
definition; the middle three stress-test it against the ways it is
misread; the last is the decision rule for assuming it in the wild.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `ProbabilityAsArea` | $P(A) = \text{area}(A)$ | The sample space is a unit square; an event is a region; probability is its share of the area. | A fair die drawn as six equal cells makes count ÷ total and area the same number — proportion is what counting was already computing. | The visual grammar for every probability argument that follows; the reason "the math of probability is the math of proportions". |
| 2 | `TheProductRule` | $P(A\cap B)=P(A)\,P(B)$ | The definition of independence: the joint probability factors. | Two experiments form a grid; an event about one is rows, the other columns, their intersection a rectangle — and rectangle area is width × height. Both cuts of the unit square run straight across. | Any time two sources of uncertainty combine: joint outcomes, error rates, parallel systems — multiply only when the cuts are straight. |
| 3 | `OneDieTwoEvents` | $\tfrac12\cdot\tfrac23=\tfrac13$ | Independence can live inside a single experiment — and one pip decides it. | On one fair die, even and $\{1,2,3,4\}$ factor exactly; slide the boundary to $\{1,2,3\}$ and $\tfrac14\neq\tfrac16$. Same events under a biased die: broken again — it is a property of the measure. | Checking independence by arithmetic instead of intuition; "separate mechanisms" is neither necessary nor sufficient. |
| 4 | `NotMutualExclusivity` | $0 \neq P(A)P(B)$ | Mutually exclusive events are not independent — they are maximally dependent. | Disjoint regions share no area, so the product test fails as loudly as possible; seeing one event tells you the other did not happen. The dependent square is the one whose cut steps. | The most-tested probability confusion; also why Venn-style pictures mislead here — disjoint circles *look* unrelated. |
| 5 | `ChainsOfTrials` | $P(A_1\cap\cdots\cap A_n)=\prod_i P(A_i)$ | A sequence of independent trials multiplies, one factor per step. | Each flip subdivides the square; HHTH is a cell of volume $(1/2)^4$. The chain needs *mutual* independence — Bernstein's coins factor in every pair yet fail the triple — and asserting the product is a modeling choice: the product measure. | The step `deep_learning/`'s CTC loss performs per frame; likelihoods of i.i.d. data; every "multiply the per-step probabilities" argument. |
| 6 | `WhenToUseIt` | — | When assuming independence is safe, and what breaks it. | Replacement installs it (aces: $\tfrac1{169}$), depletion breaks it ($\tfrac1{221}$), common causes break it with no causal link between the events, and the gambler's fallacy misreads swamping as compensation. | Reading a model's independence assumption and knowing what it costs — the question to ask before multiplying anything. |

Renders are numbered to match, so a directory listing plays in the same
order: `01_ProbabilityAsArea.mp4` … `06_WhenToUseIt.mp4`.

Render them:

```bash
uv run python probability/independence_manim.py            # all six, 1080p60
uv run python probability/independence_manim.py --list
uv run python probability/independence_manim.py -s TheProductRule -q draft
```

See the [root README](../README.md) for the full flag list.

## References

Unchecked means **unverified** — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-002 research pass
([`docs/plans/002-probability-independence.md`](../docs/plans/002-probability-independence.md)),
so all of them start unchecked. Open one, confirm it covers what the
entry claims, and tick it yourself; nothing automated will.

- [X] [TsviBT, Jaime Sevilla Mollina, "Two independent events: Square visualization"](https://www.lesswrong.com/w/4cl)
      — the aligned-square device the whole series leans on.
- [X] [3blue1brown, Bayes' theorem lesson](https://www.3blue1brown.com/lessons/bayes-theorem)
      — probability as area on a 1×1 square; the restriction teaser the
      last scene foreshadows.
- [X] [kevin_davisross, "Probability and Simulation", §3.5 Independence](https://bookdown.org/kevin_davisross/probsim-book/independence.html)
      — independence as a property of the measure; "overlap in just the
      right way".
- [X] [Wikipedia, Independence (probability theory)](https://en.wikipedia.org/wiki/Independence_(probability_theory))
      — the product form as primary definition and its edge cases.
- [X] [Wikipedia, Pairwise independence](https://en.wikipedia.org/wiki/Pairwise_independence)
      — Bernstein's example behind the ChainsOfTrials inset.
- [X] [Siegrist, Probability Spaces §2.5 (LibreTexts)](https://stats.libretexts.org/Bookshelves/Probability_Theory/Probability_Mathematical_Statistics_and_Stochastic_Processes_(Siegrist)/02:_Probability_Spaces/2.05:_Independence)
      — the definition's equivalences and zero-probability edge cases.
- [X] [MIT 6.041, Lecture 13: the Bernoulli process](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/7b9979e4868029c95f7d54b03d7d1175_MIT6_041SCF13_L13.pdf)
      — independent trials as the formal object behind "multiply per
      step".
- [X] [LibreTexts, the Gambler's Fallacy](https://stats.libretexts.org/Bookshelves/Introductory_Statistics/Introductory_Statistics_(Lane)/05:_Probability/5.04:_Gambler's_Fallacy)
      — the compensation misreading `WhenToUseIt` corrects.
- [X] [Böcherer-Linder et al., unit squares vs tree diagrams](https://link.springer.com/chapter/10.1007/978-3-319-72871-1_5)
      — the evidence base for preferring the square.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- Conditional probability — the next series, on its own branch:
  P(A|B) as renormalized area, the multiplication rule
  P(A∩B) = P(B)·P(A|B), independence rederived as P(A|B) = P(A), trees.
- Bayes' rule, once conditioning exists.
- The law of large numbers properly: swamping quantified, absolute vs
  relative deviation.
- Random variables and distributions — the die as a function, not a set.
