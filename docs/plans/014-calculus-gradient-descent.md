# Plan 014: `calculus/` — gradient descent, the walk downhill

The guide-first `gradient-descent` primitive (plan 012 D-E) seeded a
future series; this plan builds it — the second ADR-008 graduation,
after dynamic programming (plan 013). Home: `calculus/`, module
`gradient_descent_manim.py`. The book chapter
(`study_guides/primitives/gradient-descent.tex`) is the phase-0 seed:
the screen animates what the book drafted — the one-line update, the
learning-rate cliff, the sign-change taxonomy of stopping places, and
the CTC road's own 12-knob walk as the capstone.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier); design | Scene design written into the plan |
| 1 | Module stub in `calculus/`, README rows reserved | `make check` |
| 2 | Scenes at draft; layout linter clean; frames verified by eye | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, wiki graph + log; ADR-008 step: the gradient-descent primitive trued to series-backed against the built scenes; anchors for any new on-screen numbers; welcome.gif re-render (13 series) | `make test` |
| 4 | Local CodeRabbit + connection-auditor, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p60 render |

## Checklist

- [x] Phase 0: both reports pinned below; design finalized (six
  scenes; decisions D1–D7). Verifier's new finding F3 (the double
  well's basin boundary at √11) promoted into the design as scene
  5's payoff; the primitive's overclaiming sentence queued for the
  phase-3 ADR-008 truing
- [x] Phase 1: module stub (`TheSlopeBecomesAStep` placeholder) +
  README third-series Scope paragraph, subsection and row 1;
  `make check` green
- [x] Phase 2: six scenes at draft (6 files, distinct names,
  31–40 s). Linter: 41 initial findings across five categories all
  fixed — chip boxes sized under their text (seven chips widened),
  the scene-5 well plotted past its y-range into the title (x-range
  cut to ±2.0), the scene-6 caption stack pushed off-frame by
  on_frame into its neighbour (factors and quarters made side by
  side), compass/bottom-tag clear_of push-off past the frame bottom
  (restacked under the axes), curve tags pulled off the curves —
  linter clean on all six. By-eye pass caught four more the linter
  could not: the w² tag sitting ON the y-axis line, CurvedArrow
  heads drowning the small hops (rows and ping-pong arcs switched
  to plain ArcBetweenPoints), the scene-3 fee caption landing on
  the safe-rates line (thresholds moved to the empty mid-right),
  and the scene-6 linear chart collapsing all five samples onto
  the y-axis (left panel re-scoped to the first fifty steps — the
  cliff; the full 5000 kept on the log panel). Frames verified by
  eye across all six after re-render
- [x] Phase 3: README complete (six rows, all three levels; four
  descent-specific Scope exclusions; eighteen plan-014 references
  unchecked for the maintainer's pass, flags carried into the
  descriptions); wiki — `gradient-descent` node added, two edges
  delivered (derivative-toolkit's row-5 "habit that survives every
  optimizer" promise closed by `WhereTheWalkStops`; the gradient
  series' on-screen "plain gradient descent" now taught, anchor-M
  walk re-read), no new promises opened (all the near-misses are
  Scope exclusions), log entry; **ADR-008 step**: the guide's
  gradient-descent primitive trued to series-backed (header + the
  seed-sprouted closing) **and the F3 erratum fixed in print** (the
  double-well "anywhere right of 0" overclaim bounded at √11, the
  basin hop credited to the series); study INDEX row graduated,
  guide-first list down to ctc-decoding alone; references synced
  (162 entries, 145 verified); both guide PDFs rebuilt green;
  welcome re-rendered at thirteen series (rows 7+6, 402 KB, frame
  verified). `make test` green (243)
