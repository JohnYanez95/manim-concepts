# Probability

## Scope

Probability as proportion, built visually: the sample space as a unit
square, events as regions, probability as area. Five series so far. The
first covers **independence** — the product rule P(A∩B) = P(A)·P(B) as
the *primary* definition, why it is the probability-weighted upgrade of
the counting grid, the confusions it attracts, and the product over a
chain of trials. The second covers **conditional probability** —
restriction and renormalization on the same square, the multiplication
rule, total probability and trees, the inversion fallacy, and
conditional independence — closing the promises the first series and
the CTC series left open. The third covers **Bayes' rule** — the
one-line division through the door the conditional series left open,
the odds form and the waterfall, natural-frequency computation, iterated
updating, and Monty Hall done honestly with the host's protocol as the
likelihood. The fourth covers **random variables** — the die as a
function (not a set), the pmf born by sorting the quartered square,
expectation as the balance point, linearity without independence, the
binomial assembled from cell counts and cell areas, and the swamping
intuition quantified — closing the oldest promise the counting series
made. The fifth covers **softmax and likelihood** — likelihood as the
row lens on the binomial table (data pinned, parameter sweeping),
maximum likelihood as the row's peak, the log as the native scale of
accumulating independent evidence, softmax as exp-then-normalize
forced by shift invariance, temperature and the base-change answer to
"why e", and negative log-likelihood as the visible gap on the
log-sum-exp ruler — the remaining half of the bridge promised to
`deep_learning/`, delivered.

This topic exists because two earlier ones promised it: the
[multiplicative rule](../combinatorics/README.md) counts pairs as
|A|·|B|, and independence is the same rectangle with cells reweighted
from counts to areas; and the CTC series in
[`deep_learning/`](../deep_learning/README.md) multiplies per-frame
probabilities. This series teaches the unconditional product that move
rests on; the conditional form CTC actually assumes (frames independent
*given the input*) is taught in the conditional series below.

Deliberately **not** covered here:

- Log-odds as a full inference scene. The ruler now exists —
  [`algebra/`](../algebra/README.md)'s `TheEvidenceRuler` walks this
  topic's own coins — but the inference treatment belongs here, and is
  queued, not built.
- Composite-hypothesis Bayes factors and continuous priors — still
  waiting on integration: random variables now exist, densities do
  not.
- Conditioning on probability-zero events. The definition requires
  P(B) > 0; the continuous story (Borel–Kolmogorov) is genuinely
  treacherous, and honest silence beats false generality.
- Variance and the law of large numbers as theorems. The
  random-variables series computes the weak law's instances and names
  it; the proof and the spread machinery arrive together, later.
- The Galton board. Verification found physical boards are chaotic
  deterministic systems, not binomial machines — skipped by evidence,
  not oversight; the sorted square does its honest job.
- Continuous distributions and densities — the road not taken until
  integration exists.
- The binomial theorem and Pascal's triangle — `combinatorics/` owns
  them; the (1, 4, 6, 4, 1) row may nod, never depend.
- Measure-theoretic formality. "Probability is area" is used as a
  faithful picture, not developed as measure theory.
- Counting itself — that is `combinatorics/`'s job; this topic starts
  where counting hands over to proportion.
- The softmax gradient as a taught result. `TheLossThatTrains`
  foreshadows "softmax output minus occupancy" in prose; the
  single-frame half (p − one-hot) is taught by `calculus/`'s
  derivative-toolkit series, and the occupancy generalization by
  `deep_learning/`'s gradient series (`SoftmaxMinusOccupancy`).
- Entropy, KL divergence, and soft-target cross-entropy. The one-hot
  collapse is all the loss scene needs; the information-theoretic
  story is queued behind the bits/entropy thread in `algebra/`.
- Calibration methods beyond the one caveat beat. Temperature scaling
  is *named* (Guo et al. 2017) to make the point that softmax outputs
  are asserted, not measured — the methods themselves are out of
  scope.
