# Plan 009: `calculus/` — the derivative toolkit

Branch: `feat/calculus-derivatives`, cut from updated `main`
(1d8384d, the plan-008 merge).
Started: 2026-08-11.

Chosen as the roadmap's fourth stop because the plan-008 audit found
the derivative toolkit is now the **single gate behind three wiki
rows**: the CTC gradient / beam-search / peaky-dynamics bundle
(`deep_learning/` Ideas), the promised softmax-likelihood → CTC
gradient identity edge (spoken on screen by `TheLossThatTrains`'
closer), and `calculus/`'s own queued "derivative as its own toolkit"
Ideas entry. One series, multiple promises — the logarithms-series
shape. Behind it, the CTC gradient series starts with its numbers
already verified: plan 008's anchor M pins the analytic
p − one-hot gradient with a finite-difference check and Bridle
1989's prose statement.

Design rule (the post-CTC narrative direction): building-block series
ground backward. The derivative seed is already owned —
`ZoomUntilStraight` zooms a curve until it *is* straight, and
`TheMysteryConstants` showed 2^x and 10^x growing at rates
proportional to themselves without ever saying "derivative". This
series names what those scenes built, and points forward to the CTC
gradient only in when-useful framing.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research: pedagogy + source verification (agents in flight) | Scene design written into the plan |
| 1 | Plan committed, module stub in `calculus/` | `make check` |
| 2 | Scenes at draft; layout linter clean; frames verified by eye (steady beats + transition windows) | Layout linter clean + drafts verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render (`--jobs`) |

## Checklist

- [x] Phase 0: research reports received (pedagogy + source-verifier,
  both pinned below; the pedagogy agent survived one transient API
  interruption and was resumed), scene design finalized; three
  conventions decided at design time — forward quotients for every
  settling table (the symmetric quotient of a quadratic is exact and
  kills the narrative), the score-function route in place of the
  product rule, and Newton's dates kept off screen (secondary-only)
- [x] Phase 1: plan + module stub, `make check` green (204 tests;
  `--list` prints the stub)
- [x] Phase 2: all six scenes at draft (6 files, distinct names,
  31-40 s); the layout linter's first pass caught five real findings
  before any render (a persisting sum-rule block colliding with the
  chain lines, a takeaway box crossing a table, the likelihood curve
  through two captions, an edge-clipped saturation line) plus one
  restack on re-lint — all fixed, module clean; frame grids reviewed
  by eye across every beat, one further catch (the closer's takeaway
  box running near edge-to-edge, tightened)
- [x] Phase 3: README + wiki complete, `make test` green (204
  tests; calculus Scope grown to two series with the toolkit's
  exclusions, the Ideas entry struck delivered, twenty references
  landed unchecked for the maintainer's pass; wiki: node added, the
  e-and-ln toolkit promise flipped with its residual promises kept,
  two new delivered edges, both CTC-gradient rows narrowed to "only
  the identity remains", zoom lineage and the strip's fifth stop
  recorded, log entry appended)
- [ ] Phase 4: local CodeRabbit + connection-auditor clean
- [ ] Phase 5: PR, drafts cleaned, 1080p60 render verified

## Research questions the reports must settle

- Ordering: sensitivity-first (the 3b1b lineage — the nudge, the
  local stretch factor) vs limits-first (the standard course)? The
  repo's zoom device suggests sensitivity-first; confirm against the
  canonical treatments and the misconception literature.
- Which rules earn a scene: the chain rule is load-bearing for the
  CTC gradient — does the product rule earn its place (the likelihood
  curve p³(1−p) wants it), or does the log-derivative route
  (d ln L = 3/p − 1/(1−p)) make the product rule skippable?
- The MLE payoff: zero slope finds the peak the softmax series found
  by grid — how is that staged so it lands as a payoff, not a
  re-teach?
- The closer: d/dz LSE(z) = softmax(z) — the smooth max's
  sensitivities ARE the softmax shares. How much of the p − one-hot
  gradient does this series show, and how much stays for the CTC
  gradient series?
- Notation: dy/dx as a fraction — when it works, when it lies, and
  what the series commits to on screen.
- Exact numbers for every candidate beat: the difference-quotient
  table, the (e^h−1)/h → 1 ratio against the mystery constants, the
  ln-derivative checks, the likelihood-peak derivative values, the
  chain-rule example, the LSE/softmax gradient re-pinned, and the
  slope → −1 saturation of the NLL gap.

