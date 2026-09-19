# Plan 019: `signal_processing/` — the spectrum, a bank of listeners

The maintainer's ask (2026-09-19): expand toward the questions he is
working through in speech — convolution, the Fourier transform, the
short-time Fourier transform, spectrograms, mel spectrograms. The road
approved that day has four series on its main line, in dependency order,
and one side branch:

| # | Series | Lands | Status |
| --- | --- | --- | --- |
| B | The spectrum (this plan) | The DFT as projection onto probe sinusoids; bins as a filterbank; the dB magnitude spectrum; sampling as the opener, aliasing as the closer | plan 019 |
| C | Convolution | The sliding weighted sum as filtering; the convolution theorem | not planned |
| D | Windowing → STFT → spectrogram | Leakage as the convolution theorem at work (why C precedes D); framing and hop; the time–frequency tradeoff | not planned |
| E | Mel | The mel filterbank regroups B's bins — a matrix of triangles; log-mel, what a speech model reads | not planned |
| — | The FFT (side branch) | The same numbers in N log N — the divide-and-conquer row `algorithms/` promised in plan 013 | parked until that row is wanted |

A proposed opener "from air to array" was dissolved into this series:
the sample rate opens it (bin spacing sr/N means nothing without sr),
aliasing closes it, decibels land in its magnitude beat, and quantization
noise goes to Ideas.

