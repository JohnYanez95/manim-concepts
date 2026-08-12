# Study-guides index — the authoring agent's retrieval map

One row per primitive: where it lives, which plan anchors its numbers come
from, and which bib keys it may cite (plan 012 R7). Agents resolve IDs from
this table instead of crawling; the build splices the content. Grows as
primitives land.

| Primitive | File | Parent series / status | Anchor keys | Bib key prefix |
| --- | --- | --- | --- | --- |
| counting-rules | `primitives/counting-rules.tex` | combinatorics (authored, phase 2) | `001.raw81` | `combinatorics-` |
| ctc-alignment | `primitives/ctc-alignment.tex` | deep_learning alignment series (authored, phase 2) | `001.raw81`, `001.paths15`, `001.astronomical`, `010.N.t5paths` | `deep_learning-` |

Problem answer scripts (the solve-gate anchors, plan 012 R3) live in
`primitives/answers/<primitive>.py` — every answer computed, enumeration
asserted against the formula it teaches.

Guide-first primitives (no parent scenes; full research treatment before
authoring): `dynamic-programming`, `gradient-descent`, `ctc-decoding`.

Machinery:

- `anchors.yaml` → `anchors.tex` via `tools/build_anchors.py` — verified
  numbers as `\anchor{plan.letter.slug}` macros.
- `references.bib` via `tools/sync_references.py` — the READMEs'
  human-gated lists, `verified={yes|no}` carried.
- `make study` builds every objective subdirectory's guide + solutions
  manual PDFs in place.
