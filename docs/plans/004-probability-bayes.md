# Plan 004: `probability/` — Bayes' rule series

Branch: `feat/probability-bayes`, cut from updated `main` (b439a73, the
plan-003 merge).
Started: 2026-08-11.

The repo's strongest open promise, per the wiki: promised on screen twice
(`TwoSlicesOneSquare` ends at the named front door; `WhenToCondition`
defers Monty Hall here) plus four documents. Plan 003 seeded it four
ways: the front-door identity P(A)·P(B|A) = P(B)·P(A|B), the
natural-frequency cohort chips to complete, the announcement-protocol
lesson, and the Rosenthal reference (human-verified). Also riding along:
CLAUDE.md refinements from recent review rounds ("the picture is a
claim"; transition-window frame checks).

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research: pedagogy + source verification (agents in flight) | Scene design written below |
| 1 | Plan committed, CLAUDE.md refinements, module skeleton, README updates | `make check` |
| 2 | Scenes at `--quality draft`; renders verified (count, names, ffprobe, frames incl. transition windows) | Draft renders verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated, root README | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render |

## Checklist

- [x] Branch from updated main
- [x] Phase 0: research reports received, scene design finalized below
- [x] Phase 1: plan + CLAUDE.md + skeleton, `make check` green
  (CLAUDE.md refinements committed separately at f9c14d0; one ticked
  reference's description updated — the source still covers the claim,
  the tick stands — because "deferred to the Bayes series" became
  stale the moment this branch existed)
- [x] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
  (verification script ran FIRST — every displayed number plus the
  Monty Small dial enumerated, resolving the anchors' verify-before-
  animating flag; then: 6 distinct numbered files; durations 23–30 s;
  16 frames reviewed;
  one LaTeX crash — the \quadP adjacent-string bug — plus three layout
  fixes: the renaming beat now clears the old identity first, the
  invariance pools relabel to 9:12 with the picture, and scene 6's
  table header became a caption; one self-inflicted span-replace
  deleted the rows definition and was rebuilt)
- [x] Phase 3: README + wiki complete, `make test` green (node
  `bayes-rule` added; the strongest-promise edge flipped delivered with
  three citations; log-odds promised; Monty Small's Ideas bullet
  retired — enumerated and now on screen)
- [x] Phase 4: local review clean — CodeRabbit: six findings, five
  accepted (the Monty Small record written into the anchors rather than
  the claim weakened; Fall's likelihood triple corrected in two docs;
  the stale Bayes Ideas bullet removed; the halved-rates labels), one
  declined (ADR 006 — noting the local CLI does not honor
  path_instructions, confirming the research caveat; the cloud bot is
  the tuned channel). Audit: 15 findings applied, including the
  logarithms double-unlock cross-reference. The transition-window rule
  caught its first live bug: the rate-label crossfade.
- [ ] Phase 5: PR open, drafts cleaned, 1080p60 render verified

## Verified technical anchors (from the source-verifier report)

Methods: [quoted] verbatim from source · [computed] exact fractions by
enumeration, no floats · [both] two independent routes agree.

- Bayes' rule [quoted, B&H Thm 2.3.3]: P(A|B) = P(B|A)P(A)/P(B).
  Positivity lives in Thm 2.3.1 ("positive probabilities"), not inline
  — attaching conditions on screen is a correct editorial completion,
  not the verbatim theorem. Expanded denominator = "Bayes with LOTP
  opened" (their phrasing pairs them; no separately numbered theorem).
- Odds form [quoted, Thm 2.3.5]: posterior odds = prior odds ×
  likelihood ratio. B&H say "likelihood ratio"; "Bayes factor" is
  3b1b's term ("also sometimes called") — synonymous here, not in
  general statistics. Equivalence to probability form [computed] on 343
  rational triples.
- Prevalence pair completed [both, matches the conditional series
  EXACTLY]: 1:9 × 9 = 9:9 → 1/2 (the counted 9/18); 1:99 × 9 = 9:99 =
  1:11 → 1/12 (the counted 9/108). LR = sens/FPR = 9.
- Diseasitis [both, Arbital verbatim]: 20 sick → 18, 80 healthy → 24;
  18/42 = 3/7; odds (1:4)×(3:1) = 3:4 → 3/7. The waterfall IS the odds
  form drawn as plumbing — its 18:24 is literally 3:4.
- Sequential updating [both]: LRs multiply exactly when results are
  conditionally independent given the state — the assumption
  `WhenToCondition` taught; two Diseasitis tests: 1:4 → 3:4 → 9:4 =
  9/13, all three routes agree. Marginal dependence (the disease as
  common cause) is *why* the second test still moves the posterior.
- Monty [both, Rosenthal verbatim]: standard protocol (host coin-flips
  when free) → switch 2/3; Monty Fall → 1/2; Monty Crawl → host opens
  lowest available (prob 2/3, switch wins 1/2) or is forced high
  (prob 1/3, switch wins with certainty). The Proportionality
  Principle is "essentially a re-statement of Bayes' Theorem" — the
  odds form with uniform prior. Monty Small's 1/(1+p) was initially
  quoted-only; the Phase 2 verification script then enumerated it, and
  the record is: p ∈ {0, 1/4, 1/2, 3/4, 1} → P(switch wins) = 1, 4/5,
  2/3, 4/7, 1/2 — exact, matching 1/(1+p) at every value. That is what
  cleared the dial for screen and licenses the module docstring's
  "machine-verified" claim.
- Iterated-update candidates [both]: urns (3R1B vs 1R3B, LR 3: 1:1 →
  3:1 → 9:1; red-then-blue cancels to exactly 1/2); the repo's own
  two-coin pair has LR 9 — the same factor as the prevalence test.
- Flags: 3b1b's frequency counts round (89 vs 89.1) so his counted
  posteriors differ in the third decimal from exact odds values —
  never mix his numerators with odds arithmetic on screen; the repo's
  own pair is integer-exact throughout, a quiet advantage. Arbital
  verified via the greaterwrong mirror. Odds = ∞ allowed silently at
  P(Aᶜ) = 0.

## Scene design (finalized from the two research reports)

Module: `probability/bayes_rule_manim.py`, six scenes. The ordering
resolves the textbook-vs-communication camp split cleanly: the
probability form costs one line here (plan 003 pre-paid for it), so it
goes first — then the series' weight lands on counts and odds, where
the new content lives. Guardrails: integer-exact numbers only (3b1b's
own counts round — never mix his numerators with odds arithmetic); no
logarithms, no random variables; the CI license said on screen at the
moment LRs first multiply.

1. `ThroughTheFrontDoor` — divide the standing identity by P(B)
   (positivity inherited), on the two-slices frame plan 003 left up.
   Rename the parts: prior, likelihood, posterior; the denominator is
   LOTP over the hypothesis columns — the repo's own picture. The
   level-1 claim: evidence does not determine beliefs, it *updates*
   them; posterior ∝ prior × likelihood, normalize last.
2. `CountingItOut` — the first real computation in natural frequencies
   on the inherited cohort chips: Diseasitis, 100 students → 20 sick
   (18 positive) vs 80 healthy (24 positive) → 18/42 = 3/7. The prior
   is carried inside the counts, which is why counts cure base-rate
   neglect (4% → 24% correct; gynecologists 21% → 87%).
3. `TheOddsForm` — the waterfall: stream widths = prior odds (1:4),
   pass-through fractions = likelihoods (3:1), the pool = posterior
   odds 3:4 → 3/7 — the same 18:24 as the chips. The reveal: this is
   the square-drawn-as-a-tree with renormalization deferred; the three
   inherited devices are one object, and its law is posterior odds =
   prior odds × likelihood ratio. Invariance beat: scale either
   streams or fractions, only ratios survive. Police 3:4 vs 3/7.
4. `OneTestTwoPatients` — the prevalence pair completed as a
   factorization: LR = 9 is *the test's one number*; 1:9 × 9 = 1:1 →
   1/2 and 1:99 × 9 = 1:11 → 1/12 — the exact counted 9/18 and 9/108
   from plan 003, now derived instead of tallied. The "accuracy"
   collapse: one word hiding two numbers, read as a posterior. A
   posterior cannot be stated without its prior.
5. `YesterdaysPosterior` — iterated updating on the repo's own coins
   (LR 9 per head, echoing the test): 1:1 → 9:1 (9/10) → 81:1 (81/82);
   H-then-T lands back at exactly 1:1 — updating is reweighting, not
   replacement (impossible under replacement, automatic under
   reweighting). The license, on screen at the second multiplication:
   LRs multiply only for evidence conditionally independent given the
   hypothesis — `WhenToCondition`'s lesson. Zero-prior caption: a
   hypothesis at 0 stays at 0.
6. `TheHostsProtocol` — Monty at last, as ordinary Bayes with three
   streams (uniform prior over car positions) and the likelihood of
   the host's *action* under his protocol: standard (1/2, 1, 0) →
   switch 2/3; Monty Fall (1/2, 1/2, 0) → 1/2; Monty Crawl forced-high →
   switch wins certainly. Same revealed fact, three different answers
   — the two-children announcement lesson completed at series scale.
   Rosenthal's proportionality principle named as "Bayes with a
   uniform prior". Closing when-useful mapping: diagnosis, spam,
   forensics (the prosecutor's fallacy as a missing prior), and the
   boxed takeaway: never state a posterior without its prior.
   (Monty Small's 1/(1+p) only as a caption unless the Phase 2
   verification script enumerates it first — the verifier flagged it
   unenumerated.)

Deliberately deferred: log-odds (no logarithms in the repo yet),
composite-hypothesis Bayes factors, and continuous priors (needs
random variables).

## Known material gaps (for the PR body)

- **Logarithms are now the highest-leverage missing concept**: one
  logs series unblocks TWO promises in two topics — `bayes-rule` →
  log-odds (evidence as addition) and `deep_learning/`'s log-space
  numerical-stability bullet. Neither queue knew about the other until
  this branch's audit; both now cross-reference.
- Explaining-away: verified in plan 003, still unbuilt, and previously
  aimless — now aimed at the log-odds/graphical-models neighbourhood,
  next to "condition on the way it happened".
- Softmax / likelihood / log-likelihood — the last CTC bridge half;
  `ThroughTheFrontDoor` naming "likelihood" on screen gives the future
  scene its citation anchor.

## Review notes

- The two review mechanisms converged on Monty Small from opposite
  directions — the bot said "remove the unsupported claim", the auditor
  said "the claim is true but unrecorded; write it down". The auditor's
  fix was right: anchors now carry the five p values and exact results,
  and "machine-verified" is a record, not testimony.
- The transition-window frame rule (added this branch) caught its first
  real bug: the 90%→45% rate-label crossfade ghosting mid-swap.
- Recurring genre, third and fourth occurrences: promising documents
  going stale at delivery (INDEX device bullets; the plan's own gaps
  placeholder). The auditor now flags it by name every run.

Follow-up (next branch): logarithms — one series, two promises closed.
