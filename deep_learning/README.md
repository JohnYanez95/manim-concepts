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

Deliberately **not** covered here:

- Probability foundations. Per-frame softmax outputs, products of
  independent probabilities and log-likelihood are *used* here without
  being taught; they belong in a `probability/` topic that does not exist
  yet, which makes it the natural next series.
- Decoding at depth. Greedy decoding's failure appears in scene 3, but
  beam search over collapsed prefixes and language-model fusion are queued
  in Ideas, not built.
- The gradient and training dynamics — the backward pass, the
  softmax-minus-occupancy identity, and why trained outputs go peaky.
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
| 3 | `ManyPathsOneWord` | $P(Y\mid X)=\sum_{\pi\in\mathcal{B}^{-1}(Y)}\prod_{t=1}^{T} y^t_{\pi_t}$ | A transcript's probability is the **sum** over every path that collapses to it, not the best path's probability. | All 15 paths for AB at $T{=}4$, enumerated and collapsed on screen; each is one product of per-frame probabilities, and no single one is the answer. | The loss ASR/OCR models actually train on; why greedy decoding can return the wrong transcript. |
| 4 | `CountingAlignments` | $\lvert\mathcal{B}^{-1}(Y)\rvert=\binom{T+U}{T-U}$ | How big the sum from scene 3 really is. | The multiplicative rule gives $3^4{=}81$ raw paths at $T{=}4$, of which 15 spell AB; the repeat-free count is $\binom{T+U}{T-U}$, and at $T{=}100$, $U{=}50$ that is $\approx 2\times10^{40}$ — enumeration is dead on arrival. | Recognising when a sum must be reorganised rather than enumerated — the counting step `combinatorics/` promised, and the cliffhanger the trellis resolves. |
| 5 | `TheForwardTrellis` | $\alpha_t(s)=\bigl(\alpha_{t-1}(s)+\alpha_{t-1}(s{-}1)+\alpha_{t-1}(s{-}2)\bigr)\,y^t_{z'_s}$ | The exponential sum computed exactly on a $(2U{+}1)\times T$ grid. | Paths sharing a prefix share their $\alpha$; the grid's edges *are* the collapse semantics (the $s{-}2$ skip is legal only over a blank between different letters), and the two final nodes sum to the same 15 from scene 3. | The forward pass inside every CTC loss implementation; the same dynamic-programming move as the HMM forward algorithm. |
| 6 | `WhenToUseIt` | — | Which problems CTC fits, and which its assumptions forbid. | Monotonic alignment, output no longer than input, and per-frame conditional independence are exactly the trellis's shape — break one and the grid no longer describes the task. | Choose CTC for monotonic transduction; reach for attention when outputs reorder (translation); add an external language model because independence leaves language on the table; never read spike timing as segmentation. |

Renders are numbered to match, so a directory listing plays in the same
order: `01_TheAlignmentProblem.mp4` … `06_WhenToUseIt.mp4`.

Render them:

```bash
uv run python deep_learning/ctc_alignment_manim.py            # all six, 1080p60
uv run python deep_learning/ctc_alignment_manim.py --list
uv run python deep_learning/ctc_alignment_manim.py -s TheForwardTrellis -q draft
```

See the [root README](../README.md) for the full flag list.

## References

Unchecked means **unverified** — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-001 research pass
([`docs/plans/001-ctc-alignment.md`](../docs/plans/001-ctc-alignment.md)), so
all of them start unchecked. Open one, confirm it covers what the entry
claims, and tick it yourself; nothing automated will.

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
- [ ] [HuggingFace Audio Course, ch. 3: CTC](https://huggingface.co/learn/audio-course/en/chapter3/ctc)
      — practical anchors: real frame rates, and blank vs. word-space in
      real vocabularies.
- [ ] [Zeyer et al., 2021 — Why does CTC result in peaky behavior?](https://arxiv.org/abs/2105.14849)
      — the analysis behind the spiky outputs mentioned in `WhenToUseIt`.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- Beam search over collapsed prefixes — why a prefix needs two
  probabilities (ending-in-blank vs. not), and the merge step that makes
  CTC beam search different from vanilla beam search.
- Training dynamics: the error signal starting diffuse, localising, then
  collapsing into spikes (Graves 2006, fig. 4), and why blank comes to
  dominate.
- The gradient identity — per-frame gradient is softmax output minus
  posterior occupancy, which is what makes the error-signal figure
  legible.
- Log-space computation: why the product of hundreds of probabilities
  underflows and how log-sum-exp restores it.
- Forced alignment done right: label priors and alignment-aware variants,
  since raw CTC spikes are not timestamps.
