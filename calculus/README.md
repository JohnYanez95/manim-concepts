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
  machine is foreshadowed in the closer and owned by `probability/`'s
  queued likelihood series.

## Concepts

### e_and_ln_manim.py

Watch in order. Under construction — scene 1 of six is stubbed; the
full design lives in
[`docs/plans/006-calculus-e-ln.md`](../docs/plans/006-calculus-e-ln.md).

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheSplitYear` | $\lim_{n\to\infty}\left(1+\tfrac{1}{n}\right)^n = e$ | Splitting one year of 100% growth into more, smaller hops does not grow the outcome without bound — it crowds a ceiling. | Each refinement is more, smaller multiplicative hops on the strip: 2.25, 2.4414, 2.6130, 2.7146, 2.7181… strictly increasing yet under 3 (Bernoulli, 1683) — the two wrong intuitions (unbounded; collapses to 1) both die against the table. | Continuous growth is the limit every compounding process walks toward — and the first number in history defined as a limit. |

Renders: `01_TheSplitYear.mp4` (further scenes land in Phase 2).

```bash
uv run python calculus/e_and_ln_manim.py
uv run python calculus/e_and_ln_manim.py --list
```

See the [root README](../README.md) for the full flag list.

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-006 research pass
([`docs/plans/006-calculus-e-ln.md`](../docs/plans/006-calculus-e-ln.md))
and starts unchecked until a human verifies it.

- [ ] [3blue1brown, "What's so special about Euler's number e?"](https://www.3blue1brown.com/lessons/eulers-number)
      — slope of $b^x$ proportional to itself; the measured constants
      0.6931/1.0986 revealed as ln b; e defined by constant = 1.
- [ ] [3blue1brown, "The paradox of the derivative"](https://www.3blue1brown.com/lessons/derivatives)
      — derivative as best constant approximation around a point; dt as
      a concrete small number; "instantaneous" named as the paradox.
- [ ] [Better Explained, "An Intuitive Guide to Exponential Functions & e"](https://betterexplained.com/articles/an-intuitive-guide-to-exponential-functions-e/)
      — e as the maximum of continuously compounded 100% growth; the
      splitting-interest pictures behind scene 1.
- [ ] [Better Explained, "Demystifying the Natural Logarithm (ln)"](https://betterexplained.com/articles/demystifying-the-natural-logarithm-ln/)
      — ln as time-to-grow; rule of 72 from ln 2 = 0.693.
- [ ] [Strang, "Introducing e^x" (MIT)](https://math.mit.edu/~gs/calculus/Article_Exponential.pdf)
      — the four routes to e compared with pedagogical critiques; ln 2
      marked on the e^x graph; the Bernoulli/Euler reference trail.
- [ ] [Strang, Highlights of Calculus: "The Exponential Function" (MIT OCW)](https://ocw.mit.edu/courses/res-18-005-highlights-of-calculus-spring-2010/resources/the-exponential-function/)
      — slope equals height, drawn before any formula.
- [ ] [Plus magazine, "Maths in a minute: Compound interest and e"](https://plus.maths.org/content/maths-minute-compound-interest)
      — Jacob Bernoulli 1683; the limit bracketed between 2 and 3.
- [ ] [Brilliant, "The Discovery of the Number e"](https://brilliant.org/wiki/the-discovery-of-the-number-e/)
      — the discovery history: Bernoulli's compounding, Euler's
      notation dates.
- [ ] [David Tall, "A Sensible Approach to the Calculus" (local straightness)](https://homepages.warwick.ac.uk/staff/David.Tall/themes/calculus.html)
      — zooming a differentiable graph until it looks straight as the
      cognitive root of the derivative; scene 2's license.
- [ ] [arXiv:2504.10664, "A cute proof that makes e natural"](https://arxiv.org/abs/2504.10664)
      — a pre-calculus bridge between the limit and slope-equals-height
      (flagged: checked at abstract level only in the research pass).
- [ ] [MacTutor, "The number e"](https://mathshistory.st-andrews.ac.uk/HistTopics/e/)
      — Bernoulli 1683 and the 2-to-3 bounds; Goldbach letter 1731;
      Introductio 1748 with 18 places.
- [ ] [MacTutor, John Napier](https://mathshistory.st-andrews.ac.uk/Biographies/Napier/)
      — 1614 Descriptio; Napier's logs are "not really to any base" —
      the misattribution scene 6 stays away from.
- [ ] [OpenStax Calculus Vol. 1, §3.9](https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions)
      — Theorems 3.14–3.16; e defined as the unique base with slope 1
      at 0.
- [ ] [NIST DLMF §4.2](https://dlmf.nist.gov/4.2)
      — e = 2.71828 18284 59045 23536…; ln as the road-not-taken
      integral; ln e = 1.
- [ ] [Wikipedia, e (mathematical constant)](https://en.wikipedia.org/wiki/E_(mathematical_constant))
      — 30-digit e; the Meditatio manuscript, Goldbach letter, and
      Mechanica 1736 chronology.
- [ ] [Wikipedia, History of logarithms](https://en.wikipedia.org/wiki/History_of_logarithms)
      — the exact form of Napier's logarithm.
- [ ] [Wikipedia, Natural logarithm of 2](https://en.wikipedia.org/wiki/Natural_logarithm_of_2)
      — ln 2 to 30 places; the log₁₀2 digits behind the strip's 0.30103.
- [ ] [OEIS A001113 (e), A002162 (ln 2), A002392 (ln 10)](https://oeis.org/A001113)
      — digit sequences; the research pass could not fetch OEIS (403),
      so these back the two computational routes and await a human eye.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- The derivative as its own toolkit — power rule, chain rule, and the
  notation this series deliberately went without.
- ln as area under 1/t — the integral road not taken, and the honest
  start of accumulation.
- Euler's formula and complex rotation — the other famous thing e does.
- Growth in the wild: half-life and doubling time as the same picture
  (radioactive decay, population, interest — one dial, e^(rt)).
