# Plan 003: `probability/` — conditional probability series

Branch: `feat/probability-conditional`, cut from updated `main` (4c3cc1c,
the plan-002 merge).
Started: 2026-08-11.

The second probability series, promised by plan 002 and carried as
promised edges in the wiki: P(A|B) as renormalized area, the
multiplication rule, independence rederived as P(A|B) = P(A) with
P(B) > 0, and the conditional-independence residual the CTC bridge still
owes. Also riding along: CodeRabbit configuration tuning (research in
flight) so reviews stop re-litigating the repo's bookkeeping.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research: pedagogy + source verification (agents in flight); CodeRabbit tuning research | Scene design written below |
| 1 | Plan committed, `.coderabbit.yaml` tuning, module skeleton, README updates | `make check` |
| 2 | Scenes at `--quality draft`; renders verified (count, names, ffprobe, frames) | Draft renders verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated, root README | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render |

## Checklist

- [x] Branch from updated main
- [x] Phase 0: research reports received, scene design finalized below
- [x] Phase 1: plan + config tuning + skeleton, `make check` green
  (config committed separately at 76f1348; skeleton includes the
  `WhenToCondition` rename to avoid a same-README class-name collision
  with the sibling module's `WhenToUseIt`)
- [x] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
  (6 distinct numbered files; durations 24–42 s; 22 extracted frames
  reviewed; two lint stalls caught by PIPESTATUS before any render ran;
  one contrast fix — the dim beat's discarded half now WARM at 0.45
  against B at 0.4 — re-rendered and re-verified)
- [x] Phase 3: README + wiki complete, `make test` green (graph: both
  promised edges into `conditional-probability` flipped to delivered
  with on-screen citations; Bayes front-door promise recorded; device
  lineages extended; log entry appended)
- [x] Phase 4: local review clean — the tuned config's first trial
  returned ONE finding (down from 4 and 8 in plan 002's rounds), zero
  bookkeeping noise, and it was a real content catch: scene 5's
  perpendicular bands drew an independent pair while making a point
  about dependence; fixed with a stepped A. The incremental audit
  diffed 11 commits from the stamp, no full crawl, findings applied
  (stale deep_learning Scope again, the counting→conditional edge,
  three inherited devices, LOTP↔trellis clause, explaining-away seed).
- [ ] Phase 5: PR open, drafts cleaned, 1080p60 render verified

## CodeRabbit tuning (Phase 1, applied from the research report)

- YAML comments never reach the model (schema-parsed config) — the old
  ADR-pointer comment was dead weight for three rounds. Guidance now
  lives in channels the model receives: `tone_instructions` (global),
  `path_instructions` (per-path), and CLAUDE.md (auto-read by the cloud
  bot as code guidelines).
- `docs/wiki/log.md` excluded outright (`path_filters`) — append-only
  history has zero review value.
- New `path_instructions`: ADRs are settled decisions (do not
  re-raise); plans pin digests per ADR 007; the wiki is agent-maintained
  machinery, not prose; agent definitions are prompts, not docs.
- The checkbox instruction was the root cause of the tick war: it
  ordered flagging any tick in an AI-co-authored commit, which is where
  the maintainer's ticks land. Rewritten to ADR 006's actual protocol —
  ticks with a stated human verification are legitimate; flag only
  ticks with no such record.
- Caveat from the research: the CLI may not honor `path_filters` /
  `path_instructions` locally (undocumented); verify empirically with
  `coderabbit review --show-prompts` on the next local pass. `profile:
  "quiet"` is the next lever if noise persists.

## Verified technical anchors (from the source-verifier report)

Methods: [quoted] verbatim from source · [enumerated] exact fractions by
exhaustive enumeration · [two-route] two independent computations agree.

- Definition [quoted, Blitzstein & Hwang Def 2.2.1]: P(A|B) =
  P(A∩B)/P(B), defined only for P(B) > 0; undefined at P(B) = 0 (the
  limiting/Borel–Kolmogorov story stays out of scope).
- Multiplication rule [quoted, B&H Thm 2.3.1]: P(A∩B) = P(B)P(A|B) =
  P(A)P(B|A); chain rule [Thm 2.3.2] with the "n! theorems in one"
  remark. Check [two-route]: three hearts = 13/52·12/51·11/50 = 11/850
  = C(13,3)/C(52,3).
- Independence rederivation: P(A|B) = P(A) ⟺ product form ⟺ P(B|A) =
  P(B) when both defined — symmetry is a one-line divide.
- Continuity with plan 002 [enumerated, matches scene 3's fractions
  exactly]: P(even | {1,2,3,4}) = 2/4 = 1/2 = P(even) — the jewel
  through the conditional lens; P(even | {1,2,3}) = 1/3 ≠ 1/2 — the
  dependent pair (1/6 ≠ 1/4 is this, rescaled by P(B) = 1/2). Biased
  coda reusable: P(A|B) = 1/2 ≠ 4/7 = P(A).
- Asymmetry example [enumerated, own construction]: 24-cell grid,
  4 sick / 12 positive / 3 overlap: P(B|A) = 3/4 vs P(A|B) = 1/4 —
  same overlap, different denominators. (Starker 10×10 variant: 9/10
  vs 1/10.)
- Law of total probability [quoted, B&H Thm 2.3.6]; on the repo's own
  die: P(even) = 1/3·1/2 + 2/3·1/2 = 1/2 over the {1,2,3}/{4,5,6}
  partition.
- Bayes as one line [quoted, Thm 2.3.3]: equate the two multiplication
  expansions, divide by P(B) — teaser only.
- Conditional independence [quoted def; counterexamples enumerated,
  own constructions]: CI ⇏ independence (fair vs double-headed coin:
  CI given the coin, but P(A∩B) = 5/8 ≠ 9/16); independence ⇏ CI
  (two fair flips given "exactly one head": 0 ≠ 1/4 — explaining
  away). CTC's assumption verbatim [Graves 2006]: outputs conditionally
  independent "given the internal state of the network"; equivalent to
  given-the-input via the deterministic network map — the repo's
  phrasing is the standard restatement, not the paper's literal words.
- Renormalization picture: A ↦ P(A|B) is itself a probability measure
  [quoted, LibreTexts] — restricting to B and dividing by area(B) is
  the definition restated, not an analogy. B&H: "all probabilities are
  conditional."
- Flags: B&H quotes come from a chapters-1–2 excerpt (its §2.5 not
  quotable); Bayes positivity implicit in B&H, explicit in LibreTexts;
  CI counterexamples are verified constructions, not citations.

## Scene design (finalized from the two research reports)

Module: `probability/conditional_probability_manim.py`, six scenes.
Consensus spine (3b1b, Seeing Theory, MIT 18.05, Blitzstein):
restriction first, formula last; multiplication rule as the definition
rewritten; LOTP before trees-as-notation; independence rederived; end
one visible step short of Bayes. Square primary, trees second (the
research literature's finding), natural frequencies wherever people are
counted. Monty Hall deferred to the Bayes series by name (protocol
sensitivity per Rosenthal); the two-children square carries the
protocol lesson instead.

1. `TheRestrictedSquare` — restriction first: three coins (1/8 → 1/4
   given first is H, by recount), then the B-band on the unit square:
   dim what B rules out (WARM — the divide-out lineage), stretch the
   band to a fresh unit square (honest only for straight bands — the
   uniform stretch is exactly ×1/P(B)). Definition arrives last, with
   P(B) > 0. "Conditional probabilities are probabilities."
2. `IndependenceRevisited` — the continuity centerpiece: the stepped
   cut finally named. Height of A inside the B-band is P(A|B); the
   step flattening is P(A|B) = P(A) — independence rederived as an
   equivalent characterization on P(B) > 0, never as the definition.
   The die jewel through the lens: P(even|{1,2,3,4}) = 1/2 ✓;
   P(even|{1,2,3}) = 1/3 ✗ — one pip, again. Mutually exclusive
   re-read: P(A|B) = 0, maximal information. Both squares stay on
   screen: conditioning never mutates the original measure.
3. `TheMultiplicationRule` — the definition rewritten:
   P(A∩B) = P(B)·P(A|B), a rectangle identity ("souped up rule of
   product" — the combinatorics bridge speaks it back). The aces
   payoff: plan 002's 1/221 finally gets its license,
   (1/13)·(3/51). Chain rule, "n! theorems in one". Time-reversal
   beat: P(S₁|S₂) = 12/51 — conditioning is re-measuring, not
   re-running.
4. `TotalProbabilityAndTrees` — LOTP as "add up the columns" on the
   partitioned square (die partition: P(even) = 1/3·1/2 + 2/3·1/2);
   then the square morphs into the tree: branches carry conditional
   probabilities, leaves are intersections, LOTP sums the circled
   leaves; one tree labelled precisely (the R₂-really-means-R₁∩R₂
   ambiguity, shown once). Urn: P(R₂) = 5/7 two ways.
5. `TwoSlicesOneSquare` — the inversion: same overlap, two
   denominators (vertical vs horizontal slice). Quick exact hit:
   P(first H | five H) = 1 vs P(five H | first H) = 1/16. Centerpiece:
   the integer-exact prevalence pair — same 9/10-sensitive,
   1/10-false-positive test; prevalence 1/10 → P(sick|+) = 9/18 = 1/2;
   prevalence 1/100 → 9/108 = 1/12 — natural-frequency counts of
   whole people, the prior as visible column width. Ends at Bayes'
   front door: P(A)P(B|A) = P(B)P(A|B), named and left for the next
   series.
6. `WhenToCondition` — level 3 (renamed from the house `WhenToUseIt`
   pattern: the sibling module in the same README already owns that
   class name, and the contract test parses tables by scene name).
   Where conditioning is the tool: sequential
   draws (the shrinking pool now has a name), diagnosis (keep
   sensitivity and specificity as two numbers, never one "accuracy"),
   and what you actually condition on: the two-children four-cell
   square with the announcement protocol drawn in (1/2 vs 1/3 — the
   conditioning event includes how you learned it). Closes the CTC
   edge: conditional independence as a third thing — the two-coin
   example (marginally dependent, 41/100 ≠ 1/4; independent given the
   coin) is the common-cause beat made quantitative, and "given the
   input" is what CTC assumes. Monty Hall named and deferred.

Deliberately deferred: Bayes' rule as a series (odds form, waterfall,
Monty Hall done honestly), the partition form of Bayes, and
Borel–Kolmogorov / conditioning on measure-zero events (honest silence
beats false generality).

## Known material gaps (for the PR body)

- **Bayes' rule** — now the repo's most heavily promised target,
  promised on screen twice (`TwoSlicesOneSquare`'s front door,
  `WhenToCondition`'s Monty deferral) plus four documents. The next
  probability branch; this series handed it four seeds (the front-door
  identity, the cohort chips to complete, the protocol lesson, the
  Rosenthal reference).
- Softmax as a distribution, likelihood, log-likelihood — the remaining
  half of the CTC bridge, still queued.
- The explaining-away counterexample (independence ⇏ conditional
  independence: two fair flips given "exactly one head", 0 ≠ 1/4) is
  verified in this plan's anchors but unbuilt — seed for the Bayes or a
  graphical-models series.

## Review notes

- Maintainer caught a motion-discipline violation frame-sampling missed
  (scene 1's news/caption overlap) — fixed and the lesson recorded:
  extracted frames are spot checks, not proof of no-overlap between
  samples.
- Incremental connection audit: graph-first procedure held (11 commits
  diffed, changed files only); all findings applied; stamp advanced to
  23c47f2. Notable: deep_learning's Scope went stale the same way it
  did last audit — the promising document is never updated when its
  promise is delivered; watch for it every series.
- Tuned CodeRabbit, first trial: one finding, zero bookkeeping churn —
  the scene 5 stepped-A geometry catch, accepted. The config change
  (path_instructions + tone + the checkbox-protocol rewrite) did what
  the research said it would.

Follow-up (next branch): Bayes' rule — the repo's strongest open
promise, seeded four ways by this series.
