# Plan 008: `probability/` — softmax, likelihood, log-likelihood

Branch: `feat/probability-softmax-likelihood`, cut from updated `main`
(5cb1ff9, the plan-007 merge).
Started: 2026-08-11.

Chosen as the roadmap's third stop, per the sequence confirmed by the
2026-08-11 connection-audit: this series is the remaining half of the
CTC bridge — the promise `probability/README.md` has carried since the
independence series ("per-frame softmax as a distribution, likelihood
and log-likelihood"). Both of its gates are now delivered: e as the
self-paced base via `calculus/` (plan 006), and distributions-as-objects
via the random-variables series (plan 007), whose closer names this
series on screen ("likelihood is next"). Behind it waits the CTC
gradient identity — the per-frame gradient is softmax output minus
posterior occupancy, which is only legible once softmax and
log-likelihood are owned.

Design rule for this series (the post-CTC narrative direction): this is
a building-block series — it grounds every beat in prior topics
(the quartered square, the counting strip, ln's natural stride, the
underflow cliff, the binomial columns) and points forward to CTC only
in when-useful framing.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research: pedagogy + source verification (agents in flight) | Scene design written below |
| 1 | Plan committed, module stub in `probability/` | `make check` |
| 2 | Scenes at `--quality draft`; renders verified (count, names, ffprobe, frames incl. transition windows and every beat's steady state) | Draft renders verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render |

Pre-phase commit folded onto this branch (per the standing process
decision — light fixes ride the next topic branch): plan 007's Phase 5
tick, recording the merged PR #8 and the verified 1080p60 finals.

## Checklist

- [x] Phase 0: research reports received (pedagogy + source-verifier
  main report + on-request addendum, all pinned below), scene design
  finalized; two conventions decided at design time — the count lens
  everywhere (table rows and curve agree; sequence ÷4 spoken once)
  and the owned biased die over a numerically-prettier new one
- [x] Phase 1: plan + module stub, `make check` green (187 tests;
  `--list` prints the stub)
- [ ] Phase 2: all scenes render at draft; verified per CLAUDE.md
  checklist
- [ ] Phase 3: README + wiki complete, `make test` green
- [ ] Phase 4: local CodeRabbit + connection-auditor clean
- [ ] Phase 5: PR, drafts cleaned, 1080p60 render verified

## Research questions the reports must settle

- Ordering: likelihood-first (flip the lens on a picture the viewer
  owns, then meet softmax as the machine that manufactures per-frame
  distributions) vs softmax-first (scores → distribution, then ask
  how good the distribution is)?
- The likelihood flip: which owned picture stages "data fixed,
  parameter varies" best — the quartered square re-cut at varying p
  (plan 007's device), or the binomial columns?
- "Why e": how much of the answer is temperature/base-equivalence
  (any base is e at another temperature — the counting-strip
  base-as-unit lesson again) and is that the honest on-screen claim?
- Log-likelihood: how to stage product-becomes-sum so it lands as a
  re-read of `TheUnderflowCliff` and `MultiplyIsAdd` rather than a
  re-teach.
- Scope: does the gradient identity (softmax minus one-hot) get
  foreshadowed with a pinned number, or stay entirely in when-useful
  prose? MLE: Bernoulli p̂ = k/n only, or is even that deferred?
- Calibration and temperature: which belongs on screen vs in the
  README's exclusions?
- Exact numbers for every candidate beat: a clean 3-class softmax
  example, shift invariance, the overflow case and max-subtraction,
  temperature sweep values, the Bernoulli likelihood curve and its
  argmax, product-vs-sum-of-logs for a per-frame chain, and the
  float32 46-frame cliff (already on screen in `algebra/`, re-verified).

## Verified technical anchors (from the source-verifier report)

All computed in exact rationals (`Fraction`) or 60-digit `Decimal`,
two independent routes where stated; float32/float64 demos via numpy.

**A. The softmax workhorse, z = (2, 1, 0).**
e² = 7.389056…, e¹ = 2.718281…, e⁰ = 1; denominator 11.10733793.
p = (0.6652, 0.2447, 0.0900) at 4 dp. Exact sum = 1, but **the three
4-dp roundings sum to 0.9999** — a scene must never show the rounded
values totalling 1.0000 digit-by-digit.

**B. Shift invariance / subtract-max.** softmax(z + c) = softmax(z)
exactly as mathematics (e^c cancels); in float64 the observed
difference is 0 or 1 ulp (1.11e-16). On-screen phrasing: "exactly the
same distribution", never "bitwise identical".

**C. Overflow mirror.** float64 exp overflows above ~709.78. Naive
softmax(1000, 1001, 1002) = (inf, inf, inf) → **(nan, nan, nan)**;
subtract the max → softmax(−2, −1, 0) = (0.0900, 0.2447, 0.6652) —
exactly the workhorse numbers reversed (verified to 60 digits). Clean
symmetry for the animation.

**D. Temperature on z = (2, 1, 0).**
T = 0.5 → (0.8668, 0.1173, 0.0159) (4-dp sum 1.0000);
T = 1 → (0.6652, 0.2447, 0.0900) (4-dp sum 0.9999);
T = 2 → (0.5065, 0.3072, 0.1863) (4-dp sum 1.0000).
Limits verified numerically: T = 0.01 → (1, 3.72e-44, 1.38e-87) ≈
one-hot; T = 1000 → (0.333667, 0.333333, 0.333000) → uniform. T→0 is
a **limit** (clamp any dial; one-hot requires a unique argmax — holds
here).

**E. Base change = temperature.** b^z/Σb^z = softmax(z·ln b); base 2
on (2, 1, 0) is **exactly (4/7, 2/7, 1/7)** = (0.5714, 0.2857,
0.1429) by Fraction arithmetic — a rational softmax, contrasting the
irrational base-e values. Base b ≡ temperature T = 1/ln b.

**F. Softmax attribution (primary PDF, NIPS 1989 proceedings).**
John S. Bridle, "Training Stochastic Model Recognition Algorithms as
Networks can lead to Maximum Mutual Information Estimation of
Parameters", NIPS 1989. Verbatim coinage: "…a differentiable
generalisation of the 'winner-take-all' operation of picking the
maximum value. For this reason we like to refer to it as soft max."
The companion NATO chapter ("Probabilistic Interpretation of
Feedforward Classification Network Outputs…", Springer 1990,
pp. 227–236) is the conventional "Bridle 1990" citation — 1989
workshop, 1990 publication, both defensible. The Boltzmann/Gibbs form
p_i = e^(−E_i/kT)/Z is literally softmax(−E/kT) (verified
computationally); attribute the *form* to statistical mechanics
generally or Gibbs 1902 — a specific "Boltzmann 1868" claim is
unverified, avoid it.

**G. Likelihood attribution (via Aldrich 1997, Statistical Science
12(3), with verbatim Fisher quotes).** Fisher named and defined
likelihood in 1921 (Metron 1, pp. 3–32: "…we define the likelihood as
a quantity proportional to the probability that … a sample having the
observed value … should be obtained"; "We can know nothing of the
probability of hypotheses … [we] may ascertain the likelihood of
hypotheses") and generalized in 1922 (Phil. Trans. Roy. Soc. A 222,
pp. 309–368). Safe phrasing: "Fisher named it likelihood in 1921 and
defined it in general in 1922" — the "first-ever use" claim is
secondary-source only.

**H. The Bernoulli likelihood curve, data HHTH (k = 3 in n = 4).**
L(p) = p³(1−p), exact fractions:
L(0.1) = 9/10000 = 0.0009 · L(0.25) = 3/256 ≈ 0.0117 ·
L(0.5) = 1/16 = 0.0625 · L(0.7) = 1029/10000 = 0.1029 ·
**L(0.75) = 27/256 = 0.10546875 (the peak)** · L(0.8) = 64/625 =
0.1024 · L(0.9) = 729/10000 = 0.0729.
ln L: −7.0131 (p=0.1) · −2.7726 (0.5) · −2.2740 (0.7) ·
**−2.2493 (0.75)** · −2.2789 (0.8) · −2.6187 (0.9).
MLE two routes: analytic dL/dp = p²(3−4p) = 0 → p̂ = 3/4 = k/n;
grid search (1/100 and 1/1000 steps) returns exactly 3/4.
Count version C(4,3)p³(1−p) = 4p³(1−p): peak value 27/64 = 0.421875,
ln lifted by the constant ln 4 = 1.386294, argmax unchanged. Pick one
convention per picture and say the C(4,3) lift moves nothing, once.

**I. Product → sum of logs.** Probabilities (0.9, 0.8, 0.7, 0.9,
0.6): exact product 1701/6250 = **0.27216**. Per-factor ln: −0.1054,
−0.2231, −0.3567, −0.1054, −0.5108; sum = **−1.3014**
(−1.3013651503); exp(sum) = 0.27216 ✓. log₂ route: sum −1.8775,
2^sum = 0.27216 ✓.

**J. Underflow cliff re-verified (matches what `algebra/` has on
screen).** float32 smallest subnormal = 2⁻¹⁴⁹ ≈ 1.4013e-45 (numpy
prints `1e-45`); cumulative product of 0.1: 45 factors → smallest
subnormal, **46 factors → exactly 0.0**. float64: 0.1³²³ prints
1e-323 (nonzero subnormal), **0.1³²⁴ = 0.0 exactly**, both routes.
Log route survives: 324·log₁₀(0.1) = −324.0 exact; 46·ln(0.1) =
−105.9189. (Display values are Python's shortest-repr — fine at
display precision; don't claim exact stored binary values.)

**K. Monotone log → same argmax.** argmax L = argmax ln L = 3/4 on
both grids (endpoints excluded — log undefined at 0 and 1).

**L. NLL and the LSE gap, z = (2, 1, 0).** −ln softmax(z)_c =
LSE(z) − z_c = **2.4076 − z_c**: correct class scoring 2 → 0.4076;
scoring 1 → 1.4076; scoring 0 → 2.4076 (consecutive scores → NLLs
differ by exactly 1).

**M. Gradient foreshadow (pinned, NOT taught).** ∂/∂z_i
[−ln softmax(z)_c], c = the score-2 class: analytic
(−0.3348, 0.2447, 0.0900) = p − one-hot; finite differences agree to
4.6e-11. Bridle 1989 states it in prose: "the derivative before the
output nonlinearity is the difference between the corresponding
output and a one-from-N target."

**N. Vocabulary anchors.** Deep Speech (Hannun et al. 2014,
arXiv:1412.5567): character set {a…z, space, apostrophe, blank} —
29 classes (the count is arithmetic on the quoted set, not a numeral
in the paper), "the output layer is a standard softmax function".
GPT-2 (Radford et al. 2019): "The vocabulary is expanded to 50,257."

### Addendum anchors (on-request, second verifier pass)

All exact `Fraction` arithmetic, two routes where stated.

**A1. Dice MLE beat, rolls (6, 6, 3).** Fair die: (1/6)³ = 1/216 ≈
0.00463, ln −5.3753. Owned biased die (double weight on 6: p(6) =
2/7, others 1/7; sums to 1 exactly): (2/7)²(1/7) = 4/343 ≈ 0.01166,
ln −4.4514. Ratio owned/fair = 864/343 = 2.5190 (display 2.52). (A
starker new die with p(6) = 1/2 gives 1/40 = 0.025 and ratio exactly
5.4 — cleaner numbers, but the design keeps the owned die for device
continuity; decision recorded below.)

**A2. The two-lens table, P(k | n = 4, p), denominator 256
throughout.** Columns p = 1/4 · 1/2 · 3/4, rows k = 0..4:
(81, 108, 54, 12, 1)/256 · (16, 64, 96, 64, 16)/256 =
(1, 4, 6, 4, 1)/16 · (1, 12, 54, 108, 81)/256. Each column sums to
exactly 1; the p = 3/4 column is the p = 1/4 column reversed term by
term. **Pinned row k = 3: (3/64, 1/4, 27/64) = (0.0469, 0.2500,
0.4219); exact row sum 23/32 = 0.71875** — visibly ≠ 1. Convention
flag: this table is the *count* lens (carries C(4,3) = 4); its
p = 3/4 entry 27/64 is exactly 4× the sequence value 27/256.

**A3. Not a density over p.** ∫₀¹ p³(1−p) dp = 1/20 = 0.05 exactly
(Beta(4,2) route and term-by-term route agree; numeric to 2.1e-14);
count version ∫₀¹ 4p³(1−p) dp = 1/5 = 0.2 exactly. Both ≠ 1 under
either convention. Narration care: the *columns* of A2 do each sum to
1 over outcomes; it is the sweep over p that has no reason to
normalize.

**A4. CTC-flavored per-frame product.** Columns (0.7, 0.2, 0.1),
(0.6, 0.1, 0.3), (0.2, 0.1, 0.7) over {A, B, blank} — each sums to
exactly 1. Path A→A→blank: product 147/500 = **0.294 exactly**;
ln factors −0.3567, −0.5108, −0.3567; sum **−1.2242**
(−1.2241755116, Decimal and float64 routes identical); exp(sum) =
0.294 ✓. float32 at 3 frames: both routes fine (ln-route round-trip
0.29400003 — safe at 4-dp display); the contrast lives at the
46-frame cliff.

## Pedagogy findings (pinned from the pedagogy-researcher report)

**Ordering — likelihood arc first, softmax arc second, join last.** The
canonical treatments split three ways: theory-first (Goodfellow ch. 5→6
does MLE before softmax units), stats-education (StatQuest/Etz make
"probability is not likelihood" its own lesson *before* MLE — the
ordering that demonstrably makes the distinction stick), and
practitioner-first (logits → softmax → cross-entropy, likelihood
mentioned in passing — the ordering that *manufactures* the "log is
just a numerical trick" misconception). The repo carries two open
promises pointing opposite ways — random-variables closed with
"likelihood is next", e-and-ln closed with "why e appears in every
probability machine" — and the hybrid honors both: likelihood lens →
MLE → log-likelihood → softmax (e's promise pays off) → NLL of softmax
(log-sum-exp returns as `log softmax_i(z) = z_i − LSE(z)`).

**Stay fully discrete.** StatQuest's normal-curve device reads
likelihood off a density axis (values can exceed 1); the repo can use
coins, dice, and softmax columns, where every likelihood value *is* a
genuine probability of the observed data. No normal curve anywhere in
this series.

**Core devices** (each grounds in an owned picture):

1. *The two-lens grid* — the binomial table indexed by parameter p
   (columns) and outcome k (rows). A column slice is a pmf (bars sum
   to 1 — the sorted square); a row slice with the observed k pinned
   is the likelihood function, and its bars visibly do NOT sum to 1.
   "Same number, different question" as literal geometry.
2. *Likelihood curve with log-curve below, peaks aligned* — shows
   monotonicity's consequence instead of asserting it.
3. *Product of bars → sum of log heights* — reprise of MultiplyIsAdd
   and TheUnderflowCliff.
4. *The logit bar morph* (3b1b's device) — raw scores with two visible
   defects (negatives, wrong total); exp repairs one, normalizing the
   other.
5. *Shift invariance forces exp* — naive z/Σz fails on negatives and
   changes under +c; only an exponential turns an additive shift into
   a common factor the normalizer cancels. Subtract-max stability is
   then a *corollary*, not a hack.
6. *Temperature dial* — sharpens to one-hot (T→0, a limit — clamp the
   dial, never divide by zero), flattens to uniform (T→∞), winner
   never changes. Doubles as the calibration caveat (Guo et al. 2017:
   temperature scaling recalibrates without changing predictions).
7. *Base = temperature* — softmax base 2 of (3,1,0) is exactly
   (8/11, 2/11, 1/11); b^z = e^(z ln b). Discharges the e-series
   promise: nothing forces e in the family; e is the natural unit
   because ln is the natural counter.
8. *NLL as a gap* — −log softmax_c = LSE(z) − z_c: the smooth-max
   ruler (owned) vs the correct class's bar. Calculus-free, and it is
   the exact quantity CTC's gradient differentiates later.
9. *Per-frame product on the CTC matrix* — one highlighted entry per
   column, product across frames, flip to summed log-bars; legal
   *because* "independent given the input" was already taught.

**Misconceptions to counter on screen:** likelihood vs probability
(slice one table two ways — never argue definitions); "likelihood is a
distribution over parameters" (compute the total: p²(1−p) has area
1/12); "MLE finds the most probable parameter" (that's MAP — the
posterior ladder shows likelihood is the rung, not the posterior);
"the log is only numerical convenience" (three beats: monotone lens,
log as the native scale of accumulating independent evidence — the
evidence ruler *is* a log-likelihood-ratio ruler — and the log undoing
the exp so the loss never flattens; underflow survival is the bonus);
"softmax outputs are calibrated" (Guo caveat); "why e not 2 or 10"
(base = temperature); "why not divide by the sum" (the naive
normalizer failure); "low temperature changes the winner" (it never
does — monotone at every T > 0).

**Pitfalls the good treatments hit:** T = 0 is a limit, not a value;
softmax is invariant to shifts only, NOT to scaling (scaling is
temperature); the sequence-vs-count likelihood wobble (C(10,7) = 120
lifts the whole curve by a constant — state once that it moves
nothing, since the repo already put C(n,k) columns on screen);
overflow is the untaught mirror of the underflow cliff (e^710
overflows float64; subtract-max fixes it via the invariance just
proved); name the loss NLL, acknowledge the "cross-entropy" alias and
the PyTorch CrossEntropyLoss = LogSoftmax + NLLLoss split in one
breath; no gradient/saturation claims — the calculus-free survivor is
"the gap LSE(z) − z_c grows roughly linearly as the correct score
falls behind"; keep every log in ln (nats) to match the counter row.

**Scope verdict from the report:** land softmax (definition, shift
invariance, soft-argmax, why-e), likelihood (the flip), dataset
likelihood as product under conditional independence, log-likelihood
and NLL, the one-hot collapse, and the LSE-gap identity. Defer: the
gradient p − y (forward-pointer only — no derivative toolkit exists),
entropy/KL/soft-target cross-entropy, Gaussian MLE and all densities,
MAP-as-treatment, calibration methods beyond the one caveat beat.

## Scene design (built from both reports)

Module: `probability/softmax_likelihood_manim.py`. Six scenes, all
discrete throughout (no density ever drawn — every likelihood value
on screen is a genuine probability of observed data). Logs stay in ln
(nats) to match the counter row. The series splits into a likelihood
arc (1–3), a softmax arc (4–5), and the join (6).

**1. `TheLikelihoodLens` — probability and likelihood are one table
read two ways.**
Claim: likelihood is not a new number; it is the old number with the
question flipped. Build the two-lens table: three binomial pmfs for
n = 4 side by side — the sorted-square columns at p = 1/2 (owned:
(1,4,6,4,1)/16) flanked by the p = 1/4 re-cut (owned from
`TheBinomialColumns`) and its p = 3/4 mirror (addendum A2 fractions).
Column lens (COOL): pin a p, sweep k — bars sum to 1, a pmf. Row lens
(ACCENT): pin the *observed* data k = 3, sweep p — a new function of
p, and its three bars visibly do not sum to 1 (A2's row sum, 23/32 =
0.7188). Name it: likelihood, "Fisher named it in 1921".
**Convention decision: the count lens everywhere** — the table rows
carry C(4,k), so the scene-2 curve is 4p³(1−p) and its labeled points
agree with the pinned row exactly; the sequence-vs-count ÷4 is stated
once, in scene 3's constant-lift beat. Takeaway: same table, two
questions — "given the coin, what data?" vs "given the data, what
coin?". Closes `ProportionsConverge`'s on-screen "likelihood is next".

**2. `TheBestExplanation` — the peak of the row names the parameter
that explains the data best.**
Discrete first: rolls (6, 6, 3) against two candidate dice — the fair
die vs the owned biased die (double weight on 6; addendum A1 decides
whether the owned die or a starker 1/2-weight die is the cleaner
contrast). Likelihoods computed as plain products; the ratio is the
verdict, and the ratio is a rung of the owned posterior ladder
(likelihood is the update *factor* — with a flat prior "most likely
parameter" and "best explanation" coincide; that is MLE, not a
posterior). Dice decision: the **owned die** — 2.52× beats a
prettier 5.4× because the viewer already owns the die ("the balance
point belongs to the measure" continuity). Then continuous sweep on
the coin: L(p) = 4p³(1−p) (count lens, per scene 1's decision) traced
over [0,1] through the A2/H anchor values (0.0469 at 1/4, 0.25 at
1/2, peak 27/64 = 0.4219), peaking at p̂ = 3/4 = k/n =
the observed proportion — `ProportionsConverge` read backwards: the
proportion converges to p, so the proportion is the best guess at p.
Guard beat (misconception 2): the area under the curve is not 1
(addendum A3) — likelihood is never a distribution over p; making it
one takes a prior and a renormalization (the owned Bayes move,
pointed at, not performed).

**3. `AddToSurvive` — log the likelihood: nothing about the answer
changes, everything about the arithmetic does.**
Three beats, one per reason (misconception 4). (i) Monotone lens:
L(p) above, ln L(p) below, one vertical line through both peaks at
3/4 (anchors H, K) — the answer untouched. (ii) Native scale:
per-observation bars multiply (anchor I: product 0.27216) while their
log-counters stack additively (sum −1.3014, exp recovers it) — the
counting strip carrying likelihood now; the evidence ruler was a
log-likelihood-ratio ruler all along, said on screen. (iii) Survival,
the bonus: the underflow cliff reprise (anchor J: float32 dead at 46
factors of 0.1; 0.1³²⁴ = 0.0 exactly in float64) — the sum-of-logs
walks down by −105.9189 and −324 unharmed. Constant-lift beat (the
one place sequence-vs-count is spoken): the exact sequence HHTH has
likelihood p³(1−p) — the count curve divided by C(4,3) = 4 — so its
ln sits exactly ln 4 = 1.3863 below, same shape, same peak
(anchor H). Takeaway: maximize ln L; call its negative the
loss.

**4. `TheProbabilityMachine` — exp then normalize is how scores
become a distribution.**
A model emits raw scores z = (2, 1, 0) — some model, any model; the
repo's per-frame matrix is where they are headed. Defect bars: scores
can be negative and don't total 1. Naive repair z/Σz fails on screen:
shift (3, 2, 1) changes the shares, (1, −1, 0) goes negative. The
exponential repair: e^z lifts everything positive, normalize —
p = (0.6652, 0.2447, 0.0900) (anchor A; never show the rounded
values totalling 1.0000). The forcing argument (level 2): requiring
"+c on every score changes nothing" *forces* an exponential — e^c
factors out of every term and cancels (anchor B, "exactly the same
distribution"). Corollary, not hack: softmax(z) = softmax(z − max z),
so the overflow case (1000, 1001, 1002) → NaN naively is rescued to
(0.0900, 0.2447, 0.6652) — the workhorse reversed (anchor C).
Attribution beat: Bridle's coinage quoted (anchor F), "soft max" —
a differentiable winner-take-all.

**5. `TurningTheDial` — softmax is a soft argmax with a sharpness
dial, and the dial proves the outputs are asserted, not certified.**
Temperature sweep on the workhorse (anchor D): T = 0.5 sharpens to
(0.8668, 0.1173, 0.0159), T = 2 flattens to (0.5065, 0.3072,
0.1863); endpoints as limits — T→0 the one-hot winner-take-all
(clamped dial, labeled limit), T→∞ uniform. The winner never changes
at any T > 0 — exp and scaling are monotone. Why e (the e-series'
promise paid): base 2 on the same scores is exactly (4/7, 2/7, 1/7)
(anchor E) — a *rational* softmax — and b^z = e^(z ln b): every base
is e at another temperature, so nothing forces e except that ln is
the natural counter (`TheNaturalStride` re-read). Caveat beat (Guo et
al. 2017): modern networks are overconfident, and fitting one shared
T recalibrates them *without changing any prediction* — numbers that
can be rescaled wholesale were asserted, not measured.

**6. `TheLossThatTrains` — score the machine by the log-likelihood it
assigns to the truth; across independent frames, losses add.**
One-hot collapse: with a single correct class, "cross-entropy loss"
collapses to −ln p_correct — NLL (alias acknowledged once). The gap
device: −ln softmax(z)_c = LSE(z) − z_c (anchor L: 2.4076 − z_c) —
the smooth-max ruler from `TheUnderflowCliff` against the correct
class's bar; confidently wrong pays proportionally (the gap grows
roughly linearly — no slope claims). Then the join: a 3-frame
per-frame matrix (addendum A4), one entry per column highlighted —
the product license is exactly "independent given the input"
(`WhenToCondition`, quoted) — product 0.294 flipped to summed
log-bars. When-useful closer: this per-frame NLL summed over every
collapsing path is the CTC loss the trellis computes (29-class and
50,257-class softmaxes named, anchor N); and its gradient — softmax
output minus how often the truth actually used each cell, Bridle's
"output minus a one-from-N target" generalized (anchor M, foreshadow
only) — is the next series.

**Device lineage this series extends:** the sorted-square binomial
columns (two-lens table), the posterior ladder (likelihood ratio as
rung), the counting strip and evidence ruler (log-likelihood), the
underflow cliff and LSE ruler (survival, the gap loss), the
quartered-square coin (HHTH), the biased die (best explanation), the
per-frame matrix and conditional-independence license (the join).

**Deliberately not in this series** (README exclusions): the gradient
p − y as a taught result (no derivative toolkit — foreshadow only);
entropy, KL, soft-target cross-entropy; continuous likelihoods and
Gaussian MLE (densities exceed 1 — the discrete world keeps every
likelihood a probability); MAP and priors as treatment (one pointer
at the Bayes move); calibration methods beyond the one caveat.