## Verified technical anchors (from the source-verifier report)

All exact (`Fraction` / 50–60-digit `Decimal`, no floats in
load-bearing values); primary sources fetched and read (Euler via the
Ian Bruce translation PDFs — link the PDFs directly, not
17centurymaths' contents pages, which are compromised).

**A. The zoom-made-arithmetic table, f(x) = x² at x = 1, forward
quotients.** ((1+h)² − 1)/h for h = 1, 1/10, 1/100, 1/1000 =
**3, 2.1, 2.01, 2.001 → 2** — every entry an exact terminating
decimal, zero rounding. The algebra behind it: the quotient is
exactly 2x + h, so the entries are literally 2 + h. **The symmetric
quotient is exactly 2 for every h** (a property of quadratics — it
kills the settling narrative; usable only as a punchline aside,
never as the main table).

**B. (b^h − 1)/h ratio table** (6 dp): b = e → 1.718282, 1.051709,
1.005017, 1.000500 → **1**; b = 2 → 1.000000, 0.717735, 0.695555,
0.693387 → **ln 2 = 0.693147…**; b = 10 → → **ln 10 = 2.302585…**.
Every constant the built e-and-ln series shows on screen re-verified
and matching (the 0.7177/0.6956/0.69339 rows, the
0.6931/1.0986/2.0794/2.3026 lineup, 2.0794 = 3 × 0.6931, e³ ≈
20.0855).

**C. Euler anchors, quote-verified from the primary PDFs.**
*Institutiones calculi differentialis* (1755), Part I Ch. VI:
**§188** "if e shall be the number, of which the hyperbolic logarithm
is = 1 … the differential of the quantity e^x will be = e^x dx";
§186 d(a^x) = a^x dx · ln a (the mystery constants' primary anchor);
**§180** d(ln x) = dx/x; **§181** the score rule in Euler's own
words ("the differential … divided by the quantity p will give the
differential, of which the logarithm is sought"); §183 the sum of
scores d ln(pqrs) = dp/p + dq/q + dr/r + ds/s. *Introductio* (1748)
**§122** names e ("we may put steadily the letter e for this number
2,71828 1828459 etc.", 23 decimals, all correct as a truncation);
§125 the series and (1 + z/i)^i. Safe on-screen anchor: "Euler named
e in 1748 (Introductio §122) and wrote d(e^x) = e^x dx in 1755
(Institutiones §188)." Uniqueness of f′ = f, f(0) = 1 has NO citable
primary — phrase as a fact, cite nothing.

**D. ln′ = 1/x numerically** at x = 2: forward quotients 0.405465,
0.487902, 0.498754, 0.499875 → 1/2; inverse route 1/e^(ln 2) = 1/2
exact. Score check on f(p) = 4p³(1−p) at p = 1/2: 3/p − 1/(1−p) =
**4 exactly**; symmetric FD 4.00000533 (h = 10⁻³).

**E. The MLE peak.** dL/dp = 12p² − 16p³ = **4p²(3 − 4p)** (the 4
must be on screen); roots p = 0 (double — not a peak) and **p = 3/4**;
L(3/4) = 27/64. Derivative grid (exact → 4 dp): p = 1/2 → **1
exactly**; 0.7 → 49/125 = 0.3920; 3/4 → 0; 0.8 → −64/125 = −0.5120.
Score grid: 1/2 → 4; 0.7 → 20/21 = 0.9524; 3/4 → 0; 0.8 → −5/4 =
−1.2500. Setting 3(1−p) = p ⟹ p̂ = 3/4 — a linear equation.
dL/dp = L · d ln L/dp checked exactly on the whole grid.

**F. The chain-rule table — (2x)² at x = 1 (recommended).** Inner
rate **2**, outer rate 2u at u = 2 → **4**, product **8**. Forward
quotients exact: **8.4, 8.04, 8.004 → 8**. The classic misconception
(outer rate evaluated at x = 1, not u = 2) predicts 4 — the table
refutes it on screen. ((1+x)² has an invisible inner rate of 1;
e^(2x) has unclean decimals — both rejected.)

**G. The CTC chain at z = (2, 1, 0), fresh 60-digit computation
matching plan 008 and the built scene.** softmax = (0.6652, 0.2447,
0.0900) (4-dp sum 0.9999 — never show it totalling 1.0000);
LSE = 2.407605964 → 2.4076. **∂ᵢLSE = softmaxᵢ**: symmetric FD
agrees to ≤ 1.6e−14 (forward only ~1e−7 — if a precision is spoken,
say "symmetric differences, ~10⁻¹⁴", or drop the number). Nudge beat:
z₁ → 2.01 moves LSE by 0.00666 ≈ 0.6652 × 0.01. Gradient for c = a:
**(−0.3348, 0.2447, 0.0900)** = p − one-hot, exact component sum 0
(4-dp sum −0.0001 — a rounding, don't display the sum).

**H. The saturation table, z = (2, 1, t), c = the third component.**
slope = p_c − 1: t = 0 → −0.9100; −2 → −0.9868; −5 → −0.9993;
−10 → −0.99999551 (displays as −1.0000 — a rounding; p_c there is
4.49e−6, show scientific notation or omit). loss(−10) − loss(−5) =
4.999338 over Δt = 5 — the "roughly linear gap" quantified.

**I. Attributions.** Chain rule: Leibniz used it in a 1676 memoir
(with a sign error); l'Hôpital 1696 implicit; unstated in Euler
(who *uses* substitution throughout Ch. VI); first modern statement
Lagrange 1797 — via Wikipedia's history faithfully citing Hernandez
Rodriguez & Lopez Fernandez 2010 (secondary chain; the safe sentence:
"Leibniz was already differentiating a composite in a 1676
manuscript; the rule's modern statement waited until Lagrange
(1797)"). Notation: Leibniz's dx, dy, dy/dx in the manuscript of
November 11, 1675 (Jeff Miller's Earliest Uses, MacTutor-hosted);
first print 1684 (Nova Methodus). Newton's fluxion-dot dates are
secondary-only — **keep Newton's dates off screen**. The term "chain
rule" is 20th-century (ca. 1937, Merriam-Webster).

## Pedagogy findings (pinned from the pedagogy-researcher report)

**Ordering — the sensitivity/local-straightness branch, with no real
choice in the matter.** Three camps exist: limits-first (the standard
course — front-loads the hardest formal object before the learner
wants it), sensitivity-first (3blue1brown's Essence of Calculus,
Strang's function pairs — limits arrive in chapter 7 to formalize
what is already believed), and infinitesimals-first (Thompson 1910,
Keisler; David Tall's research names *local straightness* — "a
differentiable function is one which looks straight when magnified" —
the cognitive root of the derivative). The repo has already built the
entry point: `ZoomUntilStraight` IS Tall's device rendered, with dt a
real number throughout and limit formalism excluded by design. This
series *names* what that scene built (d/dx as the settling ratio)
rather than re-deriving it.

**The keystone scope decision — the score function kills the product
rule.** d ln f = f′/f is "the counting strip differentiated": under
ln, products become sums (`MultiplyIsAdd`), so derivatives of
products become sums of relative rates. L(p) = 4p³(1−p) never needs
the product rule — ln L = ln 4 + 3 ln p + ln(1−p) differentiates term
by term with only the sum rule, ln′, and one chain-rule application
(ln(1−p) → −1/(1−p)). This is also what ML practice actually does
(maximize log-likelihood) and what CTC needs (path products already
carried in log space). One honest breath required: the log route
assumes f > 0 (the score is undefined at p ∈ {0, 1}).

**Scope IN:** derivative as local sensitivity named with d/dx (extend
`ZoomUntilStraight`); one geometric computation (the x² square
nudge — an example, not the power rule as drill); sum rule + constant
multiple; the chain rule (the single most load-bearing item); d/dx
e^x = e^x and ln′ = 1/x (re-reads of owned scenes; ln′ is one
chain-rule line via e^(ln x) = x — the undo trick, `TheDebtRepaid`'s
move); the log-derivative / score function; zero slope finds the
peak, honestly (sign change + the x³ cameo); ∂ᵢLSE = softmaxᵢ as the
closer with p − one-hot on screen. **OUT:** power rule as drill,
product/quotient rules, limits/ε–δ, integrals (queued separately),
Taylor, second-derivative tests, implicit differentiation, trig.

**Core devices:** (1) zoom-until-straight run at *many* points, the
read-offs plotted as a second curve — the slope is a *function*
(kills Orton's ordinate confusion: ~20% of interviewed students
thought the derivative was the y-value); (2) the dx-nudge /
secant-settling picture; (3) the x² square nudge — two x·dx strips
plus a dx² corner that visibly dies faster than the strips as dx
shrinks (Thompson's second-order smallness, shown not hand-waved);
(4) stacked heights for the sum rule; (5) three number lines for the
chain rule — dx causes dh causes dg, the dh cancellation as the
notation keeping a promise, mechanism first; (6) derivative as local
stretch factor (zoomed straight line IS a linear stretch — composed
maps compose stretch factors, so rates multiply); (7) slope-equals-
height re-read of `TheMysteryConstants` (e as the constant-1 base BY
DEFINITION — never "we now prove", that's circular); (8) ln′ via the
undo trick + the y = x mirror (slopes reciprocate: at x = e the slope
is 1/e, mirroring e^x's slope e at height e); (9) the score reader;
(10) the sign-change ribbon (+ → 0 → − at a peak; x³ touches zero
without changing sign; L's own derivative has a second root at p = 0
that is not the peak); (11) the smooth max's sensitivity shares — the
softmax bars reborn as a gradient read-out, same bars, same order,
same colors as `probability/`'s or the picture claims a different
object.

**Misconceptions to counter on screen:** tangent-touches-once (the
zoom makes it irrelevant; show a tangent that crosses); derivative =
y-value (the dual graph); dy/dx as a fraction / Δ conflated with d
(keep dt real, show the settling; at the chain rule say the
cancellation is designed notation, with the number lines as the real
mechanism); "instantaneous rate" as oxymoron (best constant
approximation around the point — `ZoomUntilStraight`'s phrasing,
keep it); zero slope ⇒ max (the converse error — x³ and the p = 0
root); chain rule as symbol-shuffling (mechanism via propagation AND
stretch composition — two independent reasons rates multiply).

**Pitfalls:** only *smooth* curves straighten under zoom (|x| never
does — never claim universality); one-sided secant sliders paper over
two-sidedness, draft both sides once; the MLE polynomial on screen is
4p²(3 − 4p) — the 4 must be there; gradient of the LOSS vs the
log-likelihood differ by a sign — state once that p − one-hot is the
gradient of NLL; the slope ribbon must agree with its curve at every
frame (picture-is-a-claim).

**Sequence recommendation:** slope-as-function → nudge geometry →
sum + chain rules → e^x/ln in notation → zero slope finds the peak
(the MLE payoff) → the smooth max's shares (the bridge payoff, CTC
one subtraction away).

## Scene design (built from both reports)

Module: `calculus/derivatives_manim.py`. Six scenes; the toolkit is
deliberately tiny (sum rule, chain rule, e^x, ln′, the score) because
the log turns every product the CTC road carries into a sum. Forward
quotients everywhere a table settles (anchor A's symmetric-quotient
trap); dt stays a real number throughout, per the owned discipline.

**1. `TheSlopeIsAFunction` — every smooth curve carries a second
curve: its slope at each point.**
Run `ZoomUntilStraight`'s device at several points of one parabola —
zoom, straighten, read the slope — and plot the read-offs beneath:
the slope is a *function*, and d/dx names the settling ratio the
e-and-ln series built (say so on screen — this scene generalizes an
owned one). The dual graph kills Orton's ordinate confusion (a dot
sliding on both curves, height and slope visibly different numbers).
The table beat: forward quotients at x = 1 — 3, 2.1, 2.01, 2.001 → 2
(anchor A), the entries literally 2 + h. Smoothness breath: |x| never
straightens at 0 — the device needs smooth. Notation beat (anchor I):
Leibniz's dy/dx (manuscript 1675, print 1684) vs Newton's dot (no
dates); this repo writes Leibniz, because it makes the chain rule
look like cancelling fractions — a promise scene 3 examines.

**2. `NudgeInNudgeOut` — for x², the answer is drawn, not computed.**
The literal square: side x, grow by dx; two x·dx strips and a dx²
corner that visibly dies faster than the strips as dx shrinks
(Thompson's second-order smallness, shown not hand-waved). At x = 3:
slope 6, finite check 6.01 → 6. Second view: the number-line stretch
factor — spacing near x = 1 doubles, near x = 3 sextuples, collapses
at 0 (`ZoomUntilStraight` in transformation clothing; a zoomed
straight line IS a linear stretch — the seed scene 3 harvests).

**3. `NudgesAddNudgesCompose` — the toolkit's two load-bearing
rules.**
Sum rule briefly (stacked heights: one nudge, two independent height
changes, the total is the stack). Then the chain rule as causality:
three number lines — dx causes du causes dy — with the stretch
factors composing. Worked table (anchor F): (2x)² at x = 1 — inner
rate 2, outer rate 4 *at u = 2*, product 8; quotients 8.4, 8.04,
8.004 → 8; the misconception (outer rate at x = 1 → predicts 4) is
stated and refuted by the table on screen. The dh cancellation named
as the notation keeping its promise — mechanism first, mnemonic
second.

**4. `TheCurveThatIsItsOwnSlope` — the mystery constants, in
notation.**
Re-read `TheMysteryConstants`: slope of b^x = ln b · b^x (Euler §186;
the built series' own 0.6931/1.0986/2.3026 lineup re-verified,
anchor B); e is the base whose constant is 1 **by definition and
measurement** — never "we now prove" (the circularity pitfall). The
ratio table (e^h − 1)/h → 1 (anchor B). Then the undo trick:
e^(ln x) = x, chain rule, ln′ = 1/x (Euler §180; `TheDebtRepaid`'s
undo-never-cancel move differentiated); the mirror beat — at x = e
the slope of ln is 1/e, the y = x reflection of e^x's slope e at
height e (rise and run swap, so slopes reciprocate). On-screen
anchor: "Euler named e in 1748; d(e^x) = e^x dx is his, 1755."

**5. `ZeroSlopeFindsThePeak` — the grid search is over.**
The owned likelihood curve L(p) = 4p³(1−p) with a slope ribbon under
it (+ climbing, 0 at the top, − descending; the ribbon agrees with
the curve at every frame — picture-is-a-claim). The score reader
introduced as the counting strip differentiated: d ln f = f′/f
(Euler §181 — his own sentence quotable; §183 the sum of scores),
products becoming sums of relative rates. Score = 3/p − 1/(1−p):
+4 at 1/2, +0.9524 at 0.7, **0 at 3/4**, −1.25 at 0.8 (anchor E);
the zero is a *linear* equation, 3(1−p) = p. The direct route shown
once for contrast: dL/dp = 4p²(3 − 4p) — same zero, plus a second
root at p = 0 that is not a peak. Converse-error beat: x³'s slope
touches zero without changing sign. Honesty breath: the score needs
f > 0 — true for likelihoods away from the endpoints.

**6. `TheSmoothMaxsShares` — the sensitivities of LSE are the
softmax.**
Nudge z₁ = 2 by 0.01: LSE moves 0.00666 = e²'s share of the total
(anchor G). Chain rule + sum rule in one screen: ∂ᵢLSE(z) =
e^(zᵢ)/Σe^(zⱼ) = softmax(z)ᵢ — the bars the probability series just
built, reborn as a *gradient read-out* (same bars, same order, same
colors, or the picture claims a different object). Then
NLL = LSE(z) − z_c differentiates in one line: gradient =
(−0.3348, 0.2447, 0.0900) = p − one-hot, landing on the repo's
pre-verified numbers; sign convention spoken once (this is the
gradient of the NLL — descending loss is ascending likelihood). The
saturation beat (anchor H): as the correct score falls behind, the
slope p_c − 1 walks −0.9100, −0.9868, −0.9993, → −1 — the softmax
series' "roughly linear gap" now a theorem. When-useful closer:
every frame of CTC hands this exact picture a different target — the
gradient series is next.

**Device lineage this series extends:** zoom-until-straight (named
and generalized), the mystery constants (renamed d/dx), the
undo-never-cancel flip (differentiated), the counting strip (its
derivative is the score), the likelihood curve and its peak (found
honestly), the LSE ruler and softmax bars (differentiated), the
factor-out-the-max convention (unneeded at z = (2,1,0), noted).

**Deliberately not in this series** (README exclusions): the power
rule as drill (only x² appears, as geometry); product and quotient
rules (the log route replaces them — and if CTC's forward-backward
factorization ever needs a bare product rule, that decision belongs
to the gradient series); limits and ε–δ; integrals ("ln as area
under 1/t" stays queued); Taylor series; second-derivative tests;
implicit differentiation; trig derivatives.
