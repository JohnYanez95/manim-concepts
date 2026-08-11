# Algebra

## Scope

Logarithms, built the counting way: a logarithm reads the counter row of
a two-row strip — the exponent as a count of multiplicative steps — so
that multiplying becomes adding. The series exists as a double-unlock:
`probability/`'s Bayes series wanted evidence to *add* (log-odds), and
[`deep_learning/`](../deep_learning/README.md)'s CTC loss wanted products
of hundreds of probabilities to survive floating point (log-space and
log-sum-exp). Both payoffs are scenes here, on the repo's own numbers.

Deliberately **not** covered here:

- **e and the natural logarithm.** Every honest road to e — limits,
  derivatives, areas — is calculus, which the repo does not teach yet.
  One caption names the deferral; nothing pretends otherwise. All
  content is base-generic (change of base is a constant rescale), built
  in bases 2, 3, and 10.
- The inverse-function graph as a *definition* — documented to misfire;
  it may appear later as a payoff, never as the starting point.
- Exponential/logarithmic equations drill, complex logarithms, and
  Weber–Fechner beyond a motivation caption.

## Concepts

### logarithms_manim.py

Watch in order. The first three scenes build the strip, the notation,
and the law; the fourth makes negative logs content rather than edge
case; the last two are the payoffs the repo promised.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheCountingStrip` | $\log_b x = y \iff b^y = x$ | A logarithm answers "b to the what is x?" — it reads the counter row over the value row. | The strip *is* the definition: counter 0,1,2,… over values 1,2,4,…,1024; the base is the stride of one step. Conditions come free: b = 1 never moves, and positive bases never leave the positives (x > 0). | Every "how many doublings/tenfoldings?" question — halving times, digit counts, orders of magnitude. |
| 2 | `OneFactThreeNotations` | $2^6 = 64,\ \log_2 64 = 6,\ \sqrt[6]{64} = 2$ | Power, log, and root are one fact about the triple (2, 6, 64) asked three ways. | The triangle of power: cover a corner, get an operation; $b^{\log_b x} = x$ is the same number in two corners — *undo*, never "cancel". The log(a+b) trap is refuted in base 10 (log₁₀(10+10) ≈ 1.301 ≠ 2) because the base-2 instance is coincidentally true. | Reading any log identity without memorizing it; not falling for the two most-documented log errors. |
| 3 | `MultiplyIsAdd` | $\log_b(xy) = \log_b x + \log_b y$ | Multiplying values is adding counters. | 8 × 16 is hop 3 then hop 4 = hop 7 = 128 on the strip; the slide rule (Gunter 1620, Oughtred ~1622) made the law physical. Change of base is a stride change — log₄64 = 6/2 = 3 — so the base is a *unit*: ten doublings ≈ three digits is why log₁₀2 ≈ 0.301. | Any time the world multiplies and you would rather add — which is the rest of this module. |
| 4 | `ShrinkCounts` | $-\log_2 \tfrac{1}{16} = 4$ | Probabilities in (0, 1) have negative logs because they are counts of *shrinkings*. | The repo's own `ChainsOfTrials` cell: (1/2)⁴ is four halvings of the unit square. pH is the everyday negative-log; log 0 = −∞ is the zero prior, infinitely far away. And slow is not bounded: name any N, 2^N sits on the strip. | Reading log-probabilities, pH, and every "small number, big negative log" quantity without flinching. |
| 5 | `TheEvidenceRuler` | $\log_3(\text{odds}) \mathrel{+}= 2 \text{ per head}$ | On a log ruler, evidence adds: each head contributes the same length. | `YesterdaysPosterior`'s ladder re-plotted in base 3: LR 9 = 3², so heads step 0 → 2 → 4 (odds 1, 9, 81) and H-then-T walks back to exactly 0 — the multiplicative waterfall and the additive ruler are the same data. | The log-odds form of Bayes — evidence as weight (Turing's decibans); the promise `probability/`'s Ideas queue carried. |
| 6 | `TheUnderflowCliff` | $\ln(a{+}b) = \ln a + \ln(1 + e^{\ln b - \ln a})$ | Products of small probabilities die in floating point; sums of logs walk on forever — and log-sum-exp restores the one thing log space loses. | 0.5^1074 survives as float64's last subnormal, 0.5^1075 is exactly 0.0, 0.1^324 likewise — while the log₁₀ sum is exactly −324. The trellis *adds* α's, so it needs Graves' log-add identity, safe because the max factors out and the shifted terms live in [0, 1]. | CTC's forward recursion in every real implementation (the 2012 book's move; the 2006 paper rescaled) — the promise `deep_learning/`'s Ideas queue carried. |

Renders: `01_TheCountingStrip.mp4` … `06_TheUnderflowCliff.mp4`.

```bash
uv run python algebra/logarithms_manim.py
uv run python algebra/logarithms_manim.py --list
```

See the [root README](../README.md) for the full flag list.

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-005 research pass
([`docs/plans/005-algebra-logarithms.md`](../docs/plans/005-algebra-logarithms.md))
and starts unchecked until a human verifies it.

- [ ] [OpenStax College Algebra 2e, §6.3 Logarithmic Functions](https://openstax.org/books/college-algebra-2e/pages/6-3-logarithmic-functions)
      — the definition with its domain conditions, quoted in the plan's
      anchors.
- [ ] [OpenStax College Algebra 2e, §6.5 Logarithmic Properties](https://openstax.org/books/college-algebra-2e/pages/6-5-logarithmic-properties)
      — the three laws and change of base (conditions completed in the
      anchors; no fetched source boxes them all at once).
- [ ] [3blue1brown, "Triangle of Power"](https://www.3blue1brown.com/lessons/triangle-of-power)
      — one triple, three notations; the scene 2 device.
- [ ] [Better Explained, "Using Logarithms in the Real World"](https://betterexplained.com/articles/using-logs-in-the-real-world/)
      — logs as counting multiplicative steps; the wild scales.
- [ ] [Kenney & Kastberg, "Links in Learning Logarithms"](https://files.eric.ed.gov/fulltext/EJ1093384.pdf)
      — the documented misconceptions (cancel/disappear, ln = log, the
      inverse-graph failure) this series designs against.
- [ ] [Emory Math 108, logarithms via the triangle of power](https://mathcenter.oxford.emory.edu/site/math108/logs/)
      — the laws derived from the triangle; log₂3 irrational.
- [ ] [Wikipedia, Slide rule](https://en.wikipedia.org/wiki/Slide_rule)
      — Gunter/Oughtred history; multiplication as added lengths.
- [ ] [Wikipedia, Double-precision floating-point format](https://en.wikipedia.org/wiki/Double-precision_floating-point_format)
      — the float64 normal/subnormal extremes behind the cliff.
- [ ] [Wikipedia, LogSumExp](https://en.wikipedia.org/wiki/LogSumExp)
      — the max-shifted identity and why it is finite.
- [ ] [Graves, Supervised Sequence Labelling with RNNs, §7.3.1](https://www.cs.toronto.edu/~graves/preprint.pdf)
      — the log-add identity for CTC's forward recursion (the 2012
      book; the 2006 paper rescaled instead).
- [ ] [Good, "Weight of Evidence: A Brief Survey"](https://www.cs.tufts.edu/~nr/cs257/archive/jack-good/weight-of-evidence.pdf)
      — log Bayes factors and Turing's deciban, behind scene 5's lore.
- [ ] [LessWrong/Arbital, "Bayes' rule: log-odds form"](https://www.lesswrong.com/w/bayes-rule-log-odds-form)
      — evidence in bits; 0 and 1 as ±∞ on the evidence ruler.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- e and the natural logarithm, done honestly — needs a `calculus/`
  topic first; the compound-interest table can then become a scene
  instead of a caption.
- The log-odds form of Bayes as a full scene in `probability/` (this
  series builds the ruler; that series owns the inference).
- Log scales in the wild as their own visual essay — dB vs pH vs
  magnitude vs semitones, with the Weber–Fechner motivation given its
  honest approximate status.
- Information as log-counting (bits, entropy) — the natural bridge
  from this topic toward information theory.
