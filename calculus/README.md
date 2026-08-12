# Calculus

## Scope

e and the natural logarithm, built on `algebra/`'s counting strip: the
strides of the strip come in every size, and this series finds the one
that is nature's own. Compound interest poses the question (Bernoulli's
ceiling between 2 and 3), a three-beat visual notion of local growth
rate answers it (the base whose slope is its own height), and ln lands
not as a new function but as the counter row in natural units — the
unit every earlier strip was secretly ruled in. The series pays two
standing promises: `MultiplyIsAdd`'s on-screen deferral ("calculus
later makes one base natural") and `TheUnderflowCliff`'s rendered
ln-identity, re-read symbol by symbol once every symbol means
something.

Deliberately **not** covered here:

- **The derivative as a toolkit.** Only "slope at a point, read by
  zooming until straight" is built — no rules, no d/dx notation, no
  limit formalism ("increasing and bounded has a limit" is named as
  analysis, never derived).
- **Integrals.** ln as the area under 1/t is named as the road not
  taken; accumulation waits for its own series.
- **Complex exponentials and Euler's formula** — rotation is a
  different story.
- **Softmax and likelihood.** Why e appears in every probability
  machine is owned by `probability/`'s softmax/likelihood series —
  delivered: its dial scene answers with this series' own ln
  (every base above 1 is e at another temperature).

## Concepts

### e_and_ln_manim.py

