# Plan 020: `signal_processing/` — convolution, the sliding weighted sum

Series C of the road approved 2026-09-19 (plan 019's road table): after
the spectrum, before windowing. The maintainer's ask (2026-09-24, after
PR #21 merged): "start convolution". Brief, from the approved route: a
sliding weighted sum, shown first as filtering — a moving average is a
low-pass filter — then the convolution theorem: multiplying in one domain
is convolving in the other. It precedes series D because leakage is the
convolution theorem at work: the spectrum series' 1500 Hz teaser
("that smear is leakage: the windowing series explains it — and tames
it") is what D will explain using what C builds.

Home: `signal_processing/`, module `convolution_manim.py`, seven scenes.
Branch `feat/signal-processing-convolution`, cut from `main` at fdf2672
(PR #21 merged, clean, level with origin). No study-guide work (ADR 010).

## Constraints fixed before research

1. **Levels 1–2 use only built devices.** The spectrum series' grid
   (N = 8 at 8000 Hz), lollipop stems, probe pairs, the bank of five
   detectors, orthogonality checked at N = 8, dB; expectation's weighted
   sum and its linearity. No complex numbers, Euler, integrals or linear
   algebra.
2. **"Filter" is earned here** — the series where a detector's output
   becomes a signal because the window slides — and is defined on screen
   before it is used.
3. **The convolution theorem is the level-2 core**; on the 8-sample grid
   the DFT's convolution is circular, and the series must be honest about
   that without teaching it.
4. **Level 3 only** for reverb (an impulse response), convolutional
   layers, the source–filter model of speech, and the hook to series D's
   leakage.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier); scene design | Scene design written into the plan; maintainer approves |
| 1 | Module stub with shared helpers imported or copied from `spectrum_manim.py`, README second-series Scope clause + row 1 | `make check` |
| 2 | Seven scenes at draft; layout linter clean; frames verified by eye, inside transition windows too | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, Ideas; wiki node + edges (closes the `spectrum` → convolution promise, opens D's); `welcome.gif` at eighteen series; root README row | `make test` |
| 4 | `connection-auditor` → findings applied and committed → self-check against CLAUDE.md → one local CodeRabbit pass | Review clean |
| 5 | PR; the bot's one automatic review; fixes in one push; one re-review only if a finding required a change; finalise after the bot round closes | `clean-drafts` + 1080p render; bot reviews spent (≤ 2) recorded here |

## Checklist

- [x] Phase 0: pedagogy report + verifier report (anchors A–N) pinned
  below as digests; design written (seven scenes; decisions D1–D10);
  design approved by the maintainer 2026-09-24 — both open calls taken as
  recommended (the conv-layer line stays in scene 3; source–filter moves
  to scene 7 only if scene 6 runs long); the verifier addendum (O–Y) lands
  in phase 1
- [x] Phase 1: `convolution_manim.py` — the spectrum series' helpers
  copied in (`_probe`, `_reading`, `_fmt`, `_Stems`, `_number_strip`,
  `_swap_caption`, `_takeaway`, `_Bank`, `_uprights`; topic dirs are not
  packages, and this is the second series to need them — a third should
  promote them to `utils`), plus `_slide` (linear, edge neighbours drawn)
  and `_ring` (circular) with the kernel's alignment explicit, and
  `_Window` (weight tokens under the stems the window covers).
  `TheSlidingWeightedSum` built in full (50 s at draft; linter clean —
  the strip carries its two edge neighbours as muted ghost stems so the
  window can read them at the ends, and the prompt retires before the
  8-high spike arrives under it; frames verified by eye). Bug caught by
  the anchors: the causal offset was off by one (the 2-tap gave 2, 2, 5,
  5 instead of 2, 2, 2, 5, 5) — every kernel alignment is now checked
  against anchors O–P before a scene uses it. README: the road table's
  convolution row, Scope's "filter" bullet rewritten for two series and
  a circular-convolution exclusion added, subsection + row 1; verifier
  addendum (O–Y) pinned; `make check` green
- [x] Phase 2: seven scenes at draft (7 files, distinct names; 50, 55,
  51, 66, 69, 53, 43 s). New devices: `_strip` (a stem strip with its
  numbers dropped below its negative reach), `_Window` (weight tokens
  sized to the stem pitch, single-glyph ⅓ and ½), `_bank_readout` (bars
  at any column and unit — the bank's own readout is too long for two
  columns), the edge-neighbour ghost stems, the turned-arrow sum on the
  pair plane. Linter: every scene clean; what it caught — side tags off
  the left edge, the prompt under the 8-high spike, a title crossed by a
  stem, number strips crossed by negative stems, window frames crossing
  the numbers under them, an unnamed `boxed()` left behind by a FadeOut,
  side-column facts too wide for a side column (moved to two-line
  blocks, per CLAUDE.md's 35-character rule). Eyes caught — the scene-4
  caption lagging the picture by a beat (captions now leave with the old
  tone), the endless wave off-centre, the stacked responses too tight.
  Width discipline: every caption ≤ 82 characters (ruff's 100-column
  line is the harder limit at this indentation). README rows 1–7 written
  with the scenes (the source-order test reds otherwise); `make check`
  green
- [x] Phase 3: README — 28 plan-020 references unchecked (the O&S entry
  renamed so its slug does not collide with the spectrum series' ticked
  one: the sync silently overwrote the verified entry until it did), Ideas
  rewritten (convolution struck; source–filter, circular convolution as a
  concept, the other kernels queued); wiki — `convolution` node, the
  `spectrum` → convolution row flipped delivered in place, a delivered row
  from `random-variables`, a promised row for the source–filter model, the
  windowing / Euler / FFT / mel rows amended, four device stops (the
  walking window is new); Ideas amended in `calculus/` and `algorithms/`;
  `welcome.gif` at eighteen series (430 KB); root README row and "what's
  next". **Prose checked against the built scenes** (the wiki pass): the
  closing map is six lines, not seven — source–filter is the comb beat,
  not a map line; the FFT is "parked elsewhere" on screen; the walking
  window has no Σ node (docstring fixed); the plan's design section trued
  to all three. Not made, logged: convolutional layers (a level-3 pointer
  with no home node); the two-dice diagonals as a pmf convolution.
  `make test` green
- [x] Phase 4: `connection-auditor` run on ce6ea65 (incremental; zero
  numeric discrepancies — every on-screen number recomputed). **Top
  finding, README:** the Scope's "Leakage and windows" bullet still said
  a tone between rows appears twice and is never explained —
  `MultiplyingInTime` shows it a third time and explains the smear; the
  bullet now says explained, not tamed. **Second, on screen:** the
  closing map's "built here" sat over three GOOD lines of which only the
  kernel's own reading is built (reverb drawn and priced, conv layers
  named) — now "met here"; README row 7 and both wiki quotes follow. Also
  applied: the 3000 Hz reading (0.55) captioned as its siblings are;
  convolutional layers ruled a Scope exclusion, not a promised row (the
  map colours it GOOD, no home node exists and none is owed); the
  windowing row keeps one row with its closure rule written in;
  asymmetries closed (`probability/` row 4, `deep_learning/`'s encoder
  bullet, the topic Scope naming this series' far ends); an unsourced
  modulation sentence cut from row 6; the first difference's far end
  (`TheSlopeIsAFunction` on stems) named in Ideas; design section trued
  (no Σ node; source–filter stated once). Not made, logged: a trellis/DP
  reading (declined — weights input-dependent), the bank as diagonalising
  a circulant matrix (the strongest on-ramp yet for parked
  `linear_algebra/`), Whisper's two conv layers as the fact-bridge. Stamp
  advanced to ce6ea65. Self-check against CLAUDE.md: no raw colours, no
  `palette()`, every replacement out-then-in, one orphan `boxed()` found
  and named (scene 1's definition box would have sat under the takeaway).
  Drafts re-rendered (7 files), linter clean. **The one local CodeRabbit
  pass** (`coderabbit review --agent
  --base main`, on 656f03c, 13 files): two findings, both valid. Major —
  `WhatOneClickBecomes`' walked window started over x[0], x[1] for output
  0, but output n reads x[n−1] and x[n]: the picture claimed the wrong
  pair (the numbers were right, the frame was one stop late). The strip
  now carries a zero ghost at each end and the window covers x[n−1], x[n]
  — "the picture is a claim", caught by the reviewer, not the linter.
  Minor — the vocal tract's reading was drawn WARM (the cancelled colour);
  a reading is ACCENT. Both verified by re-render. Not rerun: the changes
  are the findings' own fixes, and the bot reviews them on the PR
- [x] Maintainer's source pass (2026-09-24, PR #22 open, before the bot
  round closed): he verified all twenty-eight plan-020 references — the
  Fant entry with a publisher's preview he supplied — and directed the
  ticks; `references.bib` re-synced (332 entries, 288 verified)
- [ ] Phase 5 — PR #22 opened 2026-09-24. The bot's one automatic review:
  seven findings, all valid on inspection, applied in one push. The one
  that mattered: `MultiplyingInTime` said "every frame is × a rectangle
  of eight ones" one beat after showing that × eight ones on the ring
  changes nothing — the rectangle only has lines of its own on the long
  strip, where the product's spectrum is the tone's line spread by them
  and *then* read at the rows; the captions, README row 6 and the Scope
  bullet now say so, and the whole-lap case is stated precisely (the
  copies land on the other rows' exact zeros). The rest: `FadeOut(bank)`
  would have flashed the never-added fan (`_bank_drawn` fades the drawn
  parts); the kernel tokens are `utils.chip`, scaled — its label size is
  fixed; scene 4's Smith caption names its kernel (it appeared over the
  ½ ½ picture); scene 5's tag faded in only during its fade-out; "signs
  and all" listed the readings unsigned. Riding in the same push: the
  KaTeX `\*` fix in `deep_learning/`, Fant's URL, the maintainer's
  twenty-eight ticks. One re-review requested — findings required
  changes. **Bot reviews spent: 1 of 2.** Finals: pending

## Research digests

### Verifier report (digest — `source-verifier`, 2026-09-24; anchors A–N)

Exact route sympy over Q(√2), numeric route numpy; every table by both,
agreeing to 1e-12. Conventions are the spectrum series' (plus-signed sine
sum, X[k] = aₖ − i·bₖ); kernels causal unless "centred" is said;
convolution on the 8-grid is circular.

**Corrections to the brief.** (1) The causal step's first output through
the 3-tap is ⅓, not 0 — a leading 0 needs the step to start later. (2)
"Flips sign where H < 0" is true of the *centred* 3-tap (rows 3, 4
negative); with the causal kernel drawn sliding, row 4 shows no flip
(delaying the alternating tone by one sample *is* a flip) and row 3's
flip appears as an extra half-turn on top of the delay rotation — the
picture must say which alignment it draws; magnitudes are
alignment-independent. (3) The 3-tap has no exact zero on the grid (its
zero is at k = 8/3, 2667 Hz); the 2-tap's zero is at row 4 and the 4-tap's
at rows 2 and 4. (4) Delay rotates the pair *counter-clockwise* by
k·m·45° under the repo's sign; under numpy's, clockwise — state the
convention if the direction is drawn. (5) "A bank of learned FIR filters"
is a paraphrase — LeCun's verbatim is "the kernel of the convolution is
the set of connection weights". (6) The rect-window table is dominated
by a DC term (row 0 reads 2.41, louder than the tone's own row); Hann
*confines* leakage to the neighbour rather than reducing it there.

**Anchors.** A — O&S 3rd ed.: convolution sum §2.3 eq. (2.49); circular
convolution §8.6.5 eq. (8.114); theorem eq. (8.126) x₁ ⊛ x₂ ↔ X₁X₂; dual
eq. (8.127) x₁x₂ ↔ (1/N) X₁ ⊛ X₂; linear = circular iff N ≥ L + P − 1
(§8.7.2 p. 663), otherwise the tail wraps (eq. 8.137) — shown at N = 8:
L = 4, P = 6 differ at n = 0 only, circ[0] = lin[0] + lin[8]. J. O. Smith
MDFT: "perhaps the most important single Fourier theorem of all". B —
real-pair form: pair(y) = (ac − bd, ad + bc), |Y| = |X|·|H|, angles add;
a corollary verified by computation (label as such). C — moving-average
responses on the grid, |H| rows 0–4: 2-tap [½, ½] → 1, 0.9239, 0.7071,
0.3827, 0 (= cos πk/8); 3-tap → 1, 0.8047, ⅓, 0.1381, ⅓ (centred values
negative on rows 3–4); 4-tap → 1, 0.6533, 0, 0.2706, 0. S. W. Smith ch.
15: "an exceptionally good smoothing filter … but an exceptionally bad
low-pass filter"; eq. 15-2. D — bin-centred tones through the kernels:
s₂ through the 3-tap → [−⅓, 0, ⅓, 0, −⅓, 0, ⅓, 0], row 2 reading 4/3
(**scaled by exactly ⅓**); c₄ through the 2-tap → all eight exactly 0
(**killed**); s₁ through the 2-tap → reading 3.6955 = 4 × 0.9239, pair
rotated to 112.5°; s₁ through the 3-tap → 0.8047·s₁ delayed one sample.
E — δ through any kernel returns the kernel (O&S: "an LTI system is
completely characterized by its impulse response"); a step at n = 4 on
the 8-grid through the 3-tap: linear 0, 0, 0, 0, ⅓, ⅔, 1, 1, ⅔, ⅓;
circular ⅔, ⅓, 0, 0, ⅓, ⅔, 1, 1 — the tail wraps onto n = 0, 1. F — the
fully exact theorem check: x = the 3-4-5 tone [3, 4, −3, −4, …] (plan 019
Q), h = 3-tap: y = [−4/3, 1, 4/3, −1, −4/3, 1, 4/3, −1]; readings x =
[0, 0, 20, 0, 0], h = [1, 0.8047, ⅓, 0.1381, ⅓], y = [0, 0, 20/3, 0, 0];
row-2 pair arithmetic (12, 16) × (0, ⅓) = (−16/3, 4), hypot 20/3. Also
Lyons' mix: readings [0, 4, 2, 0, 0] → [0, 3.2190, 0.6667, 0, 0]. G — the
dual, one table: s₁ × rect[1,1,1,1,0,0,0,0] reads [2.41, 2, 1, 0, 0.41]
on rows 0–4 (leakage — and a DC term); s₁ × periodic Hann [0, 0.1464,
0.5, 0.8536, 1, 0.8536, 0.5, 0.1464] reads [0, 2, 1, 0, 0]; the
unwindowed tone reads [0, 4, 0, 0, 0]. H — linearity (O&S eq. 2.24) and
time-invariance (§2.2.3) verified exactly; §2.3 derives the convolution
sum from both. I — correlation vs convolution (S. W. Smith ch. 7: "the
signal inside of the convolution machine is flipped left-for-right"):
for [1, 2, 3] they differ; for the 3-tap they coincide up to a delay of
M − 1 = 2 samples, exactly when the kernel is drawn centred — "the probe's
multiply-and-sum, now sliding" is honest for a symmetric kernel. J — DC
gain = kernel sum: [1, 2, 1]/4 → |H| 1, 0.8536, 0.5, 0.1464, 0 (the
2-tap squared: "each time domain convolution results in a multiplication
of the frequency spectra"); [1, −1] → 0, 0.7654, 1.4142, 1.8478, 2 — a
high-pass. K — reverb: J. O. Smith PASP, outputs "computed by six
convolutions" of sources with source-to-ear impulse responses; Allen &
Berkley 1979 citation only. Source–filter: Jurafsky & Martin (draft 19
Aug 2026) §15.4.6 verbatim; Fant 1960 not opened. L — LeCun et al. 1998
§II.A ("synthesizing their own feature extractor"; TDNNs for phoneme
recognition); Goodfellow et al. ch. 9 p. 328: "Many machine learning
libraries implement cross-correlation but call it convolution." M —
history (per Domínguez 2010/2015, secondary): Laplace 1778; "Faltung"
Doetsch 1923; the theorem in Borel 1899 — nothing firmer. N —
3Blue1Brown, 18 Nov 2022, owns: the two-dice sum, the flipped-and-slid
list, image kernels, polynomial multiplication, the FFT speed-up; it does
NOT do a kernel's response on a DFT grid, the impulse response as "the
kernel comes out", LTI as properties, the pair rotation, windowing.

**Sources** (16, full list to the README in phase 3): O&S 3rd ed. (MIT
OCW PDF); J. O. Smith MDFT (three pages) and PASP (two); S. W. Smith ch.
15 and ch. 7; Lyons ch. 5 (TOC only); Goodfellow, Bengio & Courville ch.
9; LeCun, Bottou, Bengio & Haffner 1998; Jurafsky & Martin ch. 15; Fant
1960 (not opened); Allen & Berkley 1979 (not opened); HF Audio Course
(no source–filter sentence — do not cite it for that); Domínguez 2010 and
2015; Wikipedia (pointers only); 3Blue1Brown.

### Pedagogy report (digest — `pedagogy-researcher`, 2026-09-24)

No code tool; every number is hand arithmetic and goes through the
verifier before it reaches a screen.

**Camp choices.** (a) Filter-first (Lyons §5.1, J. O. Smith's *Filters*,
3Blue1Brown) over impulse-response-first (S. W. Smith ch. 6, O&S ch. 2):
the probe's multiply-and-sum is owned, so the sliding sum is the smallest
new step. (b) The flip: correlation-first on a *symmetric* kernel (the
flip is invisible), then name it on an *asymmetric* one — the echo kernel
[1, 0, 0, ½] — where the probe's move puts the echo *before* the click
and convolution puts it after. Correlation asks "how much does the signal
look like this pattern here" (a detector); convolution asks "what does
this system do to a click" (a filter). (c) Build the *filter* direction
of the theorem as the level-2 argument — exactly checkable with real
pairs at N = 8 on owned devices — and state the dual, checked once,
because series D runs the dual on the 1500 Hz teaser.

**The strongest device: the kernel put on the bank.** Feed the kernel
itself to the built `_Bank`: its readings *are* the five gains
(1, 0.80, ⅓, 0.14, ⅓; centred pairs (1, 0), (0.80, 0), (⅓, 0),
(−0.14, 0), (−⅓, 0)). Why, on the pair plane from `TheProbe`: a delayed
whole-lap tone is a turned pair (row k turns 45°·k per sample); the
filter's output is a weighted sum of delayed copies; the row's sum is
linear — so the output's pair is the input's pair times the sum of the
kernel's turned arrows, three arrows of length ⅓ at 0, +45°k, −45°k
summed head to tail: k = 1 → 0.80, k = 2 → ⅓ (the side arrows cancel),
k = 3 → −0.14 (backwards), k = 4 → −⅓. That is "magnitudes multiply,
phases add" without a complex number; "checked on one kernel and four
rows — for every kernel and every N the proof needs Euler's formula"
(the second customer of the `calculus/` Euler promise).

**Recommended arc.** 1 `TheSlidingWeightedSum` (L1; "filter" defined on
screen: a filter turns a signal into a signal) · 2 `WhatOneClickBecomes`
(L1→2; the impulse response; superposition as a stack; "sums pass
through" and "the same rule at every stop" named) · 3 `TheFlip` (L2,
short; the echo kernel; causality: the centred average peeks one sample
ahead) · 4 `AMovingAverageIsALowPass` (tones through the kernel, bank
read before and after; low-pass *scales*, it does not remove — the 2-tap
killing 4000 Hz is the special case gain 0; S. W. Smith: best smoother,
worst frequency separator) · 5 `TheKernelsOwnReading` (L2 core, the
device above) · 6 `MultiplyingInTime` (L2→3; the dual checked once:
s₂ × c₁ moves the row-2 bar of 4 to two bars of 2 at rows 1 and 3, "4 ×
4 ÷ 8"; every frame *is* a multiplication by a rectangle — the 1500 Hz
teaser re-read as leakage-by-the-theorem; the source–filter pointer) ·
7 `WhereConvolutionLives` (L3 closer; reverb as a room's impulse
response; conv layers; the sliding detector → filterbank; the closing
map).

**Other devices.** The walking window (kernel weights as MUTED tokens
under three adjacent stems, an ACCENT frame whose foot drops one ACCENT
stem into a second strip — built without the Σ node the pedagogy report
proposed — `TheProbe`'s picture with the probe moving). The click
that becomes the kernel; a scaled click → a scaled shape, a later click →
a later shape; the input-side stack and the output-side machine landing
on the same numbers on one screen (S. W. Smith Figs. 6-6 and 6-8). Tones
through the kernel with the bank read before and after; the 3000 Hz
tone visibly flipping sign. The split line for the dual. The frame as
"an endless tone × a rectangle of eight ones".

**Examples proposed** (hand-verified; the addendum pins them): the spike
2, 2, 2, 8, 2, 2, 2, 2 through the 3-tap → 2, 2, 4, 4, 4, 2, 2, 2, both
sums 22 (weights sum to 1); the plain sum [1, 1, 1] triples it. The click
through the 3-tap gives ⅓, ⅓, ⅓; 1, 2, 0, 3 through [½, ½] → 0.5, 1.5,
1, 1.5, 1.5 (length 4 + 2 − 1 = 5) as three scaled shifted copies. The
echo kernel on a click: convolution ½ at +3, the unflipped slide ½ at −3.
3Blue1Brown's dice diagonals = `SameOutcomesAdd`'s two-dice level sets: a
one-caption aside at most.

**Misconceptions.** The flip as a mystery (the echo kernel answers it;
symmetric kernels hide it — say so). "Convolution blurs" as the only
intuition (the kernel is what one click becomes: delay, echo, slope,
high-pass). A filter "removes" frequencies (it scales; gain 0 is the
special case). The kernel's sum is arbitrary (the plain sum triples a
constant; row 0's gain is Σh). Circular vs linear: keep bank checks to
whole-lap tones, where "the sample before stop 0 is what the tone did one
stop earlier" is true of the tone, not an assumption of the transform;
clicks and steps live on a longer strip with the zeros drawn and never
touch the bank; the README Scope records that the DFT's theorem is
circular. Causality is not free: the centred average is the causal one a
stop early. Students compute convolution without seeing it rests on
linearity and time invariance (SSCI interviews) — make the two facts the
argument. "Multiplying in time is harmless" — the beat that makes D's
leakage a consequence.

**Pitfalls.** Negative gains on rows 3–4 of the centred 3-tap: show the
sign flip, never a hidden phase. The bank reads magnitudes; for symmetric
kernels "reading × gain" is exact, for the causal 2-tap the pair also
*turns* — caption the turn. End rows read ÷ 8: flagship gain checks on
rows 1–3 (4 → 3.22, 1.33, 0.55). The centred kernel on the grid needs ⅓
at stop 7 — say "the stop before 0 is stop 7 on a whole-lap ring" once.
Time invariance is unnamed in the repo: "the same rule at every stop",
no "LTI". Don't reuse "detector" for the filter: detector = one number
per frame, filter = a signal per signal. Fant 1960 not opened; J&M's
source–filter section neither cites Fant nor says "convolution" — credit
them for the picture and the numbers only.

**Sources** (36; full list to the README in phase 3): S. W. Smith ch. 6
(five sections), ch. 7 (three), ch. 9 §3, ch. 15 (three); Lyons 3rd ed.
contents; J. O. Smith *Filters* (three pages), MDFT (five), the CCRMA
reverb lecture; O&S 3rd ed.; MIT 6.341 L16; Goodfellow et al. ch. 9;
Wage, Buck & Hjalmarson 2006 (abstract); Sanderson 2022; Azad; Wilczek;
Jurafsky & Martin §15.4.6; Wikipedia (three pages, pointers). Third-party
reposts consulted and not to be linked.

### Verifier addendum (anchors O–Y — `source-verifier` resumed, 2026-09-24)

**Corrections that bind the design.** (1) Under the repo's plus-signed
sine sum a unit impulse at stop m has pair (cos 45°km, **+sin** 45°km)
on row k — the arrow for stop m turns *counter-clockwise* by 45°·k per
stop; any kernel's row-k pair is Σ h[m]·(cos, +sin). (2) Σy = Σx·Σh is a
theorem for the full linear output with zeros beyond both ends, and for
the ring; for eight drawn outputs with constant neighbours it holds only
when what leaks in equals what leaks out — true of the spike (x[0] = x[7]
= 2 = the neighbours), so 22 → 22 and 66 are exact, but the caption must
not claim the rule for an arbitrary strip. (3) J. O. Smith's causality
phrase is "the pulse is smeared to the 'right' (forward in time) because
the filter impulse response starts at time zero. Such a filter is said to
be causal" — and his example is a 14-point ring. (4) Goodfellow's verbatim
is "many neural network libraries implement a related function called the
cross-correlation, which is the same as convolution but without flipping
the kernel" and "Many machine learning libraries implement
cross-correlation but call it convolution." (5) S. W. Smith's sum rule is
conditional: "*If* a low-pass filter has a gain of one at DC … then the
sum of all of the points in the impulse response must be equal to one."
(6) Lyons' 5-tap gains: 0.9619 (not 0.9618) and 0.6857; his cars table
NOT verified — not on screen. (7) s₂ × c₄ = −s₂ reads 4 on row 2 as ONE
term of the complex sum (the mirror copy) — "two copies" only in the real
picture; scope the "4 × 4 ÷ 8" caption to its instance.

**Anchors.** O — the spike through the centred 3-tap → 2, 2, 4, 4, 4, 2,
2, 2 (Σ 22); through the causal 2-tap with x[−1] = 2 → 2, 2, 2, 5, 5, 2,
2, 2; through [1, 1, 1] → 6, 6, 12, 12, 12, 6, 6, 6 (Σ 66). P — the click
through the causal 3-tap → ⅓, ⅓, ⅓, 0…; −2× → −⅔ ×3; at stop 3 → ⅓ at 3,
4, 5 (a click at stop 6 or 7 would wrap — avoid). [1, 2, 0, 3] ∗ [½, ½]
linear → 0.5, 1.5, 1, 1.5, 1.5 = 1·[½,½,0,0,0] + 2·[0,½,½,0,0] +
3·[0,0,0,½,½]; y[3] = ½·3 + ½·0. Q — the echo kernel [1, 0, 0, ½] on a
click: convolution 1 at 0, ½ at +3; the unflipped slide ½ at −3, 1 at 0;
the centred 3-tap is identical both ways, E is not. R — the centred
3-tap at stops 7, 0, 1: pairs (1, 0), ((1+√2)/3, 0), (⅓, 0), ((1−√2)/3,
0), (−⅓, 0), every sine sum exactly 0 — equal to the turned-arrow sums
⅓(1 + 2cos 45°k); the causal 2-tap at stops 0, 1: row 2 pair (½, ½),
0.7071 at 45°, row 4 (0, 0). S — delay by one turns row k's pair
counter-clockwise by 45°·k: s₂ → (−4, 0) (+90°), s₁ → (−2√2, 2√2) (+45°).
T — s₂ × c₁: pairs (0,0), (0,2), (0,0), (0,2), (0,0), readings [0, 2, 0,
2, 0]; each is one term X[2]·W[∓1]/8 = (4 × 4)/8 — exact for this
instance; s₂ × c₀ = s₂. U — the step 0, 0, 0, 1, 1, 1, 1, 1 (x[8] = 1
drawn) through the centred 3-tap → 0, 0, ⅓, ⅔, 1, 1, 1, 1; through the
causal 2-tap → 0, 0, 0, ½, 1, 1, 1, 1; the ring versions wrap (do not
draw them as the strip). J. O. Smith's example reproduced: "the corners
of the rectangular pulse are 'smoothed' by the three-point filter"; the
centred version "smoothed 'in place' with no added delay". V — Lyons'
5-tap: 0.9619, 0.6857. W — J. O. Smith, CCRMA Lecture 3 (opened): "Let
t60 = 2 seconds, fs = 50 kHz — each filter requires 100,000 multiplies
and additions per sample, or 5 billion multiply-adds per second"; "In
principle, this is an exact computational model"; "the output is given
by six convolutions". Jurafsky & Martin §15.4.6 verbatim: "a 115 Hz
glottal fold vibration leads to harmonics (other waves) of 230 Hz, 345
Hz, 460 Hz"; Fig. 15.24 "Visualizing the vocal tract position as a
filter". X — S. W. Smith verbatim: "each point in the output signal
receives a contribution from many points in the input signal, multiplied
by a flipped impulse response"; "Convolving any signal with a delta
function results in exactly the same signal"; the echo: "the input signal
plus a delayed version of the input signal". Y — Goodfellow per
correction 4. Three sources added (MDFT "Convolution Example 1"; the
CCRMA reverb handout; S. W. Smith ch. 6 §"Sum of Weighted Inputs" and
ch. 7 §"Common Impulse Responses").

## Scene design

Built from the two reports above. Grid: the spectrum series' — N = 8
at 8000 Hz, rows at 0–4 kHz. Two kinds of strip: the **ring** (whole-lap
tones on 8 samples, where "the stop before 0 is stop 7" is the tone's own
repetition and circular equals linear) for everything the bank reads;
the **long strip** (a signal with the zeros beyond its ends drawn) for
clicks, steps and the 4-sample superposition, which never touch the bank.

### Decisions

- **D1 — "filter" is earned in scene 1 and defined before use:** a
  filter turns a signal into a signal; the detector gave one number per
  frame — slide the window and the numbers become a signal. Both words
  keep their own objects for the rest of the road.
- **D2 — correlation first, the flip named on an asymmetric kernel.**
  The walking window is `TheProbe`'s multiply-and-sum moving; on the
  symmetric moving average the flip is invisible, and scene 3 shows what
  it is *for* on the echo kernel [1, 0, 0, ½]: the probe's slide puts the
  echo *before* the click (a pre-echo, WARM), the flipped slide puts it
  after. Convolution = "what one click becomes"; correlation = "how much
  does the signal look like this pattern here".
- **D3 — the centred 3-tap [⅓, ⅓, ⅓] is the flagship kernel**; the
  causal 2-tap [½, ½] is the second (its exact zero at 4000 Hz; its pair
  *turns* 45° on row 2 — captioned as the half-sample delay). Centred
  kernels are drawn centred; causality is named once in scene 3 ("the
  centred average peeks one sample ahead; the causal one is the same
  output a stop late").
- **D4 — the theorem's level-2 argument is the filter direction**, on the
  pair plane: delay = a turn of 45°·k per sample on row k (`TheProbe`'s
  quarter-turn generalised); the output is a weighted sum of delayed
  copies (scene 2); sums pass through the row (`NoDoubleCounting`) — so
  the output's pair is the input's pair times the kernel's own reading in
  that row. Checked on one kernel and four rows; "for every kernel and
  every N the proof needs Euler's formula" (the Euler promise's second
  customer). The dual is *stated* and checked on one instance.
- **D5 — a low-pass scales, it does not remove.** Every tone comes out
  the same tone, scaled (and for rows 3–4 of the centred 3-tap, sign
  flipped — shown, never hidden). Gain 0 is the special case: the 2-tap
  on 4000 Hz. Flagship gain checks on rows 1–3 (4 → 3.22, 1.33, 0.55);
  the end rows read ÷ 8 and are used for gain 1 and gain ⅓ only.
- **D6 — circularity is met, not taught.** Bank checks use whole-lap
  tones only; the README Scope records that the DFT's theorem is circular
  (O&S §8.6.5) and that this series meets it where circular and linear
  agree; series D owns the case where they don't. The word "assumes"
  stays off screen (plan 019).
- **D7 — the kernel's sum is the DC gain**: the plain sum [1, 1, 1]
  triples a constant; weights summing to 1 conserve the total (the spike's
  22 → 22).
- **D8 — level 3 only:** reverb (a room's impulse response is the echo
  kernel grown long; 100 000 multiply-adds per sample at 50 kHz for a
  2 s tail — hence FFT convolution, the FFT still parked), convolutional
  layers (learned kernels slid over the input; libraries correlate and
  call it convolution), the source–filter model (glottal pulses shaped by
  the vocal tract: 115 Hz → 230, 345, 460 Hz), and the hook to D: every
  frame is a multiplication by a rectangle.
- **D9 — colour.** COOL the input signal; MUTED the kernel tokens and
  the empty bank; ACCENT the output being built (the dropped stem, the
  turned-arrow sum, the lit row); WARM the pre-echo and the sign-flipped
  tone; GOOD a confirmed match (the two views landing on the same
  numbers). Kernels of different taps are ranked by length, not
  `palette()`.
- **D10 — text.** "the sample before" in words or `MathTex`; kernel
  weights as tokens; "the same rule at every stop" for time invariance,
  never "LTI".

### Scenes

| # | Scene | Level | What is on screen |
| --- | --- | --- | --- |
| 1 | `TheSlidingWeightedSum` | 1 | The spike 2, 2, 2, 8, 2, 2, 2, 2 on a long strip; three ⅓ tokens under three adjacent stems — `TheProbe`'s multiply-and-sum, now walked along: at every stop the window's frame drops one ACCENT stem into a second strip (no Σ node is drawn), 2, 2, 4, 4, 4, 2, 2, 2. "A filter turns a signal into a signal — the detector gave one number; slide the window and the numbers become a signal." Both totals 22: the weights sum to 1. The plain sum [1, 1, 1] triples everything (66). Named: the moving average, the kernel. |
| 2 | `WhatOneClickBecomes` | 1 → 2 | One click through the kernel gives the kernel back — the impulse response, what one click becomes; −2× the click → −2× the shape; a click at stop 3 → the shape at 3, 4, 5. Then 1, 2, 0, 3 through [½, ½] two ways on one screen: the input-side stack (three scaled shifted copies of the shape, summed) and the output-side machine (one output at a time, the window read backwards) land on the same 0.5, 1.5, 1, 1.5, 1.5 — length 4 + 2 − 1 = 5, the ends drawn. The two facts named with their owners: "sums pass through" (`SameOutcomesAdd`'s move) and "the same rule at every stop". |
| 3 | `TheFlip` | 2 | The echo kernel [1, 0, 0, ½] on a click: the probe's slide (pattern unreversed) puts ½ at stop −3 — a pre-echo, WARM; the flipped slide puts it at +3 — an echo. Same numbers, one list reversed; the moving average hid it because ⅓ ⅓ ⅓ reversed is itself. Correlation = a detector's question; convolution = a filter's. Causality: the centred average peeks one sample ahead; the causal one is the same output a stop late (the step 0, 0, 0, 1, 1, 1, 1, 1 → 0, 0, ⅓, ⅔, 1, 1, 1, 1). When-useful: convolutional layers correlate and call it convolution — a learned kernel does not mind. |
| 4 | `AMovingAverageIsALowPass` | 1 → 2 | Whole-lap tones through the centred 3-tap on the ring, the bank read before and after: 1000 Hz → 0.80 as tall (4 → 3.22); 2000 Hz → exactly ⅓ (4 → 1.33); 3000 Hz → 0.14 and sign-flipped (WARM; 4 → 0.55); 4000 Hz → ⅓ and flipped (8 → 2.67, ÷ 8 noted); 0 Hz → unchanged. "Low-pass: slow tones pass, fast tones shrink — it scales, it does not remove." The 2-tap [½, ½] on 4000 Hz: all eight exactly 0 — gain 0, the special case; on 2000 Hz the pair turns 45° (the half-sample delay). S. W. Smith's verdict: the best smoother, the worst frequency separator — row 3 quieter than row 4. |
| 5 | `TheKernelsOwnReading` | 2 · core | The kernel itself on the bank (⅓ at stops 7, 0, 1 — "the stop before 0 is stop 7 on the ring"): its readings are the five gains, 1, 0.80, 0.33, 0.14, 0.33, with rows 3 and 4 negative. Why, on `TheProbe`'s pair plane: a delayed tone is a turned pair (45°·k per sample); the output is a weighted sum of delayed copies; the row's sum is linear — three arrows of length ⅓ at 0, +45°k, −45°k summed head to tail: k = 1 → 0.80; k = 2 → ⅓ (the side arrows cancel); k = 3 → −0.14; k = 4 → −⅓. Boxed: filtering in time = multiplying the readings, row by row. "Checked on one kernel and four rows — for every kernel and every N, the proof needs Euler's formula." The 2-tap's row-2 pair (½, ½): length 0.71, turned 45° — the turn of scene 4 explained. |
| 6 | `MultiplyingInTime` | 2 → 3 | The dual, stated: multiply two signals stop by stop and the readings convolve — each line of one gets a copy of the other's lines. Checked once: the 2000 Hz tone (row 2 reads 4) × a 1000 Hz cosine (row 1 reads 4): row 2 empties, rows 1 and 3 read 2 each — "4 × 4 ÷ 8 = 2, for this pair"; × the all-ones tone changes nothing. Then the hook: every frame *is* a multiplication — the 8 samples are an endless tone × a rectangle of eight ones; a whole-lap tone does not notice; the 1500 Hz sine from `WhatSetsTheSpacing` (bars 1.5, 2.85, 2.41, 0.85, 0.67, re-shown) does — its smear is the rectangle's lines copied onto the tone's: leakage, by the theorem — series D. (Source–filter moved wholly to scene 7 at build — open call 2, as recommended.) |
| 7 | `WhereConvolutionLives` | 3 · closer | Reverb: a room's impulse response is the echo kernel grown long — a 2 s tail at 50 kHz is 100 000 taps, 100 000 multiply-adds per output sample, which is why FFT convolution exists (the FFT — on screen "an algorithm story, parked elsewhere"; the README names `algorithms/`). Convolutional layers: learned kernels slid over the input. Source–filter, stated here — its only statement (scene 6 no longer carries it). The sliding detector: slide the probe and the bank becomes a filterbank whose impulse responses are the reversed probes — series D. Closing map, six lines under "met here — next on the road: the window behind every frame, then the spectrogram": echoes and rooms → reverb, one long kernel · smoothing and sharpening → a kernel's own reading · kernels a network chooses → convolutional layers · a tone between rows → windowing (D) · tones that change over time → the short-time transform (D) · the ear's own grouping → mel. (Built as six lines; the source–filter pointer lives in the comb beat above, not on the map.) |

Foundation: scenes 1–3 (the sliding sum, the impulse response, the
flip). The theorem owns scenes 4–6; scene 7 maps.

### What the series opens and closes (wiki, phase 3)

- **Closes** `spectrum` → *(convolution)*. **Delivered edges from:**
  `spectrum` (the probe's multiply-and-sum, the bank read before and
  after, the pair plane's turn, the 1500 Hz teaser re-read),
  `random-variables` (linearity — "sums pass through"; possibly the
  two-dice diagonals as a one-caption aside).
- **Promised:** windowing → STFT → spectrogram (series D — now with its
  mechanism stated: leakage by the dual; the sliding detector as a
  filterbank); mel (unchanged); the source–filter model (`signal_
  processing/` Ideas gains its first on-screen statement); the Euler
  strand gains its second customer (the theorem for every kernel and N);
  the FFT row gains its second reason (FFT convolution for long impulse
  responses).

### Open at design approval — both settled 2026-09-24 as recommended

1. **Scene 3's when-useful line on convolutional layers** — keep it
   there (it is the natural home for "libraries correlate and call it
   convolution") or move all conv-layer material to scene 7.
2. **Scene 6 carries two pointers** (the D hook and source–filter);
   if it runs long at draft, source–filter moves wholly to scene 7.
