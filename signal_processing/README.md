# Signal processing

## Scope

How sound becomes the numbers a speech model reads — told on samples the
viewer can count. The topic is a road with a destination: reading a
log-mel spectrogram with understanding. Its first series builds the
spectrum as a **bank of detectors**: eight samples, five listeners, each
one a sine-and-cosine probe pair doing the multiply-and-sum the viewer
already owns from expectation — so "the spectrum" is never a new object,
only a column of weighted sums.

The road, in dependency order ([plan 019](../docs/plans/019-signal-processing-spectrum.md)):

| Series | Lands | Status |
| --- | --- | --- |
| The spectrum | Sampling; one detector as a probe pair; the bank; why it never double-counts; spacing sr/N; decibels; the fold at half the sample rate | `spectrum_manim.py` |
| Convolution | The sliding weighted sum as filtering; the convolution theorem | not built |
| Windowing → STFT → spectrogram | Leakage as the convolution theorem at work; framing and hop; the time–frequency tradeoff | not built |
| Mel | The mel filterbank regroups the spectrum's rows; log-mel | not built |

Deliberately **not** covered here:

- **Complex exponentials.** The repo has not built Euler's formula, so
  every probe is a real sine-and-cosine pair and every reading a
  hypotenuse — Steven W. Smith's "real DFT". The complex form, and the
  reason orthogonality holds for every N rather than the N = 8 checked
  on screen, wait for that series in [`calculus/`](../calculus/README.md).
- **The word "filter".** One frame gives one number per detector; a
  filter's output is a signal, which only exists once the frame slides.
  The windowing series earns the word "filterbank".
- **Leakage and windows.** Every tone here sits exactly on a detector's
  frequency. A tone between detectors appears once, as an honest
  pointer, and is not explained.
- **The fast Fourier transform.** The same numbers computed in N log N
  steps is an algorithm story — divide and conquer, queued in
  [`algorithms/`](../algorithms/README.md) — not a concept this road
  needs.
- **Synthesis.** That the eight readings rebuild the eight samples is
  stated as bookkeeping and promised, not shown.
- **Quantization.** Bit depth and quantization noise are not on this
  road until codecs are.

## Concepts

### spectrum_manim.py

Watch in order. The first two scenes are the foundation (sound into
numbers, one detector); the middle three are the bank and nothing else;
the last two read it in decibels and find where it has to stop. Every
number traces to [plan 019](../docs/plans/019-signal-processing-spectrum.md)'s
verification pass (anchors A–Z).

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `PressureIntoNumbers` | $x[n] = \sin(2\pi n/8)$, $n = 0 \dots 7$ | A pure tone is a point going round a circle at a steady speed, the microphone reads its height, and sampling keeps that height at 8 stops — 8 numbers for 1 ms of sound at 8000 samples a second. | One lap per millisecond is a 1000 Hz tone; 8000 samples a second puts a sample every 45° of that lap, so the 8 stops on the circle *are* the 8 samples (0, 0.71, 1, 0.71, 0, −0.71, −1, −0.71) — drawn as stems, because nothing between them is stored; the shadow of the same point is the same motion a quarter-turn ahead, two readings of one rotation. | Every digital recording starts here: 8000 samples a second for telephone speech, 16 000 for speech models. A faster tone gets fewer samples per lap and needs at least two — the last scene says why. And real sound is a mix: the 8 numbers on screen at the close hide two tones, which is the question the rest of the series answers. |

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-019 research pass and starts
unchecked.

- [ ] [Smith, *Guide to DSP*, ch. 8 "The DFT"](https://www.dspguide.com/ch8.htm)
      — Steven W. Smith, *The Scientist and Engineer's Guide to Digital
      Signal Processing* (California Technical Publishing): the real
      sine-and-cosine formulation this series follows; the DFT by
      correlation.

## Ideas not yet built

- **Convolution**, **windowing → STFT → spectrogram**, **mel** — the
  road's next three series, in that order.