Watch in order. The first scene poses the question growth forces, the
second builds the only piece of calculus the series needs, the middle
two are the reveal — the constants are strides, and ln is the natural
counter row — and the last two are the payoffs, ending on the debt
`algebra/` left on screen.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheSplitYear` | $\lim_{n\to\infty}\left(1+\tfrac{1}{n}\right)^n = e$ | Splitting one year of 100% growth into more, smaller hops does not grow the outcome without bound — it crowds a ceiling. | Each refinement is more, smaller multiplicative hops: 2.25, 2.4414, 2.6130, 2.7146, 2.7181… strictly increasing yet under 3 (Bernoulli, 1683) — the two wrong intuitions (unbounded; collapses to 1) both die against the table. | Continuous growth is the limit every compounding process walks toward — the first number in history defined as a limit, and the same ceiling reappears mirrored as the binomial's zero-success limit ((1−1/n)ⁿ → 1/e) in [`probability/`](../probability/README.md)'s random-variables series. |
| 2 | `ZoomUntilStraight` | $\text{slope of } 2^x \text{ at } x = 2^x \times 0.6931\ldots$ | A growing curve has a readable growth rate at a point — no "instant" required. | Zoomed far enough, a smooth curve is straight (three panels, curvature dying); the ratio $(2^{dt}-1)/dt$ settles — 1.0, 0.7177, 0.6956, 0.69339 — with $dt$ a real number throughout; and one strip law ($2^{x+dt} = 2^x \cdot 2^{dt}$) carries the slope at 0 to every $x$. | The honest minimum of "derivative" for everything that follows — growth rate proportional to amount is what *exponential* means. |
| 3 | `TheMysteryConstants` | $0.6931 < 1 < 1.0986$ | Every base grows at a constant times its own height — and the constants obey the strip's laws before they have a name. | Base 8's constant 2.0794 is exactly three of base 2's 0.6931 (8 = 2³: three strides), so the constants are stride lengths in an undisclosed unit; between 2 and 3 sits the base whose constant is exactly 1 — and its value 2.718281828459… is scene 1's ceiling, back from a different question. | e defined by what it does (self-paced growth), not by its digits; why e is special without being big — 3ˣ outruns eˣ. |
| 4 | `TheNaturalStride` | $n \ln\!\left(1+\tfrac{1}{n}\right) \to 1$ | The undisclosed unit is the e-stride: the constants are ln b, and ln is the counter row in nature's units. | Change of base, one step: slope of bˣ at 0 = log_e b. The strip returns ruled 0, 0.693, 1, 1.386, 2.079 over 1, 2, e, 4, 8; a tiny hop costs its own size in strides (ln 1.01 = 0.0099503), so n·ln(1+1/n) = 0.9531, 0.99503, 0.99950 → 1 — the ceiling's natural counter is exactly 1, and the two definitions of e meet (the guarantee is analysis, named not derived). | Every log ever met is ln in a stretched unit; the bridge is the missing argument popular treatments skip. |
| 5 | `RateTimesTime` | $e^{rt}$ | Growth has one dial — rate × time — and e is its unit. | The knobs only multiply: 10 years at 3% ≡ 1 year at 30%; doubling means rt = ln 2, so t ≈ 0.693/r (≈13.86 years at 5% — 69.3 is the math, 72 the friendly-divisor convention); daily 5% compounding lands within 3.6×10⁻⁶ of e^0.05 — Bernoulli's ledger closes. | Doubling times, half-lives, continuous rates — every "how fast does it grow" question in one identity. |
| 6 | `TheDebtRepaid` | $\ln(a+b) = \ln a + \ln\!\left(1 + e^{\ln b - \ln a}\right),\ a \ge b$ | The repo's oldest forward reference, re-read with every symbol understood — then the inverse graph arrives as the promised payoff. | ln is the natural counter, e-to-a-counter is undo-never-cancel, and with the max factored out (a ≥ b) the shifted term lives in (0, 1]; at the cliff's own scale float64's 1 + e⁻⁴⁰ is exactly 1.0 (naive log: 0.0) while log1p(e⁻⁴⁰) ≈ 4.248×10⁻¹⁸ survives — ln(1+x) ≈ x is why handing x straight to the log keeps it; ln 2 = 0.693 marked on eˣ one point at a time, then the flip across y = x — earned, never the definition. | The stable log-sum-exp evaluation CTC implementations use in practice (log space is the 2012 book's move; the 2006 paper rescaled — see `algebra/`), now understood down to its symbols; Euler's name for the number (letter 1731, print 1736, 18 places by 1748). |

Renders are numbered to match: `01_TheSplitYear.mp4` …
`06_TheDebtRepaid.mp4`.

```bash
uv run python calculus/e_and_ln_manim.py
uv run python calculus/e_and_ln_manim.py --list
```

See the [root README](../README.md) for the full flag list.

### derivatives_manim.py

Watch after the e-and-ln series — `ZoomUntilStraight` built the
device this series names, and the mystery constants are about to
become derivatives. The toolkit is deliberately tiny: under the log,
every product the CTC road carries becomes a sum, so the sum rule,
the chain rule, and two owned derivatives are the whole kit.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheSlopeIsAFunction` | $\frac{d}{dx}$ | Every smooth curve carries a second curve — its slope at each point — and d/dx names the settling ratio the zoom built. | Zoom until straight at several points of one parabola and plot the read-offs: the forward quotients at x = 1 run 3, 2.1, 2.01, 2.001 — literally 2 + h — settling to 2; the dual graph keeps height and slope visibly different numbers; \|x\| never straightens, so the device needs smooth. | The object every gradient is made of; Leibniz's dy/dx (1675 manuscript, 1684 print) is the notation this repo commits to, because it makes the chain rule look like cancelling fractions. |

Renders: `01_TheSlopeIsAFunction.mp4`.

```bash
uv run python calculus/derivatives_manim.py
uv run python calculus/derivatives_manim.py --list
```

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-006 research pass
([`docs/plans/006-calculus-e-ln.md`](../docs/plans/006-calculus-e-ln.md))
and started unchecked; the maintainer reviewed the list (dropping two),
verified all sixteen that remain, and directed the ticks be recorded.
Future entries start unchecked until a human does the same.

