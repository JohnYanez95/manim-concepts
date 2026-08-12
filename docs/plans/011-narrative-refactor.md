# Plan 011: the narrative-refactor pass — teaching bodies point backward

Branch: `feat/narrative-refactor`, cut from updated `main` (f2cfec6,
the plan-010 merge). Started: 2026-08-12.

The charter course to CTC is complete (plans 001–010 all merged), so
the queued refactor fires: **building-block scenes ground in prior
topics — pointing backward at blocks the viewer already owns — and
forward pointers live only in when-useful framing** (the rule stated
2026-08-11; plans 007+ were designed under it, so the audit targets
the plan 001–006 era). The repo's worst-case precedent:
`TheUnderflowCliff` rendered ln before any series taught it — a debt
plan 006 existed partly to repay.

Scope: the seven pre-rule modules — `combinatorics/counting_rules`,
`deep_learning/ctc_alignment`, `probability/independence`,
`probability/conditional_probability`, `probability/bayes_rule`,
`algebra/logarithms`, `calculus/e_and_ln` — their scenes' on-screen
text and their README what/why table cells. Finding classes:
teaching-body forward references (to later-built or unbuilt
material) and devices *used* before their home series teaches them
(the highest-severity class). Closers and when-useful beats that
promise forward are ALLOWED — that is where use-case framing lives.

Dispositions: (a) allowed, no action; (b) prose-only fix (README
cell, no render); (c) scene text edit (re-render that scene);
(d) structural (a beat moves to the closer). Only scenes whose
on-screen text changes get re-rendered.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Branch; three parallel audit agents over the seven modules; findings + dispositions pinned here | Findings written into the plan; **John approves dispositions** |
| 1 | Prose-only fixes (README cells, wiki quotes) | `make test` |
| 2 | Scene text edits; layout linter on touched modules; drafts of touched scenes verified by eye | Linter clean + drafts verified |
| 3 | Local CodeRabbit + `connection-auditor` (prose-vs-built after edits), findings addressed | Review clean |
| 4 | PR, bot review; finals re-render of touched scenes only | `clean-drafts` + 1080p60 of touched scenes |

## Checklist

- [x] Phase 0: findings pinned; dispositions D1–D5 approved by the
  maintainer as proposed, 2026-08-12
- [x] Phase 1: the aces-license README cell reworded to claim only
  what the independence scene shows; `make test` green (212)
- [x] Phase 2: two scene edits — `TheUnderflowCliff` gains the ln/e
  loan caption (and the FadeOut group carries it out; `on_frame`
  imported), `TheMultiplicationRule`'s aces line now reads
  "Independence priced the aces by counting alone — now factor it:";
  algebra Scope's deferral bullet grown to name both on-screen
  captions and scoped base-generic to "all other content". Both
  touched scenes lint clean (four latent findings in untouched
  shipped scenes recorded as out of scope); both beats verified by
  frame at draft
- [x] Phase 3: local CodeRabbit clean on the first pass (zero
  findings, second time in repo history). Audit: 7 findings, all
  applied — INDEX row 63 now records the promise side of the graph's
  flagship edge (on screen at both ends, symmetric at last), the
  calculus two-promises sentence trued, the algebra antecedent slip
  fixed, and the "by counting alone" residual softened to "with no
  license shown" in both the cell and the caption (the scene was
  already in the re-render set, so full strictness was free); the
  debt premise verified surviving (character-identical MathTex in
  both modules); the TheDebtRepaid-quotes-the-loan-note replay
  recorded as a future-touch candidate; stamp advanced to aeb25f6
- [ ] Phase 4: PR, bot review, touched finals rendered

## Findings (pinned from the three audit agents)

The headline: the pre-rule material is far more compliant than the
rule's origin story suggested. Across seven modules — every on-screen
string and every what/why table cell — the agents found **zero
undeclared teaching-body forward references** and exactly **one
used-before-taught device still standing as rendered**.

### Agent A — combinatorics + ctc_alignment (16 findings)