- [x] Phase 4: local CodeRabbit returned four findings — three
  applied (the two first-order overclaims softened on screen and in
  README row 1: "the loss cannot rise" → "for a small step, the
  change is downhill"; the study-INDEX anchor row gained
  010.K.NLL), one declined with reason recorded here: the
  remove-the-chord-arrows suggestion contradicts the guide
  chapter's own committed TikZ drawing and the pedagogy digest's
  blessed chord-hop device — the geometry the research warns
  against is tangent-line travel, which the scene avoids, and the
  w-axis tick trail is present. Audit: 16 findings applied, zero
  numeric — two NEW delivered edges (gradient-descent →
  ctc-alignment, the twelve-knob table strand with its softmax
  rider; logarithms → gradient-descent, made deliverable by adding
  one caption — "× per step: a straight march on the log ruler" —
  promoting the audit's top possible), five device-lineage entries
  landed in the wiki (ribbon third stop, nudge square
  finite-stepped, bars' new appearance, loss-vs-step readout), the
  plan trued to as-built (no inset, no mapping close, no η = 3/8
  row; ticker now exact 0.0078125; screen says "over
  three-quarters"), the three stale far ends fixed (root README
  calculus row, derivatives row-5 origin cell struck delivered,
  deep_learning Scope + row 6 pointing back), study INDEX
  seed-anchor note retired, and the √11 boundary anchored
  (014.basin.sqrt11) + asserted in answers/gradient_descent.py
  (script rerun, exit 0). PDFs rebuilt; linter clean; changed
  scenes re-rendered and frame-verified; `make check` + `make
  test` (243) green
- [ ] Phase 5

## Decisions (made at design time)

1. **Home `calculus/`, module `gradient_descent_manim.py`** — the
   series is the derivative toolkit's payoff (slope-as-function +
   sign-change habit become an algorithm), and the guide already
   filed the primitive under the `calculus-` bib prefix. Scope
   boundary in the topic README: no SGD / momentum / adaptive
   steps / schedules (named once as refinements, never taught), no
   vectors or 2-D contour plots (the many-knob generalisation is
   one sentence + a loss-vs-step readout — 3b1b's own refusal to
   draw 13,002 dimensions is the precedent), no Newton's method
   (the η = 1/8 one-step teleport on the a=4 bowl may appear as an
   unnamed "perfect bet" aside at most), no continuous-time
   gradient flow.
2. **Derive, don't posit** (Nielsen's camp): the update's shape is
   forced via the repo's own nudge algebra — ΔL ≈ L′·Δw, choose
   Δw = −ηL′, get ΔL ≈ −η(L′)² ≤ 0. Level 2 before the rule runs.
3. **Discrete hops, never slides.** A dot sliding down the curve
   animates gradient flow, under which overshoot/ping-pong/
   divergence are impossible — the whole scene-2 story would be
   falsified. Grammar everywhere: tangent flash at the iterate →
   horizontal hop on the w-axis by −ηL′ → drop to the curve. The
   tangent is never extended to the axis (that drawing is Newton).
4. **The nudge-square ledger is the quantitative centerpiece**:
   ΔL = 2wΔw + Δw² with Δw = −2ηw gives exactly ΔL = 4ηw²(η−1) —
   the strips pay, the corner charges, they tie at η = 1. All four
   regimes fall out of the owned square. Every "converges iff"
   claim is pinned to its landscape on screen (the picture is a
   claim); the a=4 bowl enforces it.
5. **The basin hop is promoted to a beat, and the chapter's
   overclaim is trued** (verifier F3): at η = 0.1 the double
   well's "anywhere right of 0 settles at 1" fails beyond
   w₀ = √11 ≈ 3.317 — from 4 the walk lands at −1. Scenes claiming
   right→1 keep starts in (0, √11); scene 5 makes the crossing the
   anti-ball payoff. The ADR-008 graduation edit fixes the
   primitive's sentence in the same change (phase 3).
6. **Display precision rules**: bowl and factor-table values are
   exact dyadic — show exact (4/512 or 0.0078125). Double-well and
   road-walk values are float64 — 4 dp display, step counts always
   carry their 0.01 tolerance, exactness claims only at iter 0
   (P = 4877/10000). "Gradient → 0" at iter 5000 means ~10⁻⁴.
7. **Attribution**: Cauchy 1847 (orbit calculations, least
   squares), quoted only via Lemaréchal 2012; Curry 1944 named for
   the first convergence study; **Hadamard omitted** (unverified).

Off-screen list: "descent finds the minimum" unqualified; the ≤ in
|1−2η| ≤ 1 (equality ping-pongs — verifier F7); Hadamard 1907/1908
as fact; "convergence on quadratics is monotonic" (false for
½ < η < 1); any big-O; the uncorrected rolling-ball metaphor (if a
ball appears it is Grosse's overdamped ball-in-thick-fluid, and
only to be contradicted); "converges iff 0 < η < 1" without naming
the bowl it belongs to; loss-curve exactness claims past iter 0.