- [X] [3blue1brown, "What's so special about Euler's number e?"](https://www.3blue1brown.com/lessons/eulers-number)
      — slope of $b^x$ proportional to itself; the measured constants
      0.6931/1.0986 revealed as ln b; e defined by constant = 1.
- [X] [3blue1brown, "The paradox of the derivative"](https://www.3blue1brown.com/lessons/derivatives)
      — derivative as best constant approximation around a point; dt as
      a concrete small number; "instantaneous" named as the paradox.
- [X] [Better Explained, "An Intuitive Guide to Exponential Functions & e"](https://betterexplained.com/articles/an-intuitive-guide-to-exponential-functions-e/)
      — e as the maximum of continuously compounded 100% growth; the
      splitting-interest pictures behind scene 1.
- [X] [Better Explained, "Demystifying the Natural Logarithm (ln)"](https://betterexplained.com/articles/demystifying-the-natural-logarithm-ln/)
      — ln as time-to-grow; rule of 72 from ln 2 = 0.693.
- [X] [Strang, "Introducing e^x" (MIT)](https://math.mit.edu/~gs/calculus/Article_Exponential.pdf)
      — the four routes to e compared with pedagogical critiques; ln 2
      marked on the e^x graph; the Bernoulli/Euler reference trail.
- [X] [Strang, Highlights of Calculus: "The Exponential Function" (MIT OCW)](https://ocw.mit.edu/courses/res-18-005-highlights-of-calculus-spring-2010/resources/the-exponential-function/)
      — slope equals height, drawn before any formula.
- [X] [Plus magazine, "Maths in a minute: Compound interest and e"](https://plus.maths.org/content/maths-minute-compound-interest)
      — Jacob Bernoulli 1683; the limit bracketed between 2 and 3.
- [X] [Brilliant, "The Discovery of the Number e"](https://brilliant.org/wiki/the-discovery-of-the-number-e/)
      — the discovery history: Bernoulli's compounding, Euler's
      notation dates.
- [X] [arXiv:2504.10664, "A cute proof that makes e natural"](https://arxiv.org/abs/2504.10664)
      — a pre-calculus bridge between the limit and slope-equals-height
      (flagged: checked at abstract level only in the research pass).
- [X] [O'Connor, Robertson, "The number e"](https://mathshistory.st-andrews.ac.uk/HistTopics/e/)
      — Bernoulli 1683 and the 2-to-3 bounds; Goldbach letter 1731;
      Introductio 1748 with 18 places.
- [X] [O'Connor, Robertson, "John Napier"](https://mathshistory.st-andrews.ac.uk/Biographies/Napier/)
      — 1614 Descriptio; Napier's logs are "not really to any base" —
      the misattribution scene 6 stays away from.
- [X] [OpenStax Calculus Vol. 1, §3.9](https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions)
      — Theorems 3.14–3.16; e defined as the unique base with slope 1
      at 0.
- [X] [Wikipedia, e (mathematical constant)](https://en.wikipedia.org/wiki/E_(mathematical_constant))
      — 30-digit e; the Meditatio manuscript, Goldbach letter, and
      Mechanica 1736 chronology.
- [X] [Wikipedia, History of logarithms](https://en.wikipedia.org/wiki/History_of_logarithms)
      — the exact form of Napier's logarithm.
- [X] [Wikipedia, Natural logarithm of 2](https://en.wikipedia.org/wiki/Natural_logarithm_of_2)
      — ln 2 to 30 places; the log₁₀2 digits behind the strip's 0.30103.
- [X] [OEIS A001113 (e), A002162 (ln 2), A002392 (ln 10)](https://oeis.org/A001113)
      — digit sequences; the research pass could not fetch OEIS (403),
      so these backed the two computational routes until the
      maintainer's verification closed the gap.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- The derivative as its own toolkit — power rule, chain rule, and the
  notation this series deliberately went without.
- ln as area under 1/t — the integral road not taken, and the honest
  start of accumulation.
- Euler's formula and complex rotation — the other famous thing e does.
- Growth in the wild: half-life and doubling time as the same picture
  (radioactive decay, population, interest — one dial, e^(rt)).
