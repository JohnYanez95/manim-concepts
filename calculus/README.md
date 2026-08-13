# Calculus

## Scope

Three series so far. The first: e and the natural logarithm, built on
`algebra/`'s counting strip: the
strides of the strip come in every size, and this series finds the one
that is nature's own. Compound interest poses the question (Bernoulli's
ceiling between 2 and 3), a three-beat visual notion of local growth
rate answers it (the base whose slope is its own height), and ln lands
not as a new function but as the counter row in natural units — the
unit every earlier strip was secretly ruled in. The series pays two
standing promises, both on-screen captions since the plan-011
refactor: `MultiplyIsAdd`'s deferral ("calculus later makes one base
natural") and `TheUnderflowCliff`'s loan note on its ln-identity —
re-read symbol by symbol once every symbol means something.
The second: **the derivative as a toolkit** — d/dx naming
the settling ratio the zoom built, nudge geometry for x², the sum and
chain rules, e^x and ln differentiated, the score function finding
the likelihood peak by hand, and the smooth max's sensitivities
revealed as the softmax shares — deliberately tiny, because under the
log every product the CTC road carries becomes a sum.
The third: **gradient descent** — the toolkit's payoff. One line,
w ← w − ηL′(w), turns a readable slope into a repeatable step; the
series watches the walk succeed, prices exactly when the learning
rate betrays it (the nudge square's corner is the curvature's fee),
stamps every stopping place with the sign-change habit, retires the
rolling-ball metaphor, and closes by reading the CTC road's own
training walk off a loss-vs-step chart.

Deliberately **not** covered here:

- **Limit formalism.** The first series reads slopes by zooming until
  straight; the second names that ratio d/dx and keeps dt a real
  number throughout — ε–δ and "increasing and bounded has a limit"
  stay named as analysis, never derived.
- **The power, product and quotient rules as drill.** Only x² appears,
  as geometry; the score function (d ln f = f′/f) replaces the product
  rule wherever this repo differentiates — the CTC gradient series
  faced that decision and resolved it: its log-sensitivity route
  needed no bare product rule (plan 010, decision 2), and
  `TheProductRule`'s rectangle stays in the drawer.
- **Second-derivative tests, Taylor series, implicit and trig
  differentiation** — none of them gated the CTC gradient, now built.
- **Integrals.** ln as the area under 1/t is named as the road not
  taken; accumulation waits for its own series.
- **Complex exponentials and Euler's formula** — rotation is a
  different story.
- **SGD, momentum, adaptive steps and schedules.** The descent series
  names them once as refinements layered on the bare update and
  teaches none of them — every training run this repo shows is plain
  gradient descent, undoped.
