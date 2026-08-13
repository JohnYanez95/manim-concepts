# Study-guides index — the authoring agent's retrieval map

One row per primitive: where it lives, which plan anchors its numbers come
from, and which bib keys it may cite (plan 012 R7). Agents resolve IDs from
this table instead of crawling; the build splices the content. Grows as
primitives land.

| Primitive | File | Parent series / status | Anchor keys | Bib key prefix |
| --- | --- | --- | --- | --- |
| counting-rules | `primitives/counting-rules.tex` | combinatorics (authored) | `001.raw81` | `combinatorics-` |
| ctc-alignment | `primitives/ctc-alignment.tex` | deep_learning alignment series (authored) | `001.raw81`, `001.paths15`, `001.astronomical`, `010.N.t5paths` | `deep_learning-` |
| dynamic-programming | `primitives/dynamic-programming.tex` | algorithms DP series (series-backed since plan 013; formerly guide-first — the seed that sprouted) | `001.raw81`, `001.paths15`, `001.astronomical` | `deep_learning-`, `algorithms-` |
| independence | `primitives/independence.tex` | probability independence series (authored) | `002.*` | `probability-` |
| conditional-probability | `primitives/conditional-probability.tex` | probability conditional series (authored) | `003.*` | `probability-` |
| bayes-rule | `primitives/bayes-rule.tex` | probability Bayes series (authored) | `004.*` | `probability-` |
| logarithms | `primitives/logarithms.tex` | algebra logarithms series (authored; carries the ln loan) | `005.*` | `algebra-` |
| e-and-ln | `primitives/e-and-ln.tex` | calculus e-and-ln series (authored; repays the loan) | `006.*` | `calculus-` |
| random-variables | `primitives/random-variables.tex` | probability random-variables series (authored) | `007.*` | `probability-` |
| softmax-likelihood | `primitives/softmax-likelihood.tex` | probability softmax series (authored) | `008.*` | `probability-` |
| derivative-toolkit | `primitives/derivative-toolkit.tex` | calculus derivatives series (authored) | `009.*` | `calculus-` |
| gradient-descent | `primitives/gradient-descent.tex` | calculus gradient-descent series (series-backed since plan 014; formerly guide-first — the second seed to sprout) | `010.M.*`, `010.K.NLL`, `001.paths15`, `014.basin.sqrt11` | `calculus-` |
| ctc-gradient | `primitives/ctc-gradient.tex` | deep_learning gradient series (authored) | `010.*`, `009.G.nllgradient` | `deep_learning-` |
| ctc-decoding | `primitives/ctc-decoding.tex` | GUIDE-FIRST (seeds the future beam-search series) | `012.dec.*` | `deep_learning-` |

Problem answer scripts (the solve-gate anchors, plan 012 R3) live in
`primitives/answers/` with underscored module names
(`counting_rules.py`, `ctc_alignment.py`) — every answer computed,
enumeration asserted against the formula it teaches.

Guide wrappers splice anchors too: `ctc-algorithm/guide.tex` uses
`010.K.P`. The once-reserved seed anchors are all spent now:
`010.K.NLL` in the gradient-descent chapter, `010.L.uniformP` and
`009.G.nllgradient` in the ctc-gradient chapter.

Guide-first primitives (no parent scenes; full research treatment before
authoring): `ctc-decoding` only (dynamic-programming graduated to
series-backed — plan 013; gradient-descent likewise — plan 014).

Machinery:

- `anchors.yaml` → `anchors.tex` via `tools/build_anchors.py` — verified
  numbers as `\anchor{plan.letter.slug}` macros.
- `references.bib` via `tools/sync_references.py` — the READMEs'
  human-gated lists, `verified={yes|no}` carried.
- `make study` builds every objective subdirectory's guide + solutions
  manual PDFs in place.
