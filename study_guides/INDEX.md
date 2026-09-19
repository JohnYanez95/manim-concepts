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
| ctc-decoding | `primitives/ctc-decoding.tex` | deep_learning decoding series (series-backed since plan 015; formerly guide-first — the third seed to sprout) | `012.dec.*` | `deep_learning-` |
| inclusion-exclusion | `primitives/inclusion-exclusion.tex` | probability inclusion–exclusion series (authored — the first new primitive since v1; no guide retrieves it yet, it seeds a future counting-and-chance objective) | `016.*` | `probability-` |
| cantor-diagonal | `primitives/cantor-diagonal.tex` | probability Cantor's-diagonal series (authored; no guide retrieves it yet — with inclusion–exclusion it seeds the counting-and-chance objective) | `017.*` | `probability-` |
| spectrum | `primitives/spectrum.tex` | signal_processing spectrum series (authored — chapter 1 of the `air-to-log-mel` objective, the first primitive written toward a second guide) | `019.*`, `005.log10two` | `signal_processing-` |

Objectives — one subdirectory each, its name the objective; every one
holds `guide.tex`, `solutions.tex`, the shared `manifest.tex` (the ordered
retrievals), `macros.tex` (the roadmap), `REFINEMENTS.md` and the two
committed outcome PDFs:

| Objective | Reads | Retrieves | Status |
| --- | --- | --- | --- |
| `ctc-algorithm/` | the CTC algorithm, in full (plan 012) | fourteen primitives, counting-rules → ctc-decoding, thirteen glue transitions | complete (v1, PR #13) |
| `air-to-log-mel/` | read a log-mel spectrogram with understanding (plan 019) | `spectrum`; planned, one per series as each lands: convolution, windowing → STFT → spectrogram, mel | one chapter of four; no glue until chapter 2 (a transition sits between two chapters) |

Problem answer scripts (the solve-gate anchors, plan 012 R3) live in
`primitives/answers/` with underscored module names
(`counting_rules.py`, `ctc_alignment.py`) — every answer computed,
enumeration asserted against the formula it teaches. `spectrum.py`
adds a second route: every pair cross-checked against `np.fft.rfft`
(X[k] = aₖ − i·bₖ — the chapter's sine sum is plus-signed).

Guide wrappers splice anchors too: `ctc-algorithm/guide.tex` uses
`010.K.P`, `air-to-log-mel/guide.tex` uses `019.R.readings`. The
once-reserved seed anchors are all spent now: `010.K.NLL` in the
gradient-descent chapter, `010.L.uniformP` and `009.G.nllgradient` in
the ctc-gradient chapter.

Guide-first primitives: none remain — dynamic-programming (plan
013), gradient-descent (plan 014) and ctc-decoding (plan 015) have
all graduated to series-backed. The mode stays legitimate (ADR 008):
a future guide may again draft chapters the screen later animates.

Machinery:

- `anchors.yaml` → `anchors.tex` via `tools/build_anchors.py` — verified
  numbers as `\anchor{plan.letter.slug}` macros.
- `references.bib` via `tools/sync_references.py` — the READMEs'
  human-gated lists, `verified={yes|no}` carried.
- `make study` builds every objective subdirectory's guide + solutions
  manual PDFs in place.
