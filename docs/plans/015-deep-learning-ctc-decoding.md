# Plan 015: `deep_learning/` — CTC decoding, the collapsed-prefix beam

The last guide-first chapter graduates: plan 012's `ctc-decoding`
primitive seeded this series (ADR 008, book-to-screen — the third
and final such graduation), and the wiki's oldest remaining promised
strand — row 42's "beam search over collapsed prefixes" — is
delivered on screen. Home: `deep_learning/`, module
`ctc_decoding_manim.py`, seven scenes. The label-prior-variant
strand of row 42 stays promised (it is loss-side, not decoding).

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier); design | Scene design written into the plan |
| 1 | Module stub in `deep_learning/`, README rows reserved | `make check` |
| 2 | Seven scenes at draft; layout linter clean; frames verified by eye | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, wiki graph + log; ADR-008 step: the ctc-decoding primitive trued to series-backed (the guide-first set empties); anchors for new on-screen numbers; welcome.gif re-render (14 series) | `make test` |
| 4 | Local CodeRabbit + connection-auditor, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p60 render |

## Checklist

- [x] Phase 0: both reports pinned below; design finalized (seven
  scenes; decisions D1–D9). Research ran in the plan-014 session
  (2026-08-12, parallel with the descent series' pass); digests
  pinned verbatim from that session's reports
- [ ] Phase 1
- [ ] Phase 2
- [ ] Phase 3 (branch note: cut from main at 9d0c86a while PR #16
  was open — the shared files this phase touches (wiki INDEX/log,
  study INDEX, welcome, root README) are edited against that state;
  reconcile with plan 014's rows on merge)
- [ ] Phase 4
- [ ] Phase 5

## Decisions (made at design time)

1. Home `deep_learning/`, seven scenes; the guide's ctc-decoding
   chapter is the ADR-008 seed; the primitive graduates to
   series-backed in phase 3 (last guide-first chapter — the set
   empties).
2. Failure-motivated camp ordering (Distill/Scheidl/the chapter) —
   forced: no LM is taught here, killing the implementation-ordered
   camp's motivation; Graves 2006's prefix search is a DIFFERENT
   algorithm and stays off screen (Scope exclusion names it).
3. Numbers: 012.dec anchors + verifier-confirmed E2 (q-band, 1/√2),
   E3 leaderboard (27 paths, A 0.3170, runner-up AB 0.2610, AA/ABA
   exact tie — never strictly ordered), E4 coin overcount (1/8 vs
   3/8), and the verifier's constructed flagship pruning table
   (y₁=y₂=(A .5, B .1, ε .4), y₃=(A .5, B .4, ε .1)) — traces to
   plan 015's pinned digest; adding it to answers/ctc_decoding.py is
   a human-gated follow-up (verifier flag 10), noted not done.
4. Two-ledger visibility rule (picture-is-a-claim): every prefix
   chip shows two stacked bars wherever merging happens; a
   one-number chip appears only in the explicitly-marked one-ledger
   counterexample, WARM.
5. Probability space on screen; one caption states production runs
   the ledgers in log space with the taught log-add (logsumexp,
   never max — max silently reverts to path search).
6. Kept beam totals are never labeled as posteriors (width-1 kept
   0.2150 / width-2 0.2990 vs true 0.3170 in E3; width-2 kept
   exactly 37/100 in the flagship IS the posterior only because no
   A-feeder was pruned — say why when shown).
7. "Width 2 keeps every candidate that carries mass" (flag 1): the
   frame-2 candidate list either shows AA at 0 or not at all.
8. ∅ stays a live candidate on screen and can win (the gradient
   series' bias model decoded empty); init p_b(∅)=1, p_nb(∅)=0
   ("before any frame, all mass ends in blank").
9. Spikes phrasing (flag 6): "the loss never paid for timing, so
   spike positions are not calibrated segment boundaries" — never
   "spikes are far from the sound". Graves eq. 4 reproduced without
   the paper's odd π∈N^t subscript (flag 8).

Off-screen list: a one-ledger prefix chip claiming exactness;
"beam width 1 is just greedy" (false — TF issue #21051); a quoted
O(T·k·V) (derived, not sourced — attribute Hannun 2014 Algorithm
1's loop nest and "A_prev never larger than k"); Scheidl's 0.48/0.52
and the CMU recitation matrices (near-misses of the anchored
numbers); Graves fig. 2 captioned as the beam; merge as max;
per-frame LM multiplication.

## Scene design

**1. `TheInverseProblem`** — training scored a given transcript;
deployment gets a clip and no reference. The road's loop drawn:
waveform → per-frame scores → ??? → words. The honest target
argmax_Y P(Y|X) with P the alignment sum; Graves quoted: "we do not
know of a general, tractable decoding algorithm" — so two
approximations, the cheap one and the honest one, are the series.
Formula last: Y* = argmax_Y P(Y|X).

**2. `TheFrameFavourites`** — best-path decoding on the familiar
matrix: argmax cells highlighted per frame, concatenate, collapse
through B. The three-frame agreement example (y₁=(.5,.2,.3),
y₂=(.4,.3,.3), y₃=(.2,.3,.5)): greedy A,A,ε → "A", and the full
leaderboard confirms A first at 0.3170 with AB second at 0.2610 —
greedy is not always wrong; with one favourite chain clearly ahead,
the max speaks for the sum. Graves's caveat on screen: "trivial to
compute … not guaranteed to find the most probable labelling."
Complexity beat: T lookups and one collapse pass.

**3. `TheModelHeardNothing`** — the anchored construction: T=2,
y(A)=0.4, y(ε)=0.6. Greedy takes the blank twice: "" with 0.36. The
transcript A pools AA + Aε + εA = 0.64 — the pooled-team bar rises
past the single-path bar (the alignment series' sum-vs-max device in
its deployment costume). The verdict: read correctly, the model
heard an A; read greedily, it heard nothing. The dial generalised:
y(ε)=q — greedy goes empty at q > 1/2, the empty transcript truly
wins only at q > 1/√2 ≈ 0.7071 (at q=0.7 still 0.49 vs 0.51): a
whole band where greedy lies, and the blank must win by a √2
margin. When greedy gets away with it: trained outputs are peaked
and blank-heavy (WhyTheSpikesAppear's delivered result) — the mass
hoards on one path and the max speaks for the sum; the hedging
inputs are exactly where it stops.

**4. `SearchTheTranscripts`** — searching over transcripts without
enumeration. First the wrong design: a beam over PATHS wastes its k
slots on duplicate spellings of one transcript and splits its mass
(sum-vs-max sneaks back at beam scale). Relabel the axis: candidates
are collapsed prefixes, and path masses pouring into the same prefix
MERGE — arrows converging on a node, the dynamic-programming move
(`algorithms/` named it: shared prefixes stored once) on a pruned
frontier. The two-frame lattice made kinetic: three colored streams
into prefix A (new letter from ∅ / blank extension / silent merge),
pooling 0.64 against greedy's lone 0.36. Width 2 keeps every
candidate that carries mass here (AA shown at exactly 0) — the
answer is exact; pruning, when it bites, is the only approximation.

**5. `TheTwoLedgers`** — one subtlety makes CTC's beam different
from every textbook beam. A prefix must carry two masses: p_b
(paths ending in blank) and p_nb (ending in its last letter) —
because the two halves have different futures. The repeat fork:
propose A onto prefix A — the p_nb share merges silently back; only
the p_b share can open a genuine double letter (the door beat,
streams routed by ledger). Proof it is correctness, not
bookkeeping: the coin frames (y=1/2 each, T=3) — true P(AA) = 1/8
(only AεA); a one-ledger beam reports 3/8, crediting AAε and εAA,
both of which truly collapse to A — a 3× overcount; wrong answers,
not slow ones. Then the repo-native close no external treatment can
draw: the unpruned beam's ledger table lands digit for digit beside
the forward trellis's final column — p_b + p_nb IS the trellis's
two-final-nodes sum. The beam is the forward recurrence wearing a
search harness. Init pinned: p_b(∅)=1 ("before any frame, all mass
ends in blank").

**6. `ThePriceOfPruning`** — the flagship table (frames
(A .5, B .1, ε .4) ×2, then (A .5, B .4, ε .1)): the exact posterior
crowns A at 0.37; greedy agrees ("A"); width 2 returns A with kept
total exactly 37/100 (no A-feeder was pruned); width 1 returns AB —
wrong, and wrong DIFFERENTLY from greedy: pruning ∅ at frame 1
silently deleted a fifth of the total mass, all of it bound for A,
and AB overtook A inside the beam (0.18 vs 0.17 at frame 3). Kept
totals understate posteriors — never read one as P(A). Pruning is
the only approximation the beam makes, and the price is paid where
mass hedges.

**7. `TheLoopClosed`** — the WhenToUseIt-format closer. The decision
rule mapped: peaked outputs → greedy (production default, usually
right); hedging inputs → the beam. The splice point production leans
on: per-EXTENSION scoring is where an external language model
multiplies in (Deep Speech's Q(c) = log P(c|x) + α log P_lm(c) +
β word_count(c), α, β tuned by cross-validation, beams 1000–8000 —
patching exactly the hole the alignment series declared: frames
independent given the input, language left on the table). One
inherited caution at deployment's door: the loss never paid for
timing, so spike positions are not calibrated segment boundaries —
a decoder returns WHAT was said; WHEN is forced alignment, a
different tool. One production caption: the ledgers run in log
space with the log-add the logarithms series taught (logsumexp,
never max). The loop closes: train on the sum, decode by the
favourites or the ledgers, deploy — waveform to weights to words.

**Device lineage:** the per-frame matrix (fifth series), the
pooled-bar sum-vs-max (alignment scene 3, reborn), the trellis
final column (the forward recurrence, third re-read), the
WARM-overcount convention (the one-ledger counterexample), the
WhenToUseIt mapping close (seventh series).

Scene-length target 30–45 s; formula last per scene.

---

## Pinned report: pedagogy researcher (digest — ADR 007)

Consensus order (Distill, Graves 2006, Scheidl, Borgholt, Hannun 2014,
CMU 11-785): decoding as the inverse problem (Graves: "we do not know
of a general, tractable decoding algorithm" — then his two
approximations, the same two this series teaches) → best-path defined
(h(x) ≈ B(π*), "not guaranteed to find the most probable labelling")
→ greedy's failure on a countable example (the chapter's 0.36-vs-0.64
construction is the strongest available: symmetric, near 2:1 verdict)
→ when greedy gets away with it (peaked outputs; only this repo can
supply the WHY — WhyTheSpikesAppear) → the collapsed-prefix beam
(Distill's central move: the y-axis switches from alignments to
output prefixes, merging = arrows converging) → the two ledgers
FORCED by the collapse map (repeat-extension fork; taught as
correctness via the one-ledger overcount, never as optimization) →
LM fusion foreshadow only (per-EXTENSION annotation, not per-step) →
spikes-not-timestamps → loop closed. Camp split: failure-motivated
(Distill/Scheidl/the chapter) vs implementation-ordered (Hannun 2014
Algorithm 1 case table — learners get lost when it precedes the why)
vs historical-exact (Graves 2006 prefix search — NO beam). Repo
constraints force the failure-motivated camp.

Visual devices: Distill's paired beam figures (path-beam wastes slots
on duplicate spellings; relabel the axis to collapsed prefixes and
arrows converge — the entire difference carried by what the y-axis
means); Distill's T=3 repeat fork (one proposal, two outgoing arrows
— the picture that forces the two ledgers); Graves fig. 2
mass-conserving prefix tree on {X,Y} (0.7+0.2+0.1=1.0 at every node
— beautiful for mass-splitting, but depicts a DIFFERENT algorithm:
best-first exact prefix search — never caption it as the beam); the
chapter's own two-frame tikz lattice made kinetic (three colored
streams into prefix A: new-letter / blank-extension / silent-merge);
two-ledger chip: stacked p_b/p_nb bars inside each candidate node —
on a repeat proposal only the p_b bar's stream passes through to the
double-letter child, the p_nb stream bends back (silent merge);
pruning as a sorted bar list with a cut line at k (MUTED below);
**beam = forward recurrence side by side** (unpruned ledger table
next to the forward trellis's final column, same digits; final score
p_b+p_nb IS Graves eq. 8's α_T(|l′|)+α_T(|l′|−1)) — the repo-native
device no external treatment can draw; greedy as argmax-highlighted
cells on the familiar matrix, pooled-team bar rising past the
single-path bar (alignment scene 3's device "in its deployment
costume"); LM fusion as two multiplied factors living on the
extension arrow, not on the clock.

Verified examples: E1 the anchored construction (ledgers t=1:
''(0.6,0), A(0,0.4); t=2: '' p_b=0.36; A new 0.24 + merge 0.16 →
p_nb=0.40, blank ext 0.24 → p_b; width 2 exact); E2 boundary
q > 1/√2, wrong band (1/2, 1/√2), q=0.7 → 0.49 vs 0.51 ("blank must
win by a √2 margin"); E3 one-ledger overcount 0.375 vs 0.125 (3×;
answers change, not speed); E4 greedy-agrees T=3 {A,B,ε} matrix —
P(A)=0.3170 from six paths, P(∅)=0.045 — so the series doesn't teach
"greedy always wrong"; E6 Graves fig. 2 numbers verified from the
ICML PDF (root 1.0 → X .7, Y .2, e .1; X→ X .1, Y .5, e .1; XY→
X .1, Y .1, e .3; XY wins at 0.3); E7 CMU recitation tree is
one-ledger with a suspected typo (0.132794 vs recomputed 0.132704)
— documented evidence the one-ledger picture ships in respected
courses; DO NOT reuse its numbers.

Misconceptions with counters: greedy is THE decode (E1 pooled bars —
a callback to alignment scene 3, not a new idea); beam the paths,
collapse at the end (the natural wrong design — course material
ships it; duplicate spellings split a transcript's mass and the
sum-vs-max error returns at beam scale); the two probabilities are
bookkeeping (E3: wrong answers, not slow ones; the door metaphor);
wider beam always helps (peaked outputs make pure-acoustic beam ≈
greedy — pyctcdecode-without-LM evidence; width pays only where
mass hedges); width-1 beam = greedy (FALSE — it still merges and
keeps two ledgers; TF issue #21051 corrected their own docs);
spike positions are timestamps (Graves fig. 1 caption "follow the
spikes" is about ORDER, routinely misread as timing — explicit
contrast beat); beam score vs begins-with mass (two glossaries:
time-synchronous score = P(transcript of first t frames is EXACTLY
ℓ); Graves-tree node = P(labelling BEGINS with ℓ) — one figure, one
semantics).

Pitfalls: the one-ledger merge is silently wrong AND ships (any
one-number prefix chip claiming exactness violates
picture-is-a-claim; both ledgers visible wherever merging happens);
TF merge_repeated fossilizes the path/prefix conflation (one
in-the-wild caption, not a scene); Graves 2006 prefix search ≠
prefix beam search (blogs cite it for the algorithm it doesn't
contain); log space: the merge is logsumexp, NEVER max (max quietly
reverts to path search); tiny example may honestly run in
probability space IF a beat says production runs ledgers in logs
with the taught log-add (Awni's gist does); init p_b(∅)=1,
p_nb(∅)=0 ("before any frame, all mass ends in blank"); ∅ stays a
live candidate and can WIN (the gradient series' bias model decodes
empty — dropping ∅ breaks the motivating failure); the repeat case
has two halves — route p_b(ℓ)·y(c) into ℓ+c's p_nb AND p_nb(ℓ)·y(c)
back into ℓ's own p_nb, or on-screen totals visibly stop matching
the trellis; pruned-prefix resurrection never fires at this scale —
say "pruning is the only approximation, and here it makes none",
fold resurrection into the future beam-search series; LM per
extension, no dynamics; number hygiene — use only the 012.dec
anchors plus verifier-confirmed E2/E3/E4/E6 (Scheidl's and CMU's
near-miss matrices would break number tracing).

Key takeaway: the chapter's two-frame lattice made kinetic — three
colored streams pooling 0.64 against greedy's 0.36, ledger bars
stacked inside the winning node, totals then appearing digit for
digit beside the forward trellis's final column — delivers sum-vs-max,
merging-as-DP, ledgers-as-grammar (proved by 0.375-vs-0.125), and
beam-IS-the-forward-recurrence in one composite picture. The repo
outdoes the canonical source here: Distill never taught the trellis,
so it cannot land that final identity; this repo can.

### Sources (for the topic README, `- [ ]`, authors as credited)

- Awni Hannun, "Sequence Modeling with CTC" (Distill 2017),
  <https://distill.pub/2017/ctc/> — already ticked in repo.
- Alex Graves, Santiago Fernández, Faustino Gomez, Jürgen
  Schmidhuber, "Connectionist Temporal Classification" (ICML 2006),
  <https://www.cs.toronto.edu/~graves/icml_2006.pdf> — already ticked.
- Awni Y. Hannun, Andrew L. Maas, Daniel Jurafsky, Andrew Y. Ng,
  "First-Pass Large Vocabulary Continuous Speech Recognition using
  Bi-Directional Recurrent DNNs" (2014),
  <https://arxiv.org/abs/1408.2873> — Algorithm 1, origin of the
  p_b/p_nb prefix beam; init p_b(∅)=1; word-boundary LM factor.
- Awni Hannun, "Example CTC Decoder in Python" (gist),
  <https://gist.github.com/awni/56369a90d03953e370f3964c826ed4b0> —
  the reference implementation; the merging case commented; stable
  logsumexp ledgers.
- Lasse Borgholt, "CTC Networks and Language Models: Prefix Beam
  Search Explained",
  <https://medium.com/corti-ai/ctc-networks-and-language-models-prefix-beam-search-explained-c11d1ee23306>
  — implementation-ordered walkthrough; pruned-prefix recovery.
- Harald Scheidl, "Beam Search Decoding in CTC-trained Neural
  Networks",
  <https://harald-scheidl.medium.com/beam-search-decoding-in-ctc-trained-neural-networks-5a889a3d85a7>
  — smallest numeric greedy failure (0.48 vs 0.52); Pb/Pnb updates.
- Ameya Mahabaleshwarkar, CMU 11-785 F22 recitation "CTC Decoding",
  <https://deeplearning.cs.cmu.edu/F22/document/recitation/Recitation9/rec9_beamsearch.pdf>
  — greedy→exhaustive→beam ordering; ships the one-ledger tree
  (suspected typo documented).
- Zeyu Zhao, "CTC Prefix Beam Search Decoding Algorithm with
  Language Model",
  <https://zhaozeyu1995.github.io/CTC-Prefix-Beam-Search-Decoding-Algorithm-with-Language-Model/>
  — raw-probability-space foil.
- Ryan Leary, TensorFlow PR #15586 "Remove invalid merge_repeated
  option from CTC beam decoder",
  <https://github.com/tensorflow/tensorflow/pull/15586> — the
  conflation fossilized in an API.
- TensorFlow issue #21051 (no single credited author),
  <https://github.com/tensorflow/tensorflow/issues/21051> — width-1
  beam ≠ greedy, correcting the docs.
- Philipp V. Rouast, Marc T. P. Adam, "Single-stage intake gesture
  detection using CTC loss and extended prefix beam search",
  <https://arxiv.org/abs/2008.02999> — no gain beyond width 3 on
  their task (seen via excerpt, not verified on-page).
- Andrei Andrusenko, Aleksandr Laptev, Vladimir Bataev, Vitaly
  Lavrukhin, Boris Ginsburg, "Fast Context-Biasing for CTC and
  Transducer ASR models with CTC-based Word Spotter",
  <https://arxiv.org/abs/2406.07096> — beam-without-LM tracks greedy
  (seen via excerpt, not verified on-page).
- (Reusable, already filed under probability/: Hannun et al., Deep
  Speech, arXiv 1412.5567 — the LM-fusion citation.)

## Pinned report: source verifier (digest — ADR 007)

Answer script `answers/ctc_decoding.py` rerun, exit 0, all four
assertions pass; every number below independently re-derived in exact
Fractions and matching. Anchors 012.dec.{greedymass 0.36, summass
0.64, beamblank 0.24, beamletter 0.40} all agree.

1. Two-frame construction (T=2, y(A)=0.4, y(ε)=0.6) — VERIFIED dual
   route (4-path enumeration + two-ledger beam agree exactly).
   "" = 9/25 = 0.36; A pools AA 4/25 + Aε 6/25 + εA 6/25 = 16/25 =
   0.64. Ledgers after frame 2, prefix A: p_b = 6/25 = 0.24 (blank
   ext), p_nb = 2/5 = 0.40 (new 0.24 + merge 0.16). After frame 1:
   ""=(0.6, 0), A=(0, 0.4). LOOSE (flag 1): "width 2 keeps every
   candidate" — frame 2 has THREE candidates {"", A, AA}; width 2
   prunes AA, which carries exactly zero mass (can only open from
   p_b(A)=0), so the answer is still exact. A scene showing the
   frame-2 list must show AA at 0 or not at all.
2. Boundary (y(ε)=q, T=2): P("")=q², P(A)=1−q². Greedy empty iff
   q > 1/2 STRICT (q = 1/2 is an argmax tie — flag 3); empty truly
   wins iff q > 1/√2 (algebraic, 2q²=1, bracketed both sides;
   0.7071 is display rounding). q=0.7: exactly 49/100 vs 51/100.
3. Three-frame leaderboard (y₁=(.5,.2,.3), y₂=(.4,.3,.3),
   y₃=(.2,.3,.5)) — 27 paths, exact, dual route, total mass 1:
   A 317/1000 = 0.3170 (6 paths) · AB 261/1000 = 0.2610 (5) ·
   B 177/1000 = 0.1770 (6) · BA 49/500 = 0.0980 (5) · "" 9/200 =
   0.0450 · AA 3/100 = 0.0300 · ABA 3/100 = 0.0300 · BAB 3/125 =
   0.0240 · BB 9/500 = 0.0180. Greedy → "A", right. AA and ABA TIE
   exactly at 3/100 (no strict order on screen — flag 4). Runner-up
   is AB 0.2610, NOT "" (flag 5). A beam's KEPT total (0.2150 w1,
   0.2990 w2) understates true P(A)=0.3170 — never label a kept
   total as the posterior (flag 4).
4. Coin stretch (y=1/2 each, T=3): true P("")=1/8, P(A)=3/4 (6
   paths), P(AA)=1/8 (only AεA); nothing else possible (AAA needs
   T≥5). One-ledger beam reports binomial C(3,k)/8: AA = 3/8 =
   0.375 — exactly 3×, crediting AAε and εAA (both truly A).
   Step table: f1 ("" 1/2, A 1/2); f2 ("" 1/4, A 1/2, AA 1/4).
5. Pruning costs something — CONSTRUCTED (exhaustive tenths-grid
   search, exact, tie-free; NOT in any source or the answer script —
   flag 10; adding to the committed answer script is the natural
   follow-up). (a) T=2 simplest: y=(A 2/5, B 1/10, ε 1/2) both
   frames → width-1 returns "" (wrong, = greedy), width-2 "A"
   (right, 14/25); no T=2 tenths example where width-1's wrong
   answer differs from greedy (0 hits exhaustively). (b) FLAGSHIP
   T=3: y₁=y₂=(A .5, B .1, ε .4), y₃=(A .5, B .4, ε .1). Posterior:
   A 37/100 = 0.37 · AB 57/200 = 0.285 · AA 1/10 · B 93/1000 ·
   BA 3/40 · ABA 1/40 · BAB 1/50 · BB = "" = 2/125. Greedy "A"
   RIGHT; width-2 "A" (kept total exactly 37/100 = true P(A));
   width-1 "AB" WRONG and wrong differently from greedy. Width-1
   trace: f1 keeps A(0, 1/2), killing "" and its ε-first feeders
   (εAA 1/10, εAε 1/50, εεA 2/25); f3 candidates AB(0, 9/50,
   .18) > A(9/200, 1/8, .17) > AA(0, 1/10) → AB. Mechanism: pruning
   "" silently deleted 1/5 of total mass that collapses to A,
   letting AB overtake INSIDE the beam.
6. Primary quotes (verbatim from PDFs): Graves 2006 §3.2 best-path
   h(x) ≈ B(π*) "trivial to compute … However it is not guaranteed
   to find the most probable labelling"; prefix search "Given enough
   time … always finds the most probable labelling. However, the
   maximum number of prefixes it must expand grows exponentially";
   (reproduce eq. 4 without the paper's odd π∈N^t subscript —
   flag 8). Distill 2017: "we store the output prefixes after
   collapsing" / "keep track of two probabilities for each prefix".
   p_b/p_nb SYMBOLS from Hannun-Maas-Jurafsky-Ng 2014 §3 (quoted);
   two-mass idea already Graves 2012 book §7.5.2 γ(p_n,t)/γ(p_b,t).
   Deep Speech §2.2 exact: "Q(c) = log(ℙ(c|x)) + α log(ℙ_lm(c)) +
   β word_count(c)", α, β "set by cross-validation", beam "1000-8000".
   Spikes: Graves 2006 "series of spikes separated by strongly
   predicted blanks"; Zeyer 2021 abstract "converges towards peaky
   behavior with a 100% error rate". FLAG 6: NO source states
   verbatim that spike positions are uncalibrated vs segment timing
   — Graves 2006 §6 even leans opposite ("approximate segmentation
   is sufficient" for keyword spotting). Defensible claim: "the loss
   never paid for timing, so spike positions are not calibrated
   segment boundaries" — never "spikes are far from the sound".
7. Complexity: greedy = per-frame argmax + collapse, verbatim
   supported. Beam O(T·k·V) is DERIVED from Hannun 2014 Algorithm
   1's loop nest ("size of A_prev is never larger than the beam
   width k") — attribute the loop structure, don't quote a big-O
   (flag 7).
8. Graves 2012 book Figure 7.5 precedent: blank=(0.7, 0.6),
   A=(0.3, 0.4) → P(blank path)=0.42 vs P(A)=0.58 — the field's
   canonical best-path-failure picture, asymmetric cousin of the
   chapter's 0.36/0.64.

Sources (verifier; authors as credited): Graves-Fernández-Gomez-
Schmidhuber ICML 2006 pdf; Hannun Distill 2017; Hannun et al. Deep
Speech arXiv:1412.5567; Hannun-Maas-Jurafsky-Ng arXiv:1408.2873;
Zeyer-Schlüter-Ney arXiv:2105.14849; Graves 2012 book preprint
(cs.toronto.edu/~graves/preprint.pdf).
