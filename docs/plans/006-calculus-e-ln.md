# Plan 006: `calculus/` — e and the natural logarithm

Branch: `feat/calculus-e-ln`, cut from updated `main` (9e8fc00, the
plan-005 merge).
Started: 2026-08-11.

Chosen over random variables by the repo's promise-strength convention
(third time: Bayes after plan 003, logarithms after plan 004). The
logarithms → e/ln promise is the graph's strongest — stated on screen
("that story waits"), in `algebra/README.md` Scope and Ideas, and on the
root README — and it is the graph's only **on-screen debt**:
`TheUnderflowCliff` renders `ln(a+b) = ln a + ln(1 + e^{ln b − ln a})`
before any series teaches what ln is. Closing it makes an existing
rendered forward reference honest, and unblocks the e-half of the
softmax bridge plus the eventual CTC gradient story — the next two
stops on the roadmap toward CTC training.

**Pre-phase.** This branch opens with two commits that belong to plan
005's aftermath, folded here by maintainer decision (no separate fix
PR): the `TheUnderflowCliff` box-leak fix (`344f4f1`) and the
finalisation audit's wiki bookkeeping (`8674288`). Consequence carried
to the finalise gate: `06_TheUnderflowCliff.mp4` re-renders at 1080p60
alongside this series' finals, since the render verified at plan 005's
close predates the fix.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| pre | Box-leak fix cherry-picked; finalisation-audit bookkeeping | Committed (344f4f1, 8674288) |
| 0 | Research: pedagogy + source verification (agents in flight) | Scene design written below |
| 1 | Plan committed, topic dir + README skeleton, module stubs | `make check` |
| 2 | Scenes at `--quality draft`; renders verified (count, names, ffprobe, frames incl. transition windows and every beat's steady state) | Draft renders verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated, root README; new topic → re-render `docs/assets/welcome.gif` | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render, **incl. re-render of `06_TheUnderflowCliff`** |

## Checklist

- [x] Pre-phase: fix + audit bookkeeping committed; branch renamed from
  `fix/underflow-cliff-box-leak` after the fold-in decision
- [x] Phase 0: research reports received (pedagogy + source-verifier,
  both pinned below), scene design finalized below
- [x] Phase 1: plan + topic skeleton, `make check` green (171 tests —
  the new topic joined the contract suite; `--list` prints the stub)
- [ ] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
- [ ] Phase 3: README + wiki complete, `make test` green
- [ ] Phase 4: local review + audit clean
- [ ] Phase 5: PR, drafts cleaned, 1080p60 render verified (this series
  plus the scene-6 re-render)

## Research questions the reports must settle

- Ordering: compound-interest-first (e as a limit the viewer watches
  saturate) vs derivative-first (e as the base whose slope is itself) —
  which route fits a viewer whose only tool is the logarithms series'
  counting strip?
- How far into "derivative" this series must go: it cannot assume any
  calculus, so "local stride/growth rate" needs a treatment that is
  honest without epsilon-delta.
- The device lineage: the plan-005 audit named `MultiplyIsAdd`'s
  base-is-a-unit stride device as the natural opening — confirm or
  refute against how the canonical treatments open.
- The payoff scene: `algebra/README.md` defers the inverse-function
  graph "as a payoff, never as the starting point", and the underflow
  cliff's ln identity is the standing debt — how do the best treatments
  land ln as *natural*?
- Exact numbers for every candidate beat: the (1+1/n)^n table (plan
  005's anchors carry a machine-verified start), slopes of 2^x and 3^x
  at 0, ln(1+x) ≈ x, e's digits, and the historical attributions
  (Bernoulli, Euler) with dates verified.

## Pedagogy findings (pinned from the pedagogy-researcher report)

**The ordering question is settled by a merge, not a pick.** Four
canonical routes to e exist (Strang's "Introducing e^x" enumerates
them): compound-interest-first (Bernoulli/BetterExplained),
derivative-first (3b1b/MIT), series-first, and ln-as-area-first. The
last two need machinery the viewer lacks (power-rule derivatives;
integrals) — excluded. The first two have complementary documented
weaknesses: 3b1b's route shows the measured constants behave like logs
only *empirically* (he asks viewers for a geometric picture), and the
compounding route never explains why the ceiling is *that* number.
**The repo's counting strip is the missing geometric picture in both**
— no canonical source exploits it because none has a viewer pre-trained
on "the base is a stride." Order: stride cold-open (the `MultiplyIsAdd`
on-screen promise) → compounding poses the question → local growth rate
built visually → mystery constants → ln revealed as the natural stride
→ payoffs. Strides answer questions, growth poses them: the compounding
story must arrive immediately after the cold open.

**How far into "derivative": exactly three beats, no further.**
(a) Tall's local-straightness zoom — magnified smooth curves look
straight, so "slope here" means something; (b) the ratio
(b^dt − 1)/dt with dt a *concrete on-screen number* (0.1, 0.01, 0.001),
watched to settle — the limit experienced, never defined; (c) slope of
b^x everywhere = b^x · (slope at 0), which is one strip-law step
(b^(x+dt) = b^x · b^dt — a hop is the same length everywhere) that most
treatments skip and the strip makes visual. Never say "instantaneous"
(3b1b's named paradox); no d/dx, no limit notation.

**The central device: the mystery-constant reveal on stride grammar.**
Slopes at 0: base 2 → 0.6931, base 3 → 1.0986, base 8 → 2.0794 — and
the viewer notices base 8's constant is exactly *three of* base 2's
(8 = 2³: three strides). The constants obey the strip's laws before
they are named: they ARE stride lengths in an undisclosed unit, and e
is the base whose stride is exactly 1 — the unit the strip was secretly
ruled in all along. The bridge that closes both routes honestly:
ln((1+1/n)^n) = n·ln(1+1/n) ≈ n·(1/n) = 1, using only the taught log
laws plus a visually-built ln(1+x) ≈ x.

**Misconceptions to design against:** "more compounding → unbounded"
and "(1+1/n)^n → 1" (the two wrongs bracket the truth — race them on
screen); e's digits must never come first (e is the answer to a
question); "instantaneous" taken literally; "ln is a harder animal"
(it's the same counter row in nature's units); e^(ln y) = y uses the
algebra series' undo-language, never "cancel"; "e^x grows fast because
e is big" (3^x outgrows it — e is the *self-paced* base).

**Pitfalls with teeth:** Jacob (1683, compounding) vs Johann (1697,
exponential series) Bernoulli — popular sources pick the wrong brother;
Bernoulli bracketed the limit in [2,3] but never named or computed e
(don't overclaim); the slope table must be the one-sided ratio
(0.7177, 0.6956, 0.6934), not the faster-converging symmetric
difference, or a viewer who checks catches the scene; drawn digits are
the verifier's digits, consistently truncated; 69.3 is the math, 72 the
divisibility convention — never conflate; the inverse-function graph
stays last (payoff, never definition — Kenney & Kastberg, already a
repo constraint).

## Verified technical anchors (from the source-verifier report)

Method tags per plan 005's convention: [quoted] verbatim from a fetched
source · [computed-exact] integer/`Fraction` arithmetic, correctly
rounded · [computed-mp] mpmath dps=60 cross-checked against an exact
route · [computed-float] float64 where the float behaviour IS the claim
· [reasoned] standard argument, spot-checked. Checked against plan
005's anchors: no disagreements.

- **The table** [computed-exact through n=10⁵, computed-mp beyond]:
  (1+1/n)^n = 2, 2.25 (9/4), 2.44140625 (625/256), 2.613035290225
  (n=12, exactly 13¹²/12¹²), 2.692596954437 (n=52), 2.714567482022
  (n=365), 2.718126691620 (n=8760), 2.718268237174 (n=10⁵) → e.
  Strictly increasing (exact comparison, n=1..60 + all table n);
  bounded &lt; 3 via C(n,k)/nᵏ ≤ 1/k! ≤ 2^(1−k) (exact term-by-term at
  n=365; general case [reasoned]). "Increasing + bounded ⇒ limit
  exists" is analysis — this series may *name* it, not derive it.
- **e** = 2.718281828459 on screen [computed-exact: the exact interval
  [S₂₀, S₂₀ + 1/(20!·20)] pins 19 decimal places with no floating
  point; agrees with DLMF 4.2.11 [quoted]].
- **Series contrast** [computed-exact/mp]: partial sums of Σ1/k! hit
  2.7182818… by S₁₀ (error 2.7e−8) while the limit route needs
  n ≈ 1.36×10⁶ for 1e−6 — error of the table is ≈ e/(2n), first-order.
- **Slopes at 0** — the mystery constants: ln 2 =
  0.6931471805599453…, ln 3 = 1.0986122886810969… [three routes: exact
  atanh-series interval (20 rigorous places), mpmath, libm — all
  agree]. One-sided ratio (2^dt−1)/dt = 1.0, 0.7177, 0.6956, 0.69339
  at dt = 1, 0.1, 0.01, 0.001 [computed-float]; base 3: 2.0, 1.1612,
  1.1047, 1.09922; base 8's constant 2.0794 = 3·ln 2 exactly
  [computed-mp]; base 10 → 2.302585; base e: 1.0517, 1.0050, 1.0005
  → 1. The scene draws the ONE-SIDED table (the symmetric quotient has
  visibly different rows — 0.6937 at h=0.1 — and float cancellation
  makes it non-monotone below h≈1e−5; never animate h below 1e−4).
- **Derivative identities** [quoted, OpenStax Calc Vol 1 §3.9, Thms
  3.14–3.16]: E′(x) = eˣ; (ln x)′ = 1/x; (bˣ)′ = bˣ ln b; e defined as
  the unique base with slope 1 at 0, 2.7182 &lt; e &lt; 2.7183. Bisection on
  slope-at-0 = 1 reproduces e to 25 digits [computed-mp] — the two
  definitions *shown* to agree; the equivalence proof is analysis,
  named not claimed.
- **The bridge** [computed-mp]: n·ln(1+1/n) = 0.9531, 0.99503,
  0.99950 (n = 10, 100, 1000) → 1; ln(1.1) = 0.09531, ln(1.01) =
  0.0099503, ln(1.001) = 0.0009995. ln(1+x) ≈ x is honest only for
  |x| ≤ 0.1 on screen (at x=0.5 the x²/2 error description is already
  24% off) — show the error column or keep x small.
- **Payoff numbers**: e³ = 20.0855, ln(20.08) = 2.99972 [computed-mp];
  doubling at 5%: 0.6931/0.05 = 13.86 yr (69.3 is the math, 72 the
  divisibility convention); r=0.05 daily: (7301/7300)³⁶⁵ =
  1.051267496467 EXACT vs e^0.05 = 1.051271096376, gap 3.6e−6 matching
  r²e^r/(2n) [computed-exact/mp].
- **The debt beat** [computed-float]: ln(1+e^d): d=0 → ln 2; d=−20 →
  2.0611536203e−9 (naive log(1+exp d) has only 8 correct digits);
  d=−40 → 4.2484e−18 while naive collapses to exactly 0.0
  (1+e⁻⁴⁰ == 1.0 in float64). log1p matches truth at full precision at
  every d. The visible contrast lives at d=−20/−40, not d=−5.
- **History** [quoted MacTutor/Wikipedia]: **Jacob** Bernoulli examined
  compound interest 1683, proved the limit lies between 2 and 3, never
  named it (publication 1690, Acta Eruditorum — Wikipedia-sourced,
  keep the two years distinct). Euler: e in a letter to Goldbach 25 Nov
  1731; first in PRINT in Mechanica 1736 [single-source flag];
  Introductio 1748 gives 18 places (verified correct — some accounts
  say 23, unverified, stay at 18). Napier 1614 is NOT base e — "not
  really to any base" [quoted MacTutor]; even "base 1/e" is off by
  5e−8 relative [computed-mp]. Avoid the Napier rabbit hole on screen.
- **Change-of-base constants**: log₁₀2 = 0.301029995664 (algebra/'s
  0.30103 confirmed), ln 10 = 2.302585092994, log₂e = 1.442695040889
  = 1/ln 2 [identity-checked to 21 digits; ln 10 and log₂e digit
  strings rest on two computational routes — OEIS fetch 403'd; A001113
  / A002162 / A002392 listed for human verification].

## Scene design (built from both reports)

Six scenes. Names are the viewing order; every number above traces to
the anchors section.

1. **`TheSplitYear`** — *what is it saying.* Cold open on the standing
   promise: the counting strip returns, with `MultiplyIsAdd`'s closing
   caption replayed — "calculus later makes one base natural — that
   story waits." The wait is over; but strides come in every size, so
   which could be nature's own? Growth poses the question strides
   can't: Jacob Bernoulli, 1683 — $1 at 100% for one year. Split the
   year: 2 hops of ×1.5 → 2.25; 4 hops → 2.4414; 12 hops → 2.6130 —
   each refinement drawn as more, smaller multiplicative hops on the
   strip (interest earning interest, spatially). Race the two wrong
   intuitions in WARM: "more compounding → unbounded" vs "(1+1/n) → 1
   so the power → 1" — the table (n=52, 365, 8760) crowds a ceiling
   instead: 2.7146, 2.7181… Bernoulli proved the ceiling sits between
   2 and 3 and never named it. Close on the unnamed ceiling — the
   first number in history defined as a limit.
2. **`ZoomUntilStraight`** — the honest mini-derivative, three beats
   and no more. (a) Magnify a smooth growth curve until it is
   indistinguishable from a line: "slope here" means something
   (local straightness). (b) Read the slope of 2ˣ at 0 as a
   rise-over-run ratio with dt a *real number on screen*: dt = 1 →
   1.0; 0.1 → 0.7177; 0.01 → 0.6956; 0.001 → 0.69339 — the readout
   settles; never the word "instantaneous". (c) One strip-law step:
   b^(x+dt) = b^x · b^dt — a hop is the same length everywhere — so
   the slope anywhere is the height times the slope at 0. Growth rate
   proportional to amount, earned in one visual beat.
3. **`TheMysteryConstants`** — *why, part 1.* The lineup: base 2's
   settling constant 0.6931; base 3's → 1.0986; base 8's → 2.0794 —
   and 2.0794 is exactly *three of* 0.6931 (8 = 2³: three strides!).
   Base 10 → 2.3026. The constants obey the counting strip's laws
   before anyone names them: they are stride lengths in some
   undisclosed unit. Then the squeeze: 0.6931 &lt; 1 &lt; 1.0986 — between
   base 2 and base 3 sits the base whose constant is exactly 1, the
   base whose growth rate IS its height. Bisect toward it: 2.71828…
   — the ceiling from scene 1, reappearing from a different question.
   e is not big (3ˣ outruns eˣ) — it is the self-paced base.
4. **`TheNaturalStride`** — *why, part 2: ln lands.* The undisclosed
   unit disclosed: slope-of-bˣ-at-0 is the length of one base-b stride
   measured in e-strides — change-of-base, already taught, one step.
   The natural strip: values 1, 2, e, 4, 8 over counters 0, 0.693, 1,
   1.386, 2.079 — ln is not a new animal, it is the counter row in
   nature's units; every log the viewer has met was ln in a stretched
   unit. Build ln(1+x) ≈ x visually: one tiny hop ×(1+x) costs ≈ x
   natural strides (ln 1.1 = 0.0953, ln 1.01 = 0.00995, ln 1.001 =
   0.0009995 — |x| ≤ 0.1 only). Then the bridge that no popular
   treatment closes: ln((1+1/n)^n) = n·ln(1+1/n) = 0.9531, 0.99503,
   0.99950 → 1. The compounding ceiling is the value whose natural
   counter is exactly 1 — the two definitions of e are the same
   number, shown, not asserted (the full equivalence proof is
   analysis; named as such in a caption).
5. **`RateTimesTime`** — *when is it useful, part 1.* e^(rt): the
   growth dial has two knobs that only multiply — 10 years of 3% ≡
   1 year of 30%. Doubling time = 0.693/r: at 5%, 13.86 years — 69.3
   is the mathematics, 72 the divisibility convention (both on
   screen, honestly labelled). ln as time-to-grow: e³ = 20.09, so
   reaching 20× takes 3 natural units (ln 20.08 = 2.99972).
   Continuous compounding closes Bernoulli's ledger: daily at 5% =
   1.0512675 exactly vs continuous e^0.05 = 1.0512711 — the gap
   3.6e−6, the limit arrived.
6. **`TheDebtRepaid`** — *when useful, part 2 + the promised payoffs.*
   The repo's oldest forward reference re-rendered:
   ln(a+b) = ln a + ln(1 + e^(ln b − ln a)) from `TheUnderflowCliff` —
   and for the first time every symbol means something; read it aloud
   symbol by symbol. Its engine ln(1+e^d) at the cliff's own scale:
   at d=−40 the naive float64 route returns exactly 0.0 (1+e⁻⁴⁰ == 1.0)
   while the identity's value 4.25e−18 survives — the underflow story,
   now with its machinery understood. Then the deferred payoff arrives
   last, as `algebra/README.md` promised: ln 2 = 0.693 marked on the
   eˣ graph one point at a time (the input that yields 2), then the
   full exp/ln inverse graph — the flip earned, never the definition.
   Euler's name for the number (letter 1731, in print 1736,
   Introductio 1748 to 18 places) and the takeaway box: **e is the
   base whose stride is 1 — nature's unit for growth.**

Deliberately not covered (→ README Scope): integrals (ln as area
under 1/t is named as the road not taken), derivatives as a general
toolkit (only slope-at-a-point is built), complex exponentials/Euler's
formula, and the softmax bridge (foreshadowed: "why e appears in every
probability machine" waits for the likelihood series).
