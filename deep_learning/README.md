# Deep learning

## Scope

The alignment machinery of Connectionist Temporal Classification (Graves et
al., 2006): how a sequence model maps $T$ input frames to a shorter
transcript when nothing in the data says which frames belong to which
character — the training problem behind speech recognition, OCR and
handwriting recognition. The series builds the blank token and the collapse
map from their failure modes, treats a transcript's probability as a sum
over every alignment that spells it, and shows why that exponential sum is
computable on a small grid.

The counting prerequisites live in
[`combinatorics/`](../combinatorics/README.md): the
[multiplicative rule](../combinatorics/README.md#concepts) sizes the raw
path space here, and the partition scene's closing example — "counting the
alignments a sequence model can take" — promised exactly this topic.

A second series differentiates the loss the first one built: the backward
half of the trellis, posterior occupancy as the truth's soft target, the
identity — per-frame gradient is softmax output minus occupancy — and the
training dynamics that identity makes legible, through to why trained CTC
outputs go peaky and what a label prior changes.

A third series closes the road's loop at deployment: decoding as the
inverse problem, best-path reading of the frame favourites and the
construction where it hears nothing, the collapsed-prefix beam with
its two ledgers (the collapse map's grammar carried into the search),
the price of pruning made exact on one table, and the splice point
where an external language model multiplies in.

Deliberately **not** covered here:

- Probability foundations. Per-frame softmax outputs, products of
  independent probabilities and log-likelihood are *used* here without
  being taught. The unconditional product is taught in
  [`probability/`](../probability/README.md) (the independence series),
  and conditional independence — the form this topic actually assumes —
  in its conditional series (`WhenToCondition`). Softmax as a
  distribution and log-likelihood are now taught there too — the
  softmax/likelihood series scores this topic's own per-frame matrix
  and names the CTC loss in its closer. The calculus the gradient
  series leans on (chain and sum rules, the score function,
  ∂LSE = softmax, p − one-hot) is taught in
  [`calculus/`](../calculus/README.md)'s derivative toolkit — and
  the update rule the training beats run is now taught there too,
  by its gradient-descent series.
- Beam-search internals at scale. The decoding series builds the
  collapsed-prefix beam and prices pruning exactly on small tables;
  width/pruning dynamics at production scale, log-space ledger
  implementation and language-model fusion's tuning are named (one
  formula, one caption) but not taught — and Graves 2006's exact
  best-first "prefix search" is a different algorithm, deliberately
  off screen.
- Training realism. The gradient series' dynamics scenes use plain
  gradient descent on the worked example — no SGD noise, schedules or
  architecture effects; and the label prior is named as the peakiness
  fix, not built as its own loss variant.
- The encoder itself. RNN and transformer acoustic models are out of
  scope: CTC begins at the per-frame probability matrix, and so does this
  topic.

## Concepts

### ctc_alignment_manim.py

Watch in order. The first two scenes set up the problem and the one piece of
machinery CTC invents; the middle three climb the argument — a transcript's
probability is a sum over paths, that sum explodes combinatorially, and the
trellis computes it anyway; the last says where the tool applies and where
its assumptions forbid it.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheAlignmentProblem` | — | A transcript says *what* was said, not *when*: $T$ frames, $U$ characters, no per-frame labels. | Several different frame-to-letter alignments of the same clip are all consistent with the pair — the data cannot prefer one, so training must not require one. | Any monotonic sequence task where per-frame labels are infeasible to collect: speech, handwriting, OCR, keyword spotting. |
| 2 | `TheBlankToken` | $\mathcal{B}$: merge repeats, **then** drop $\varepsilon$ | CTC adds one output class $\varepsilon$ — "nothing new to emit". | Bare per-frame emission with repeat-merging can never write a double letter (HELLO → HELO) and forces held sounds to emit; $\varepsilon$ fixes both, and only the merge-then-drop order keeps it working. | Reading any CTC model's raw output stream; vocabulary design — blank and word-space are different tokens. |
| 3 | `ManyPathsOneWord` | $P(Y\mid X)=\sum_{\pi\in\mathcal{B}^{-1}(Y)}\prod_{t=1}^{T} y^t_{\pi_t}$ | A transcript's probability is the **sum** over every path that collapses to it, not the best path's probability. | All 15 paths for AB at $T{=}4$, enumerated and collapsed on screen; each is one product of per-frame probabilities, and no single one is the answer. | The loss ASR/OCR models actually train on; why greedy decoding can return the wrong transcript — the failure `TheModelHeardNothing` now runs in full at deployment. |
| 4 | `CountingAlignments` | $\lvert\mathcal{B}^{-1}(Y)\rvert=\binom{T+U}{T-U}$ | How big the sum from scene 3 really is. | The multiplicative rule gives $3^4{=}81$ raw paths at $T{=}4$, of which 15 spell AB; the repeat-free count is $\binom{T+U}{T-U}$, and at $T{=}100$, $U{=}50$ that is $\approx 2\times10^{40}$ — enumeration is dead on arrival. | Recognising when a sum must be reorganised rather than enumerated — the counting step `combinatorics/` promised, and the cliffhanger the trellis resolves. |
| 5 | `TheForwardTrellis` | $\alpha_t(s)=\bigl(\alpha_{t-1}(s)+\alpha_{t-1}(s{-}1)+\alpha_{t-1}(s{-}2)\bigr)\,y^t_{z'_s}$ | The exponential sum computed exactly on a $(2U{+}1)\times T$ grid. | Paths sharing a prefix share their $\alpha$; the grid's edges *are* the collapse semantics (the $s{-}2$ skip is legal only over a blank between different letters), and the two final nodes sum to the same 15 from scene 3. | The forward pass inside every CTC loss implementation; the same dynamic-programming move as the HMM forward algorithm — now named for what it is by [`algorithms/`](../algorithms/README.md)'s `TheTrellisWasAMemo` — run in log space in practice, since the raw product dies fast (float32: 46 frames at p = 0.1; see [`algebra/`](../algebra/README.md)). |
| 6 | `WhenToUseIt` | — | Which problems CTC fits, and which its assumptions forbid. | Monotonic alignment, output no longer than input, and per-frame conditional independence are exactly the trellis's shape — break one and the grid no longer describes the task. | Choose CTC for monotonic transduction; reach for attention when outputs reorder (translation); add an external language model because independence leaves language on the table — `TheLoopClosed` now shows exactly where it splices in; never read spike timing as segmentation — the gradient series' `WhyTheSpikesAppear` now supplies the why. |

Renders are numbered to match, so a directory listing plays in the same
order: `01_TheAlignmentProblem.mp4` … `06_WhenToUseIt.mp4`.

Render them:

```bash
uv run python deep_learning/ctc_alignment_manim.py            # all six, 1080p60
uv run python deep_learning/ctc_alignment_manim.py --list
uv run python deep_learning/ctc_alignment_manim.py -s TheForwardTrellis -q draft
```

See the [root README](../README.md) for the full flag list.

### ctc_gradient_manim.py

The gradient of the loss the alignment series built. Scenes 1–3 construct
the object the derivative needs (the backward trellis, the constant
column, occupancy); 4–5 differentiate, landing the identity the softmax
and derivative closers promised on screen (and the alignment series
queued in Ideas); 6–7 watch the identity during training —
Graves' error-signal arc made countable, then the peakiness mechanism.
Every on-screen number traces to
[plan 010](../docs/plans/010-ctc-gradient.md)'s verification pass (exact
rational arithmetic, two independent routes).

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheOtherHalfOfTheTrellis` | $\beta_T(s)=1$ at the two final states, else $0$; $\beta_t(s)=\sum_i \beta_{t+1}(s{+}i)\,y^{t+1}_{z'_{s+i}}$ | $\alpha$ answered "how did we get here?"; $\beta$ answers "how do we finish?" — the same grid, swept against the arrows. | Unit weights first: the backward counts mirror the forward counts (this example's palindromic symmetry, not a theorem), and the ledger cut — $\alpha$'s column pockets frame $t$'s emission, $\beta$ starts at $t{+}1$ — keeps every emission counted exactly once. | The backward half of forward–backward — the HMM lineage (Rabiner 1989) that every CTC implementation inherits. |
| 2 | `PathsThroughACell` | $P(Y\mid X)=\sum_s \alpha_t(s)\,\beta_t(s)$ — for any $t$ | $\alpha\cdot\beta$ is the probability of the truth's paths through a cell, and every column of products sums to the same $P$. | Ways in times ways out — 2 × 4 = 8 of the 15 paths cross (t=2, A), the multiplicative rule now carrying probability; every path crosses every column exactly once, so the sweep returns 15 four times at unit weights and 0.4877 four times on the real matrix. | The constant column is the bookkeeping self-check (a double-counted emission scales its column visibly) and the identity the gradient is about to lean on. |
| 3 | `WhereTheTruthSpendsItsTime` | $\gamma_t(s)=\dfrac{\alpha_t(s)\,\beta_t(s)}{P(Y\mid X)}$ | Divide each column by its own sum and it becomes a distribution: where the truth spends frame $t$ — "how often the truth used each cell", now an object. | Each path occupies exactly one cell per frame, so columns sum to 1 — the divide-by-P is the conditional series' renormalized slice, said on screen; blank's three rows fold into one class ($\mathrm{lab}$, drawn once); rows are expected dwell times, not probabilities (A holds 1.7578 of the 4 frames — the balance point returns); at uniform outputs $\gamma$ collapses to path counts over 15, and the closer stands a $\gamma$ column beside the one-from-N bar — the target, gone soft. | The soft alignment implementations actually compute — Baum–Welch's E-step object, and the soft target the gradient is about to hand the softmax. |
| 4 | `TheSensitivityOfTheSum` | $\dfrac{\partial L}{\partial \ln y_t(k)} = -\gamma_t(k)$ | Nudge one cell's log-probability and the loss moves by exactly that cell's occupancy. | Each path uses frame $t$ exactly once, so $P$ is linear in any one cell; scaling the cell by $(1{+}h)$ scales every path through it together, so shares add into occupancy — the smooth max's shares at path scale, with the score function doing the bookkeeping. | The sensitivity-of-a-log-sum reading that turns "differentiate this monster" into "read off a share" — the exact move that differentiated LSE. |
| 5 | `SoftmaxMinusOccupancy` | $\dfrac{\partial L}{\partial u_t(k)} = y_t(k) - \gamma_t(k)$ | The identity: the per-frame gradient of the CTC loss is softmax output minus occupancy. | The log-softmax Jacobian $\delta_{jk}-y_k$ plus the constant column $\sum_j \gamma_j = 1$ collapse the chain in two lines; on the scored matrix every gradient row sums to 0; let one path survive and $\gamma$ snaps one-hot — $p-\text{one-hot}$ as the degenerate case, Bridle's "one-from-N target" gone soft. | The backward pass CTC implementations hard-code — which is also the trap: anything but a true log-softmax input keeps the loss right while the gradient goes silently wrong. |
| 6 | `TheErrorSignalLearns` | — | The training error signal starts diffuse, localises around predictions, then virtually disappears (Graves et al. 2006, figure 4 — rebuilt on countable frames). | With uninformative outputs the push $\gamma - y$ is the target's path counts in pure fractions; three snapshots of one gradient descent (loss 0.7181 → 0.1602 → 0.0356) on one shared scale localise and die; frame 3 settles mixed at (0.032, 0.218, 0.750) because all three of its choices collapse to AB — $y$ matches $\gamma$ out of indifference, not certainty. | Reading error-signal and training-curve plots: a vanished gradient does not mean one-hot outputs — and the walk itself, this exact trajectory re-read, is now taught by `calculus/`'s `TheRoadsOwnWalk`. |
| 7 | `WhyTheSpikesAppear` | — | Peaky outputs are topology plus weight sharing, not acoustics. | Blank's head start is counted with the input never entering: A 21, B 21, ε 18 at T=4 (the fair boundary case), blank ahead for good from T=5, share → 2/3 in the one-letter limit; a single softmax forced to serve every frame descends to blank-everywhere at T=12 — (0.0919, 0.0919, 0.8162), an empty decode, 100% error at a local optimum — while free per-frame outputs never spike. | Why a label prior fixes peaky CTC; spikes are a steerable training artifact, never timestamps — and the identity's family (one-hot cross-entropy, distillation, CTC) is one gradient shape with different targets. |

Renders are numbered to match: `01_TheOtherHalfOfTheTrellis.mp4` …
`07_WhyTheSpikesAppear.mp4`.

Render them:

```bash
uv run python deep_learning/ctc_gradient_manim.py            # all seven, 1080p60
uv run python deep_learning/ctc_gradient_manim.py --list
uv run python deep_learning/ctc_gradient_manim.py -s SoftmaxMinusOccupancy -q draft
```

### ctc_decoding_manim.py

Watch after both CTC series — the alignment series built the sum this
one searches, and the gradient series explains why trained outputs
make the cheap decoder usually right. The road's loop closes here:
train, decode, deploy.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheInverseProblem` | $Y^\* = \operatorname{argmax}_Y P(Y \mid X)$ | Nobody deploys a loss: a clip arrives with no reference transcript, and decoding — finding the transcript the model believes — is search, which training never had to do. | Training's loop had the transcript handed to it and only ever scored it; deployment inverts the arrow, and the honest target is the argmax over transcripts of the alignment series' sum over paths — a space that grows exponentially, so the series' two decoders are both approximations (Graves: "we do not know of a general, tractable decoding algorithm"). | Framing every decoding choice that follows: the cheap approximation (best-path) and the honest one (the beam) are answers to this search problem, not afterthoughts. |
| 2 | `TheFrameFavourites` | $h(x) \approx \mathcal{B}(\text{argmax per frame})$ | Best-path (greedy) decoding: take each frame's favourite symbol, collapse through B — T lookups and one pass, "trivial to compute … not guaranteed to find the most probable labelling". | On y₁ = (.5, .2, .3), y₂ = (.4, .3, .3), y₃ = (.2, .3, .5) the favourites read A, A, ε → "A", and the 27-path leaderboard's top masses agree: A leads at 0.3170 with AB second at 0.2610 — with one favourite chain clearly ahead, mass concentrates and the max speaks for the sum (the per-frame matrix is the object the softmax series scored, its argmaxes now ringed). | The production decode: when a model is confident, greedy is fast and right — and knowing exactly why it can be trusted is what makes its failure mode legible. |
| 3 | `TheModelHeardNothing` | $0.36 \text{ vs } 0.16 + 0.24 + 0.24 = 0.64$ | Sum-vs-max returns in its deployment costume: greedy crowns the heaviest single path while the truth belongs to the transcript whose team of paths is heaviest. | Two frames at y(A) = 0.4, y(ε) = 0.6: greedy takes the blank twice and announces the empty transcript (mass 0.36) while A pools three paths to 0.64 — read correctly the model heard an A, read greedily nothing; the dial y(ε) = q shows a whole band (½ < q < 1/√2) where greedy lies (at q = 0.7: 0.49 vs 0.51) — the blank must win by a √2 margin. | Trained CTC outputs are peaked and blank-heavy (the gradient series' delivered result), so greedy usually gets away with it — and the hedging inputs, accents and noise, are exactly where it stops. |
| 4 | `SearchTheTranscripts` | — | Searching transcripts without enumeration: the beam's candidates must be collapsed prefixes, not paths, and path masses pouring into one prefix merge. | A beam over paths wastes its slots on duplicate spellings of one transcript and splits its mass — sum-vs-max sneaks back at beam scale; relabel the candidates to collapsed prefixes and three streams (new letter, blank extension, silent merge) converge on prefix A, pooling 0.64 against greedy's 0.36 — the dynamic-programming move `algorithms/` named, on a pruned frontier; width 2 keeps every candidate that carries mass here (AA sits at exactly zero), so the answer is exact. | The standard compromise for exponential output spaces — and the reason CTC beam search is the forward recurrence's sibling, not a generic tree search. |
| 5 | `TheTwoLedgers` | $P(\text{prefix}) = p_b + p_{nb}$ | A prefix must carry two masses — paths ending in blank and paths ending in its last letter — because the collapse map gives the two halves different futures. | The repeat fork: proposing A onto prefix A routes only the p_b share into a genuine AA (a blank stood between); the p_nb share merges silently back — and collapsing the two numbers into one forces wrong answers, not slow ones: on coin frames (y = ½, T = 3) the true P(AA) = 1/8 but a one-ledger beam reports 3/8, crediting AAε and εAA, both of which truly collapse to A; the unpruned ledgers land digit for digit on the trellis's final column — the beam is the forward recurrence wearing a search harness, initialised at p_b(∅) = 1. | The correctness detail every real CTC decoder implements (Hannun et al. 2014's Algorithm 1) — and the reason production code that drops it silently overcounts double letters. |
| 6 | `ThePriceOfPruning` | — | Pruning is the beam's only approximation, and its bill can be itemised exactly. | On frames (A .5, B .1, ε .4) ×2 then (A .5, B .4, ε .1): the exact posterior crowns A at 0.37, greedy agrees, width 2 agrees (kept total exactly 0.37 — no A-feeder was ever pruned); width 1 returns AB — cutting ∅ at frame 1 deleted half of all mass, including a fifth of everything that was bound for A, and inside the beam AB (0.18) overtakes A (0.17) — wrong, and wrong differently from greedy. | Reading beam output honestly: kept totals understate posteriors, wider beams pay off exactly where mass hedges, and a pruning failure is not a greedy failure. |
| 7 | `TheLoopClosed` | $Q(c) = \log P(c \mid x) + \alpha \log P_{\mathrm{lm}}(c) + \beta\,\mathrm{word\_count}(c)$ | The decision rule mapped — greedy when peaked, the beam when hedging — and the beam's per-extension scoring is the natural splice for an external language model. | The blend is tuned, not derived (α, β by cross-validation; beams 1000–8000 in Deep Speech), patching exactly the hole the alignment series declared: frames independent given the input, language left on the table; production ledgers run in log space with the log-add the logarithms series taught (the merge is a log-add, never a max); and the loss never paid for timing, so spike positions are not calibrated segment boundaries — a decoder returns what, forced alignment answers when. | Deploying CTC systems: choose the decoder by the output's shape, splice the language model at the extension, and never read spikes as timestamps — the road's loop closes: train, decode, deploy. |

Renders: `01_TheInverseProblem.mp4` …
`07_TheLoopClosed.mp4`.

```bash
uv run python deep_learning/ctc_decoding_manim.py
uv run python deep_learning/ctc_decoding_manim.py --list
```

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of a research pass — the alignment series'
([`docs/plans/001-ctc-alignment.md`](../docs/plans/001-ctc-alignment.md))
or the gradient series'
([`docs/plans/010-ctc-gradient.md`](../docs/plans/010-ctc-gradient.md)) —
started unchecked, and was then opened, confirmed, and ticked by the
maintainer (plan-010 pass: 2026-08-12). Future entries start unchecked
until a human does the same.

- [X] [Graves et al., 2006 — Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf)
      — the original ICML paper; source of the collapse map, the forward
      recurrence, and the trellis figure (whose example target is CAT).
- [X] [Hannun, "Sequence Modeling with CTC", Distill 2017](https://distill.pub/2017/ctc/)
      — the canonical visual explanation; the alignment table, trellis and
      counting arguments here follow its lineage.
- [X] [Scheidl, "An Intuitive Explanation of CTC"](https://harald-scheidl.medium.com/intuitively-understanding-connectionist-temporal-classification-3797e43a86c)
      — the smallest fully numeric loss example (one letter, two frames).
- [X] [Ogun, "Breaking down the CTC Loss"](https://ogunlao.github.io/blog/2020/07/17/breaking-down-ctc-loss.html)
      — worked forward/backward grids for "door"; states the skip rule
      precisely.
- [X] [Stanford CS224S, lecture 10: end-to-end ASR](https://web.stanford.edu/class/cs224s/semesters/2022-spring/lecture-slides/224s.22.lec10.pdf)
      — CTC in context: language-model fusion and the comparison with
      attention models.
- [X] [CMU 11-785, recitation 8: CTC](http://www.cs.cmu.edu/afs/cs/user/bhiksha/WWW/courses/deeplearning/Fall.2018/www/recitations/recitation8.pdf)
      — the "CTC is a family of losses" framing that demystifies the blank.
- [X] [HuggingFace Audio Course, ch. 3: CTC](https://huggingface.co/learn/audio-course/en/chapter3/ctc)
      — practical anchors: real frame rates, and blank vs. word-space in
      real vocabularies.
- [X] [Zeyer et al., 2021 — Why does CTC result in peaky behavior?](https://arxiv.org/abs/2105.14849)
      — the analysis behind the spiky outputs mentioned in `WhenToUseIt`;
      the gradient series' scene 7 animates its mechanism (uniform-init
      posterior = alignment counts, blank's topological dominance, the
      feed-forward 100%-error theorem, the label-prior fix). arXiv
      preprint, cited as such on screen.
- [X] [Alex Graves, *Supervised Sequence Labelling with RNNs* (2012)](https://www.cs.toronto.edu/~graves/preprint.pdf)
      — Springer 2012, author's preprint. Chapter 7: the emission-free
      β convention the gradient series adopts (eqs. 7.12–7.13), the
      division-free p = Σαβ (7.26), the identity ∂L/∂a = y − occupancy
      (7.34), and the log-scale-over-rescaling advice (§7.3.1).
- [X] [Jason Eisner, the forward–backward spreadsheet (ACL-02)](https://www.cs.jhu.edu/~jason/papers/eisner.tnlp02.pdf)
      — "An Interactive Spreadsheet for Teaching the Forward-Backward
      Algorithm": the classroom-proven constant-column checksum scene 2
      is built around, and posterior-as-reconstruction pedagogy.
- [X] [Lawrence R. Rabiner, the HMM tutorial (Proc. IEEE, 1989)](https://www.cs.sjsu.edu/~stamp/RUA/Rabiner.pdf)
      — Proc. IEEE 77(2):257–286: γ = αβ/P as expected state occupancy,
      the HMM forward–backward lineage scene 1 name-drops (cited as
      printed in Graves 2006; no direct quotes on screen).
- [X] [Peter Bell, Edinburgh ASR lecture 13: CTC (2024-25)](https://www.inf.ed.ac.uk/teaching/courses/asr/2024-25/asr13-ctc.pdf)
      — "End-to-end systems 1: CTC"; a modern course treatment
      consulted in the pedagogy pass — evidence the gradient story is
      the untaught half (stops at the forward algorithm).
- [X] [Mark Hasegawa-Johnson, UIUC ECE 537 lecture 20: CTC (2022)](https://courses.grainger.illinois.edu/ece537/fa2022/slides/lec20.pdf)
      — second course data point from the pedagogy pass, same finding.
- [X] [PyTorch Forums, "Question about CTC gradient"](https://discuss.pytorch.org/t/question-about-ctc-gradient/65624)
      — answered by Thomas Viehmann; the real logits-vs-log-probs
      confusion scene 5's when-useful beat addresses.
- [X] [PyTorch issue #122243, non-normalized CTC inputs](https://github.com/pytorch/pytorch/issues/122243)
      — forward loss right, backward silently wrong unless the input is
      a true log-softmax; scene 5's implementation trap.

From the plan-015 research pass
([`docs/plans/015-deep-learning-ctc-decoding.md`](../docs/plans/015-deep-learning-ctc-decoding.md)),
unverified until a human ticks them:

- [X] [Hannun, Maas, Jurafsky and Ng, "First-Pass LVCSR" (2014)](https://arxiv.org/abs/1408.2873)
      — Awni Y. Hannun, Andrew L. Maas, Daniel Jurafsky and Andrew
      Y. Ng, "First-Pass Large Vocabulary Continuous Speech
      Recognition using Bi-Directional Recurrent DNNs": Algorithm 1,
      the origin
      of the p_b/p_nb prefix beam; init p_b(∅) = 1; the beam-width
      bound the complexity beat is read from.
- [X] [Awni Hannun, "Example CTC Decoder in Python" (gist)](https://gist.github.com/awni/56369a90d03953e370f3964c826ed4b0)
      — the reference implementation everyone copies; the merging
      case commented; log-space ledgers with a stable logsumexp.
- [X] [Awni Hannun et al., "Deep Speech: Scaling up end-to-end speech recognition"](https://arxiv.org/abs/1412.5567)
      — §2.2's Q(c) language-model-fusion objective scene 7 quotes,
      α, β set by cross-validation, beams 1000–8000.
- [X] [Lasse Borgholt, "CTC Networks and Language Models: Prefix Beam Search Explained"](https://medium.com/corti-ai/ctc-networks-and-language-models-prefix-beam-search-explained-c11d1ee23306)
      — the implementation-ordered walkthrough (the camp the series
      deliberately does not follow) and pruned-prefix recovery.
- [X] [Harald Scheidl, "Beam Search Decoding in CTC-trained Neural Networks"](https://harald-scheidl.medium.com/beam-search-decoding-in-ctc-trained-neural-networks-5a889a3d85a7)
      — the smallest numeric greedy failure (0.48 vs 0.52) and the
      Pb/Pnb update equations; its numbers deliberately not reused
      (near-misses of the anchored construction).
- [X] [Ameya Mahabaleshwarkar, CMU 11-785 F22 recitation 9: CTC decoding](https://deeplearning.cs.cmu.edu/F22/document/recitation/Recitation9/rec9_beamsearch.pdf)
      — greedy → exhaustive → beam ordering; ships the one-ledger
      tree (documented evidence the single-mass presentation ships
      in respected courses; a suspected typo noted in the plan).
- [X] [Zeyu Zhao, "CTC Prefix Beam Search Decoding Algorithm with Language Model"](https://zhaozeyu1995.github.io/CTC-Prefix-Beam-Search-Decoding-Algorithm-with-Language-Model/)
      — code-first case enumeration in raw probability space; the
      cautionary foil for the log-space caption.
- [X] [Ryan Leary, TensorFlow PR #15586](https://github.com/tensorflow/tensorflow/pull/15586)
      — "Remove invalid merge_repeated option from CTC beam
      decoder": the path/prefix conflation fossilized in an API.
- [X] [TensorFlow issue #21051](https://github.com/tensorflow/tensorflow/issues/21051)
      — width-1 beam ≠ greedy (the beam still merges and keeps two
      ledgers), correcting the API docs; no single credited author.
- [X] [Philipp V. Rouast and Marc T. P. Adam, "Single-stage intake gesture detection…"](https://arxiv.org/abs/2008.02999)
      — no improvement beyond beam width 3 on their task (seen via
      search excerpt in the research pass, not verified on-page).
- [X] [Andrei Andrusenko et al., "Fast Context-Biasing" (2024)](https://arxiv.org/abs/2406.07096)
      — beam-without-LM tracks greedy on peaked outputs (seen via
      search excerpt in the research pass, not verified on-page).

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- ~~Beam search over collapsed prefixes~~ — delivered by the decoding
  series: `SearchTheTranscripts` relabels the candidates to collapsed
  prefixes with the merge on screen, `TheTwoLedgers` forces the two
  probabilities from the collapse map (and prices the one-ledger
  overcount 3/8 vs 1/8), `ThePriceOfPruning` itemises the beam's one
  approximation. What stays unbuilt at scale is a Scope exclusion
  (the beam-internals bullet), not a queue entry.
- ~~Training dynamics~~ — delivered by the gradient series:
  `TheErrorSignalLearns` rebuilds Graves fig. 4's arc countable, and
  `WhyTheSpikesAppear` delivers blank dominance and the peakiness
  mechanism.
- ~~The gradient identity~~ — delivered: `SoftmaxMinusOccupancy` lands
  ∂L/∂u = y − γ, receiving `TheSmoothMaxsShares`' p − one-hot as the
  one-path degeneration.
- A label-prior CTC variant built as its own loss — scene 7 names it as
  the peakiness fix (Zeyer et al.); constructing it, with the
  prior-corrected trellis, is unbuilt. It is a Bayes move — the
  prior-and-renormalize step `probability/`'s `TheBestExplanation`
  named — so a future build has its grounding waiting.
- ~~Log-space computation~~ — delivered by
  [`algebra/`](../algebra/README.md)'s `TheUnderflowCliff`: the
  0.1³²⁴ hard zero, the −324 log sum, and Graves' log-add identity
  for the trellis's additions (float32 dies at 46 frames).
- Forced alignment done right: label priors and alignment-aware variants,
  since raw CTC spikes are not timestamps.
