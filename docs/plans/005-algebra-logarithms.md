# Plan 005: `algebra/` — logarithms series

Branch: `feat/algebra-logarithms`, cut from updated `main` (5ae00ee, the
plan-004 merge).
Started: 2026-08-11.

The double-unlock the plan-004 audit surfaced: one logarithms series
closes two promises in two topics — `bayes-rule` → log-odds (evidence as
addition) and `deep_learning/`'s log-space bullet (why the product of
hundreds of probabilities underflows and how log-sum-exp restores it).
Both Ideas queues cross-reference it. New topic directory `algebra/` —
logarithms are neither probability nor counting, and exponents/logs are
the conventional algebra home; the topic starts narrow on purpose.

Branch note: the first cut of this branch briefly sat on a stale main —
PR #5 showed merged in conversation but was still OPEN on GitHub; the
pull-and-verify step caught it, the merge was completed, and the branch
re-cut from the true tip. The fresh-branch rule earns its keep again.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research: pedagogy + source verification (agents in flight) | Scene design written below |
| 1 | Plan committed, topic dir + README skeleton, module stubs | `make check` |
| 2 | Scenes at `--quality draft`; renders verified (count, names, ffprobe, frames incl. transition windows) | Draft renders verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated, root README | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render |

## Checklist

- [x] Branch from updated main (re-cut after completing the PR #5 merge)
- [x] Phase 0: research reports received, scene design finalized below
- [ ] Phase 1: plan + topic skeleton, `make check` green
- [ ] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
- [ ] Phase 3: README + wiki complete, `make test` green
- [ ] Phase 4: local review clean
- [ ] Phase 5: PR open, drafts cleaned, 1080p60 render verified

## Verified technical anchors (from the source-verifier report)

Methods: [quoted] verbatim · [computed-exact] integers/fractions ·
[computed-float] float64 where the float behaviour IS the claim ·
[reasoned] standard argument, counterexample-checked, not verbatim.

- Definition [quoted, OpenStax §6.3]: log_b(x) is the exponent y with
  b^y = x, for b > 0, b ≠ 1, x > 0. The three laws need M, N > 0 (power
  law needs M > 0 even when M^n > 0 — the (−2)² counterexample). No
  single fetched source boxes ALL conditions at once [flag]; state
  them fully anyway. b ≠ 1's reason (1^y is always 1, no unique
  exponent) is [reasoned], ours not the textbook's.
- Change of base [quoted, OpenStax §6.5]: log_b M = log_c M / log_c b,
  all bases positive and ≠ 1.
- Ladders [computed-exact]: 2^0..2^10 and 3^0..3^6 (729). HAZARD:
  math.log(243, 3) = 4.999999999999999 — on-screen integer logs come
  from the exponent, never a float log call.
- The log-odds bridge [computed-exact, repo's own numbers]: urn LR
  red = 3, blue = 1/3 exactly → log₃ odds moves +1 per red, −1 per
  blue; red-then-blue returns to exactly 0. The rendered coins/test
  LR 9 = 3²: each head adds exactly +2; chain 0→2→4→6, odds 729 = 3⁶
  on the ladder. FLAG: the urn is a plan-004 *candidate*, not a
  rendered scene — lean on the rendered LR-9 coins for callbacks.
- Underflow [computed-float]: float64 min normal 2⁻¹⁰²² ≈ 2.2e-308,
  min subnormal 2⁻¹⁰⁷⁴ ≈ 4.9e-324. 0.1^323 survives (subnormal);
  0.1^324 == 0.0 exactly, both routes. Meanwhile the log₁₀ sum is
  exactly −324. Power-of-two variant: 0.5^1074 last survivor,
  0.5^1075 == 0, log₂ sum exactly −1075. CTC dies at ~seconds of
  audio; Graves 2012 [quoted]: recursions "soon lead to underflows".
- Log-sum-exp [quoted, Wikipedia + Graves 2012 eq. 7.19]: LSE = max +
  log(sum of exp(xᵢ − max)); finite because the shifted terms live in
  [0,1] with one exactly 1. Graves' own ln(a+b) = ln a + ln(1+e^(ln b
  − ln a)) is the CTC forward recursion's log-space sum. ATTRIBUTION
  [flag]: the 2006 paper RESCALES (Rabiner-style); log-space is the
  2012 book, which calls rescaling "less robust" — never credit the
  2006 paper with log space.