- **Newton's method and second-derivative machinery.** Curvature
  stays geometric (the nudge square's corner); the one-step teleport
  at the perfect rate appears as an unnamed aside at most.
- **Contour plots and vector machinery.** Many knobs cost one
  sentence and a loss-vs-step chart — 3blue1brown's own refusal to
  draw 13,002 dimensions is the precedent, not a compromise.
- **Continuous-time gradient flow.** The discrete hop is the object;
  a dot sliding smoothly down the curve cannot overshoot, ping-pong
  or diverge, and would silently falsify the learning-rate story.
- **Softmax and likelihood as content.** The concepts live in
  `probability/`'s softmax/likelihood series (its dial scene answers
  "why e" with this topic's own ln); the derivatives series here only
  *differentiates* those owned objects — the score of a likelihood,
  the sensitivities of the smooth max — and teaches neither afresh.

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
| 2 | `NudgeInNudgeOut` | $d(x^2) = 2x\,dx + dx^2$ | For x² the derivative is drawn, not computed — and the discarded term dies for a visible reason. | Grow the square's side by dx: two x·dx strips and a dx·dx corner; halve dx and the strips halve while the corner quarters — second-order small, discarded honestly; at x = 3 the slope is 6 (finite check 6.01); the number-line view shows the same fact as a local stretch factor (×2 near 1, ×6 near 3). | "Nudge in, response out" is the operational meaning of every derivative downstream — and the stretch factor is the seed the chain rule harvests. |
| 3 | `NudgesAddNudgesCompose` | $\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$ | The toolkit's two load-bearing rules: changes add across a sum, rates multiply along a chain. | Heights stack, so their changes stack; a nudge propagates through three number lines (dx causes du causes dy) with stretch factors composing — (2x)² at x = 1: inner rate 2, outer rate 4 at u = 2, product 8, and the quotient table 8.4, 8.04, 8.004 refutes the classic mistake (outer rate at x = 1 predicts 4); the du cancellation is Leibniz's notation keeping its promise. | Every use downstream is "ln of something" or "exp of something" — the chain rule is the single most load-bearing tool in the kit. |
| 4 | `TheCurveThatIsItsOwnSlope` | $\frac{d}{dx}e^x = e^x,\ \ \frac{d}{dx}\ln x = \frac{1}{x}$ | The mystery constants were derivatives all along, and e is the base whose constant is 1. | The slope of b^x is ln b · b^x (the owned 0.6931/1.0986/2.3026 lineup); (e^dt − 1)/dt settles through 1.7183, 1.0517, 1.0050, 1.0005 to 1 — by definition and measurement, nothing proved twice; ln′ = 1/x falls out of differentiating the undo e^(ln x) = x, and the y = x mirror swaps rise and run (slope 1/e at x = e). | The two derivatives the whole CTC road needs; Euler named e in 1748 (Introductio §122) and wrote d(e^x) = e^x dx in 1755 (Institutiones §188). |
| 5 | `ZeroSlopeFindsThePeak` | $\frac{d \ln L}{dp} = \frac{3}{p} - \frac{1}{1-p} = 0 \Rightarrow \hat{p} = \tfrac34$ | The curve-sweep is over: set the score to zero and the likelihood peak falls out of a linear equation. | The score d ln f = f′/f is the counting strip differentiated — under ln, products become sums of relative rates (Euler §181); on the owned curve the score runs +4, +0.9524, 0, −1.25 at p = 1/2, 0.7, 3/4, 0.8, flipping sign exactly at the peak, and the general line k/p − (n−k)/(1−p) = 0 derives p̂ = k/n — the claim `ProportionsConverge` made, now a theorem; the direct route 4p²(3 − 4p) has a second root at p = 0 that is a valley floor, and x³'s slope touches zero with no peak at all — zero slope is necessary, not sufficient; the score needs f > 0. | Maximum likelihood done honestly wherever a model is fitted — and the sign-change check is the habit that survives every optimizer, delivered by this topic's `WhereTheWalkStops`, which stamps every stopping place with it. |
| 6 | `TheSmoothMaxsShares` | $\frac{\partial}{\partial z_i}\mathrm{LSE}(z) = \mathrm{softmax}(z)_i$ | The sensitivities of the smooth max are the softmax shares — and the loss gradient is softmax minus one-hot. | Nudge z₁ = 2 by 0.01 and LSE moves 0.00666 = e²'s share of the total; one chain rule and one sum rule derive ∂ᵢLSE = softmaxᵢ, the owned bars reborn as a gradient read-out summing to 1; NLL = LSE − z_a (the correct class scoring 2) differentiates to (−0.3348, 0.2447, 0.0900) = p − one-hot, and as the correct score falls behind the slope walks −0.9100, −0.9868, −0.9993 → −1 — the softmax series' "roughly linear gap", now a theorem. | The gradient inside every classifier's training step; each frame of CTC hands this picture a different target — delivered by `deep_learning/`'s `SoftmaxMinusOccupancy`, which receives p − one-hot as the one-path special case, exactly as this closer promised. |

Renders: `01_TheSlopeIsAFunction.mp4` … `06_TheSmoothMaxsShares.mp4`.

```bash
uv run python calculus/derivatives_manim.py
uv run python calculus/derivatives_manim.py --list
```

### gradient_descent_manim.py

Watch after the derivatives series — every beat leans on the slope
being a function and on the sign-change habit. The rule is one line;
the series is about what the line does, what its single dial
controls, and what its stopping place does and does not certify.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheSlopeBecomesAStep` | $w \leftarrow w - \eta\,L'(w)$ | A slope is a reason to move: step against it, over and over, and for a small enough step the loss falls. | The nudge algebra forces the rule's shape — ΔL ≈ L′·Δw, choose Δw = −ηL′ and ΔL ≈ −η(L′)² ≤ 0; on L = w² with η = ¼, w₀ = 4 the walk halves forever (4, 2, 1, ½ — under 0.01 by step 9, w₉ = 4/512), and the steps shrink on their own because the slope does: the brake is the landscape's, not a schedule's. | The update inside every training loop this repo shows; the walk's stopping condition is the toolkit's zero-slope, inherited blindness and all. |
| 2 | `TheLearningRateIsABet` | $\lvert 1 - 2\eta\rvert < 1 \iff 0 < \eta < 1$ | The dial has a cliff, not a dimmer: one factor per bet decides glide, overshoot, ping-pong or blow-up. | On the bowl the update is w ← (1−2η)w, so each η is a scaling factor: ¼ → ×½ glides; ¾ → ×(−½) crosses the bottom every step yet converges — and its losses 16, 4, 1, ¼ are identical to the glide's, so the losses cannot betray the zigzag; 1 → ×(−1) ping-pongs 4, −4 forever; 5/4 → ×(−3/2) diverges; η = 1/40 arrives in 117 steps against 9 — too small never lies, it bills you. | Convergence is \|factor\| < 1, not monotonicity — the habit that reads real training curves without panicking at oscillation, and the claim stays pinned to its bowl. |
| 3 | `TheCornerChargesTheFee` | $\Delta L = 4\eta w^2(\eta - 1)$ | The learning rate is a bet about curvature, and the nudge square's corner is the fee that collects on it. | The toolkit's square with a finite step: strips pay 2wΔw, the corner charges Δw² back; with Δw = −2ηw the ledger reads exactly 4ηw²(η−1) — strips grow like η, the corner like η², tying at η = 1 (at w = 4: ΔL = −12, 0, +20 for η = ¼, 1, 5/4); on the sharper bowl 4w² the same η = ¼ ping-pongs (factor −1) and safe rates end at ¼. | Why there is no universally safe learning rate: the threshold is the landscape's property, read where the corner catches the strips — one bowl's glide is another's cliff. |
| 4 | `WhereTheWalkStops` | $L'(w) = 0$ | Gradient descent stops at flat ground, full stop — and cannot tell a valley from a hilltop from a shelf. | On the double well (L′ = w³ − w, flat at −1, 0, 1, η = 0.1): from 0.5 the walk climbs monotonically into the valley at 1 (within 0.01 by step 24); from exactly 0 it sits on the hilltop forever, gradient zero, certifying nothing (nudged to 0.1 it falls in by step 42); on w³/3 the crawl slows into a shelf that is no minimum at all — only the sign-change stamp says which flat ground was found. | The optimizer inherits the toolkit's blindness: zero slope is necessary, never sufficient — reading a converged run means asking what kind of flat it stopped on. |
| 5 | `TheWalkIsNotABall` | $w_1 = 4 - 0.1 \cdot 60 = -2$ | The rule jumps; a ball rolls — and the difference changes which valley the walk ends in. | Same double well, η = 0.1: from w₀ = 2 the walk is tame (2.0000, 1.4000, 1.2656, never below 1 — a ball would agree); from w₀ = 4 the slope is 60, one hop lands at −2, and the walk settles in the LEFT valley — impossible without teleporting; the basin map on the w-axis: starts in (0, √11 ≈ 3.317) land at +1; in (√11, ≈4.32) they cross — and farther out the map shatters (4.5 bounces back to +1; 5 diverges). A ball coasts, rolls off hilltops, never teleports; the rule has no memory, sits, and just did. | Retires the rolling-ball picture before it does damage: the honest metaphor is a walker reading the ground underfoot, one step at a time. |
| 6 | `TheRoadsOwnWalk` | $\mathbf{w} \leftarrow \mathbf{w} - \eta\,\nabla L(\mathbf{w})$ | Many knobs cost one sentence — the gradient collects every knob's slope — and the road's own training walk reads off one loss-vs-step chart. | The CTC road's 12-knob loss (η = 1) walks 0.7181 → 0.1602 (10) → 0.0356 (50) → 0.0088 (200) → 0.0003 (5000): ×0.86 per step early, ×0.9993 late — over three quarters gone in ten steps, and the log-axis replot still visibly falls; the long flat tail is scene 1's automatic brake at scale; frame 3 settles mixed at (0.032, 0.218, 0.750) with gradient ≈ 10⁻⁴ — y matches γ out of indifference, not certainty. | Reading real training curves: a plateau is the rule working, not failing. The bare update is the engine under deep learning — Cauchy, 1847, computing planetary orbits (as quoted by Lemaréchal); convergence theory a century later (Curry, 1944); everything else is refinement. |

Renders: `01_TheSlopeBecomesAStep.mp4` …
`06_TheRoadsOwnWalk.mp4`.

```bash
uv run python calculus/gradient_descent_manim.py
uv run python calculus/gradient_descent_manim.py --list
```

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
The first block below came out of the plan-006 research pass
([`docs/plans/006-calculus-e-ln.md`](../docs/plans/006-calculus-e-ln.md))
and started unchecked; the maintainer reviewed that list (dropping
two), verified all sixteen that remain, and directed the ticks be
recorded. The plan-009 block that follows was likewise verified by
the maintainer (one MacTutor credit corrected in his pass) and ticked
on his instruction.

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
- [X] [J J O'Connor and E F Robertson, "The number e" (MacTutor)](https://mathshistory.st-andrews.ac.uk/HistTopics/e/)
      — Bernoulli 1683 and the 2-to-3 bounds; Goldbach letter 1731;
      Introductio 1748 with 18 places.
- [X] [J J O'Connor and E F Robertson, "John Napier" (MacTutor)](https://mathshistory.st-andrews.ac.uk/Biographies/Napier/)
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

From the plan-009 research pass
([`docs/plans/009-calculus-derivatives.md`](../docs/plans/009-calculus-derivatives.md)),
for the derivatives series (the two 3blue1brown lessons above, already
verified for the e-and-ln series, carry into this one):

- [X] [Grant Sanderson, "The Essence of Calculus" (series)](https://www.3blue1brown.com/lessons/essence-of-calculus/)
      — the visual-first sequence this series' ordering follows:
      intuition before limits, limits arriving last.
- [X] [Grant Sanderson, "Power Rule through geometry"](https://www.3blue1brown.com/lessons/derivatives-power-rule/)
      — the x² square nudge: two strips of 2x·dx and a discardable
      dx² corner.
- [X] [Grant Sanderson, "Visualizing the chain rule and product rule"](https://www.3blue1brown.com/lessons/chain-rule-and-product-rule/)
      — stacked heights for the sum rule; the propagating nudge
      through three number lines.
- [X] [Grant Sanderson, "The other way to visualize derivatives"](https://www.3blue1brown.com/lessons/derivatives-and-transforms)
      — the derivative as a local stretch factor; composed maps
      compose their factors.
- [X] [Silvanus P. Thompson, Calculus Made Easy (1910)](https://www.gutenberg.org/files/33283/33283-pdf.pdf)
      — dx as "a little bit of x"; second-order smallness as the
      visible reason the corner dies.
- [X] [Gilbert Strang, "Big Picture of Calculus" (MIT OCW)](https://ocw.mit.edu/courses/res-18-005-highlights-of-calculus-spring-2010/resources/big-picture-of-calculus/)
      — calculus as pairs of functions: one tells how the other
      changes — the dual-graph device.
- [X] [Gilbert Strang, "Big Picture: Derivatives" (MIT OCW)](https://ocw.mit.edu/courses/res-18-005-highlights-of-calculus-spring-2010/resources/big-picture-derivatives/)
      — slope read from function pairs before any formula.
- [X] [David Tall, "Cognitive Roots"](https://homepages.warwick.ac.uk/staff/David.Tall/themes/cognitive-roots.html)
      — local straightness ("looks straight when magnified") as the
      cognitive root; the research backing the zoom device.
- [X] [A. Orton, "Students' understanding of differentiation" (1983)](https://link.springer.com/article/10.1007/BF00410540)
      — 110 clinical interviews: the ordinate confusion, dx conflated
      with finite increments, "rules without reasons".
- [X] [Leonhard Euler, Institutiones calculi differentialis I.VI (Bruce)](http://www.17centurymaths.com/contents/euler/diffcal/part1ch6.pdf)
      — §180 d(ln x) = dx/x; §181 the score rule in Euler's words;
      §183 the sum of scores; §186 d(a^x); §188 d(e^x) = e^x dx.
- [X] [Leonhard Euler, Introductio in analysin infinitorum I.VII (Bruce)](https://www.17centurymaths.com/contents/euler/introductiontoanalysisvolone/ch7vol1.pdf)
      — §122 the letter e and its 23 decimals; §125 the series and
      (1 + z/i)^i.
- [X] [Lawrence Murray, "Gradients of Softmax and Logsumexp"](https://indii.org/blog/gradients-of-softmax-and-logsumexp/)
      — the explicit ∇LSE = softmax derivation via the log-derivative
      rule.
- [X] [Nick Higham, "What Is the Log-Sum-Exp Function?"](https://nhigham.com/2021/01/05/what-is-the-log-sum-exp-function/)
      — LSE properties and the stable shifted form (the gradient
      itself lives in Murray's post).
- [X] [Gilbert Strang and Edwin Herman, OpenStax Calculus vol. 1, §3.6](https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule)
      — the standard limits-first chain-rule treatment, for contrast.
- [X] [H. Jerome Keisler, Elementary Calculus: An Infinitesimal Approach](https://people.math.wisc.edu/~keisler/calc.html)
      — the rigorous modern form of the infinitesimals-first camp.
- [X] [Jeff Miller, Earliest Uses of Symbols of Calculus](https://mathshistory.st-andrews.ac.uk/Miller/mathsym/calculus/)
      — hosted on MacTutor, created and maintained by John O'Connor
      and Edmund Robertson (University of St Andrews); Leibniz's dx,
      dy, dy/dx in the manuscript of November 11, 1675.
- [X] [Wikipedia, Chain rule (history section)](https://en.wikipedia.org/wiki/Chain_rule)
      — Leibniz's 1676 memoir (with a sign error), l'Hôpital
      implicit, Lagrange 1797 — citing Hernandez Rodriguez and Lopez
      Fernandez (2010).
- [X] [Hernandez Rodriguez and Lopez Fernandez, on the chain rule's history](https://scholarworks.umt.edu/tme/vol7/iss2/10/)
      — the underlying scholarship for the chain-rule history claims
      (landing page; text paywalled at verification time).
- [X] [Wikipedia, Nova Methodus pro Maximis et Minimis](https://en.wikipedia.org/wiki/Nova_Methodus_pro_Maximis_et_Minimis)
      — Leibniz's 1684 Acta Eruditorum paper, the first publication
      of the differential calculus.
- [X] [Yu. V. Sidorov, "Exponential function" (Encyclopedia of Mathematics)](https://encyclopediaofmath.org/wiki/Exponential_function)
      — (e^x)' = e^x as a modern reference statement.

From the plan-014 research pass
([`docs/plans/014-calculus-gradient-descent.md`](../docs/plans/014-calculus-gradient-descent.md)),
unverified until a human ticks them:

- [X] [Grant Sanderson, "Gradient descent, how neural networks learn" (3blue1brown)](https://www.3blue1brown.com/lessons/gradient-descent/)
      — the canonical intro: 1-D first, auto-shrinking steps, the
      local-minimum caveat, and the explicit refusal to visualize
      13,002 dimensions (the precedent for scene 6's one-sentence
      generalisation).
- [X] [Michael Nielsen, *Neural Networks and Deep Learning*, ch. 1](http://neuralnetworksanddeeplearning.com/chap1.html)
      — the derive-the-update route (choose the nudge so
      ΔC ≈ −η‖∇C‖² < 0) scene 1 follows, and the ball metaphor
      deployed with its own disclaimer.
- [X] [MIT 6.390 course notes, ch. 3, "Gradient descent"](https://introml.mit.edu/notes/gradient_descent.html)
      — 1-D-first ordering, the worked (x−2)² example, stopping
      criteria, and the oscillation/divergence pathologies.
- [X] [Gabriel Goh, "Why Momentum Really Works" (Distill)](https://distill.pub/2017/momentum/)
      — used only for its plain-descent analysis: the per-component
      factor 1 − αλ and the stability condition |1 − αλ| < 1.
- [X] [Jeremy Cohen and Alex Damian, "Part I: how does gradient descent work?"](https://centralflows.github.io/part1/)
      — the quadratic stability threshold 2/curvature and the
      flow-vs-discrete-steps contrast ("flow never oscillates") that
      scene 2's hop grammar guards.
- [X] [Ben Frederickson, "An Interactive Tutorial on Numerical Optimization"](https://www.benfrederickson.com/numerical-optimization/)
      — the learning-rate slider over animated iterate paths.
- [X] [Stanford CS231n course notes, "Neural Networks Part 3"](https://cs231n.github.io/neural-networks-3/)
      — the loss-curve cartoon per learning rate and the log-scale
      replot advice scene 6 uses.
- [X] [Jeremy Jordan, "Setting the learning rate of your neural network"](https://www.jeremyjordan.me/nn-learning-rate/)
      — the Goldilocks step diagrams and per-rate loss trajectories.
- [X] [Google Machine Learning Crash Course, "Gradient descent"](https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent)
      — iteration-table pedagogy with exact numbers per step.
- [X] [Ian Goodfellow, Yoshua Bengio and Aaron Courville, *Deep Learning*, §4.3](https://www.deeplearningbook.org/contents/numerical.html)
      — figure 4.1's sign-annotated bowl and figure 4.2's 1-D
      critical-point triple (flagged: fetched truncated in the
      research pass; figure annotations not re-verified).
- [X] [Mark Ainsworth and Yeonjong Shin, "Plateau Phenomenon" (arXiv)](https://arxiv.org/abs/2007.07213)
      — "Plateau Phenomenon in Gradient Descent Training of ReLU
      Networks": plateaus can end — apparent stagnation then renewed
      descent, so a flat stretch certifies neither arrival nor
      failure.
- [X] [Roger Grosse, CSC2541 lecture 9 slides](https://www.cs.toronto.edu/~rgrosse/courses/csc2541_2021/slides/lec09.pdf)
      — plain descent as the extreme-viscosity limit of the ball
      metaphor (flagged: confirmed via search excerpt, slides not
      fetched in the research pass).
- [X] [Andrew Ng, CS229 lecture notes 1](https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf)
      — the classic posit-the-rule course sequence, with the
      fixed-rate-still-converges observation.
- [X] [Claude Lemaréchal, "Cauchy and the Gradient Method"](https://ems.press/content/book-chapter-files/27368?nt=1)
      — Documenta Mathematica (2012), the scholarly note scene 6's
      history quotes ride on: Cauchy's 1847 Comptes Rendus note, its
      astronomy motivation, and "convergence is just sloppily
      mentioned".
- [X] [Augustin-Louis Cauchy, "Méthode générale" (C. R. 1847)](https://www.probabilityandfinance.com/pulskamp/Cauchy/Orbits/1847%20CR%20536%28383%29.pdf)
      — "Méthode générale pour la résolution des systèmes
      d'équations simultanées", C. R. Acad. Sci. Paris 25:536–538,
      1847; cited exactly per Lemaréchal's reference list (scan
      located and verified by the maintainer; the research pass had
      quoted it only via Lemaréchal).
- [X] [Haskell B. Curry, "The method of steepest descent" (QAM 1944)](https://www.ams.org/journals/qam/1944-02-03/S0033-569X-1944-10667-3/S0033-569X-1944-10667-3.pdf)
      — "The method of steepest descent for non-linear minimization
      problems", Quart. Appl. Math. 2(3):258–261, 1944; the first
      convergence study of the discrete method (paper located and
      verified by the maintainer; the research pass had confirmed
      only the bibliographic record).
- [X] [Ioannis Mitliagkas, IFT 6085 lecture 5 notes](https://mitliagkas.github.io/ift6085-2019/ift-6085-lecture-5-notes.pdf)
      — the scalar-quadratic rate ρ = |1 − αh| and the 2/h threshold
      (flagged: the notes' own "ρ ≤ 1" slip at equality is wrong —
      the repo's exact computation is the load-bearing check).
- [X] [Geoff Gordon and Ryan Tibshirani, CMU 10-725 lecture 5 notes](https://www.cs.cmu.edu/~ggordon/10725-F12/scribes/10725_Lecture5.pdf)
      — the fixed-step t ≤ 1/L convergence rate (a sufficient
      constant; the sharp quadratic threshold stays 2/L″).

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- ~~The derivative as its own toolkit~~ — delivered by this topic's
  derivatives series; the chain rule and the score carry the kit.
- ln as area under 1/t — the integral road not taken, and the honest
  start of accumulation.
- Euler's formula and complex rotation — the other famous thing e does.
- Growth in the wild: half-life and doubling time as the same picture
  (radioactive decay, population, interest — one dial, e^(rt)). The
  descent series' bowl walk w_k = 4·2⁻ᵏ already pre-draws the
  discrete half-life.
