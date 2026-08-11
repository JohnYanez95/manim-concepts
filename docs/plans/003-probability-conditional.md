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
- [ ] Phase 0: research reports received, scene design finalized below
- [ ] Phase 1: plan + config tuning + skeleton, `make check` green
- [ ] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
- [ ] Phase 3: README + wiki complete, `make test` green
- [ ] Phase 4: local review clean
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

## Verified technical anchors

(pinned when the source-verifier report lands)

## Scene design

(finalized after the research reports; the promised edges it must close:
renormalized area, multiplication rule, P(A|B) = P(A) rederivation with
P(B) > 0, and — if the design supports it — conditional independence
for the CTC residual)

## Known material gaps (for the PR body)

(named after scene design settles; Bayes at minimum stays queued)

## Review notes

(filled in at the end)