- MLE beyond the discrete world: no Gaussian, no densities, no
  regularity conditions — likelihood values here are always genuine
  probabilities of the data, which is the simplification the whole
  series leans on.

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
| 2 | `IndependenceRevisited` | $P(A\mid B)=P(A)$ | The stepped cut from the independence series was conditional probability all along — the step's height inside the band is P(A\|B). | The step flattening *is* P(A\|B) = P(A), the equivalent characterization of independence on P(B) > 0. The die jewel re-read: P(even \| {1,2,3,4}) = 2/4 = 1/2 ✓; P(even \| {1,2,3}) = 1/3 ✗. Disjoint re-read: P(A\|B) = 0 — maximal information. Conditioning never mutates the original measure — P(A) still answers in the old one (the closing caption pins it). | Recognizing independence as "conditioning changes nothing" — and why the product form stays the definition (it survives P(B) = 0 and is symmetric). |
| 3 | `TheMultiplicationRule` | $P(A\cap B)=P(B)\,P(A\mid B)$ | The definition read backwards: a joint probability is a width times a conditional height. | It is one rectangle on the square — the counting rule of product carrying probabilities. The chain rule extends it ("n! theorems in one": every expansion order is valid). Time reversal costs nothing: P(S₁\|S₂) = 12/51 = P(S₂\|S₁) — conditioning is re-measuring, not re-running. | The license the independence series used without a name: (4/52)(3/51) = 1/221 is P(A₁)·P(A₂\|A₁) — every sequential-sampling computation, and the shrinking pool made rigorous. |
| 4 | `TotalProbabilityAndTrees` | $P(A)=\sum_i P(B_i)\,P(A\mid B_i)$ | An unconditional probability is the weighted average of its conditional pieces over a partition. | Columns of width P(Bᵢ) carrying rectangles of height P(A\|Bᵢ) tile the square — total probability is "add up the rectangles". A tree is the same square drawn: branches carry conditional probabilities, leaves are intersections, and the sum over circled leaves is the same addition. On the repo's die: P(even) = 1/3·1/2 + 2/3·1/2 = 1/2. | Splitting a hard probability over cases; reading and writing tree diagrams without confusing conditional labels for joint ones. It is also the law the CTC forward trellis runs on — each α-column is total probability over predecessor states. |
| 5 | `TwoSlicesOneSquare` | $P(A\mid B)\neq P(B\mid A)$ | The two conditionals share their numerator and nothing else — the inversion fallacy, drawn. | The same overlap read as a share of the B-band versus the A-band. Exact hit: P(first H \| five H) = 1 vs P(five H \| first H) = 1/16. The prevalence pair: one 9/10-sensitive, 1/10-false-positive test gives P(sick\|+) = 1/2 at 10% prevalence and 1/12 at 1% — whole-person counts — the prior carried by the counts themselves. | The transposed conditional (prosecutor's fallacy, base-rate neglect) — and the series' exit: P(A)P(B\|A) = P(B)P(A\|B) is Bayes' front door, left for the next series. |
| 6 | `WhenToCondition` | — | When conditioning is the tool, and what exactly you condition on. | The conditioning event includes *how you learned it*: the four two-children family chips give 1/3 given "at least one girl" but 1/2 once the announcement rule is drawn as weights. Conditional independence is a third thing: two coins (9/10 vs 1/10 heads) are marginally dependent (41/100 ≠ 1/4) yet independent given the coin — the common-cause beat made quantitative. | Sequential draws, diagnosis (sensitivity and specificity stay two numbers), protocol-aware conditioning; CTC's "independent given the input" finally taught. Monty Hall deferred to the Bayes series, where the host's protocol can be handled honestly. |

Renders: `01_TheRestrictedSquare.mp4` … `06_WhenToCondition.mp4`.

```bash
uv run python probability/conditional_probability_manim.py
uv run python probability/conditional_probability_manim.py --list
```

See the [root README](../README.md) for the full flag list.

### bayes_rule_manim.py

Watch after the conditional series — scene 1 divides the exact identity
its last scene left on screen. The middle four are where the new content
lives: counts, the odds form, the factorized prevalence pair, and
iteration; the last closes the repo's strongest deferred promise.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `ThroughTheFrontDoor` | $P(A\mid B)=\dfrac{P(B\mid A)\,P(A)}{P(B)}$ | Bayes' rule is the front-door identity divided by P(B) — one line, then three names: prior, likelihood, posterior. | The division is the two-slices picture re-read; the denominator is total probability over the hypothesis columns — both already on screen in the conditional series. Positivity is inherited. | Updating any hypothesis on any evidence — a diagnosis after a test result, a model after new data — via the level-one claim of the series: evidence does not determine beliefs, it updates them; posterior ∝ prior × likelihood, normalize last. |
| 2 | `CountingItOut` | $\tfrac{18}{18+24}=\tfrac{3}{7}$ | The first Bayes computation needs no formula — count whole people. | Diseasitis on the cohort chips: 100 students → 20 sick (18 positive), 80 healthy (24 positive); the answer is the share of positives who are sick. The prior travels inside the counts, which is why counts cure base-rate neglect. | The format that turns 4% correct into 24% (and gynecologists from 21% to 87%) — how to actually communicate a posterior. |
| 3 | `TheOddsForm` | $\text{post odds}=\text{prior odds}\times LR$ | Only ratios matter: prior odds times the likelihood ratio is the whole law. | The waterfall — streams at prior widths 1:4, pass-through 3:1, pool at 3:4 → 3/7 — is the square-drawn-as-a-tree with renormalization deferred; the chips, the tree, and the two slices were one object all along. Scale streams or fractions and the pool ratio never moves. | The form in which updating is a single multiplication; keep 3:4 and 3/7 visibly distinct. |
| 4 | `OneTestTwoPatients` | $1{:}9\times 9 = 1{:}1,\quad 1{:}99\times 9 = 1{:}11$ | One test has one number (LR = 9); the posterior belongs to the patient. | The prevalence pair completed as a factorization: the counted 9/18 and 9/108 fall out as 1/2 and 1/12 from the same LR against two priors. "90% accurate" is one word hiding two numbers, read as a posterior. | The medical-test paradox, the prosecutor's fallacy in update clothing — a posterior can never be stated without its prior. |
| 5 | `YesterdaysPosterior` | $1{:}1\xrightarrow{\times 9}9{:}1\xrightarrow{\times 9}81{:}1$ | Yesterday's posterior is today's prior; likelihood ratios multiply. | On the repo's own two coins (LR 9 per head): H → 9:1, HH → 81:1, and H-then-T lands back at exactly 1:1 — impossible if evidence replaced belief, automatic if it reweights. Multiplying is licensed only by conditional independence given the hypothesis — `WhenToCondition`'s lesson, said on screen. | Sequential evidence done right: chained tests, accumulating observations; a zero prior stays zero under any evidence of nonzero probability (a finite likelihood ratio cannot rescue it) — geometrically, it sits infinitely far down `algebra/`'s evidence ruler. |
| 6 | `TheHostsProtocol` | $\text{post}\propto\text{prior}\times P(\text{action}\mid\text{hyp})$ | Monty Hall is ordinary Bayes once the likelihood is the host's behavior, not the revealed fact. | A proportionality table over the door chips (uniform prior over car positions, one row per protocol): standard (1/2, 1, 0) → switch 2/3; Monty Fall (1/2, 1/2, 0) → 1/2; Monty Crawl forced-high → switch wins certainly. Same door opened, three answers — the announcement-protocol lesson at series scale. | Rosenthal's proportionality principle as everyday Bayes: diagnosis, spam, forensics — and the closing rule of the whole topic: condition on what happened *the way it happened*, then multiply. |

Renders: `01_ThroughTheFrontDoor.mp4` … `06_TheHostsProtocol.mp4`.

```bash
uv run python probability/bayes_rule_manim.py
uv run python probability/bayes_rule_manim.py --list
```

See the [root README](../README.md) for the full flag list.

### random_variables_manim.py

Watch after the independence series — the stamped square is
`ChainsOfTrials`' quartered square, third appearance. The first two
scenes build the variable and its distribution as one visible move,
the middle two define and weaponize expectation, the fifth closes the
repo's oldest promise, and the closer turns the swamping intuition
into exact numbers.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheStampedSquare` | $X:\Omega\to\mathbb{R}$ | A random variable is a fixed rule reading a random outcome — the die as a function, not a set. | The function is ink stamped on the sample space before anything is rolled: six faces labeled, then every cell of the 16-cell square stamped with its head count. The only random object is where the dart lands; the label is looked up, never generated. | Every measurement attached to a random process is this — a fixed rule reading a random outcome. |
| 2 | `SortTheSquare` | $P(X{=}k) = \tfrac{\#\{\omega : X(\omega) = k\}}{16}$ | The pmf is the square's own area, sorted by value. | The 16 stamped cells slide into columns grouped by value: (1, 4, 6, 4, 1)/16, conserved area, bars visibly summing to 1 — five unequal bars from sixteen equal cells. Y = tails sorts into the same columns while X + Y = 4 in every cell: one blueprint, two houses. | The distribution forgets which cell was which; the variable remembers — the distinction every "the distribution IS the variable" error trips over. |
| 3 | `TheBalancePoint` | $E[X] = \sum_x x \cdot P(X{=}x)$ | Expectation is the balance point of the weights — defined, not simulated. | The fulcrum under the die's flat bars balances at 3.5, which is not a face; summing stamps over cells (32/16) equals summing values times weights (2) — the sort was a regrouping; the biased die (double weight on 6) moves the balance to 27/7 — the balance point belongs to the measure. | Huygens (1657): the fair price of a ticket — the number you act on, with no long run in sight. |
| 4 | `SameOutcomesAdd` | $E[X{+}Y] = E[X] + E[Y]$ | Expectations add — independence not required. | One sum over the same outcomes; addition distributes. The maximally dependent pair X and 4−X sums to 4 always; the owned 6×6 grid paints the two-dice sum as diagonals — (1,2,3,4,5,6,5,4,3,2,1)/36 — and E = 7 lands twice: by the diagonals and as 3.5 + 3.5. | Linearity is the workhorse: it prices any bundle from its parts, and it is what makes E = np honest with zero combinatorics. |
| 5 | `TheBinomialColumns` | $P(X{=}k) = \binom{n}{k} p^k (1-p)^{n-k}$ | The sorted columns are the binomial distribution — the promise the counting series made, closed. | Cells per column are C(4,k), counted the way the combinations series counts H/T words; re-cut at p = 1/4 the cells go unequal but every k-head cell keeps the same area p^k q^(4−k) (a product ignores factor order), so column k weighs C(4,k)·p^k q^(4−k): coefficient = cell count, power = one cell's area, nothing smuggled. E = np by indicator stamps. | The count-of-successes model wherever trials repeat unchanged (fixed n, two outcomes, constant p, independent) — and no replacement means no binomial, as the aces taught; the binomial even touches e: zero successes in n trials of chance 1/n → 1/e ≈ 0.3679. |
| 6 | `ProportionsConverge` | $P\!\left(\lvert\tfrac{S_n}{n} - \tfrac12\rvert \le 0.05\right) \to 1$ | Proportions converge while counts spread — the swamping intuition, quantified. | Exact binomial sums, no new machinery: within ±5% of half climbs 0.4966 → 0.7287 → 0.9986 (n = 20, 100, 1000) while within ±5 heads falls 0.7287 → 0.2720 → 0.0876 (n = 100, 1000, 10000) — and the two n = 100 rows are the same band, one number telling two stories. | The gambler's fallacy dies by two columns moving in opposite directions; the weak law of large numbers (Bernoulli, proved by ~1689, printed 1713) is named and promised with variance; average surprisal over the 16 cells is exactly 4 bits; and per-frame distributions are pmfs like these — likelihood is next, the promise the softmax/likelihood series below now keeps. |

Renders: `01_TheStampedSquare.mp4` … `06_ProportionsConverge.mp4`.

```bash
uv run python probability/random_variables_manim.py
uv run python probability/random_variables_manim.py --list
```

### softmax_likelihood_manim.py

Watch after the random-variables series — its closer said "likelihood
is next", and this series is that promise kept: the sorted-square
columns re-read as a likelihood, then the machine that manufactures
per-frame distributions, then the loss that trains it.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheLikelihoodLens` | $L(p) = P(\text{data} \mid p)$ | Likelihood is not a new number — it is the old table read along the other axis, data pinned, parameter sweeping. | Three binomial columns (p = 1/4, 1/2, 3/4) each sum to 1; pin the observed k = 3 and the row across them (3/64, 1/4, 27/64) sums to 23/32 — a pmf one way, not one the other. | The question every fitted model answers — "given the data, which parameter?" — begins as this flipped reading; Fisher named it in 1921. |
| 2 | `TheBestExplanation` | $\hat{p} = \arg\max_p L(p)$ | The row's peak names the parameter that explains the data best — maximum likelihood. | Rolls 6, 6, 3: the owned double-weight die out-explains the fair one 4/343 vs 1/216, ratio 2.52 — a posterior-ladder rung, an update factor, not a verdict; the coin's whole curve 4p³(1−p) peaks at p̂ = 3/4 = k/n, the observed proportion; the area under it is 1/5 ≠ 1, so likelihood is no distribution over p — a prior and renormalization would make one. | Fitting anything is this move: pick the parameter that makes the data most probable; the ratio beat is why the same numbers feed Bayes when a prior exists. |
| 3 | `AddToSurvive` | $\ln \prod_i p_i = \sum_i \ln p_i$ | Log the likelihood: the answer is untouched, the arithmetic becomes additive. | Log is monotone, so both curves peak at 3/4 (HHTH's exact-sequence curve sits ln 4 lower — same shape, same peak); five frames multiply to 0.27216 while their counters add to −1.3014; and the cliff: 0.1⁴⁶ stores as exactly 0.0 in float32 where the sum walks to −105.9189 unharmed. | The losses of likelihood-trained models are log-likelihoods: hundreds of per-frame factors underflow any float, sums never do — the logarithms series' cliff, met again as the reason training lives in log space. |
| 4 | `TheProbabilityMachine` | $\mathrm{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$ | Exp then normalize turns arbitrary scores into a distribution. | Dividing by the sum fails twice — shifts change the shares, negatives make negative "probabilities" — while exp lifts every score positive and normalizing totals 1; for smooth per-score recipes, shift invariance forces the exponential (e^c cancels), and the same invariance is the stability trick: (1000, 1001, 1002) overflows to NaN naively, subtract the max and the answer returns. | Softmax is the standard output layer for multi-class classifiers; Bridle named it in 1989 — a differentiable winner-take-all. |
| 5 | `TurningTheDial` | $\mathrm{softmax}(z / T)$ | Softmax is a soft argmax with a sharpness dial — and the dial is a caveat about what the outputs mean. | On z = (2, 1, 0): T = 0.5 sharpens to (0.8668, 0.1173, 0.0159), T = 2 flattens to (0.5065, 0.3072, 0.1863), and the winner never changes — monotone at every T > 0, with one-hot and uniform as limits; base 2 gives exactly (4/7, 2/7, 1/7) and b^z = e^(z ln b), so every base above 1 is a temperature — nothing forces e except that ln is the natural counter. | Sampling temperature in every LLM playground; and calibration: one fitted T recalibrates an overconfident net without changing a prediction (Guo et al. 2017) — softmax outputs are asserted, not measured. |
| 6 | `TheLossThatTrains` | $-\ln \mathrm{softmax}(z)_c = \mathrm{LSE}(z) - z_c$ | Score the machine by the log-likelihood it assigns the truth; over independent frames, losses add. | With one correct class, cross-entropy collapses to −ln p(correct), and for softmax scores that is a visible gap: the smooth-max ruler LSE(z) = 2.4076 minus the correct score — 0.4076, 1.4076, 2.4076 as the truth's rank falls; the per-frame matrix multiplies to 0.294 only because frames are independent given the input, and its logs add to −1.2242. | The loss behind classifier training; the trellis sums the collapsing paths' products into P(transcript given input), and the CTC loss is its negative log (29-way per frame in Deep Speech, 50,257-way in GPT-2) — and its gradient, softmax minus occupancy, is delivered by `deep_learning/`'s `SoftmaxMinusOccupancy`, exactly as this closer promised. |

Renders: `01_TheLikelihoodLens.mp4` … `06_TheLossThatTrains.mp4`.

```bash
uv run python probability/softmax_likelihood_manim.py
uv run python probability/softmax_likelihood_manim.py --list
```

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

- [X] [Blitzstein & Hwang, Introduction to Probability, chs. 1–2 excerpt](https://law-and-algorithms.github.io/assets/files/Probability_Book_Excerpt_BlitzsteinHwang.pdf)
      — Def 2.2.1 and Thms 2.3.1–2.3.6 quoted verbatim in the plan's
      anchors; "conditional probabilities are probabilities".
- [X] [MIT 18.05, Reading 3: conditional probability](https://math.mit.edu/~dav/05.dir/class3-prep.pdf)
      — the consensus spine: reduced sample space first, trees as the
      multiplication rule drawn, "souped up rule of product".
- [X] [Seeing Theory, ch. 2: compound probability](https://seeing-theory.brown.edu/compound-probability/index.html)
      — the interactive sample-space-shrinking device scene 1 inherits.
- [X] [3blue1brown, "The quick proof of Bayes' theorem"](https://www.3blue1brown.com/lessons/bayes-theorem-quick)
      — the two-slices picture behind `TwoSlicesOneSquare` and the
      series' exit line.
- [X] [Böcherer-Linder & Eichler 2017 (Frontiers, open access)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.02026/full)
      — unit square beats tree at quantifying the subset relation; both
      improve with natural frequencies.
- [X] [Rosenthal, "Monty Hall, Monty Fall, Monty Crawl"](https://probability.ca/jeff/writing/montyfall.pdf)
      — why the host's protocol changes the answer; the variants
      `TheHostsProtocol` animates.

From the plan-004 research pass
([`docs/plans/004-probability-bayes.md`](../docs/plans/004-probability-bayes.md)),
for the Bayes series:

- [X] [3blue1brown, "The medical test paradox"](https://www.3blue1brown.com/lessons/better-bayes)
      — the Bayes factor as the test's one number; the odds-form update
      as the exact rule (his frequency counts round; the repo's do not).
- [X] [Yudkowsky, Santamaria, So8res, Robert Eidschun, et al.,
  "Waterfall diagrams and relative odds"](https://www.lesswrong.com/w/waterfall-diagram?lens=bayes_waterfall_diseasitis)
      — the waterfall as the odds form; Diseasitis 1:4 × 3:1 = 3:4.
- [X] [Yudkowsky, So8res, Smith, et al., "Bayes' rule: odds form"](https://www.lesswrong.com/w/bayes-rule-odds-form?lens=introduction-to-bayes-rule-odds-form)
      — prior odds × relative likelihoods = posterior odds.
- [X] [MIT 18.05, class 11: Bayesian updating](https://math.mit.edu/~dav/05.dir/class11-prep.pdf)
      — the update table; yesterday's posterior as today's prior; the
      likelihood column is not a distribution.
- [X] [Gigerenzer & Hoffrage 1995, "How to Improve Bayesian Reasoning Without Instruction"](https://www.semanticscholar.org/paper/49045496d186fec8ba8348a752de2a16b1739ef5)
      — natural frequency formats and why they work.
- [X] [Weber, Binder & Krauss 2018, "Why Can Only 24% Solve Bayesian
  Reasoning Problems in Natural Frequencies: Frequency Phobia in Spite
  of Probability Blindness"](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6194348/)
      — the 4% vs 24% meta-analysis figure and why normalized
      frequencies lose the benefit.
- [X] [Wikipedia, Conditional probability](https://en.wikipedia.org/wiki/Conditional_probability)
      — the definition, the P(B) > 0 requirement, and the
      Borel–Kolmogorov caveat kept out of scope.
- [X] [Wikipedia, Conditional independence](https://en.wikipedia.org/wiki/Conditional_independence)
      — the definition behind `WhenToCondition`'s CTC closer.
- [X] [Wikipedia, Boy or girl paradox](https://en.wikipedia.org/wiki/Boy_or_girl_paradox)
      — Gardner's retraction and the protocol-dependence the
      two-children beat draws.

The entries below came out of the plan-007 research pass
([`docs/plans/007-probability-random-variables.md`](../docs/plans/007-probability-random-variables.md))
and started unchecked; the maintainer corrected the author
attributions, verified all sixteen, and directed the ticks be
recorded. Future entries start unchecked until a human does the same.

- [X] [Grinstead & Snell, Introduction to Probability, §6.1 (LibreTexts)](https://stats.libretexts.org/Bookshelves/Probability_Theory/Introductory_Probability_(Grinstead_and_Snell)/06%3A_Expected_Value_and_Variance/6.01%3A_Expected_Value_of_Discrete_Random_Variables)
      — Definition 6.1 (expectation), Theorem 6.2 (linearity) and the
      verbatim no-independence remark behind `SameOutcomesAdd`.
- [X] [Grinstead & Snell, §6.2 Variance (LibreTexts)](https://stats.libretexts.org/Bookshelves/Probability_Theory/Introductory_Probability_(Grinstead_and_Snell)/06%3A_Expected_Value_and_Variance/6.02%3A_Variance_of_Discrete_Random_Variables)
      — variance definition, the shortcut, npq, die 35/12 — the
      pre-verified anchors the future LLN series inherits.
- [X] [Grinstead & Snell, ch. 8 (source)](https://math.dartmouth.edu/~prob/prob/ch8.tex)
      — Theorem 8.2, the weak law `ProportionsConverge` names via
      Bernoulli; the 1713 attribution.
- [X] [Illowsky & Dean, OpenStax Introductory Statistics 2e, §4.3](https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution)
      — the binomial experiment conditions named in
      `TheBinomialColumns`.
- [X] [Holmes, Illowsky & Dean, OpenStax Introductory Business Statistics 2e, §4.2](https://openstax.org/books/introductory-business-statistics-2e/pages/4-2-binomial-distribution)
      — the explicit pmf formula (the sibling volume headlines what the
      statistics volume leaves to calculators).
- [X] [Orloff & Bloom, MIT 18.05, class 4b: expectation](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_class04-prep-b.pdf)
      — the balance-point picture, "need not be a possible value", the
      outcome-table linearity proof, E = np by indicators.
- [X] [Joe Blitzstein, Stat 110](https://stat110.hsites.harvard.edu/)
      — RV-as-function ordering; "sympathetic magic" (variable vs
      distribution), the error `SortTheSquare`'s twin beat refutes.
- [X] [Grant Sanderson (3blue1brown), "Binomial distributions"](https://www.3blue1brown.com/lessons/binomial-distributions/)
      — the sequence-grouping route to C(n,k)p^k(1-p)^(n-k); its
      likelihood pivot marks the next series' door, not this one's.
- [X] [Kunin et al., Seeing Theory, ch. 1 & 3](https://seeing-theory.brown.edu/basic-probability/index.html)
      — the distribution-first branch this series deliberately does not
      take (long-run simulation as meaning), for contrast.
- [X] [Gauvrit & Morsanyi, "The Equiprobability Bias…" (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4310748/)
      — full title "The Equiprobability Bias from a Mathematical and
      Psychological Perspective"; Lecoutre 1992's randomness-read-as-
      uniformity, surviving instruction — why `SortTheSquare` refutes
      by mechanism.
- [X] [Eric-Jan Wagenmakers (Bayesian Spectacles), a Galton board vs its model](https://www.bayesianspectacles.org/a-galton-board-demonstration-of-why-all-statistical-models-are-misspecified/)
      — why the physical board is not a binomial machine; the Scope
      exclusion's evidence.
- [X] [J J O'Connor and E F Robertson, "Blaise Pascal" (MacTutor)](https://mathshistory.st-andrews.ac.uk/Biographies/Pascal/)
      — the five-letter 1654 correspondence and the problem of points.
- [X] [J J O'Connor and E F Robertson, "Christiaan Huygens" (MacTutor)](https://mathshistory.st-andrews.ac.uk/Biographies/Huygens/)
      — De Ratiociniis in Ludo Aleae (1657), the first printed
      probability work: `TheBalancePoint`'s fair-price close.
- [X] [J J O'Connor and E F Robertson, "Jacob Bernoulli" (MacTutor)](https://mathshistory.st-andrews.ac.uk/Biographies/Bernoulli_Jacob/)
      — died 1705; Ars Conjectandi, Basel 1713 — the proved-by-~1689 vs
      printed-1713 split `ProportionsConverge` keeps distinct.
- [X] [Wikipedia, Ars Conjectandi](https://en.wikipedia.org/wiki/Ars_Conjectandi)
      — the nephew-publisher detail and the 1684-1689 timeline.
- [X] [Wikipedia, Binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution)
      — pmf, mean np, the conditions cross-check.

From the plan-008 research pass
([`docs/plans/008-probability-softmax-likelihood.md`](../docs/plans/008-probability-softmax-likelihood.md)),
for the softmax/likelihood series:

- [X] [Josh Starmer, "In Statistics, Probability is not Likelihood" (StatQuest)](https://www.youtube.com/watch?v=pYxNSUDSFH4)
      — the fixed-distribution/varying-data vs fixed-data/varying-
      distribution split; the evidence that the distinction wants its
      own lesson before MLE.
- [X] [Josh Starmer, "Maximum Likelihood, clearly explained!!!" (StatQuest)](https://www.youtube.com/watch?v=XepXtl9YKwc)
      — candidate distributions sliding under pinned data; MLE as the
      peak.
- [X] [Alexander Etz, "Introduction to the Concept of Likelihood and Its Applications"](https://journals.sagepub.com/doi/10.1177/2515245917744314)
      — likelihood as proportional to the probability of data, not a
      distribution over parameters; ratios as evidence; the Bayes
      connection scene 2 points at.
- [X] [John Aldrich, "R. A. Fisher and the Making of Maximum Likelihood 1912–1922"](https://jhanley.biostat.mcgill.ca/bios601/Likelihood/Fisher%20and%20history%20of%20mle.pdf)
      — the verbatim Fisher 1921/1922 quotes behind scene 1's naming
      beat (Metron 1; Phil. Trans. Roy. Soc. A 222).
- [X] [Kristoffer Magnusson, "Understanding Maximum Likelihood" (interactive)](https://rpsychologist.com/likelihood/)
      — the slider-driven likelihood-curve device, and the survey of
      what this series deliberately defers.
- [X] [Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, ch. 6](https://www.deeplearningbook.org/contents/mlp.html)
      — §6.2.2.3: log-likelihood "undoes the exp",
      log softmax = z − LSE(z), the subtract-max trick, soft argmax.
- [X] [John S. Bridle, "Training Stochastic Model Recognition…" (NIPS 1989)](https://proceedings.neurips.cc/paper/1989/file/0336dcbab05b9d5ad24f4333c7658a0e-Paper.pdf)
      — the coinage ("we like to refer to it as soft max") and the
      gradient-identity prose the closer foreshadows.
- [X] [John S. Bridle, "Probabilistic Interpretation…" (Springer, 1990)](https://link.springer.com/chapter/10.1007/978-3-642-76153-9_28)
      — the conventional "Bridle 1990" citation; normalized
      exponentials as conditional probabilities.
- [X] [Guo, Pleiss, Sun and Weinberger, "On Calibration of Modern Neural Networks"](https://arxiv.org/abs/1706.04599)
      — overconfidence and temperature scaling; the caveat beat's
      source.
- [X] [jdhao, "Softmax Temperature"](https://jdhao.github.io/2022/02/27/temperature_in_softmax/)
      — the (1, 5, 7, 10) temperature sweep with near-one-hot and
      near-uniform endpoints.
- [X] [Joseph Salmon and François-David Collin, "Softmax or soft(arg)max?"](https://josephsalmon.eu/blog/softmax/)
      — soft-argmax naming, log-sum-exp as the smooth max, the
      temperature limits.
- [X] [Gao Hongnan, "Why softmax preserves order…"](https://www.gaohongnan.com/playbook/why_softmax_preserves_order_translation_invariant_not_invariant_scaling.html)
      — shift invariance yes, scale invariance no — the correction the
      dial scene keeps straight.
- [X] [Remy Lau, "Cross-entropy, negative log-likelihood, and all that jazz"](https://towardsdatascience.com/cross-entropy-negative-log-likelihood-and-all-that-jazz-47a95bd2e81/)
      — NLL and cross-entropy as the same masking operation; the
      PyTorch naming confusion.
- [X] [James D. McCaffrey, "PyTorch CrossEntropyLoss vs NLLLoss"](https://jamesmccaffreyblog.com/2020/06/11/pytorch-crossentropyloss-vs-nllloss-cross-entropy-loss-vs-negative-log-likelihood-loss/)
      — CrossEntropyLoss = LogSoftmax + NLLLoss, the alias beat's
      practical anchor.
- [X] [Penn State STAT 415, lesson 1.2: Maximum Likelihood Estimation](https://online.stat.psu.edu/stat415/lesson/1/1.2)
      — the standard binomial L(p) = p^k(1−p)^(n−k) lesson with MLE at
      k/n.
- [X] [Kilian Q. Weinberger, CS4780: "Estimating Probabilities from Data"](https://www.cs.cornell.edu/courses/cs4780/2022fa/lectures/lecturenote04.html)
      — coin-flip MLE with the peak at the empirical proportion; the
      MLE→MAP progression behind the not-a-posterior guard.
- [X] [Grant Sanderson, "But what is a GPT?" (3blue1brown)](https://www.3blue1brown.com/lessons/gpt)
      — the logit-bars → exp → normalize morph and temperature as the
      practitioner meets them.
- [X] [Enes Zvornicanin, "What Is and Why Use Temperature in Softmax?"](https://www.baeldung.com/cs/softmax-temperature)
      — the confidence-dial framing: low sharpens, high flattens,
      winner unchanged.
- [X] [Wikipedia, Softmax function](https://en.wikipedia.org/wiki/Softmax_function)
      — properties reference: Bridle attribution, shift invariance,
      base/temperature equivalence.
- [X] [Awni Hannun et al., "Deep Speech: Scaling up end-to-end speech recognition"](https://arxiv.org/abs/1412.5567)
      — the 29-class character softmax ({a…z, space, apostrophe,
      blank}) named in the closer.
- [X] ["Language Models are Unsupervised Multitask Learners" (GPT-2)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
      — Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei
      and Ilya Sutskever; "the vocabulary is expanded to 50,257", the
      closer's other anchor.
- [X] [J. Willard Gibbs, Elementary Principles in Statistical Mechanics (1902)](https://archive.org/details/elementaryprinci00gibbrich)
      — the canonical-distribution form softmax(−E/kT) descends from;
      cited for the form, not a specific 1868 claim.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- ~~Per-frame softmax as a distribution, likelihood and
  log-likelihood~~ — delivered by this topic's softmax/likelihood
  series; the bridge to `deep_learning/` is closed — its gradient
  series received it.
- Explaining away — the verified-but-unbuilt half of the conditional
  independence story (independence ⇏ CI: two fair flips given "exactly
  one head", 0 ≠ 1/4; plan 003's anchors).
- The log-odds inference scene — `algebra/`'s `TheEvidenceRuler`
  built the ruler on this topic's coins; the inference treatment (the
  residual of that delivered edge) belongs here.
- The law of large numbers as a theorem — `ProportionsConverge`
  computes its instances exactly; the proof wants variance, and the
  two arrive together.
- ~~Random variables and distributions~~ — delivered by this topic's
  random-variables series; `TheStampedSquare` opens on exactly the
  promised die-as-a-function.
