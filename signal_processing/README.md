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
| 2 | `TheProbe` | $a_k = \sum_n x[n]\cos(2\pi kn/8)$, $b_k = \sum_n x[n]\sin(2\pi kn/8)$, reading $\sqrt{a_k^2 + b_k^2}$ | One detector: multiply the samples by a known tone, stop by stop, and add. A matching tone sums to 4, a different tone cancels to 0 — and it takes a sine-and-cosine pair of probes not to be fooled by when the tone starts. | The 2-lap probe is all integers (0, 1, 0, −1…): against itself every product is a square, 0 + 1 + 0 + 1 + 0 + 1 + 0 + 1 = 4, and squares cannot cancel; a 1-lap tone against the 3-lap probe gives four halves up and two wholes down, exactly 0. It is expectation's weighted sum with weights that can be negative and add to 0 — a pattern, not a probability. The sine probe alone is fooled: the tone 3, 4, −3, −4 reads 16, and the same tone one sample later reads 12. The pair is not: (12, 16), then (−16, 12), (−12, −16), (16, −12) — a quarter-turn per sample on a circle of radius 20, so the distance never moves. True for every starting angle; shown here for four. | 20 ÷ 4 = 5: the detector recovers an amplitude the samples never touch (the largest sample is 4). Every spectrum plot is this measurement repeated at each frequency. |
| 3 | `TheBankOfDetectors` | five detectors, $k = 0 \dots 4$, at $k \cdot 1000$ Hz | Five detectors listen to the same 8 samples, each at its own fixed frequency. A pure tone lights exactly one row; a mix lights its parts; and the column of readings, turned on its side, is the spectrum. | The rows stand labelled — 0, 1000, 2000, 3000, 4000 Hz — before any sound arrives: a row is an address, not a discovery. A 2000 Hz tone lights row 2 alone, reading 4; a 3000 Hz tone started elsewhere lights row 3 alone, again 4. The first scene's mix lights two rows, 4 and 2 — row 2's pair is (1.41, −1.41), and its bar is that pair's distance, the last scene's lesson inside the bank. Reading ÷ 4 gives the amplitudes: 1 and 0.5. | Reading any spectrum: the horizontal axis is a row of fixed addresses, each bar a weighted sum of the same samples — nothing new was added to the viewer's toolkit to build it. The signal is Lyons' worked example; the numbers on screen are computed (plan 019, anchor R). |
| 4 | `NoDoubleCounting` | $\sum_n p_i[n]\,p_j[n] = 0$ for every pair of different probes | The mix split cleanly because every probe reads exactly 0 on every other probe — so no bar can borrow from another. | A reading of a sum is the sum of the readings (the weighted sum is linear, owned since the dice), so it is enough to check probe against probe: the 8 × 8 table has 8, 4, 4, 4, 4, 4, 4, 8 on its diagonal and 0 in all C(8, 2) = 28 other pairs — computed, not proved; the reason for every N waits for Euler's formula. Why 4: squares never cancel, and height² + shadow² = 1 at every stop, so 8 stops share out 8 between two probes that take the same values in a different order. Why 8 at the ends: at 0 and 4 laps the sine probe is all zeros, so the cosine keeps everything — those rows read ÷ 8 and do depend on when the tone starts. | 1 + 2·3 + 1 = 8 readings from 8 samples: nothing is lost, which is why the transform can be undone (promised, not shown). Each detector is exactly deaf at the other detectors' frequencies — and only there, which is the next scene's warning. |
| 5 | `WhatSetsTheSpacing` | $f_k = k \cdot sr/N$, spacing $= sr/N = 1/\text{duration}$ | The detectors sit sr ÷ N apart — one over how long the window listens. Sampling faster buys reach; only listening longer buys finer spacing. | Probe k fits k laps into a window lasting N ÷ sr seconds: 8 ÷ 8000 s = 1 ms, so k laps per millisecond is k × 1000 Hz. Three banks side by side: 8 samples at 8000 Hz and 16 samples at 16 000 Hz are both 1 ms and both 1000 Hz apart — the faster rate reached 8000 Hz, no finer; 16 samples at 8000 Hz listens 2 ms and sits 500 Hz apart. | A speech model's front end: Whisper's 400 samples at 16 000 Hz is 25 ms — 201 rows, 40 Hz apart, up to 8000 Hz. The cost of spacing: a 1500 Hz sine starting at 0 sits between two rows and every row answers (1.5, 2.85, 2.41, 0.85, 0.67) — leakage, the windowing series' subject. Slide the window and each detector's output becomes a signal — a filterbank; a mel filterbank regroups those 201 rows into 80. |
| 6 | `TheSpectrumInDecibels` | $L = 10\log_{10}(P/P_0) = 20\log_{10}(A/A_0)$ dB | A tone 100 times quieter is invisible on linear bars and sits at −40 dB on a log axis: decibels are ten times the log of a power ratio, always against a stated reference. | Readings 4, 2 and 0.04: the third has no visible bar. One definition — 10 × log₁₀ of a power ratio (Bell System, 1929); power goes as amplitude², and the log turns the square into × 2, hence 20 × log₁₀ of an amplitude ratio — the logarithm series' ruler at work. Against the loudest row: 0 dB, 20 × log₁₀(½) = −20 × 0.301 = −6.02 dB, and 20 × log₁₀(1/100) = −40 dB. Empty rows are log 0 = −∞, so 0 dB means "equal to the reference", never silence — and real systems pick a floor: Whisper keeps 8 decades of power below its loudest value, 80 dB. | A real trumpet note (4096 samples at 22 050 Hz: 2049 detectors, 5.4 Hz apart): the second harmonic is the loudest, the 624 Hz fundamental 1.56 dB below it, then −3.23, −7.21, −11.98 dB — a real note lands between rows, so a window shaped those levels. And the same ruler elsewhere: pH, stellar magnitude, semitones — each a constant times the log of a ratio; that the ear itself hears in logs is an approximate motivation, not a law. |
| 7 | `TheFoldAtNyquist` | $\cos(2\pi(8-k)n/8) = \cos(2\pi kn/8)$, $\sin(2\pi(8-k)n/8) = -\sin(2\pi kn/8)$ | The bank stops at half the sample rate because nothing above it can be told apart: at the 8 stops, probe 7 is probe 1, and a 7000 Hz tone sampled at 8000 Hz *is* a 1000 Hz tone. | Number for number the 7-lap cosine probe equals the 1-lap one, and the 7-lap sine probe is the 1-lap one with every sign flipped; likewise 6 is 2 and 5 is 3 — run past row 4, the table of zeros lights up (c₃ × c₅ adds to 4, s₃ × s₅ to −4). The reason is on the first scene's circle: stepping 7/8 of a lap forward lands on the same stops as 1/8 of a lap backward — same shadow, height flipped. Two curves, 1000 Hz and 7000 Hz, pass through the same 8 samples; on the ruler, 5000 lands on 3000, 6000 on 2000, 7000 on 1000. | The first scene's promise cashed: strictly below sr ÷ 2 — exactly at it, a sine samples to silence. The impostor is a clean lower tone, not noise, so it must be filtered out *before* sampling: hence 8000 Hz for telephone speech, 16 000 Hz for speech models. Sampling theorem: E. T. Whittaker 1915 · Kotelnikov 1933 · Shannon 1949. The closing map: the bank and decibels are built; windowing, the short-time transform and mel are the road ahead. |

Renders are numbered to match:
`01_PressureIntoNumbers.mp4` … `07_TheFoldAtNyquist.mp4`.

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
