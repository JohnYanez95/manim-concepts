# Probability

## Scope

Probability as proportion, built visually: the sample space as a unit
square, events as regions, probability as area. Two series so far. The
first covers **independence** — the product rule P(A∩B) = P(A)·P(B) as
the *primary* definition, why it is the probability-weighted upgrade of
the counting grid, the confusions it attracts, and the product over a
chain of trials. The second covers **conditional probability** —
restriction and renormalization on the same square, the multiplication
rule, total probability and trees, the inversion fallacy, and
conditional independence — closing the promises the first series and
the CTC series left open.

This topic exists because two earlier ones promised it: the
[multiplicative rule](../combinatorics/README.md) counts pairs as
|A|·|B|, and independence is the same rectangle with cells reweighted
from counts to areas; and the CTC series in
[`deep_learning/`](../deep_learning/README.md) multiplies per-frame
probabilities. This series teaches the unconditional product that move
rests on; the conditional form CTC actually assumes (frames independent
*given the input*) is deferred to the conditional-probability series.

Deliberately **not** covered here:

- Bayes' rule. The conditional series ends deliberately at its front
  door — P(A)·P(B|A) = P(B)·P(A|B), named and left. The full treatment
  (odds form, the waterfall device, Monty Hall done honestly with the
  host's protocol) is its own future series.
- Conditioning on probability-zero events. The definition requires
  P(B) > 0; the continuous story (Borel–Kolmogorov) is genuinely
  treacherous, and honest silence beats false generality.
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
| 4 | `NotMutualExclusivity` | $0 \neq P(A)P(B)$ | Mutually exclusive events with positive probability are never independent — they are maximally dependent. | Disjoint regions share no area, so the product test fails as loudly as possible; seeing one event tells you the other did not happen. (A zero-probability event is trivially independent of everything — the one exception.) | The most-tested probability confusion; also why Venn-style pictures mislead here — disjoint circles *look* unrelated. |
| 5 | `ChainsOfTrials` | $P(A_1\cap\cdots\cap A_n)=\prod_i P(A_i)$ | A sequence of independent trials multiplies, one factor per step. | Each flip subdivides the square; HHTH is a cell of volume $(1/2)^4$. The chain needs *mutual* independence — Bernstein's coins factor in every pair yet fail the triple — and asserting the product is a modeling choice: the product measure. | The step `deep_learning/`'s CTC loss performs per frame; likelihoods of i.i.d. data; every "multiply the per-step probabilities" argument. |
| 6 | `WhenToUseIt` | — | When assuming independence is safe, and what breaks it. | Replacement installs it (aces: $\tfrac1{169}$), depletion breaks it ($\tfrac1{221}$), common causes break it with no causal link between the events, and the gambler's fallacy misreads swamping as compensation. | Reading a model's independence assumption and knowing what it costs — the question to ask before multiplying anything. In [CTC](../deep_learning/README.md), the word is the common cause across frames — exactly why an external language model helps at decode time. |

Renders are numbered to match, so a directory listing plays in the same
order: `01_ProbabilityAsArea.mp4` … `06_WhenToUseIt.mp4`.

Render them:

```bash
uv run python probability/independence_manim.py            # all six, 1080p60
uv run python probability/independence_manim.py --list
uv run python probability/independence_manim.py -s TheProductRule -q draft
```

### conditional_probability_manim.py

Watch after the independence series — its centerpiece re-reads that
series' own stepped-cut picture. The first two scenes build conditioning
as restriction and name what the step always was; the middle three are
the machinery (multiplication rule, total probability, trees) and the
inversion; the last is what you actually condition on, closing the
conditional-independence residual the CTC series left open.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheRestrictedSquare` | $P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}$ | Conditioning is restriction then renormalization: throw away what B rules out, re-measure inside what is left. | Three coins by recount (1/8 → 1/4 given the first is heads); on the square, dimming outside B and stretching the band by 1/P(B) preserves every within-band proportion — the slice is a genuine probability space. Defined only for P(B) > 0. | Every "given that…" question; the formula is the picture's bookkeeping, which is why it comes last. |
| 2 | `IndependenceRevisited` | $P(A\mid B)=P(A)$ | The stepped cut from the independence series was conditional probability all along — the step's height inside the band is P(A\|B). | The step flattening *is* P(A\|B) = P(A), the equivalent characterization of independence on P(B) > 0. The die jewel re-read: P(even \| {1,2,3,4}) = 2/4 = 1/2 ✓; P(even \| {1,2,3}) = 1/3 ✗. Disjoint re-read: P(A\|B) = 0 — maximal information. Conditioning never mutates the original measure: both squares stay on screen. | Recognizing independence as "conditioning changes nothing" — and why the product form stays the definition (it survives P(B) = 0 and is symmetric). |
| 3 | `TheMultiplicationRule` | $P(A\cap B)=P(B)\,P(A\mid B)$ | The definition read backwards: a joint probability is a width times a conditional height. | It is one rectangle on the square — the counting rule of product carrying probabilities. The chain rule extends it ("n! theorems in one": every expansion order is valid). Time reversal costs nothing: P(S₁\|S₂) = 12/51 = P(S₂\|S₁) — conditioning is re-measuring, not re-running. | The license the independence series used without a name: (4/52)(3/51) = 1/221 is P(A₁)·P(A₂\|A₁) — every sequential-sampling computation, and the shrinking pool made rigorous. |
| 4 | `TotalProbabilityAndTrees` | $P(A)=\sum_i P(B_i)\,P(A\mid B_i)$ | An unconditional probability is the weighted average of its conditional pieces over a partition. | Columns of width P(Bᵢ) carrying rectangles of height P(A\|Bᵢ) tile the square — total probability is "add up the rectangles". A tree is the same square drawn: branches carry conditional probabilities, leaves are intersections, and the sum over circled leaves is the same addition. On the repo's die: P(even) = 1/3·1/2 + 2/3·1/2 = 1/2. | Splitting a hard probability over cases; reading and writing tree diagrams without confusing conditional labels for joint ones. |
| 5 | `TwoSlicesOneSquare` | $P(A\mid B)\neq P(B\mid A)$ | The two conditionals share their numerator and nothing else — the inversion fallacy, drawn. | The same overlap read as a share of the B-band versus the A-band. Exact hit: P(first H \| five H) = 1 vs P(five H \| first H) = 1/16. The prevalence pair: one 9/10-sensitive, 1/10-false-positive test gives P(sick\|+) = 1/2 at 10% prevalence and 1/12 at 1% — whole-person counts, the prior as visible column width. | The transposed conditional (prosecutor's fallacy, base-rate neglect) — and the series' exit: P(A)P(B\|A) = P(B)P(A\|B) is Bayes' front door, left for the next series. |
| 6 | `WhenToCondition` | — | When conditioning is the tool, and what exactly you condition on. | The conditioning event includes *how you learned it*: the two-children square gives 1/3 given "at least one girl" but 1/2 once the announcement protocol is drawn in. Conditional independence is a third thing: two coins (9/10 vs 1/10 heads) are marginally dependent (41/100 ≠ 1/4) yet independent given the coin — the common-cause beat made quantitative. | Sequential draws, diagnosis (sensitivity and specificity stay two numbers), protocol-aware conditioning; CTC's "independent given the input" finally taught. Monty Hall deferred to the Bayes series, where the host's protocol can be handled honestly. |

Renders: `01_TheRestrictedSquare.mp4` … `06_WhenToCondition.mp4`.

```bash
uv run python probability/conditional_probability_manim.py
uv run python probability/conditional_probability_manim.py --list
```

See the [root README](../README.md) for the full flag list.

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-002 research pass
([`docs/plans/002-probability-independence.md`](../docs/plans/002-probability-independence.md))
and started unchecked; all nine were then opened, confirmed, and ticked
by the maintainer, who also corrected author attributions. Future
entries start unchecked until a human does the same.

- [X] [TsviBT, Jaime Sevilla Mollina, "Two independent events: Square visualization"](https://www.lesswrong.com/w/4cl)
      — the aligned-square device the whole series leans on.
- [X] [3blue1brown, Bayes' theorem lesson](https://www.3blue1brown.com/lessons/bayes-theorem)
      — probability as area on a 1×1 square; the restriction move the
      conditional-probability series will inherit.
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

From the plan-003 research pass
([`docs/plans/003-probability-conditional.md`](../docs/plans/003-probability-conditional.md)),
for the conditional series:

- [ ] [Blitzstein & Hwang, Introduction to Probability, chs. 1–2 excerpt](https://law-and-algorithms.github.io/assets/files/Probability_Book_Excerpt_BlitzsteinHwang.pdf)
      — Def 2.2.1 and Thms 2.3.1–2.3.6 quoted verbatim in the plan's
      anchors; "conditional probabilities are probabilities".
- [ ] [MIT 18.05, Reading 3: conditional probability](https://math.mit.edu/~dav/05.dir/class3-prep.pdf)
      — the consensus spine: reduced sample space first, trees as the
      multiplication rule drawn, "souped up rule of product".
- [ ] [Seeing Theory, ch. 2: compound probability](https://seeing-theory.brown.edu/compound-probability/index.html)
      — the interactive sample-space-shrinking device scene 1 inherits.
- [ ] [3blue1brown, "The quick proof of Bayes' theorem"](https://www.3blue1brown.com/lessons/bayes-theorem-quick)
      — the two-slices picture behind `TwoSlicesOneSquare` and the
      series' exit line.
- [ ] [Böcherer-Linder & Eichler 2017 (Frontiers, open access)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.02026/full)
      — unit square beats tree at quantifying the subset relation; both
      improve with natural frequencies.
- [ ] [Rosenthal, "Monty Hall, Monty Fall, Monty Crawl"](https://probability.ca/jeff/writing/montyfall.pdf)
      — why the host's protocol changes the answer; the reason Monty
      Hall is deferred to the Bayes series.
- [ ] [Wikipedia, Conditional probability](https://en.wikipedia.org/wiki/Conditional_probability)
      — the definition, the P(B) > 0 requirement, and the
      Borel–Kolmogorov caveat kept out of scope.
- [ ] [Wikipedia, Conditional independence](https://en.wikipedia.org/wiki/Conditional_independence)
      — the definition behind `WhenToCondition`'s CTC closer.
- [ ] [Wikipedia, Boy or girl paradox](https://en.wikipedia.org/wiki/Boy_or_girl_paradox)
      — Gardner's retraction and the protocol-dependence the
      two-children beat draws.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- Bayes' rule — conditioning now exists, and the conditional series
  ends at its front door: the odds form, the waterfall device, the
  prevalence pair completed, and Monty Hall with the host's protocol
  done honestly (Rosenthal).
- Per-frame softmax as a distribution, likelihood and log-likelihood —
  the remaining half of the bridge promised to `deep_learning/`.
- The law of large numbers properly: swamping quantified, absolute vs
  relative deviation.
- Random variables and distributions — the die as a function, not a set.