## Scene design

Module: `calculus/gradient_descent_manim.py`, six scenes. Worked
objects: the bowl L = w² (η = ¼, w₀ = 4), the factor table
(½, −½, −1, −3/2), the nudge square (strips + corner), the a = 4
second bowl, the double well w⁴/4 − w²/2 (η = 0.1), the road's
12-knob walk (0.7181 → 0.0003).

**1. `TheSlopeBecomesAStep`** — a slope is a reason to move; one
line turns it into motion. Sign-annotated bowl (slope negative →
step right; slope positive → step left; f′ = 0 — the walk has
nowhere to go). The nudge derivation (decision 2): ΔL ≈ L′·Δw, so
choose Δw = −ηL′ and the loss must fall — the rule's shape forced,
not posited. Then the walk runs: 4 → 2 → 1 → ½ by chord hops
(tangent flash, horizontal hop, drop to curve), the automatic
brake named (near the bottom the slope is small, so the step is
small — no schedule imposed), step ticker to k = 9, w₉ = 4/512 <
0.01. Formula last: w ← w − ηL′(w).

**2. `TheLearningRateIsABet`** — one dial, four fates, on one
bowl. The update collapses to w ← (1−2η)w: the walk is repeated
scaling on the w-axis (NudgeInNudgeOut's stretch factor, now
iterated). Four number-line rows *(as built: the identical-losses
beat is carried in captions, not an inset — the losses 16, 4, 1, ¼
spoken exactly)*: η = ¼ glides (×½); η = ¾ overshoots every step
and converges (×−½) — and its losses are identical to the glide's,
step for step (the losses can't betray the zigzag; convergence is
|factor| < 1, not monotonicity); η = 1 ping-pongs 4, −4, 4 forever
(×−1); η = 5/4 diverges 4, −6, 9 (×−3/2). Coda: η = 1/40 also
arrives — in 117 steps against 9 (too small never lies; it bills
you). The claim pinned to the picture: for THIS bowl, 0 < η < 1.

**3. `TheCornerChargesTheFee`** — why the cliff sits at η = 1:
the repo's nudge square with the step no longer infinitesimal.
ΔL = 2wΔw + Δw²: the two strips pay 2w·Δw of descent; the corner
charges Δw² back. With Δw = −2ηw the ledger reads exactly
ΔL = 4ηw²(η−1): strips grow like η, the corner like η² — they tie
at η = 1 (checks at w = 4: η = ¼ → −12, η = 1 → 0, η = 5/4 →
+20). Then the bet's other side: the a = 4 bowl (corner four
times fatter). The SAME η = ¼ that glided now ping-pongs
(factor −1) *(as built: the ping-pong arc and the thresholds line
carry the beat; the η = 3/8 divergence row was not drawn)*; safe
rates end at ¼, not 1.
The learning rate is a bet about curvature — geometric only: how
sharply the bowl bends across the step, η·L″ < 2 shown as the
strips-vs-corner tie, never as a second-derivative formalism.
(Optional aside, unnamed: η = 1/8 on this bowl teleports to the
bottom in one step — the perfect bet requires knowing the bowl.)