Home: a new topic, `signal_processing/`, module `spectrum_manim.py`,
seven scenes. Branch `feat/signal-processing-spectrum`, cut from `main`
at 9277a9c (PR #20 merged, clean, level with origin). First series under
the review budget (ADR 009).

## Constraints fixed before research

1. **The repo has built no sine, no inner product, no complex number.**
   Levels 1–2 use only owned devices (plan 011's rule), so the probes are
   real sine-and-cosine pairs — two multiply-and-sum measurements per
   frequency, magnitude the hypotenuse — and "lining up" grounds backward
   in the weighted sum of `TheBalancePoint`. The complex form is a
   promised pointer to Euler's formula (`calculus/` Ideas), never a
   device this series leans on.
2. **The foundation gets at most two of the seven scenes.** The generic
   Fourier visual exists elsewhere and is good; what justifies this
   series is the speech angle — the bins as a bank of listeners —
   and that owns the middle of the series. It is also the thread series E
   picks up.
3. **Tones are bin-centred throughout.** Leakage is series D's subject;
   at most one honest pointer in a when-useful beat.
4. **Decibels land in the magnitude-spectrum beat**, grounded backward in
   `algebra/`'s logarithm series — delivering the dB strand of that
   topic's "log scales in the wild" Idea.
5. **Second study-guide objective, approved 2026-09-19:** "from air to
   log-mel". This series' primitive is its first chapter; series C–E
   author theirs toward it (ADR 008). Guide structure is designed in
   phase 0 alongside the scenes.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier); scene design; guide-objective structure | Scene design written into the plan; maintainer approves |
| 1 | Topic dir `signal_processing/`, README skeleton (Scope incl. not-covered, the road table), first scene in full | `make check` |
| 2 | Seven scenes at draft; layout linter clean; frames verified by eye, inside transition windows too | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, Ideas; wiki node + edges + promises (Euler, FFT/divide-and-conquer, convolution, leakage); ADR-008 step: `primitives/spectrum.tex`, `answers/spectrum.py`, `019.*` anchors, solve gate; the new guide objective's directory, manifest and INDEX row; `welcome.gif` at seventeen series; root README topic row | `make test` |
| 4 | `connection-auditor` → findings applied and committed → self-check against CLAUDE.md → one local CodeRabbit pass | Review clean |
| 5 | PR; the bot's one automatic review; fixes in one push; one re-review only if a finding required a change; finalise after the bot round closes | `clean-drafts` + 1080p render; bot reviews spent (≤ 2) recorded here |

## Checklist

- [x] Phase 0: pedagogy report + verifier report (anchors A–P) + verifier
  addendum (anchors Q–Z, the exact on-screen objects) pinned below as
  digests; design written (seven scenes; decisions D1–D12); design
  approved by the maintainer 2026-09-19 — the approval took both open
  calls as recommended: the trumpet beat stays, credited to the Freesound
  page under its current CC BY 4.0 with librosa's converted copy noted in
  the README; "detector" in this series, "filterbank" earned in series D
- [x] Phase 1: topic dir `signal_processing/`; module with the shared
  helpers (`_probe`, `_Stems`, `_number_strip`, `_swap_caption`) and
  `PressureIntoNumbers` built in full (57 s at draft; linter clean; frames
  verified on a contact sheet — the mix strip's three negative numbers ran
  together at 0.95 spacing, so the sample pitch went to 1.0 and the mix
  strip to size 18); README with Scope (six exclusions), the road table,
  row 1, one reference; `references.bib` regenerated (the sync test reds
  on any new README reference — run `tools/sync_references.py`);
  `make check` green — but its hooks only see tracked files: the new
  README's over-long reference title was caught by the commit hook, not
  the gate (reference link lines stay ≤ 80 columns, full names in the
  description)
- [x] Phase 2: seven scenes at draft (7 files, distinct names; 57, 72,
  49, 51, 55, 66, 78 s). Shared devices: `_Stems` (lollipops), `_Bank`
  (five rows — probe-pair thumbnails, Σ node, bar; the end rows drawn with
  one probe), `_uprights` (bar charts), `_reading` (plus-signed pair and
  distance). Linter clean on all seven; what it caught on the way: the
  match note and the pair label at the frame edge, the pair plane's axis
  tags and point labels crossed by its circle (tags became a legend under
  the plane, labels hang outward from their points), Σ glyphs touching
  their node circles, the probe table's key under the caption line, the
  dB tag on the "0 dB" label. What only eyes caught, on contact sheets:
  number strips running together (−0.71 −1 −0.71) — pitch widened, strips
  to size 18; the row labels touching the probe thumbnails; two ladder
  headers reading as one line; dB charts with no labelled floor (−50 dB
  and −20 dB now on screen — a bar's height is a claim). Bugs: FadeIn on
  an `always_redraw` mobject fails (its family is rebuilt every frame —
  add, don't fade); `_Stems` stored `self.scale`, shadowing
  `Mobject.scale`, which broke `FadeIn` on the group itself. Transition
  windows: every in-place replacement goes through `_swap_caption`
  (out, then in); mid-fade frames checked on scenes 4 and 6. The 7000 Hz
  curve verified by eye through all eight 1000 Hz samples. README rows
  2–7 written with this commit (the source-order test reds otherwise);
  `make check` green with the new files staged
- [x] Phase 3: README complete — seven rows at all three levels, 50
  plan-019 references unchecked for the maintainer's pass (link lines
  kept under the 80-column rule, full names in the descriptions; the
  pedagogy pass's third-party repost of Lyons' chapters deliberately not
  linked — the publisher's sample is), Ideas with eight entries. Wiki:
  `spectrum` node; three delivered edges (`random-variables`,
  `logarithms`, `counting-rules`), four promised (convolution, windowing
  → STFT → spectrogram, mel, the inverse), two rows amended rather than
  duplicated (Euler's first waiting customer; the FFT as divide and
  conquer's second example), the grid device's new stop; Ideas amended
  in `algebra/`, `calculus/`, `algorithms/`; `linear_algebra/` logged as
  parked with its on-ramp, no promised row (nothing on screen names it).
  **Prose checked against the built scenes** — the wiki pass found four
  planned beats no scene contained: built three (Euler named under the 28
  zeros; convolution on the closing map; the numpy `fft`/`rfft` mirror
  caption), dropped one from the plan (the Gauss/Fourier history credit —
  README only); "the last scene's lesson" read as the final scene and
  became "the previous scene's"; "filter it out" became "remove it" (the
  Scope retires the word); the two-curve caption now says *cosines*, the
  phase that picture actually draws. ADR 008: `primitives/spectrum.tex`
  (seven sections, seven TikZ figures, eight problems),
  `answers/spectrum.py` (exact pairs in Q(√2), every pair cross-checked
  against `np.fft.rfft` with X[k] = aₖ − i·bₖ; verification verified by a
  flipped sign), 39 `019.*` anchors transcribed from anchors A–Z, INDEX
  row + a new Objectives table. **Solve gate 8/8** (fresh-context solver,
  statements plus a vocabulary preamble only; no statement needed
  changing). Second objective built: `study_guides/air-to-log-mel/`
  (18 pp + 5 pp solutions; stations 2–4 drawn dashed; no glue until
  chapter 2); `make study` green, ctc PDFs untouched. Tool fix on the way:
  `check_study_layout.py` crashed on a C0 control character pdftotext
  emits for big delimiters — stripped before XML parsing, reproduced
  first. `welcome.gif` at seventeen series (the second row carries five;
  428 KB); root README row, study-track sentence, and the "what's next"
  paragraph (`linear_algebra/` parked, to be returned to). `make test`
  and `make check` green with everything staged. **For the maintainer:**
  plan 012 R5's on-page "unverified" mark was never implemented — this
  chapter, like the two before it, cites `verified={no}` keys unmarked
- [x] Phase 4: `connection-auditor` run on 94c3c10 (incremental; zero
  numeric discrepancies). **Top finding built:** scene 4 said "reading of
  (A + B) = reading of A + reading of B" — false where "reading" is the
  distance (the series' own 12 and 16 make 20, not 28); linearity belongs
  to each probe's sum, and the scene now says so ("the pair adds, sum by
  sum — the distance is taken last"). **Second, built in part:** D8's
  "never a spectrum without its waveform" held in scene 3 only — the
  leakage chart now stands beside its 8 samples ("one and a half laps in
  the window — not a whole number"); scene 6's charts have no room, so the
  claim was narrowed in the README and D8, not built. Wording applied:
  rows 59 and 88 trued, row 101's pH strand, a promised row for the
  log-scales essay, three device bullets (the sampled rotation; stems,
  never staircases; the linear-then-log replot shared with
  `TheRoadsOwnWalk`), the far-end scenes named in the topic Scope with
  matching cells in `probability/` and `combinatorics/`, "appears once" →
  twice (the trumpet is a second off-row tone), the guide's "two curves" →
  "two cosines", scene 7 quoting scene 1 accurately; design section trued
  to the build; stamp advanced to 94c3c10. Not made, logged: spectrum ↔
  CTC (the STFT hop is the honest joint; Whisper is not a CTC model),
  orthogonality as disjointness, the shadow as sin′ = cos. Self-check
  against CLAUDE.md: no raw colours, no `palette()` (the rows are ranked),
  every in-place replacement out-then-in, every bar chart's floor
  labelled; one over-budget caption trimmed. Drafts re-rendered (7 files),
  linter clean. **The one local CodeRabbit pass**
  (`coderabbit review --agent --base main`, on 99c1304, 27 files): one
  finding, minor, valid — `TheBankOfDetectors`' feed loop tested `signal`
  after assigning it, so the second pass faded the "the 8 samples" tag in
  again while it was already on screen; the loop now enumerates, and the
  tag and fan-out arrive once. Verified by re-render (49 s, a
  second-iteration frame checked). Not rerun: the change is the finding's
  own fix, and the bot reviews it on the PR
- [ ] Phase 5 — bot reviews spent: _ of 2

## Research digests

### Pedagogy report (digest — `pedagogy-researcher`, 2026-09-19)

The agent had no code tool; its numbers are hand arithmetic and every one
goes through the verifier before it reaches a screen.

**Headline.** N = 8 at sr = 8000 Hz for every scene that shows arithmetic
(bin spacing 1000 Hz, Nyquist 4000 Hz — Lyons' canonical example, and
Jurafsky & Martin's telephone-speech rate). Every probe value is in
{0, ±√2/2, ±1}; k = 2 gives all-integer probes; every sum the series needs
is an exact 0, 4 or 8. N = 12 drags √3 into the cross products and 12 kHz
is nobody's rate; N = 16 has no exact values. N = 16 and N = 400 appear
only as bank *shapes*, without arithmetic.

**Camp choices.** (a) Real sin/cos pair, not complex exponentials — this
is Steven W. Smith's ch. 8 "real DFT" in full, a respectable primary
formulation, and Lyons' worked example is real in practice. (b)
Analysis-first (detectors), not synthesis-first ("signals are sums of
sines") — the filterbank differentiator needs it; synthesis shrinks to a
bookkeeping beat (8 numbers in, 8 out) plus a promise. (c) Sine from the
circle — one object then gives the (shadow, height) pair, phase, and the
wagon-wheel picture of aliasing. (d) Aliasing last works because the fold
can be re-derived from the probes (c₇ = c₁); scene 1 plants "two samples
per cycle" for scene 7 to cash.

**The two-scene foundation holds** because sampling and the rotating
point are *one* picture (the 8 stops on the circle are the samples), and
because everything that would overload scene 2 — orthogonality in full,
the N/2, the bookkeeping — is a property of the bank and belongs in the
middle anyway.

**Recommended arc.** 1 `PressureIntoNumbers` (L1, foundation) · 2
`TheProbe` — one detector is a pair (L1→2, foundation) · 3
`TheBankOfDetectors` (L1 of the bank claim) · 4 `NoDoubleCounting` (L2) ·
5 `WhatSetsTheSpacing` (L2→3) · 6 `TheSpectrumInDecibels` (all three
levels for dB) · 7 `TheFoldAtNyquist` (L3, limits and closer).

**Devices.** Sampled rotation (circle with 8 stops → stems; lollipops,
never a staircase). Product bars with sort-and-stack cancellation (match:
0+½+1+½+0+½+1+½ = 4; mismatch s₁·s₃: four halves against two wholes,
cancelled in WARM — S. Smith Fig. 8-8 rebuilt countable). The raised floor
(s₁² and c₁² are the same values rearranged, sum to 1 at every stop, so
each totals 4 = N/2 — only Pythagoras on the radius). The pair-point on a
circle of radius A·N/2: integer tone 3, 4, −3, −4 reads (12, 16) → 20;
delayed one sample (−16, 12) → still 20; sine-only reads 16, then 12. The
fan-out bank: five rows (0–4 kHz), each a probe pair + Σ node + bar; the
bar column turned on its side *is* the spectrum. The 8×8
probe-against-probe table on the repo's outer-product grid: diagonal
8, 4, 4, 4, 4, 4, 4, 8, all C(8,2) = 28 off-diagonal pairs 0 — "computed,
not proved". Three banks side by side: (8k, 8) and (16k, 16) both 1000 Hz
spacing — sr buys reach; (8k, 16) 500 Hz — duration buys spacing;
Whisper's bank 16000/400 → 25 ms, 40 Hz, 201 rows. Linear vs dB bars
(amplitudes 1, 0.5, 0.01 → 0, −6.02, −40 dB; the 20 is `MultiplyIsAdd`
pulling the square out front; −6.02 = −20 × 0.301). Aliasing trio:
backward-stepping point, two curves through 8 dots, the folded ruler
(5→3, 6→2, 7→1 kHz).

**Flagship signal.** Lyons' Example 1: sin(2π·1000·n/8000) +
0.5·sin(2π·2000·n/8000 + 3π/4); rows read 4 and 2.

**Misconceptions to design against.** A bin is a detector's reading at a
fixed address, not "the frequency in the signal" (rows on screen before
any signal). Higher sr does not buy finer resolution. No staircases. One
probe per frequency is not enough. 0 dB is "equal to the reference", not
silence (silence is −∞); dB always carries its reference on screen.
Exactly sr/2 is not captured (s₄ is all zeros) — say "below sr/2". An
aliased tone is a clean lower tone, not noise. Never a spectrum without
its waveform (concept-inventory evidence: < 28 % link time and frequency
plots).

**Pitfalls.** Say **"detector", not "filter"**, and never "narrow": one
frame yields one number per row; a filter's output is a signal, which only
happens when the frame slides (series D earns the word), and at N = 8 each
row's main lobe is 2 kHz wide — what is true is that each detector is
exactly deaf at the *other detectors'* frequencies, and only there.
Normalisation: reading ÷ 4 on rows 1–3 but ÷ 8 on rows 0 and 4 — keep
flagship tones off the end rows, state the exception once. N/2 + 1 rows,
N numbers (1 + 2·3 + 1). Sign convention: on-screen sin-sum is
plus-signed; numpy's imaginary part is its negative — README note. An
aliased *sine* flips sign — show it, don't pick the phase that hides it.
Orthogonality and phase-invariance are **demonstrated at N = 8, not
proved for all N**; the all-N reason is a promise to Euler — caption
honestly. The weighted-sum grounding must state its differences from
expectation (weights can be negative and sum to 0). "The DFT assumes
periodicity" is publicly disputed among experts — keep the word "assumes"
off screen. Weber–Fechner approximate only. The between-bins teaser (1.5
kHz: every row answers) is phase-dependent — pin the phase.

**Sources** (31, full list carried to the README References in phase 3):
S. W. Smith ch. 8 (five sections); Lyons ch. 2–3 + DSPRelated blog 2013;
J. O. Smith MDFT (four sections) and SASP (two); Jurafsky & Martin SLP3
draft ch. 15–16; Sanderson 2018; Schaedler; Swanson; Azad; Weber 2005;
Wage, Buck, Welch & Wright 2002; Montgomery 2012–13; Chaudhari 2020;
comp.dsp 2011; MIT OCW 6.341 L21; openai/whisper `audio.py`; Wikipedia
"Aliasing". Flagged unverified by the agent: Lyons edition ↔ section
mapping; O&S 3rd-ed. section titles; the log-scales constants (pH, Pogson,
semitones).

### Verifier report (digest — `source-verifier`, 2026-09-19; anchors A–P)

Two routes per number: exact (sympy, minimal-polynomial tests) and numeric
(numpy against `np.fft`). Nothing in either repo was modified.

**Corrections to the brief — each one binds the design.**

1. *The end rows have no sine partner.* At k = 0 and k = N/2 the sine probe
   is identically zero: Σ sin·sin = 0 there, a pure sine at row N/2 samples
   to silence, and the end rows' magnitude *does* depend on phase
   (A·N·|cos φ|). "The reading ignores the starting angle" holds only for
   0 < k < N/2.
2. *Orthogonality as tabled holds for 0 ≤ k, m ≤ N/2.* Over all k, m:
   Σcos·cos = (N/2)·{δ(k−m) + δ(k+m)}, Σsin·sin = (N/2)·{δ(k−m) − δ(k+m)}
   (mod N). At N = 8, probes 3 and 5: cos·cos = +4, sin·sin = −4 — the
   fold of scene 7 already present inside scene 4's identity.
3. *Gauss c. 1805 is not the DFT's first appearance.* Heideman, Johnson &
   Burrus: Clairaut 1754 has the earliest formula (cosine-only); Gauss has
   "the earliest explicit formula for the general DFT" and an FFT-like
   algorithm, written c. Oct–Nov 1805, published posthumously 1866. No
   Lagrange year on screen (HJB is internally inconsistent).
4. *Nyquist 1928 is not a source for the sampling theorem* (Lüke 1999);
   Shannon 1949 p. 12 named the "Nyquist interval" in his honour, and
   footnotes **J. M.** Whittaker 1935, not E. T. Whittaker 1915 (the
   mathematical origin). Credit line, every part verified: "Sampling
   theorem — E. T. Whittaker 1915 · Kotelnikov 1933 · Shannon 1949".
5. *"Nyquist frequency" is a terminology clash* (Oppenheim & Schafer use
   it for the signal's band limit, not sr/2). On screen: "half the sample
   rate (sr/2)". And the condition is strict: **below** sr/2.
6. *Martin 1929 defines the decibel by power ratio only*; the 20·log₁₀
   amplitude form is derived (power ∝ amplitude²) — J. O. Smith MDFT
   "Decibels", NIST SP 811 §8.7.
7. *Whisper: paper and code differ.* Paper §2.2: 16 kHz, "80-channel
   log-magnitude Mel spectrogram", 25 ms windows, 10 ms stride. Code:
   power (`abs()**2`), log₁₀ (not dB), clamp to max − 8.0, (x + 4)/4.
   128 mel bins is large-v3's model card, not the 2022 paper.
8. *A bin as a filter*: the impulse response is the *time-reversed* probe,
   and the clean statement is about the pair jointly — each real filter
   alone oscillates on a steady tone; the hypotenuse is steady.
9. *16-bit*: 20·log₁₀(2¹⁶) = 96.33 dB is range-to-one-step; 98.09 dB is
   full-scale-sine SNR. The Ideas note uses the first, labelled.

**Anchors.** A — DFT definition; real form X[k] = aₖ − i·bₖ, |X| =
hypot(aₖ, bₖ) (J. O. Smith MDFT "The DFT"; O&S 3rd ed. §8.5 eq. 8.67);
Smith: "the DFT is proportional to the set of coefficients of projection
onto the sinusoidal basis set". B — a bin-centred tone reads A·N/2 on
interior rows at every phase (N = 8: interior always 4; ends 8, 6.9282,
5.6569, 0 at 0°, 30°, 45°, 90°). C — orthogonality, all 3·N² sums exact
for N = 8, 12, 16; N = 8 diagonals cos·cos [8, 4, 4, 4, 8], sin·sin
[0, 4, 4, 4, 0]. D — spacing sr/N, N/2 + 1 rows (5, 7, 9, 201 for N = 8,
12, 16, 400). E — probe tables (N = 8: only 0, ±√2/2, ±1; k = 2 integer).
F — single tones at bin 2 with pointwise product rows (sin → (0, 4); cos →
(4, 0); 45° → (2√2, 2√2); all other rows exactly (0, 0)). G — mixture
1.0·bin 1 + 0.5·bin 3 → |X| = [0, 4, 0, 2, 0], ratio −6.0206 dB. H —
aliasing: cos(N−k) = cos(k), sin(N−k) = −sin(k) sample for sample; 5 kHz
at sr 8 kHz → 3 kHz (`|rfft|` = [0, 0, 0, 4, 0]); 10 kHz at 16 kHz → 6
kHz; Shannon Theorem 1 verbatim (p. 11). I — dB: 20·log₁₀2 = 6.0206,
10·log₁₀2 = 3.0103, ×10 amplitude = 20 exactly; Martin 1929 verbatim. J —
96.33. K — the bin as an FIR filter snapshot at n = N−1 (Smith MDFT
"Frequencies in the Cracks" + footnote; SASP "DFT Filter Bank": "taking a
snapshot of all filter-bank channels at time N−1 yields the DFT"); bin
response peak N at k·sr/N, **exact zeros at every other bin centre**,
nonzero between (N = 8, bin 2: −3.87 dB at 1.5 and 2.5, −12.96 dB at 3.5).
L — Whisper: 400 samples = 25 ms, hop 160 = 10 ms, 40 Hz spacing, 201
rows to 8000 Hz, 3000 frames per 30 s. M — the maintainer's trumpet
(librosa `trumpet`, Mihai Sorohan, Freesound 77711, **CC-BY 3.0 —
attribution required**; sr 22 050; first 4096 samples, Hann, 2049 rows
5.3833 Hz apart): harmonics at 624.46, 1248.93, 1873.39, 2497.85, 3122.31
Hz reading −1.56, 0.00, −3.23, −7.21, −11.98 dB re the strongest — the
second harmonic beats the fundamental; pitch D♯5/E♭5. Not bin-centred:
the window shapes these levels. N — Fourier: memoir read 21 Dec 1807,
*Théorie analytique de la chaleur* 1822. O — Gauss per item 3. P — Cooley
& Tukey 1965 (citation only).

**Flags.** MDFT/SASP section *numbers* are inferred — cite by section
title + URL. The real-form anchors (aₖ/bₖ, A·N/2, the sin/cos table) are
corollaries verified by exact computation, not verbatim in any opened
text. Not opened (citation metadata only): Nyquist 1928, Kotelnikov 1933,
both Whittakers, Allen & Rabiner 1977, Cooley & Tukey 1965, Gauss, Clairaut,
Fourier's originals, IEC 60027-3. Whisper constants read from `main`
today, no commit pinned.

**Outside the repo, for the maintainer:** the verifier found that
`unit-1.py` plots linear amplitude under a "dB" label (its spectrum
panel), so the figure he has seen is not the course's dB plot — reported
to him, not acted on. One unintended side effect: librosa cached a small
licence text under `~/.cache/librosa/`.

### Verifier addendum

Digest — `source-verifier` resumed, 2026-09-19; anchors Q–Z, the exact
on-screen objects of the design below. Exact route: stdlib `Fraction`
arithmetic in Q(ζ₁₆); numeric route: numpy.

- **Q — the 3-4-5 tone.** [3, 4, −3, −4, 3, 4, −3, −4] = 3c₂ + 4s₂ is a
  2 kHz tone of amplitude exactly 5 (max |sample| = 4). Pairs at delays 0,
  1, 2, 3: (12, 16), (−16, 12), (−12, −16), (16, −12) — hypotenuse 20
  every time, a quarter-turn per sample; all other rows (0, 0). Sine-only
  readings 16, 12, −16, −12. Computation only.
- **R — Lyons' Example 1.** Samples 0.3536, 0.3536, 0.6464, 1.0607,
  0.3536, −1.0607, −1.3536, −0.3536 (exact forms in √2/4). Plus-signed
  pairs: row 1 (0, 4) → 4; row 2 (**+1.4142, −1.4142**) → 2; rows 0, 3, 4
  exactly 0. numpy's X(2) = 1.414 + j1.414: our b is the negative of its
  imaginary part. Lyons 3rd ed. is **© 2011** (ISBN 978-0-13-702741-5);
  §2.1, §3.1, §3.4, §3.5, §3.8 confirmed from the publisher's contents
  pages; the example's *printed* numbers, its sub-numbering and eq. (2-5)
  NOT verified — the README says the signal is Lyons', the numbers are
  computed.
- **S — three-tone mix.** Magnitudes [0, 4, 2, 0.04, 0]; dB re the
  loudest 0, −6.02, −40 exactly, by the amplitude and the power route
  alike. The repo's owned number is **0.301** (`logarithms_manim.py` l.
  259, README row 3): caption "−6.02 = −20 × 0.301", never 0.30103.
- **T — the between-rows teaser.** 1500 Hz sine-phase: magnitudes 1.4966,
  2.8478, 2.4142, 0.8478, 0.6682 on rows 0–4 (dB re loudest −5.59, 0,
  −1.43, −10.52, −12.59); Parseval 4 = 4 exact. Every sin-sum is exactly 0
  (the tone is even about n = 0) — a *sine*-phase tone registering wholly
  in the cos-sums. Cosine-phase alternative: every cos-sum exactly 1,
  magnitudes 1, 2.3980, 2.7979, 1.1921, 1.
- **U — tables.** Scene 4's Gram matrix over c₀, c₁, s₁, c₂, s₂, c₃, s₃,
  c₄: diagonal [8, 4, 4, 4, 4, 4, 4, 8], all 28 off-diagonal pairs exactly
  0, rank 8. Extended to k, m = 0..7: cos·cos has +4 at (1,7), (2,6),
  (3,5); sin·sin has −4 there; (0,0) and (4,4) are 8 and 0.
- **V — the raised floor.** s₁² = 0, ½, 1, ½… and c₁² = 1, ½, 0, ½…; sum 1
  at every stop, 4 each; same for k = 2 (0, 1, 0, 1… / 1, 0, 1, 0…) and
  k = 3.
- **W — the fold.** 5000 → 3000, 6000 → 2000, 7000 → 1000 Hz with reading
  4, cosine identical, sine negated. **Beyond that the pattern changes:**
  8000 → row 0 and 12000 → row 4 with reading 8 (sines vanish); 9000 and
  10000 land on rows 1 and 2 with the sine *not* flipped. Stepping ⅞ lap
  and stepping ⅛ lap backwards give the identical angle list 0, 315, 270,
  225, 180, 135, 90, 45.
- **X — three banks** as designed (1 ms/1000 Hz/5 rows; 1 ms/1000 Hz/9
  rows; 2 ms/500 Hz/9 rows).
- **Y — log scales.** pH is −log₁₀ of hydrogen-ion *activity* (Sørensen's
  1909 original was concentration; IUPAC sources NOT opened). Stellar
  magnitude: Pogson 1856 (opened) adopts 2.512 so that a constant "is
  exactly 5" — 5 magnitudes = ×100 is the exact modern reading, implicit
  not verbatim (2.512⁵ = 100.02). Semitones 12·log₂; a 3:2 fifth =
  7.0196. Fechner 1860 / Stevens 1957 not opened — caption stays at
  "approximate motivation", consistent with `algebra/README.md`'s Scope.
- **Z — Whisper's floor.** Pinned to `openai/whisper` 8609812 (2026-08-31),
  `audio.py` ll. 147–157. "Keeps 8 decades of power below its loudest
  value — 80 dB" is accurate (8 log₁₀-power units, not 160 dB); the
  loudest value is over the whole 30 s input, and an absolute clamp at
  10⁻¹⁰ applies first.
- **Trumpet (anchor M restated).** 624.46, 1248.93, 1873.39, 2497.85,
  3122.31 Hz at −1.56, 0.00, −3.23, −7.21, −11.98 dB. Licence discrepancy:
  librosa's metadata says CC BY 3.0, Freesound's page today says CC BY
  4.0; librosa's copy is converted (44.1 kHz stereo WAV → 22 050 Hz mono
  OGG). Full attribution strings for both are in the verifier's output.

**Amendments to the design from the addendum** (applied to the table
below where it is a wording change, listed here where it is a constraint):
scene 7's folded ruler shows **5 → 3, 6 → 2, 7 → 1 only** — past 8 kHz the
sine no longer flips and the end stops read 8, so the simple "cosine same,
sine negated" caption would be false there; scene 5's teaser shows **one
magnitude bar per row**, captioned with its phase ("a 1.5 kHz sine
starting at 0"), never the pairs; scene 6's caption uses 0.301; the
README's sign-convention note covers row 2's (+1.41, −1.41) against
numpy's 1.414 + j1.414.

## Scene design

Built from the two reports above. Grid for all arithmetic: **N = 8
samples at sr = 8000 Hz** — 1 ms of sound, rows at 0, 1, 2, 3, 4 kHz.

### Decisions

- **D1 — "detector", not "filter"; never "narrow".** One frame gives one
  number per row. What is true and on screen: each detector is exactly
  deaf at the *other detectors'* frequencies (anchor K), and only there.
  The word "filterbank" appears once, in a when-useful beat, as what the
  bank becomes when the frame slides (series D earns it).
- **D2 — real pairs, plus-signed.** Each interior row is a (shadow,
  height) = (cos-sum, sin-sum) pair; the bar is the hypotenuse. numpy's
  imaginary part is the negative of our sin-sum — a README note, not a
  screen beat.
- **D3 — the end rows are honest.** Rows 0 and 4 have no sine partner
  (s₀, s₄ are all zeros — not drawn), read ÷ 8 rather than ÷ 4, and do
  depend on phase. Flagship tones stay on rows 1–3; the exception is
  stated once, in scene 4, and cashed in scene 7 ("a sine at exactly sr/2
  samples to silence — *below* sr/2").
- **D4 — demonstrated, not proved.** Orthogonality is an exhaustive check
  at N = 8 ("computed, not proved"); phase-invariance is shown at the
  phases the grid offers ("true for every starting angle — shown here for
  four"). The all-N reason is a promised pointer to Euler's formula.
- **D5 — the weighted sum is re-grounded with its differences stated**:
  `TheBalancePoint`'s Σ x·w, but these weights can be negative and sum
  to 0 — they are a pattern to match, not a probability.
- **D6 — flagship signal: Lyons' Example 1** (1 kHz sine + half-size
  2 kHz tone started at 135°): rows read 4 and 2, citable, and row 2's
  pair (1.41, −1.41) cashes scene 2's lesson inside the bank. Scene 6
  adds a whisper-quiet third tone (amplitude 0.01 at 3 kHz).
- **D7 — stems, never staircases;** a continuous curve through samples
  is a claim, drawn only for the source tone (scene 1) and the two
  aliases (scene 7).
- **D8 — the bank scenes keep the waveform beside their readings:** the
  8-stem strip sits beside the bank in scene 3 and beside the leakage
  chart in scene 5. Scene 6's charts stand without it (no room) — so
  "never a spectrum without its waveform" is narrowed to the bank
  scenes, not built (trued after the phase-4 audit).
- **D9 — dB always carries its reference on screen** ("re: the loudest
  row"). One definition (10·log₁₀ of a power ratio, Martin 1929); the 20
  is `MultiplyIsAdd` pulling the square out front. Silence is −∞
  (`ShrinkCounts`' log 0), which is why real systems put in a floor.
- **D10 — sampling-theorem wording and credit** per verifier items 4–5:
  "half the sample rate (sr/2)", strict "below"; credit line Whittaker
  1915 · Kotelnikov 1933 · Shannon 1949. The Gauss c. 1805 / Fourier 1822
  history stays in the README's References — no screen beat was built
  for it (trued in phase 3).
- **D11 — the trumpet is scene 6's when-useful beat**, as five bars from
  anchor M's numbers (no audio dependency at render time): "a real
  trumpet note — 2049 detectors 5.4 Hz apart", second harmonic the
  loudest, with the honest pointer that a real note is not bin-centred
  and a window shaped these levels (series D). On-screen credit and README
  attribution for the CC-BY recording. *Open for the maintainer — see
  below.*
- **D12 — colour.** COOL the signal's stems; MUTED the probes and the
  empty bank; WARM cancelled product tiles and the aliased impostor;
  ACCENT the reading being built (the hypotenuse, the lit row, the
  spectrum); GOOD the confirmed match. The five rows are *ranked* (by
  frequency), so they are not `palette(i)`.

### Scenes

| # | Scene | Level | What is on screen |
| --- | --- | --- | --- |
| 1 | `PressureIntoNumbers` | 1 · foundation | A pure tone as a point going round a circle; the microphone reads its height. Sample 8 times in 1 ms: the 8 stops at 45° steps become 8 stems, then a strip of 8 numbers (sr = 8000 per second, so 8 samples last 8/8000 = 1 ms). The shadow (horizontal) is the same motion a quarter-turn ahead — two readings of one point. Planted for scene 7, as built: "8 samples per lap here; a faster tone gets fewer — and needs at least two". Closing question: which tones are hiding in these 8 numbers? |
| 2 | `TheProbe` | 1 → 2 · foundation | Probe k is a point doing k laps per window; k = 2 has integer values (0, 1, 0, −1… and 1, 0, −1, 0…). Multiply-and-sum is the owned weighted sum with signed weights (D5). Match: s₂ on s₂ → 0, 1, 0, 1, 0, 1, 0, 1 = 4 — squares cannot cancel. Mismatch: s₁ on s₃ → four halves up, two wholes down, cancelled in WARM = 0. Then the sine probe alone is fooled: the tone 3, 4, −3, −4… reads 16; delayed one sample, 12. Add the shadow probe: (12, 16), hypotenuse 20; delayed (−16, 12), still 20 — the pair-point walks a circle, its distance never changes; amplitude 20 ÷ 4 = 5, a peak the samples never touch. |
| 3 | `TheBankOfDetectors` | 1 (the bank) | The 8-stem strip fans out to five rows — 0, 1, 2, 3, 4 kHz — each a probe pair, a Σ node, an output bar; the rows stand labelled *before* any signal arrives (a row is an address, not a discovery). Pure tones one at a time: exactly one row lights. Lyons' mix: row 1's pair (0, 4) reads 4, row 2's pair (1.41, −1.41) reads 2 — the bar is the hypotenuse, scene 2's lesson inside the bank → amplitudes 1 and 0.5. The bar column turns on its side: that is the spectrum — no new object, a column of weighted sums. |
| 4 | `NoDoubleCounting` | 2 | Why the mix split cleanly. (i) Linearity, as built — of each probe's *sum*, not of the reading: "a probe's sum on (tone A + tone B)" / "= its sum on A + its sum on B" — `SameOutcomesAdd`'s move ("a weighted sum of a sum is the sum of the weighted sums — owned since dice") — then the guard "the pair adds, sum by sum — the distance is taken last (12 and 16 made 20)" and "so it is enough to ask: what does each probe sum to on every other probe?". (ii) The 8 × 8 probe-against-probe table (a bare table of numbers — the counting grid's descendant, drawn, not named on screen): diagonal 8, 4, 4, 4, 4, 4, 4, 8 lit, all C(8, 2) = 28 off-diagonal cells 0 — computed, not proved (D4). Why 4: height² + shadow² = 1 at every stop (the radius), 8 stops give 8, and sine and cosine take the same values in a different order — 4 each. Why 8 at the ends: no sine partner, the cosine keeps it all (D3). Bookkeeping: 1 + 2·3 + 1 = 8 readings from 8 samples — nothing lost; "the readings rebuild the samples" is a promise. |
| 5 | `WhatSetsTheSpacing` | 2 → 3 | Probe k fits k laps in a window lasting N/sr seconds, so row k listens at k·sr/N: spacing = sr/N = 1 ÷ duration. Three banks side by side: (8 kHz, 8) and (16 kHz, 16) — both 1000 Hz apart, the faster rate bought *reach* (to 8 kHz), not finer spacing; (8 kHz, 16) — 500 Hz apart, listening longer bought spacing. Whisper's bank: 16 000 Hz, 400 samples → 25 ms, 40 Hz apart, 201 rows to 8000 Hz. When-useful: slide the frame and each detector's output becomes a signal — a filterbank (series D); a 1.5 kHz sine starting at 0 — its 8 samples drawn as stems to the left of the chart, tagged "the 8 samples", under the beat's first caption "a 1500 Hz sine: one and a half laps in the window — not a whole number" — sits between rows and every row answers — bars 1.50, 2.85, 2.41, 0.85, 0.67, one magnitude per row, phase named in the caption — leakage, the one computed teaser (series D); a mel filterbank regroups these 201 rows into 80 (series E). |
| 6 | `TheSpectrumInDecibels` | 1 · 2 · 3 for dB | The flagship mix gains a third tone at amplitude 0.01: readings 4, 2, 0.04 — on linear bars the third is invisible. dB re the loudest row: 0, −6.02, −40. One definition — 10·log₁₀ of a power ratio; power goes as amplitude², and `MultiplyIsAdd` pulls the 2 out front: 20·log₁₀ of an amplitude ratio; −6.02 = −20 × 0.301, the repo's own log₁₀ 2. Empty rows: log 0 = −∞, so real systems choose a floor — Whisper keeps 8 decades of power below its loudest value, 80 dB. When-useful: the trumpet (D11), second harmonic 0 dB, fundamental −1.56, then −3.23, −7.21, −11.98; and the log-scales table — dB, pH, stellar magnitude, semitones, each a constant × a log of a ratio, a ruler with its own stride; Weber–Fechner named as approximate. |
| 7 | `TheFoldAtNyquist` | 3 · limits, closer | Why the bank stops at row 4. At the 8 stops probe 7 *is* probe 1 — c₇ = c₁, s₇ = −s₁ — likewise 6 ↔ 2, 5 ↔ 3; scene 4's table extended past row 4 lights cells it called zero (probes 3 and 5: +4 and −4). Three short pictures: the point stepping ⅞ lap per sample is the point stepping ⅛ lap backwards (the wagon wheel — and why the sine flips sign, shown not hidden); two cosines through the same 8 dots, 7 kHz in WARM over 1 kHz; the frequency ruler folded at 4 kHz — 5 → 3, 6 → 2, 7 → 1. Scene 1's planted line cashed, quoted as built: "the first scene said at least two per lap — strictly, more than two: below sr ÷ 2" (row 4's sine is silence). The aliased tone is a clean lower tone, not noise — so it must be removed *before* sampling. In practice: 8 kHz telephone, 16 kHz speech models; "in numpy, the upper half of fft's output is this mirror — rfft returns the bank". Credit line (D10). Closing map, six lines — two GOOD (built), four MUTED (ahead): which tones → the bank · quiet beside loud → dB · echoes and smoothing → convolution · between rows → windowing · changing over time → the STFT · the ear's grouping → mel. |

Foundation: scenes 1–2. The bank is drawn in scene 3; scenes 5–7 show
its readings as ladders, upright bars and probe strips. Scenes 3–5 are
about nothing else.

### What the series opens and closes (wiki, phase 3)

- New node `spectrum`. **Delivered edges from:** `random-variables` (the
  weighted sum and its linearity, re-used with signed weights),
  `logarithms` (dB is `MultiplyIsAdd` and `ShrinkCounts` at work — the dB
  strand of `algebra/`'s log-scales Idea delivered; the essay itself stays
  in Ideas, narrowed), `counting-rules` (the outer-product grid; C(8, 2)).
- **Promised, each with a home-queue entry:** the complex form and the
  all-N orthogonality reason → Euler's formula (`calculus/` Ideas, already
  queued — gains its first customer); convolution, windowing → STFT →
  spectrogram, mel (the road's series C–E, `signal_processing/` Ideas);
  the inverse ("the readings rebuild the samples"); the FFT → the
  divide-and-conquer row `dynamic-programming` already promises
  (`algorithms/` Ideas gains the FFT as its second example); quantization
  noise and the 96.33 dB range (Ideas only).
- `linear_algebra/`: the projection reading of the bank ("the DFT is
  proportional to the coefficients of projection" — anchor A) is recorded
  as the on-ramp, in Ideas; no promise opened by this series.

### The second study-guide objective (approved 2026-09-19)

`study_guides/air-to-log-mel/` — objective: read a log-mel spectrogram
with understanding. Four chapters, one per main-line series; this plan
builds the directory, manifest, `guide.tex`/`solutions.tex` and chapter 1
(`primitives/spectrum.tex`, `answers/spectrum.py`, `019.*` anchors); the
guide compiles with one chapter and grows by one per series, glue authored
from the wiki edges each series lands. No guide-first chapters planned.
Problems (six to eight, solve-gated) sized to double as diagnostics:
compute a row's pair and reading from 8 samples; say which row fires and
why the others read 0; spacing, row count and reach from sr and N; convert
reading ratios to dB and back; where a tone above sr/2 lands; spot the
claim that is false (a staircase, "higher sr → finer spacing", "0 dB is
silence").

### Open at design approval — both settled 2026-09-19 as recommended

1. **The trumpet beat (D11)** — include it (recommended: it is the plot he
   has worked with, and it makes scene 6's when-useful concrete), accepting
   a CC-BY on-screen credit and a forward lean on windowing in a level-3
   beat; or drop it and close scene 6 on the log-scales table alone. If
   included: which licence version the credit cites — librosa's metadata
   says CC BY 3.0, Freesound's page today says CC BY 4.0 (recommended:
   credit the Freesound page with its current 4.0 licence, and note
   librosa's converted copy in the README; the series shows five numbers
   measured from the recording, never the audio).
2. **"Detector" over "filter" (D1)** — a deliberate departure from the
   route's "bins as a filterbank" wording; the theme is unchanged, the
   word waits for series D.