- `counting_rules_manim.py`: **zero** forward references in any
  on-screen string; all forward pointers in the README live in the
  when-useful column. A model citizen.
- `ctc_alignment_manim.py`: the probability machinery (per-frame
  products, P(Y|X) notation, the y_t factors — homes: independence
  002, conditional 003, softmax 008, all later) is used throughout
  the teaching bodies (scenes 3 and 5, plus README rows 3/5). But
  this is the repo's **declared debt**: the topic Scope says
  "products of independent probabilities … are *used* here without
  being taught", and 002/003/008 have since repaid it (008 scores
  this module's own matrix) — the ln-precedent pattern, completed.
  Un-buildable any other way without gutting the motivating opener.
  All other forward pointers (log-space, attention, LM fusion, spike
  timing) sit correctly in when-useful/closer framing.

### Agent B — independence + conditional + bayes (8 findings)

- Zero teaching-body forward references; zero used-before-taught
  devices (no log/ln/e/evidence-ruler notation anywhere in the three
  modules — the odds→log-odds lineage crosses into `algebra/` only
  in one when-useful README cell). All CTC mentions are *backward*
  (001 precedes 002/003/004).
- One borderline: `independence_manim.py:699`'s caption "the law of
  large numbers swamps; it does not compensate" name-drops the LLN
  (007's territory) — but inside `WhenToUseIt`, the series' level-3
  field guide, with self-contained arithmetic.
- One backward prose-vs-built nit: conditional's
  `TheMultiplicationRule` says on screen "The independence series
  showed this with no license: 4/52·3/51" — but the built
  independence scene shows only 1/221 vs 1/169, never the
  factorization. The claim overstates what the earlier scene
  displayed.

### Agent C — logarithms + e_and_ln (4 findings)

- `e_and_ln_manim.py`: fully clean — every recall points backward.
- **The one standing debt**: `TheUnderflowCliff`'s log-add identity
  block (`logarithms_manim.py:516-520`, ln and e in a level-2
  teaching movement). The plan-006 repayment is real but lives
  entirely *downstream*: `TheDebtRepaid` re-reads the identity, and
  the READMEs document the deferral — but the algebra scene as
  rendered carries no on-screen deferral for ln; a viewer at series
  position 6 meets ln cold. The debt is also **canonized**:
  `TheDebtRepaid` opens with "The repo's oldest forward reference —
  rendered before ln meant anything", so erasing the debt (e.g.
  rewriting base-2) would orphan that premise and cascade into
  calculus. The minimal honest fix is one added deferral caption
  inside the ln block — an on-screen IOU; one-scene re-render.
- `MultiplyIsAdd`'s closing deferral and the calculus row-1
  when-useful pointer: allowed.
- Consistency rider: algebra Scope's "All content here stays
  base-generic" must stay consistent with whatever the ln-block
  disposition is.

## Dispositions (proposed — the phase-0 gate is John's approval)

| # | Item | Proposal |
| --- | --- | --- |
| D1 | `TheUnderflowCliff` ln block | **(c)-small**: add one on-screen deferral caption inside the ln movement ("ln is a name calculus will earn — take the identity on credit" or similar); keeps `TheDebtRepaid`'s premise true, warns the viewer; re-render one scene. Tied README cells reviewed for consistency |
| D2 | `TheMultiplicationRule` overstatement | **(c)-small**: reword the on-screen line so it claims only what the independence scene showed (the unlicensed 1/221, not a displayed factorization); re-render one scene |
| D3 | ctc_alignment probability machinery | **Accept as declared-and-repaid debt** — recorded here; no edits |
| D4 | LLN name-drop in `WhenToUseIt` | **Allowed** — level-3 field guide; no action |
| D5 | All remaining findings | **Allowed** — when-useful/closer framing, exactly where the rule wants forward pointers |

Re-render scope under this proposal: two scenes
(`TheUnderflowCliff`, `TheMultiplicationRule`) — draft verify, then
1080p60 finals for those two only.
