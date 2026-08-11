# Plan 001: `deep_learning/` topic — CTC alignment series

Branch: `feat/ctc-alignment`, cut from updated `main` (bb4df4a).
Started: 2026-08-11.

The first plan recorded under the numbered-plans rule; the repo scaffold and
the combinatorics topic predate it, so the record starts here.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research: how CTC is best taught, technical details verified against Graves 2006 + Distill | Scene design written below |
| 1 | Process rules in CLAUDE.md, plan committed, topic dir, README skeleton, first scene stub | `make check` |
| 2 | Scenes, iterated at `--quality draft`; renders verified (count, names, ffprobe, extracted frames) | Draft renders verified by eye |
| 3 | Numbered concepts table with all three levels, references as `- [ ]`, links back to `combinatorics/`; root README topics row | `make test` |
| 4 | Local CodeRabbit pass, findings addressed | Review clean |
| 5 | PR (body names the material gaps → next branch), bot review, finalise | `make clean-drafts` + 1080p render |

## Checklist

- [x] Branch from updated main
- [x] Phase 0a: technical verification report received
- [x] Phase 0b: pedagogy report received, scene design finalized below
- [x] Phase 1: rules + plan + skeleton, `make check` green
- [x] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
  (6 distinct numbered files, ffprobe durations 13–30 s, 23 extracted
  frames reviewed; 4 layout collisions found and fixed, re-rendered,
  re-extracted, clean)
- [x] Phase 3: topic README complete, `make test` green (full `make
  check` run, exit 0; two references already human-verified)
- [x] Phase 4: local review clean — one finding (reset the human-verified
  reference ticks), declined with reasoning in ADR 006
- [x] Phase 5: PR open (#2), drafts cleaned, 1080p render verified
  (11 files across both modules; every duration exactly the scripted
  time ÷ 0.75 after the pacing change below)

## Verified technical anchors (from the research pass)

Facts the scenes must not contradict, verified against the Graves 2006 ICML
paper and the Distill 2017 article, with counts checked by exact enumeration:

- Collapse rule: merge repeats **then** remove blanks. Discriminating case:
  `A-A → AA` but `AA → A` — so double letters force a blank between them.
- Extended sequence: blanks interleaved, length `2U+1`. The paper's own
  trellis figure (Fig. 3) uses the target **CAT** — reusing it is an homage.
- Forward recurrence: three terms, skip `s-2 → s` allowed exactly when
  `z's` is not blank and `z's ≠ z's₋₂`. Init over first two states;
  terminate on last two.
- Exact drawable counts: `AB` at `T=4` has **15** paths (all listable);
  `OO` at `T=4` has **5** (the blank is mandatory); `CAT` at `T=4` has
  **7**, at `T=6` has **84**. Repeat-free closed form: `C(T+U, T−U)`.
  Distill's headline: `T=100, U=50` gives ≈ `2 × 10⁴⁰` alignments.
- Minimum length: `T ≥ U + (adjacent duplicate pairs)` — verified
  computationally; implicit rather than verbatim in the sources.
- Assumptions: monotonic alignment, output ≤ input, per-frame conditional
  independence. Rules out reordering tasks (translation → attention).

## Scene design (finalized from the two research reports)

Module: `deep_learning/ctc_alignment_manim.py`, six scenes. The pedagogy
consensus spine is problem → naive failure → blank → collapse map with a
tiny full enumeration → counting/explosion → trellis → properties. What
each scene borrows is noted inline.

1. `TheAlignmentProblem` — level 1. Frames of input vs. characters of
   text; the dataset pairs them but nothing says which frames are which
   letter, and there is no single true alignment. Problem-first ordering
   is the consensus of every good source (Distill, CS224S, CMU).
2. `TheBlankToken` — levels 1–2. Naive per-frame emission + merge-repeats
   fails twice: doubled letters ("HELLO" → "HELO") and forced emission on
   held sounds. ε fixes both. Collapse rule is merge repeats **then**
   drop blanks — walk one example in the wrong order to show it break
   (known stumbling block per both reports). Minimal pair: "TO" vs "TOO".
3. `ManyPathsOneWord` — level 2 pivot. B⁻¹ as a set: enumerate **all 15**
   paths for target AB at T=4 (verified count), collapse a few live.
   The claim CTC makes: P(text) = Σ over its paths of Π per-frame probs.
   "OO" at T=4 has only 5 — the fiber depends on the word.
4. `CountingAlignments` — level 2, the `combinatorics/` callback. The
   multiplicative rule gives 3⁴ = 81 possible paths at T=4 over {A,B,ε};
   15 spell AB. Repeat-free closed form C(T+U, T−U) (= C(6,2) = 15 ✓);
   at T=100, U=50 it is ≈ 2 × 10⁴⁰ — enumeration is dead, which is the
   cliffhanger for the trellis. This is the counting step
   `PartitionRule`'s when-useful column foreshadowed.
5. `TheForwardTrellis` — level 2 payoff. Extended sequence ε A ε B ε
   (2U+1 = 5 rows) × T=4 columns; edges are the collapse semantics (skip
   over ε allowed only between different letters — inset shows why O→O
   would break "OO"). Run the recurrence with unit weights so the counts
   are visible: the two final nodes sum to the same 15 from scene 3.
   Init on the first two states, terminate on the last two (a detail
   sources gloss over, per the pitfalls list).
6. `WhenToUseIt` — level 3. Where the tool applies: speech, OCR,
   handwriting — anything monotonic with unknown timing. The assumptions
   (monotonic, output ≤ input, per-frame conditional independence) and
   what they rule out: translation reorders → attention; spike timing is
   not segmentation; independence is why external language models help.

Deliberately deferred to "Ideas not yet built": beam-search decoding with
prefix merging, peaky-output training dynamics (Graves Fig. 4), the
gradient identity (softmax − occupancy), and numerical stability in log
space.

## Known material gaps (for the PR body)

- No `probability/` topic yet: CTC leans on products of independent
  probabilities, log-likelihood, and softmax-per-frame — asserted here, not
  taught. Likely the next branch.
- Dynamic programming as its own concept (shared-prefix reuse) is used
  inline here but deserves its own treatment.

## Review notes

- Local CodeRabbit pass: one finding, declined (ADR 006 — human-verified
  reference ticks stay ticked).
- PR bot pass: three findings — the same checkbox reset (declined, ADR
  006), and two accepted: CLAUDE.md/README wording had drifted from ADR
  004 on docstring length, and the plan's phase table now spells
  `make clean-drafts` in full.
- Watching feedback landed two repo-wide rules mid-review, both now in
  CLAUDE.md under motion discipline: scenes render at the native 0.75×
  pace (`PLAYBACK_SPEED` in `utils/scene.py` — player-side slowdown was
  juddering 60 fps output), and in-place text swaps are sequenced rather
  than crossfaded. The pacing change's first draft double-stretched
  waits; caught by an end-to-end duration check and pinned by a test.
- References in both topic READMEs were opened, verified, and ticked by
  the maintainer during the session.

Follow-up (next branch): `probability/` per the gaps section above.