**4. `WhereTheWalkStops`** — the update is zero exactly where
L′ = 0, and the rule cannot tell which flat ground it found. The
double well (L′ = w³ − w, flat at −1, 0, 1): walk from 0.5
climbs the well's inner slope to the valley at 1 (monotone, never
overshoots; within 0.01 by step 24); from exactly 0 the walk sits
on the hilltop forever — gradient zero, certifying nothing; nudge
to 0.1 and it falls in (step 42). The sign-change test (the
derivative series' habit) stamps each stop: − to + valley, + to −
hilltop; and the shelf (L = w³/3 from w₀ = 1) crawls
sub-geometrically into flat ground that is no minimum at all.
Zero gradient is where the walk ends; the sign change around it
is what was found.

**5. `TheWalkIsNotABall`** — the rule jumps; a ball rolls. Side
by side on the double well at η = 0.1: from w₀ = 2 the walk is
tame (1.4000, 1.2656, … never below 1 — a ball would say the
same); from w₀ = 4 the slope is 60, the first hop lands at −2,
and the walk settles in the LEFT valley — impossible for a ball
without momentum, routine for a rule that reads only the slope
where it stands. The 1-D basin map: starts in (0, √11) land at
+1; past √11 ≈ 3.317 they cross. Ball-physics contrasts stamped:
a ball coasts (the rule has no memory), a ball released on the
hilltop rolls off (the rule sits), a ball never teleports (the
rule just did). Close: the metaphor to keep is a walker reading
the ground underfoot, one step at a time.

**6. `TheRoadsOwnWalk`** — many knobs, one sentence; then the
road's real walk, read with everything the bowl taught. The
gradient collects every knob's slope; the update steps against it
— that is all "plain gradient descent" ever meant (the phrase the
CTC gradient series put on screen). The 12-knob loss from the
alignment table walks 0.7181 → 0.1602 (10) → 0.0356 (50) →
0.0088 (200) → 0.0003 (5000) on a loss-vs-step readout — the only
readout there is, readable after scene 2's spoken losses. Shrink
factors: 14% of the loss per step early, under 0.1% late (0.86 vs
0.9993); over three quarters gone in ten steps; the same curve
replotted on a log axis still visibly descends. The long flat
tail IS scene 1's automatic brake at scale — one mechanism, two
moods; frame 3 settles mixed at (0.032, 0.218, 0.750) with
gradient ~10⁻⁴ — matching γ out of indifference (the gradient
series' gem, now explained by the walk that produced it).
When-useful close: this bare update is the engine under
essentially all of deep learning; everything real training adds
is refinement, none of it taught here; and the rule is older than
the field — Cauchy, 1847, computing planetary orbits (as quoted
by Lemaréchal), with convergence theory arriving a century later
(Curry, 1944).

**Device lineage this series extends:** the nudge square (d(w²) =
2w·dw + dw², now with a finite step and a priced corner), the
stretch factor (NudgeInNudgeOut's local scaling, iterated into
fates), the sign-change ribbon (stamping the stopping places),
the loss-vs-step readout (scene 6's two panels; scene 2 carries
its seed as captions). *(As-built truing, phase 4: the planned
"shared loss-vs-step inset" and "WhenToUseIt mapping close" were
not built — scene 2 speaks the identical losses in captions and
scene 6 closes on a caption stack; the lineage list above is the
as-built set, and all of it is now recorded in the wiki's device
section.)*

Scene-length target: 30–45 s each at the repo's pace, formula
last in every case.

---

## Pinned report: pedagogy researcher (digest — ADR 007)

Consensus order (3b1b NN ch.2, Nielsen ch.1, Ng, MIT 6.390 ch.3,
Goodfellow §4.3): motivate the loss → 1-D first, always → posit/derive
the rule and run it with exact numbers on a quadratic → the automatic
brake as a named beat → learning-rate regimes AFTER the success story
(no canonical source teaches failure first) → critical points that
aren't minima → many dimensions in one breath (3b1b explicitly
REFUSES to visualize 13,002 dimensions and switches to a loss-vs-step
readout — the repo's black-box constraint is the canonical move, not
a compromise). Camp splits: (a) qualitative vs quantitative on the η
threshold — intro camp keeps "too large" a cartoon; the dynamical
camp (Goh's Distill momentum analysis, Cohen–Damian central-flows)
makes the per-step factor |1−ηλ| < 1 and threshold 2/curvature the
centerpiece; the chapter's 1−2η table is the quantitative result
with intro machinery — the series' differentiator. (b) Derive vs
posit: Nielsen derives (pick the nudge so ΔL ≈ −η(L′)² ≤ 0);
recommend siding with Nielsen — the repo owns the pieces
(NudgeInNudgeOut).

Visual devices: sign-annotated bowl (Goodfellow fig 4.1); chord-hop
animation (dots + straight chords — a dot sliding smoothly animates
gradient FLOW, under which overshoot/ping-pong/divergence are
impossible); tangent flash + HORIZONTAL hop (never travel along the
tangent — that's wrong geometry, and a tangent extended to the axis
is accidentally Newton); the per-step shrink factor as signed
number-line scaling (×½, ×(−½), ×(−1), ×(−3/2)) — NudgeInNudgeOut's
stretch-factor device reborn, preferred over a cobweb chart (same
content, owned grammar); four-regime panel with shared loss inset;
**the nudge-square ledger** (the series' strongest original device):
ΔL = 2wΔw + Δw² with Δw = −2ηw gives exactly ΔL = 4ηw²(η−1) — the
linear strips pay the descent, the Δw² corner charges the
curvature's fee, they tie at η=1; all four regimes fall out of the
repo's own square picture; loss-vs-step inset trained on the bowl,
then the ONLY readout for the 12-knob walk; 1-D basin map for the
double well; ball metaphor only as Grosse's overdamped
ball-in-thick-fluid correction (the repo's "walk" frame is safer —
keep it).

Verified examples: E1 glide (4, 2, 1, ½; k=9 first below 0.01);
E2 four regimes incl. η=¾ walk 4, −2, 1, −½; E3 the η=¾ loss curve
is IDENTICAL to η=¼'s (|−½|=|½|) — the loss inset can't see the
zigzag; E4 η=1/40 takes 117 steps vs 9 vs 1 (η=½ teleports: factor
0, one-shot Newton foreshadow, unnamed); E5 ledger checks (w=4:
η=¼ → ΔL=−12; η=1 → 0; η=5/4 → +20); E6 same bet two bowls (η=¾
glides on w², diverges on 2w² — factor −2); E7 double well walks
(from 0.5 → valley 1, local factor 0.8; from 0 sits on the hilltop;
from 0.1 falls in); E8 **basin hop** (w₀=4, η=0.1: L′=60, w₁=−2,
settles at −1 — impossible for a ball; boundary √11 ≈ 3.3166);
E9 shelf crawl (L=w³/3 from w₀=1: harmonic crawl into the shelf at
0 — run only from w₀>0); E10 the road's walk (repo-pinned).

Misconceptions with working counters: zero gradient = solved
(critical-point triple + the hilltop SIT); smaller η always safer
(it bills you: 117 vs 9 vs 1); overshoot = broken (η=¾ converges;
convergence is |factor|<1, not monotonicity); the rolling ball
(inertia, continuity, hilltop roll-off — all false for the rule;
E8 side-by-side); flat tail = stalled (shrink factors 0.86 vs
0.9993, log-scale replot, brake and tail are ONE mechanism in two
moods; plateaus can even end — Ainsworth–Shin); η is the step
length (it's a dial: stride η|L′| varies); there is a safe η
(threshold is the landscape's property — E6).

Pitfalls: flow vs steps (the consequential one); horizontal hops;
don't draw Newton; **the chapter overclaims** — "anywhere right of 0
settles at 1" is false at η=0.1 for w₀ > √11 (E8) — restrict starts
or promote the hop to a beat, and true the .tex; keep
oscillate-AND-converge distinct (most cartoons erase the ½<η<1
regime); every "converges iff 0<η<1" claim is per-landscape (E6
enforces); no 2-D contours (they presuppose vectors); show the
physiology curve linear AND log once; a fetched Distill summary
claimed quadratic convergence is "always monotonic" — false in the
1<αλ<2 band, don't inherit.

Key takeaway: the shrink factor made visible and priced by the
nudge-square ledger fuses the intro camp's bowl with the dynamical
camp's threshold using zero new machinery; the sign-change test
discriminates the stopping places; the loss inset trained on the
bowl becomes sufficient for the pinned walk, whose 0.86/0.9993
factors replay the brake at scale.

## Pinned report: source verifier (digest — ADR 007)

Answer script `answers/gradient_descent.py` executed, exit 0, all
assertions pass. Exact arithmetic (Fraction) except where flagged.

1. **Bowl walk** — VERIFIED exact, two routes (iteration + closed
   form 4·2⁻ᵏ). η=¼ on w²: factor exactly ½; walk 4, 2, 1, ½, …;
   first |w|<0.01 at k=9, w₉ = 4/512 = 1/128 = 0.0078125 exactly
   (dyadic — safe to display exact).
2. **Factor table** — VERIFIED exact: η ∈ {¼, ¾, 1, 5/4} → factors
   {½, −½, −1, −3/2}; convergence iff |1−2η| < 1 iff 0 < η < 1
   (η=1 gives exactly −1). η=¾ trajectory from 4 (exact dyadic):
   4, −2, 1, −½, ¼, −⅛, 1/16, −1/32, 1/64. η=5/4: 4, −6, 9,
   −27/2, 81/4.
3. **Curvature threshold** — VERIFIED exact: L = aw² → factor
   1−2aη, converge iff 0 < η < 1/a; equivalently η·L″ < 2 (L″=2a).
   Display second bowl **a=4** (threshold ¼): η=1/16 → factor ½
   (glides, same shrink as bowl 1's η=¼); **η=¼ → factor −1
   (ping-pong: the SAME η that glided on w²)**; η=3/8 → factor −2
   (diverges 4, −8, 16, −32). η=1/8 → factor 0, one-step
   convergence (optional "perfect bet" beat).
4. **Double well** w⁴/4 − w²/2 — L′ = w³ − w, roots −1, 0, 1
   exact; sign-change classification valley/hilltop/valley exact
   at ±0.01 offsets; L″ = 2, −1, 2. Trajectories float64 vs
   50-digit Decimal agree to ~2·10⁻¹⁶ — display 4 dp, no exactness
   claims (F1). η=0.1: from 0.5 → valley 1, within 0.01 at step 24
   (0.5000, 0.5375, 0.5757, 0.6142, …, monotone, never overshoots);
   from −0.5 exact mirror; from 0 sits forever (update exactly 0);
   from 0.1 → valley 1 at step 42 (0.1000, 0.1099, 0.1208, …);
   from 2 → tame, never crosses below 1, step 15 (2.0000, 1.4000,
   1.2656, 1.1894, …). Step counts carry the 0.01 tolerance (F2).
   **F3 (new finding): one step is g(w) = 0.1w(11 − w²), negative
   for w₀ > √11 ≈ 3.317 — from w₀ = 4: w₁ = −2, settles at −1, the
   LEFT valley.** The chapter's "anywhere right of 0 settles at 1"
   holds only for 0 < w₀ < √11 at η = 0.1. Safe starts: 0.1, 0.5,
   2; the crossing itself is scene material.
5. **The road's walk** — VERIFIED three routes at iter 0 (script's
   15-path enumeration; independent forward–backward on ε A ε B ε;
   exact Fraction P(AB|X) = 4877/10000 → −ln = 0.7181); losses at
   4 dp exactly 0.7181 / 0.1602 / 0.0356 / 0.0088 / 0.0003; frame 3
   at iter 5000 = (0.0324, 0.2177, 0.7499) → displayed (0.032,
   0.218, 0.750); max |gradient| ≈ 1.3·10⁻⁴ ("→ 0" means that, not
   0); argmax path A A ε B; shrink factors 0.860706 → 0.86 and
   0.999326 → 0.9993; drop 77.7% ("over three quarters" safe).
   Float64 throughout — 4 dp display, exactness only at iter 0 (F4).
6. **Attribution** — Lemaréchal, "Cauchy and the Gradient Method"
   (Documenta Mathematica ISMP 2012) fetched in full: Cauchy 1847,
   "Méthode générale pour la résolution des systèmes d'équations
   simultanées", C. R. Acad. Sci. Paris 25:536–538 — presented 18
   Oct 1847; context astronomic orbit calculations, least squares,
   step x ← x − θX; "Convergence is just sloppily mentioned", the
   promised follow-up paper "does not seem to exist". Quote Cauchy
   only "as quoted by Lemaréchal" (originals not fetched). Curry
   1944 (Quart. Appl. Math. 2(3):258–261) bibliographically
   confirmed, first convergence study — paper not fetched.
   **Hadamard 1907/1908 UNVERIFIED (F5) — do not lean on it.**
7. **Convergence condition** — the iff is proved exactly here
   (§2–3); citable corroboration is course notes (IFT 6085
   Mitliagkas: ρ = |1−αh|, 2/h threshold; CMU 10-725 Gordon/
   Tibshirani Thm 5.1 sufficient rate), NOT Boyd/N&W (neither
   states the fixed-step quadratic iff quotably — F6). The iff
   stays attached to the quadratic bowl on screen. F7: IFT notes'
   "ρ ≤ 1" is wrong at equality (ping-pong) — never import the ≤.

Flags F1–F8 as numbered above (F8: the Goodfellow "engine" line is
a positioning claim, unverified as a number).
