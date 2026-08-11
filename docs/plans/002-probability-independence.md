# Plan 002: `probability/` topic — independence series

Branch: `feat/probability-independence`, cut from updated `main` (98d529a,
the plan-001 merge).
Started: 2026-08-11.

The first of two probability series named in plan 001's gaps: independence
now, conditional probability on its own branch once this one merges. This
series is the bridge the CTC topic promised — why multiplying
probabilities is ever legitimate — so it must stand without conditional
probability, which does not exist in the repo yet.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research: how independence is best taught, examples exactly verified | Scene design written below |
| 1 | Plan committed, topic dir, README skeleton, scene stubs | `make check` |
| 2 | Scenes, iterated at `--quality draft`; renders verified (count, names, ffprobe frames + durations, extracted frames) | Draft renders verified by eye |
| 3 | Concepts table with all three levels, references as `- [ ]`, links back to `combinatorics/` and `deep_learning/`; root README topics row | `make test` |
| 4 | Local CodeRabbit pass, findings addressed | Review clean |
| 5 | PR (body names conditional probability as the next branch), bot review, finalise | `make clean-drafts` + 1080p60 render |

## Checklist

- [x] Branch from updated main
- [x] Phase 0: research reports received, scene design finalized below
- [x] Phase 1: plan + skeleton, `make check` green
- [x] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
  (6 distinct numbered files; durations 17–39 s; 17 extracted frames
  reviewed; 2 defects found and fixed — the HH overlap tint was
  overwritten, the 6×6 side note center-aligned into the grid —
  re-rendered, re-verified clean)
- [x] Phase 3: topic README complete, `make test` green (full `make
  check` run, exit 0; all nine references human-verified)
- [ ] Phase 4: local review clean
- [ ] Phase 5: PR open, drafts cleaned, 1080p60 render verified

## Verified technical anchors (from the research pass)

Every fraction below was computed by exact enumeration (no floats) and
checked against the definition sources; scenes must not contradict them.

- Definition: A, B independent iff P(A∩B) = P(A)·P(B) — the product form
  is the *primary* definition (conditional form P(A|B)=P(A) is the
  equivalent characterization requiring P(B) > 0, deferred to the
  conditional-probability series).
- Fair die, independent pair: A = {even}, B = {1,2,3,4} —
  1/2 · 2/3 = 1/3 = P({2,4}) ✓. Dependent pair: A = {even}, B = {≤3} —
  1/2 · 1/2 = 1/4 ≠ 1/6 = P({2}).
- Two dice: every {first ∈ S} vs {second ∈ T} pair is independent — the
  6×6 grid is the outer product of its margins; S×T is a rectangle of
  |S|·|T| cells. The area model is this picture made continuous, and it
  *models* independence by construction (bands realize any independent
  pair; a dependent pair cannot be drawn as perpendicular bands).
- Mutually exclusive ≠ independent: disjoint A, B with positive
  probability always fail the product test (0 ≠ P(A)P(B) > 0) — they are
  maximally dependent. Die instance: {even} vs {1,3,5}.
- Pairwise ≠ mutual: two coins, A = first H, B = second H, C = exactly
  one head — all three pairs factor (1/4 each) but P(A∩B∩C) = 0 ≠ 1/8.
- Without replacement: two cards, P(both aces) = (4/52)(3/51) = 1/221 ≠
  (1/13)² = 1/169; replacement restores exactly 1/169. P(second is ace)
  = 1/13 too (enumerated, 204/2652).
- Independent trials: P(HHTH) = (1/2)⁴ = 1/16; the general product over
  a sequence is the product measure — the exact structure a sequence
  model asserts when it multiplies per-frame probabilities (the chain
  rule degenerates to the plain product exactly under independence).
- Edge case (mention or not, decide in design): P = 0 or P = 1 events
  are trivially independent of everything.

## Scene design (finalized from the two research reports)

Module: `probability/independence_manim.py`, six scenes. The product
formula is taught as the *primary* definition (it is, in rigorous texts —
and the conditional route is unavailable before plan 003 anyway). The
central visual is the aligned unit square (Arbital's device), which is
the repo's multiplication-rule grid reweighted from counts to areas.
Venn diagrams are deliberately absent — they carry no information about
independence and reinforce the mutual-exclusivity confusion.

1. `ProbabilityAsArea` — level 1 groundwork. The unit square: sample
   space as a 1×1 square, event as region, probability as area
   (3blue1brown's grammar). A die as six equal cells; counting →
   proportions is the bridge from `combinatorics/`.
2. `TheProductRule` — the definition. Two coins as a 2×2 grid, two dice
   as 6×6: an event about the first experiment is rows, about the second
   is columns, the intersection is a rectangle — area = width × height.
   Aligned square: both cuts straight all the way across. Boxed:
   A ⊥ B iff P(A∩B) = P(A)·P(B).
3. `OneDieTwoEvents` — the jewel example. A = even, B = {1,2,3,4} on a
   single die: 1/2 · 2/3 = 1/3 ✓ independent, though both are about the
   same roll. Slide B's boundary one pip (≤3): 1/4 ≠ 1/6, dependent.
   Independence is arithmetic about the measure, not "separate
   machines" — a biased die breaks the first pair too.
4. `NotMutualExclusivity` — the top-tested confusion, head-on. Disjoint
   events with positive probability always fail the product test —
   knowing A occurred tells you B did not: maximally dependent. The
   broken-square picture: dependence is the cut stepping; independence
   is the knife-edge where it straightens.
5. `ChainsOfTrials` — the bridge. Each flip subdivides the square;
   HHTH occupies a cell of volume (1/2)⁴ = 1/16; with per-step p's the
   box has side lengths p₁…pₙ. Honest captions: the chain needs
   *mutual* independence (Bernstein inset: pairwise isn't enough — all
   three pairs factor, the triple gives 0 ≠ 1/8), and the product is a
   modeling assumption (the product measure) — exactly what
   `deep_learning/`'s CTC formula purchases per frame.
6. `WhenToUseIt` — level 3. Replacement installs independence,
   depletion breaks it (aces: 1/221 vs 1/169); common causes break it
   without any causal link between the events; the gambler's fallacy is
   the law of large numbers misread as compensation — it works by
   swamping. Closing: independence is a property of the model's
   measure; assuming it is a purchase, so know what you paid.

## Known material gaps (for the PR body)

- Conditional probability: P(A|B), the equivalent definition of
  independence via P(A|B) = P(A), Bayes' rule — the **next branch**, as
  requested.

## Review notes

(filled in at the end)
