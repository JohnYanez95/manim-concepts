# Plan 010: `deep_learning/` — the CTC gradient identity and training dynamics

Branch: `feat/ctc-gradient`, cut from updated `main` (ebcf856, the
plan-009 merge). Started: 2026-08-12.

This is the roadmap's end target — the series plans 006–009 existed to
gate. Three wiki promise rows converge on it: `ctc-alignment` →
*(gradient / peaky dynamics)*, `softmax-likelihood` → *(the CTC
gradient identity)* (spoken on screen by `TheLossThatTrains`' closer),
and `derivative-toolkit` → *(the CTC gradient identity)* (spoken on
screen by `TheSmoothMaxsShares`' closer, which leaves p − one-hot
itself on the final frame). It starts with anchors pre-verified: plan
008 M (p − one-hot analytic + Bridle 1989 prose), plan 009 G/H (LSE
gradient = softmax, the saturation walk), and the plan-008 A4
per-frame matrix whose first three columns are already on screen.

Design rule (post-CTC narrative direction): this series IS the target,
so it points backward liberally — the trellis, the softmax bars, the
balance point, the score function all return — and forward only in
when-useful framing.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research: pedagogy + source verification (two agents); design | Scene design written into the plan |
| 1 | Plan committed, module stub in `deep_learning/` | `make check` |
| 2 | Scenes at draft; layout linter clean; frames verified by eye (steady beats + transition windows) | Layout linter clean + drafts verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render (`--jobs`) |

## Checklist

- [x] Phase 0: both research reports received and pinned below; scene
  design finalized (seven scenes); five conventions decided at design
  time (see Decisions)
- [ ] Phase 1: plan + module stub, `make check` green
- [ ] Phase 2: all seven scenes at draft; layout linter clean; frames
  verified by eye
- [ ] Phase 3: README + wiki complete, `make test` green — **John's
  source-validation checkpoint**
- [ ] Phase 4: local CodeRabbit + connection-auditor, findings
  addressed
- [ ] Phase 5: PR, bot review, `clean-drafts`, 1080p60 finals

## Decisions (made at design time)

1. **β convention: the 2012 book's (exclusive)** — β starts its
   product at t+1, so β_T = 1 at the two final states,
   p(z|x) = Σ_s α_t(s)β_t(s) at any t with no division, and the
   gradient is division-free (Graves 2012 eqs. 7.12/7.13/7.26/7.34).
   The 2006 paper's β includes the frame-t emission and drags 1/y
   factors through everything. The emission-ownership "ledger cut"
   (α's column pockets frame t's emission; β starts at t+1) is drawn
   once, in scene 1, and the column checksum is the standing
   self-check: if a column's α·β sum comes out scaled, an emission got
   counted twice. Verifier confirmed both conventions cell-by-cell
   (β₂₀₀₆ = β₂₀₁₂ · y, identical P and gradients).
2. **Derivation route: log-sensitivity, no product rule.** The rider
   from calculus Scope ("if the CTC gradient series ever needs a bare
   product rule, that decision belongs to it") resolves to **not
   needed**. Route: −ln P is a log of a sum of path-products; nudging
   ln y at one cell scales every path through that cell by the same
   factor, so ∂ln P/∂ln y_t^k = the posterior share of paths through
   the cell = γ_t(k) — `TheSmoothMaxsShares`' "the sensitivity of a
   smooth max is the share" at path scale. A linearity observation
   (P is linear in any single y_t^k: each path uses frame t exactly
   once) opens the scene. Then the owned log-softmax step
   (∂ln y_j/∂u_k = δ_jk − y_k, one line from ∂LSE = softmax) plus the
   checksum Σ_j γ_t(j) = 1 collapses the Jacobian to y − γ. The
   checksum is load-bearing in the algebra, not just verification —
   the device pays twice. `TheProductRule`'s rectangle stays in the
   drawer.
3. **The matrix's fourth column is ratified**: (A, B, ε) =
   (0.1, 0.7, 0.2) — a permutation of column 1, giving the story
   shape A-ish, A-ish, ε-ish, B-ish and exact P(AB|X) = 0.4877.
   Columns 1–3 are verbatim plan-008 A4, already on screen in
   `TheLossThatTrains`. Every anchor-K table depends on this choice;
   **flagged for the maintainer at the phase-3 checkpoint** (verifier
   FLAG 1).
4. **Sign convention pinned once, in scene 5**: the series draws the
   *gradient of the loss*, ∂L/∂u = y − γ (descending loss is
   ascending likelihood — the plan-009 wording). Scene 6's
   fig.-4-style error panels plot "the push" γ − y (above the axis =
   raise this activation) and *say so on screen* the moment the axis
   appears — Graves' own figure uses the push sign, and a panel that
   silently flips would contradict the equation beside it (verifier
   FLAG 9). Per-column sums are 0 in both signs — the self-check that
   survives the flip.
5. **Two training toys, kept visually distinct** (verifier FLAGs 5,
   7; pedagogy pitfalls): the *free-logit* descent on the worked
   example converges to an honest alignment (A A ε B, frame 3
   deliberately mixed) — it demonstrates fig. 4's arc, NOT
   peakiness. Peakiness needs shared parameters: the Zeyer bias
   model at T=12 (blank 0.8162, 100% error). A scene claiming the
   worked example itself "goes peaky" would be false. Blank
   dominance is conditioned on T (at T=4 blank is NOT dominant:
   counts A 21, B 21, ε 18; dominance from T ≥ 5).

Off-screen list (verified wrong, unverifiable, or trap): the paper's
rescaled log-loss ln p = Σ ln C_t (fails by exact computation on our
example, 0.6212 vs 0.4877 — no published erratum exists; verifier
FLAG 3); any dataset name for fig. 4 (the caption names none — FLAG
2); "blank always dominates" unconditioned (false at T=4 — FLAG 5);
direct Rabiner quotes (citation verified only as printed in Graves —
FLAG 10); the plan-009 saturation endpoint −0.99999551 as "−1.0000";
Zeyer cited as anything but an arXiv preprint (FLAG 6).

Grid/bars split (pedagogy pitfall): α/β/γ live on the 5-state grid
(ε A ε B ε); the softmax-bars view is 3-class. lab(z, k) sums states
into classes — blank owns three rows — and that summation is drawn
exactly once (scene 3) before any bars claim to be γ.

## Scene design

Module: `deep_learning/ctc_gradient_manim.py`, seven scenes. The
worked example throughout: Y = AB, alphabet {A, B, ε}, T = 4,
z′ = (ε, A, ε, B, ε), the 5×4 trellis from `TheForwardTrellis`, 15
paths, and the ratified matrix (columns = frames, rows = A/B/ε):
0.7/0.2/0.1 · 0.6/0.1/0.3 · 0.2/0.1/0.7 · 0.1/0.7/0.2.

**1. `TheOtherHalfOfTheTrellis` — α answered "how did we get here?";
β answers "how do we finish?".** The owned grid returns with its
skip-edge semantics intact. Unit weights first: run the recurrence
right-to-left, arrows against the grain (Graves' own gloss on his
fig. 3), and the backward counts mirror the forward counts — this
example is symmetric under time-reversal + A↔B, countable on screen.
The ledger cut beat: each column's emission is a coin exactly one of
the two variables may pocket — α's column owns frame t's emission, β
starts at t+1 (so β_T = 1 at the two final states). Formula last:
the β recurrence (mirror of `TheForwardTrellis`'s, with β̄_t(s) =
β_{t+1}(s) + β_{t+1}(s+1) and the same skip legality). Real-matrix β
table lands (anchor K). Level 3 seed: this is the backward half of
forward-backward, the HMM lineage named (Rabiner 1989, name-drop
only).

**2. `PathsThroughACell` — α·β is the probability of the truth's
paths through a cell.** Prefix bundle × suffix bundle: everything
left of cell (t=2, A) converging in, everything right diverging out —
the cell is a waist; 2 prefixes × 4 suffixes = 8 of the 15 paths, the
multiplicative rule from `combinatorics/` reborn weighted. Then the
checksum, the series' strongest device (Eisner's constant column):
sweep a highlighted column across the grid — at unit weights every
column sums to **15**, the flagship number's third return; on the
real matrix every column sums to the same **P(AB|X) = 0.4877**, which
also equals α's two-final-state sum and β's two-initial-state sum.
Why: every path crosses every column exactly once. Formula last:
p(z|x) = Σ_s α_t(s)β_t(s), for any t. The checksum is also the
bookkeeping self-check: a doubly-pocketed emission scales a column
visibly.

**3. `WhereTheTruthSpendsItsTime` — divide each column by its own sum
and it becomes a distribution: occupancy.** γ_t(s) = α_t(s)β_t(s)/P.
Columns sum to 1 because each path occupies exactly one cell per
column (countable; and worth saying it's the topology that grants
this). The states→class summation drawn once: blank's three rows fold
into one bar, lab(z, k). Rows are NOT probabilities — A's row sums to
1.4: rows are expected dwell times, the balance-point fulcrum slid
under a row (`TheBalancePoint` re-grounded: occupancy is an
expectation over the posterior path distribution); 1.4 + 1.4 + 1.2 =
4 = T. Uniform-outputs beat: γ collapses to path counts/15 — scene 4
of the alignment series reborn as a target distribution (anchor L's
exact fractions: t=1 A 2/3, ε 1/3, B 0). A γ column pulled out of the
grid and stood next to `TheSmoothMaxsShares`' one-hot bar: a *soft*
target. Formula last: γ = αβ/P, named "how often the truth used each
cell" — the promise's exact wording, now an object.

**4. `TheSensitivityOfTheSum` — nudge one cell and the loss moves by
exactly that cell's occupancy.** Opening beat: P is *linear* in any
single y_t^k — each path uses frame t exactly once, so the variable
appears to power 0 or 1; the slope of a linear function is its
coefficient, and the coefficient is α·β by the waist picture (no new
calculus). Main beat, the log-sensitivity route: nudge ln y at cell
(t, k) multiplicatively and every path through the cell scales by the
same factor while every other path stands still — so
∂ln P/∂ln y_t^k = the share of P passing through the cell = γ_t(k).
The score function d ln f = f′/f (owned by `ZeroSlopeFindsThePeak`)
does the bookkeeping. In LSE each term owned its own z_i; here many
paths share one cell, so shares *add* into occupancy —
`TheSmoothMaxsShares` at path scale. Formula last:
∂L/∂ln y_t^k = −γ_t(k).

**5. `SoftmaxMinusOccupancy` — the identity.** The per-frame y comes
from a softmax, so push through the owned log-softmax derivative
(∂ln y_j/∂u_k = δ_jk − y_k, one line from plan-009's
∂LSE = softmax); the checksum Σ_j γ_t(j) = 1 kills the Jacobian's
second term on screen — the device pays its second time. Formula
last: **∂L/∂u_t^k = y_t^k − γ_t(k)** (Graves 2012 eq. 7.34). Sign
convention spoken once (decision 4). The gradient table on the real
matrix (anchor K): t=1 (−0.2028, +0.2000, +0.0028) … t=4 (+0.1000,
−0.2487, +0.1487); every row sums to 0, and the 4-dp displays sum to
0.0000 digit-exact (FLAG 11 — safe to show the sum). Degeneration
beat: fade 14 of the 15 paths and γ's columns snap to one-hot along
the survivor — the identity IS p − one-hot, `TheSmoothMaxsShares`'
closing frame received: "every frame of CTC hands this exact picture
a different target", the promise closed with Bridle's "one-from-N
target" generalized to a soft one. Wrong-transcript beat: score BA
instead and t=1 A flips to exactly +0.7000 (state unreachable →
occupancy 0 → gradient = y itself). Level 3: this identity is what
CTC backward passes hard-code (PyTorch's kernel implements the
paper's eq. 16) — and it silently breaks if the input isn't a genuine
log-softmax: the forward loss stays correct, the gradient goes wrong
(PyTorch issue #122243). The clean form lives at the logits; the
y-form drags 1/y factors (eq. 7.31, all-negative — it only pushes
up, which is why the u-form is the teachable one).

**6. `TheErrorSignalLearns` — watch y − γ over training: diffuse,
localised, gone.** Graves fig. 4's three stages reconstructed
computable on the worked grid (the figure itself cited, no dataset
named — FLAG 2; its caption quoted: (a) "the error is determined by
the target sequence only", (b) "the error localises", (c) "virtually
disappears"). Stage (a): uniform outputs → γ is exactly path
counts/15, input-independent — the error bars are pure fractions
(t=1: −1/3, +1/3, 0), diffuse and time-symmetric. Stage (b): the
free-logit descent from the repo matrix (anchor M trajectory, float64,
displayed 4 dp): loss 0.7181 → 0.1602 (10 iters) → 0.0356 (50); the
error localises where y already leans. Stage (c): loss 0.0003 at
5000 iters, bars shrink into the axis — and the teaching gem: frame
3 converges to the *mixed* (0.032, 0.218, 0.750) with gradient → 0,
because once frames 1, 2, 4 say A, A, B, all three choices at frame
3 collapse to AB — the error disappears because y matches γ, not
because y went one-hot. Error panels plot the push γ − y, stated on
axis-arrival (decision 4); every column of bars balances to zero
(sign-change-ribbon grammar). Three-stage small-multiples layout:
output bars left, error bars right, exactly fig. 4's shape on 4
countable frames.

**7. `WhyTheSpikesAppear` — peakiness is topology + weight sharing,
not acoustics; and the identity is everywhere.** `WhenToUseIt`
warned "never read spike timing as segmentation"; this scene supplies
the mechanism. Blank-dominance counting beat, conditioned on T
(decision 5): at T=4 blank is NOT dominant (A 21, B 21, ε 18 — on
screen, the honest small case); at T=5 it is (56, 56, 63), and the
share grows with T (T=10: blank 0.48 of all path-cells; for target
"A", blank's share → 2/3). The input never appears in the
computation — dominance is topological (Zeyer's uniform-init
posterior = alignment counts). Then the shared-parameter beat: a
single softmax forced to serve every frame (the Zeyer bias model) —
at T=4 it settles honestly (0.4, 0.4, 0.2); at T=12 it converges to
(0.0919, 0.0919, 0.8162) — argmax blank at every frame, decoding to
the empty string: **peaky behavior with 100% error rate**, the
trap Zeyer, Schlüter & Ney (arXiv 2021) prove for a FFNN from
uniform init — a *local* optimum (the global optimum has zero
error), prevented by a label prior in the loss. When-useful close,
the mapping scene grammar: the gradient's soft target is one family
— one-hot cross-entropy (the degenerate case), distillation's soft
teacher targets, CTC's occupancy — Bridle's "output minus target"
across all of them; γ itself is the soft alignment implementations
compute (Baum-Welch's E-step object); spikes are a training
artifact, steerable, not timestamps.

Scene-length target: 30–45 s each at the repo's pace, formula last in
every case.

**Device lineage this series extends:** the trellis grid (now swept
both directions), the multiplicative rule (prefix × suffix waist),
Eisner's constant column (new device, named the checksum), the
softmax bars (fourth appearance — reborn as a γ read-out and an
error read-out), the balance-point fulcrum (dwell-time rows), the
sign-change ribbon (error bars balancing about the axis), the
score-function route (products → sums of relative rates, third
appearance), factor-out-the-max's habit of pinning conventions
early (the ledger cut).

---

## Pinned report: pedagogy researcher

ORDERING — consensus across sources that actually teach this (most
don't): (1) β as the mirror sweep; (2) α·β = ways-in × ways-out; (3)
the column checksum (every column sums to the same P — Eisner's
constant column, his students' documented favorite moment); (4)
γ = αβ/P as posterior occupancy, columns are distributions, rows are
expected dwell (Rabiner's "expected number of times in state i");
(5) the gradient identity last; (6) training dynamics (fig. 4, then
Zeyer's mechanism, label prior as fix).

Camp split, stark: Distill (Hannun), Edinburgh ASR (Bell), UIUC ECE
537 (Hasegawa-Johnson), Stanford CS224S all stop at the forward
algorithm — the gradient is taught essentially nowhere visually.
Treatments that do teach it split again: Graves derives formula-first
(γ never named as an object); the HMM-pedagogy lineage (Rabiner,
Eisner) makes γ a first-class citizen before any gradient. Take the
HMM branch: γ first as an object with meaning (a soft target, an
expectation), gradient second — the repo owns every ingredient.

Derivation route: avoid the product rule entirely. (a) Log-
sensitivity route (generalizes `TheSmoothMaxsShares` exactly):
∂ln P/∂ln y_t^k = γ_t(k); one owned log-softmax step + the checksum
collapses to y − γ; the checksum is load-bearing in the algebra. (b)
Linearity route as backup/opening: P is linear in any single y_t^k
(each path uses frame t exactly once); slope = coefficient = α×β by
shared prefixes. Bare-product-rule rider resolves to: not needed.

Recommended arc: six scenes (the plan splits the sixth into two);
names, claims and devices as adopted above.

Staging fig. 4: each stage computable on the tiny example — (a)
uniform outputs → γ = path-count shares, input-independent (Zeyer
proves uniform-init posterior = alignment-count proportions); (b) γ
sharpens where y already leans; (c) y ≈ γ, bars vanish, per-column
sums always zero. Blank dominance CANNOT be shown on the flagship
example (blank's occupancy there is 18/60 = 30% — labels dominate at
T = 2U); the honest beat is topological counting plus the
shared-parameter toy. Do NOT animate "descent on this free-logit grid
goes peaky" — it demonstrably does not (converges to the honest
majority alignment); peakiness needs weight sharing.

Misconceptions (with the counter that works): (1) "β includes frame
t's emission too" — the ledger picture + checksum catches the double
count; (2) "the target is the best path" (Viterbi one-hot thinking) —
two paths sharing a cell add their shares; degeneration shows one-hot
as the special case; (3) "γ is a probability over the grid" — rows
sum past 1 (1.4); columns are distributions, rows are expectations;
(4) logits/probs/log-probs give three different "the gradient" — the
clean y − γ lives at the logits (PyTorch forum confusion documented);
(5) sign of the error signal — Graves plots γ − y but derives y − γ;
pin one convention, use column-sums-to-zero as the self-check; (6)
"blank dominates because speech is mostly silence" — no: it's
topological, the input never enters the computation; (7) "spikes are
where the letters are" — refuted in `WhenToUseIt`; now supplied with
the mechanism.

Technical pitfalls: the 2006/2012 convention fork (adopt 2012; at
unit weights the two coincide, which is exactly why the counting
introduction is safe); suspected typos in the thesis (eq. 7.27's
spurious leading minus, eq. 7.15's y^t vs the definition's t+1) —
verify recurrences by recomputation, never inherit; ICML eq. 16's
Z_t is a per-timestep normalizer, not P (implementations have
misread it) — skip rescaling, the repo owns log-space; lab(z, k)
sums over states (blank owns U+1 rows) — a grid mapping class to one
row is wrong from the first frame; columns-sum-to-1 needs
one-state-per-frame topology (breaks for RNN-T — worth one line);
Ogun's per-frame "loss" framing double-counts — don't copy; fig. 4's
TIMIT curves are unreproducible at video scale — reconstruct the
stages on the toy grid, cite the figure as the empirical original.

KEY TAKEAWAY: the single strongest device is the column checksum
ripening into the soft target — it proves the bookkeeping, it is
load-bearing in the derivation, it grounds occupancy in
`TheBalancePoint`, and it makes the finale computable: at uniform
init γ is scene-4's path counts divided by 15, which is why the
error "is determined by the target sequence only" and why blank's
dominance is topological.

Sources consulted (all URLs verified by the agent): Graves et al.
2006 (ICML, cs.toronto.edu/~graves/icml_2006.pdf); Graves 2012
thesis/book (cs.toronto.edu/~graves/phd.pdf and preprint.pdf);
Hannun, Distill 2017 (distill.pub/2017/ctc/); Ogun 2020 blog
(ogunlao.github.io); Eisner, "An Interactive Spreadsheet for
Teaching the Forward-Backward Algorithm" (ACL-02 workshop,
cs.jhu.edu/~jason/papers/eisner.tnlp02.pdf); Zeyer, Schlüter & Ney
2021 (arXiv:2105.14849); Rabiner 1989 (Proc. IEEE 77(2):257–286);
Bell, Edinburgh ASR lecture 13 (2025); Hasegawa-Johnson, UIUC ECE
537 lecture 20 (2022); PyTorch forums "Question about CTC gradient"
(T. Viehmann); PyTorch issue #122243.

---

## Pinned report: source verifier

Method: exact `fractions.Fraction` arithmetic; brute-force path
enumeration and the trellis recurrence as two independent routes,
exact agreement everywhere. Graves 2006 equations verified against
rendered page images. Training trajectories float64 (flagged).

**A. Path probability (Graves 2006).** Eq. (2) p(π|x) = ∏ y^t_{π_t};
the conditional-independence sentence verbatim; eq. (3)
p(l|x) = Σ_{π∈B⁻¹(l)} p(π|x).

**B. Forward variable (2006 eqs. 5–8).** Init α₁(1) = y¹_b,
α₁(2) = y¹_{l₁}; recurrence (6)/(7) with the skip condition;
eq. (8) p(l|x) = α_T(|l′|) + α_T(|l′|−1).

**C. The two β conventions, both primary.** 2006 eq. (9): β's
product starts at t′ = t (includes frame-t emission); init
β_T(|l′|) = y^T_b. 2012 book eq. (7.12): product starts at t+1;
eq. (7.13) β(T,U′) = β(T,U′−1) = **1**. Consequences (2012):
eq. (7.26) p(z|x) = Σ_u α(t,u)β(t,u) for any t, no division;
eq. (7.34) **∂L/∂a^t_k = y^t_k − (1/p) Σ_{u∈B(z,k)} α β**.
[computed] β₂₀₀₆ = β₂₀₁₂ · y^t cell-by-cell exactly; identical P and
gradients.

**D. α·β and eqs. (14)–(15).** "the product … is the probability of
all the paths … that go through the symbol s at time t" (verbatim);
eq. (14) p = Σ_s αβ/y for any t [computed: verified at all four t];
lab(l,k) "which may be empty"; eq. (15)'s 1/y² correct under the
2006 convention.

**E. Eq. (16) verified correct as printed** [computed]: with
recursively rescaled α̂, β̂ and the printed Z_t it equals
y − occ exactly, all t, k. Equivalent unrescaled forms all verified
identical: y − (1/(y·p))Σαβ₂₀₀₆ = y − (1/p)Σαβ₂₀₁₂ = **y − occ**.
Matches the promised phrasing "softmax output minus how often the
truth used each cell" (a posterior expectation, not a count).

**F. A real discrepancy in the paper** [computed]: the unnumbered
line ln p(l|x) = Σ_t ln C_t **fails** on our example — ∏C_t = 0.6212
(= Σ over ALL five final states) vs p = 0.4877 (final two only).
Valid for the HMM forward algorithm it was borrowed from, not for
CTC. No published erratum found; the 2012 book itself drops
rescaling ("less robust, and can fail for very long sequences",
§7.3.1, recommending log-scale). Keep off screen.

**G. Figure 4, exact caption** (verified against page image):
"Evolution of the CTC Error Signal During Training. The left column
shows the output activations … (the dashed line is the 'blank'
unit); the right column shows the corresponding error signals.
Errors above the horizontal axis act to increase the corresponding
output activation and those below act to decrease it. (a) Initially
the network has small random weights, and the error is determined by
the target sequence only. (b) The network begins to make predictions
and the error localises around them. (c) The network strongly
predicts the correct labelling and the error virtually disappears."
The caption names **no dataset**. Plotted sign = the push (γ − y).

**H. Bridle 1989**: reused from plan 008 anchors F/M (verified
there); "the derivative before the output nonlinearity is the
difference between the corresponding output and a one-from-N
target."

**I. Zeyer, Schlüter & Ney 2021 (arXiv:2105.14849, preprint, v2
June 2021 — no peer-reviewed venue found).** Abstract verbatim
fetched (includes: "we prove that a feed-forward neural network
trained with CTC from uniform initialization converges towards peaky
behavior with a 100% error rate"). Remark 4.3: gradient =
−Σ q_t·∂log p_t, q_t "also known as soft-alignment" (= occupancy),
computed by forward-backward (Baum-Welch). Theorem 4.6 (bias model,
uniform init → peaky); its proof uses ∂L/∂b = T·(softmax(b) −
E_t[q_t]). Theorem 4.12 (FFNN, uniform init, their Example 4.9
B\*a+B\*, T ≥ 16 → peaky, suboptimal local optimum, 100% error).
Remark 4.11: the global optimum has 0% error — peakiness is a local
trap. Remark 3.10's "For the CTC topology, blank always has this
property [dominance]" is **loose** — false at our T=4 (see N).

**J. Rabiner 1989**: citation verified as printed in Graves'
bibliography (Proc. IEEE 77(2):257–286); the paper itself NOT
fetched — name-drop only, no direct quotes.

**K. The worked example, exact [computed, two routes agree].**
Matrix (rows A/B/ε; cols t=1..4): 0.7/0.2/0.1 · 0.6/0.1/0.3 ·
0.2/0.1/0.7 · 0.1/0.7/0.2. Columns 1–3 verbatim plan-008 A4; column
4 NEW (FLAG 1). 15 paths (= C(6,2), matches plan 001).
**P(AB|X) = 4877/10000 = 0.4877 exactly**; −ln P = 0.7181. Forward,
backward and brute force agree exactly (α: 0.025 + 0.4627; β:
0.0474 + 0.4403).

α (rows s=1..5 = ε A ε B ε):
0.1 / 0.03 / 0.021 / 0.0042 · 0.7 / 0.48 / 0.102 / 0.0123 ·
0 / 0.21 / 0.483 / 0.117 · 0 / 0.07 / 0.076 / 0.4627 ·
0 / 0 / 0.049 / 0.025.

β (2012 convention, the scene's):
0.474 / 0.14 / 0 / 0 · 0.629 / 0.72 / 0.7 / 0 ·
0.197 / 0.58 / 0.7 / 0 · 0.065 / 0.23 / 0.9 / 1 ·
0.042 / 0.14 / 0.2 / 1.

γ = αβ/P (columns each sum exactly to 1):
0.0972 / 0.0086 / 0 / 0 · 0.9028 / 0.7086 / 0.1464 / 0 ·
0 / 0.2497 / 0.6933 / 0 · 0 / 0.0330 / 0.1403 / 0.9487 ·
0 / 0 / 0.0201 / 0.0513.

Per-class occupancy (exact fractions /4877): t=1 A 4403 (0.9028),
B 0, ε 474 (0.0972); t=2 A 3456 (0.7086), B 161 (0.0330), ε 1260
(0.2584); t=3 A 714 (0.1464), B 684 (0.1403), ε 3479 (0.7133);
t=4 A 0, B 4627 (0.9487), ε 250 (0.0513).

**Gradient table ∂L/∂u = y − occ** (each row sums exactly to 0; 4-dp
displays also sum to 0.0000 digit-exact — FLAG 11):
t=1: A −0.2028, B +0.2000, ε +0.0028;
t=2: A −0.1086, B +0.0670, ε +0.0416;
t=3: A +0.0536, B −0.0403, ε −0.0133;
t=4: A +0.1000, B −0.2487, ε +0.1487.
(t=1 B exactly +0.2000 = y since occ = 0; t=4 A exactly +0.1000;
t=1 ε exact value 137/48770.)

∂L/∂y = −occ/y (eq. 7.31 form), 4 dp: t=1 (−1.2897, 0, −0.9719);
t=2 (−1.1811, −0.3301, −0.8612); t=3 (−0.7320, −1.4025, −1.0191);
t=4 (0, −1.3553, −0.2563) — all ≤ 0, only pushes up; why the u-form
is the teachable one.

Wrong transcript BA (same matrix): P = 363/10000 = 0.0363 exactly,
−ln P = 3.3159; t=1 A flips to exactly +0.7000 (state unreachable,
occupancy 0), B −0.7532, ε +0.0532; t=4 B +0.7000 exactly. Rows sum
to 0.

**L. Uniform-outputs beat, exact.** P = 15·(1/3)⁴ = 5/27 = 0.1852;
−ln P = 1.6864. Occupancy: t=1 (A 2/3, B 0, ε 1/3); t=2 (8/15, 1/5,
4/15); t=3 (1/5, 8/15, 4/15); t=4 (0, 2/3, 1/3). Gradient y − occ:
t=1 (−1/3, +1/3, 0); t=2 (−1/5, +2/15, +1/15); t=3 (+2/15, −1/5,
+1/15); t=4 (+1/3, −1/3, 0). Time-symmetric (t↔5−t with A↔B).

**M. Free-logit training toy [computed, float64 — FLAG 8].** GD on
4×3 logits, loss −ln P(AB|X), lr 1.0. From uniform: loss 1.6864 →
0.1953 (10) → 0.0310 (50) → 0.0070 (200) → 0.0013 (1000) → 0.0003
(5000); argmax path A A B B; blank does NOT dominate. From the repo
matrix (u = ln y): 0.7181 → 0.1602 (10) → 0.0356 (50) → 0.0088
(200) → 0.0003 (5000); argmax A A ε B; frame 3 converges to the
mixed (0.032, 0.218, 0.750) with gradient → 0 — all three frame-3
choices collapse to AB, so the loss goes indifferent: the error
disappears because y matches γ, not because y is one-hot.

**N. Shared-parameter (bias) toy [computed].** Label-occurrence
counts over all AB-paths (exact): T=4: 15 paths, A 21, B 21, ε 18 —
blank NOT dominant; T=5: 35 paths, 56/56/63 — dominant from here;
T=6: 126/126/168; T=8: 462/462/756; T=10: 1287/1287/2376 (blank
0.48). Bias model (Zeyer Def. 4.5), uniform init, lr 0.05: T=4
converges to (0.4, 0.4, 0.2), honest; **T=12 converges to (0.0919,
0.0919, 0.8162) — argmax blank everywhere, empty decode, 100%
error** — Theorem 4.6's mechanism on the repo's own alphabet and
transcript.

**O. Plan-009 anchors G/H reused** (verified there at 60 digits):
gradient at z = (2,1,0) = (−0.3348, 0.2447, 0.0900) = p − one-hot
(4-dp sum −0.0001, don't display the sum); saturation walk −0.9100,
−0.9868, −0.9993, then −0.99999551 (never display as −1.0000).

FLAGS: (1) matrix column 4 (0.1, 0.7, 0.2) is NEW, chosen by the
verifier, ratified in Decisions — maintainer to confirm at phase 3;
(2) fig. 4 names no dataset — attribute to "Graves et al. 2006"
without one; (3) ln p = Σ ln C_t fails as printed — off screen;
(4) eqs. (5)/(9) slice l with an l′-index — don't reproduce the
paper's subscripts, use the 2012 formulation; (5) Zeyer Remark
3.10's "always" is false at T=4 — condition every dominance claim on
T; (6) Zeyer is an arXiv preprint — cite as such; (7) the 4-frame
free-logit toy does NOT go peaky — never claim it does; the two toys
stay visually distinct; (8) training trajectories are float64 — 4 dp,
no exactness claims; (9) fig. 4 plots the push (γ − y), the negative
of the gradient — state the sign when both appear; (10) Rabiner not
independently fetched — no direct quotes; (11) all occupancy and
gradient 4-dp row sums are digit-exact (1.0000/0.0000) on this
example — checked, safe to show summing on screen (luck of these
numbers; plan 008's workhorse summed to 0.9999).

Sources: Graves et al. 2006 ICML (icml_2006.pdf); Graves 2012,
*Supervised Sequence Labelling with Recurrent Neural Networks*
(Springer SCI 385; author's preprint, cs.toronto.edu/~graves/
preprint.pdf) — NEW reference for the topic README; Zeyer, Schlüter
& Ney, arXiv:2105.14849; Rabiner 1989 (as printed in Graves'
bibliography); plans 008 (A4, F, M) and 009 (G, H). Verification
scripts in the session scratchpad: `ctc_verify.py`, `ctc_train.py`,
`ctc_bias.py`.
