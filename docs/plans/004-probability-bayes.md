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
- [ ] Phase 0: research reports received, scene design finalized below
- [ ] Phase 1: plan + CLAUDE.md + skeleton, `make check` green
- [ ] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
- [ ] Phase 3: README + wiki complete, `make test` green
- [ ] Phase 4: local review clean
- [ ] Phase 5: PR open, drafts cleaned, 1080p60 render verified

## Verified technical anchors

(pinned when the source-verifier report lands)

## Scene design

(finalized after the research reports; the promises it must close: walk
through the front door left at the end of `TwoSlicesOneSquare`, complete
the prevalence pair, do Monty Hall honestly with the host's protocol per
Rosenthal, and deliver the odds form / waterfall the Ideas queue names)

## Known material gaps (for the PR body)

(named after scene design settles)

## Review notes

(filled in at the end)