- Slide rule [quoted]: Gunter 1620 single scale, Oughtred ~1622 two
  scales; sliding adds logs. log₁₀2 ≈ 0.301, log₁₀3 ≈ 0.477 are
  irrational [reasoned, parity argument] — screen shows ≈ only; the
  bit-for-bit float agreement of 0.301+0.477 = log₁₀6 is rounding
  luck, not a demonstrable exactness.
- e without calculus [quoted, OpenStax §6.1]: the compound-interest
  table (2, 9/4, 625/256, …, → 2.718281828…) stabilizes; name the
  number, defer the why. MUST NOT claim: derivatives, areas under
  1/t, Σ1/n!, or any non-circular "natural" justification — all
  calculus. Even "the limit exists" is analysis; the honest move is
  the table plus an explicit "that story needs calculus."

## Scene design (finalized from the two research reports)

Module: `algebra/logarithms_manim.py`, six scenes. The spine is the
counting camp's two-row strip (counter above, values below) — the
inverse-graph definition is documented to misfire (Kenney & Kastberg's
"Nora") and appears nowhere. e is an explicit Scope exclusion: every
road to it is calculus, and neither consumer needs it. The log-odds
payoff anchors on the rendered LR-9 coins (integer-exact in base 3),
never Diseasitis (irrational logs). All on-screen integer logs come
from exponents, never float log calls.

1. `TheCountingStrip` — exponents as counted multiplications: the
   two-row strip (0,1,2,… over 1,2,4,…,1024). Invert the question,
   not the function: "2 to the what is 64?" — a logarithm reads the
   counter row. Definition boxed with its full conditions (b > 0,
   b ≠ 1 because 1's ladder never moves, x > 0).
2. `OneFactThreeNotations` — the triple (2, 6, 64) asked three ways;
   the triangle of power; b^(log_b x) = x as *undo, never cancel*
   (the "they just disappear" interviews). The log(a+b) disaster
   refuted in base 10 — log₁₀(10+10) ≈ 1.301 ≠ 2 — because the base-2
   instance is coincidentally TRUE (log₂(2+2) = 2), a trap the scene
   itself must sidestep.
3. `MultiplyIsAdd` — the product law as hops on the strip (8 × 16:
   hop 3 + hop 4 = hop 7 = 128); the slide rule (Gunter 1620,
   Oughtred ~1622) as the law made physical; change of base as a
   stride change (log₄64 = 6/2 = 3, integer-exact); the base as a
   unit — ten doublings ≈ three digits (1024 ≈ 1000) is why
   log₁₀2 ≈ 0.301, shown with ≈ only. One caption on e: "calculus
   later makes one base natural — that story waits."
4. `ShrinkCounts` — negative logs from the repo's own square:
   `ChainsOfTrials`' (1/2)⁴ cell re-read as four halvings,
   −log₂(area) = 4. Probabilities in (0,1) are shrink counts; pH as
   the everyday negative-log; log 0 = −∞ (the zero prior, infinitely
   far — the log-space form of "multiplication cannot resurrect");
   and slow-is-not-bounded: name any N, 2^N sits on the strip.
5. `TheEvidenceRuler` — consumer #1. `YesterdaysPosterior`'s odds
   ladder re-plotted on the base-3 ruler: each head adds exactly +2
   (0 → 2 → 4; odds 1, 9, 81), H-then-T walks back to exactly 0.
   "Each head multiplies by 9" becomes "each head adds the same
   length." Deciban lore as a caption (Turing; ~1 deciban is the
   smallest evidence humans perceive).
6. `TheUnderflowCliff` — consumer #2. The value row falls off
   float64's floor (0.5^1074 survives, 0.5^1075 == 0; 0.1^324 == 0)
   while the counter row walks on (log₁₀ sum exactly −324); Graves
   quoted ("soon lead to underflows"); log-sum-exp as the one move
   the trellis's *additions* need — log₂(2⁻¹⁰ + 2⁻¹⁰) = −9 exactly,
   and the max-shift is safe because it factors out and the shifted
   terms live in [0,1]. Attribution kept honest: the 2006 paper
   rescales; log-space is the 2012 book. Closing: the wild scales
   (dB, pH, magnitude, semitones) and the boxed takeaway — whenever
   the world multiplies and you would rather add.

Deliberately deferred: e and ln (calculus), Weber–Fechner as anything
more than motivation, the paper-folding stack (thought experiment
only, if used at all), and log-odds beyond the coins (Diseasitis'
logs are irrational).

## Known material gaps (for the PR body)

(named after scene design settles)

## Review notes

(filled in at the end)
