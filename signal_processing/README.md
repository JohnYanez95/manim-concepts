# Signal processing

## Scope

How sound becomes the numbers a speech model reads — told on samples the
viewer can count. The topic is a road with a destination: reading a
log-mel spectrogram with understanding. Its first series builds the
spectrum as a **bank of detectors**: eight samples, five listeners, each
one a sine-and-cosine probe pair doing the multiply-and-sum the viewer
already owns from expectation — so "the spectrum" is never a new object,
only a column of weighted sums.

It stands on three series already built. The probe's multiply-and-sum is
[`probability/`](../probability/README.md)'s expectation —
`TheBalancePoint`'s weighted sum with the measure taken away — and the
reason a mix splits is `SameOutcomesAdd`'s linearity. The convolution
series spends that linearity once more — `WhatOneClickBecomes`' "sums
pass through" is `SameOutcomesAdd`'s move carrying the impulse
response — and otherwise stands on the spectrum series alone: the probe
walked (`TheSlidingWeightedSum`), the bank read before and after
(`AMovingAverageIsALowPass`), the pair plane's turn
(`TheKernelsOwnReading`). Decibels are
[`algebra/`](../algebra/README.md)'s counting strip: `MultiplyIsAdd`'s
law and its log₁₀2 ≈ 0.301, `ShrinkCounts`' log 0 = −∞, and the list
`TheUnderflowCliff`'s closer planted. The 28 pairs of the probe table are
[`combinatorics/`](../combinatorics/README.md)'s `CombinationRule`. The
road's destination is where
[`deep_learning/`](../deep_learning/README.md)'s begins from the other
side; the encoder between them is out of scope in both topics.

The road, in dependency order ([plan 019](../docs/plans/019-signal-processing-spectrum.md)):

| Series | Lands | Status |
| --- | --- | --- |
| The spectrum | Sampling; one detector as a probe pair; the bank; why it never double-counts; spacing sr/N; decibels; the fold at half the sample rate | `spectrum_manim.py` |
| Convolution | The sliding weighted sum as a filter; what one click becomes; the flip; a moving average as a low-pass; the kernel's own reading as the convolution theorem; multiplying in time | `convolution_manim.py` |
| Windowing → STFT → spectrogram | Leakage as the convolution theorem at work; framing and hop; the time–frequency tradeoff | not built |
| Mel | The mel filterbank regroups the spectrum's rows; log-mel | not built |

Deliberately **not** covered here:

- **Complex exponentials.** The repo has not built Euler's formula, so
  every probe is a real sine-and-cosine pair and every reading a
  hypotenuse — Steven W. Smith's "real DFT". The complex form, and the
  reason orthogonality holds for every N rather than the N = 8 checked
  on screen, wait for that series in [`calculus/`](../calculus/README.md).
- **The word "filter".** In the spectrum series one frame gives one
  number per detector, and a filter's output is a signal — so that
  series says "detector" throughout. The convolution series earns
  "filter" in its first scene, by sliding the window: from then on a
  detector is one number per frame and a filter is a signal per signal.
- **Convolutional layers.** `WhereConvolutionLives` names them as where
  the sliding weighted sum lives ("the kernel of the convolution is the
  set of connection weights — LeCun, 1998") and `TheFlip` notes they
  slide unflipped; a learned kernel is the encoder's business, out of
  scope at both ends of this road —
  [`deep_learning/`](../deep_learning/README.md)'s Scope says the same
  from its side. Named, not promised: no series is queued.
- **Circular convolution.** On the 8-sample grid the DFT's convolution
  theorem is circular (Oppenheim & Schafer §8.6.5). The convolution
  series meets it where circular and linear agree — whole-lap tones on
  the ring, and clicks and steps on a longer strip with the zeros beyond
  its ends drawn — and never teaches the wrap. The windowing series owns
  the case where they differ.
- **Leakage and windows.** Every worked tone on the bank sits exactly
  on a detector's frequency. A tone between detectors appears three
  times: `WhatSetsTheSpacing`'s 1500 Hz sine and the trumpet note in
  `TheSpectrumInDecibels` as honest pointers, and the 1500 Hz sine again
  in `MultiplyingInTime`, where the smear is *explained* — the
  rectangle's lines copied onto the tone's, by the theorem — but not
  tamed: the window's shape, and what a quieter one buys, is the
  windowing series'.
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
| 3 | `TheBankOfDetectors` | five detectors, $k = 0 \dots 4$, at $k \cdot 1000$ Hz | Five detectors listen to the same 8 samples, each at its own fixed frequency. A pure tone lights exactly one row; a mix lights its parts; and the column of readings, turned on its side, is the spectrum. | The rows stand labelled — 0, 1000, 2000, 3000, 4000 Hz — before any sound arrives: a row is an address, not a discovery. A 2000 Hz tone lights row 2 alone, reading 4; a 3000 Hz tone started elsewhere lights row 3 alone, again 4. The first scene's mix lights two rows, 4 and 2 — row 2's pair is (1.41, −1.41), and its bar is that pair's distance, the previous scene's lesson inside the bank. Reading ÷ 4 gives the amplitudes: 1 and 0.5. | Reading any spectrum: the horizontal axis is a row of fixed addresses, each bar a weighted sum of the same samples — nothing new was added to the viewer's toolkit to build it. The signal is Lyons' worked example; the numbers on screen are computed (plan 019, anchor R). |
| 4 | `NoDoubleCounting` | $\sum_n p_i[n]\,p_j[n] = 0$ for every pair of different probes | The mix split cleanly because each probe's sum on a mix is the sum of its sums on the parts, and every probe sums to exactly 0 against every other probe — so no bar can borrow from another. | Each probe's sum on a mix is the sum of its sums on the parts (the weighted sum is linear — `SameOutcomesAdd`'s move, owned since the dice; the pair adds, the distance is taken last: 12 and 16 made 20), so it is enough to ask what each probe sums to on every other probe: the 8 × 8 table has 8, 4, 4, 4, 4, 4, 4, 8 on its diagonal and 0 in all C(8, 2) = 28 other pairs — computed, not proved; the reason for every N needs Euler's formula, and the screen says so. Why 4: squares never cancel, and height² + shadow² = 1 at every stop, so 8 stops share out 8 between two probes that take the same values in a different order. Why 8 at the ends: at 0 and 4 laps the sine probe is all zeros, so the cosine keeps everything — those rows read ÷ 8 and do depend on when the tone starts. | 1 + 2·3 + 1 = 8 readings from 8 samples: nothing is lost, which is why the transform can be undone (promised, not shown). Each detector is exactly deaf at the other detectors' frequencies — and only there, which is the next scene's warning. |
| 5 | `WhatSetsTheSpacing` | $f_k = k \cdot sr/N$, spacing $= sr/N = 1/\text{duration}$ | The detectors sit sr ÷ N apart — one over how long the window listens. Sampling faster buys reach; only listening longer buys finer spacing. | Probe k fits k laps into a window lasting N ÷ sr seconds: 8 ÷ 8000 s = 1 ms, so k laps per millisecond is k × 1000 Hz. Three banks side by side: 8 samples at 8000 Hz and 16 samples at 16 000 Hz are both 1 ms and both 1000 Hz apart — the faster rate reached 8000 Hz, no finer; 16 samples at 8000 Hz listens 2 ms and sits 500 Hz apart. | A speech model's front end: Whisper's 400 samples at 16 000 Hz is 25 ms — 201 rows, 40 Hz apart, up to 8000 Hz. The cost of spacing: a 1500 Hz sine starting at 0 — its 8 samples sit beside the bars and show one and a half laps, not a whole number of laps in the window — sits between two rows and every row answers (1.5, 2.85, 2.41, 0.85, 0.67): leakage, the windowing series' subject. Slide the window and each detector's output becomes a signal — a filterbank; a mel filterbank regroups those 201 rows into 80. |
| 6 | `TheSpectrumInDecibels` | $L = 10\log_{10}(P/P_0) = 20\log_{10}(A/A_0)$ dB | A tone 100 times quieter is invisible on linear bars and sits at −40 dB on a log axis: decibels are ten times the log of a power ratio, always against a stated reference. | Readings 4, 2 and 0.04: the third has no visible bar. One definition — 10 × log₁₀ of a power ratio (Bell System, 1929); power goes as amplitude², and the log turns the square into × 2, hence 20 × log₁₀ of an amplitude ratio — the logarithm series' ruler at work. Against the loudest row: 0 dB, 20 × log₁₀(½) = −20 × 0.301 = −6.02 dB, and 20 × log₁₀(1/100) = −40 dB. Empty rows are log 0 = −∞, so 0 dB means "equal to the reference", never silence — and real systems pick a floor: Whisper keeps 8 decades of power below its loudest value, 80 dB. | A real trumpet note (4096 samples at 22 050 Hz: 2049 detectors, 5.4 Hz apart): the second harmonic is the loudest, the 624 Hz fundamental 1.56 dB below it, then −3.23, −7.21, −11.98 dB — a real note lands between rows, so a window shaped those levels. And the same ruler elsewhere: pH, stellar magnitude, semitones — each a constant times the log of a ratio; that the ear itself hears in logs is an approximate motivation, not a law. |
| 7 | `TheFoldAtNyquist` | $\cos(2\pi(8-k)n/8) = \cos(2\pi kn/8)$, $\sin(2\pi(8-k)n/8) = -\sin(2\pi kn/8)$ | The bank stops at half the sample rate because nothing above it can be told apart: at the 8 stops, probe 7 is probe 1, and a 7000 Hz tone sampled at 8000 Hz *is* a 1000 Hz tone. | Number for number the 7-lap cosine probe equals the 1-lap one, and the 7-lap sine probe is the 1-lap one with every sign flipped; likewise 6 is 2 and 5 is 3 — run past row 4, the table of zeros lights up (c₃ × c₅ adds to 4, s₃ × s₅ to −4). The reason is on the first scene's circle: stepping 7/8 of a lap forward lands on the same stops as 1/8 of a lap backward — same shadow, height flipped. Two cosines, 1000 Hz and 7000 Hz, pass through the same 8 samples; on the ruler, 5000 lands on 3000, 6000 on 2000, 7000 on 1000. | The first scene's promise cashed: it said at least two samples per lap; strictly, more than two — below sr ÷ 2. Exactly at sr ÷ 2, a sine samples to silence. The impostor is a clean lower tone, not noise, so it must be removed *before* sampling: hence 8000 Hz for telephone speech, 16 000 Hz for speech models. In numpy, the upper half of `fft`'s output is this mirror; `rfft` returns the bank. Sampling theorem: E. T. Whittaker 1915 · Kotelnikov 1933 · Shannon 1949. The closing map: the bank and decibels are built; convolution, windowing, the short-time transform and mel are the road ahead. |

Renders are numbered to match:
`01_PressureIntoNumbers.mp4` … `07_TheFoldAtNyquist.mp4`.

### convolution_manim.py

Watch after the spectrum series. The first three scenes build the filter
(the window walks; what one click becomes; the flip and what it is for);
the middle three are the convolution theorem — a moving average read on
the bank, the kernel's own reading, multiplying in time; the last maps
where convolution lives. Every number traces to
[plan 020](../docs/plans/020-signal-processing-convolution.md)'s
verification pass (anchors A–Y).

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheSlidingWeightedSum` | $y[n] = \tfrac13\,(x[n{-}1] + x[n] + x[n{+}1])$ | Slide a window of weights along a signal, multiplying and adding at every stop, and the output is a signal too: that is a filter, and the window is its kernel. | The spectrum series' probe did multiply-and-sum once, for one number; here the same window of three weights of ⅓ walks the strip 2, 2, 2, 8, 2, 2, 2, 2 (steady at 2 beyond both ends, drawn) and drops one output at every stop — 2, 2, 4, 4, 4, 2, 2, 2: the spike spread over three stops and lowered, a moving average. The weights sum to 1, so the totals agree (22 in, 22 out); weights 1, 1, 1 make everything three times as loud (66) — the sum of the weights is the gain. | "A filter turns a signal into a signal" — the word the spectrum series withheld, earned by sliding. Every smoothing, every echo and every learned kernel in a network is this walk with a different window; the moving average is the first and the plainest. |
| 2 | `WhatOneClickBecomes` | $y = \sum_k x[k]\, h[n-k]$ | A filter is known by what one click becomes — its impulse response. A signal is a sum of scaled, shifted clicks, so its output is the same sum of scaled, shifted responses. | One click through the ⅓ ⅓ ⅓ window gives the kernel back; a click of −2 gives the shape −2 as tall, a click three stops later gives the shape three stops later. Then 1, 2, 0, 3 through ½ ½ two ways on one screen: three scaled, shifted responses stacked and added by column, and the window walked one output at a time — both land on 0.5, 1.5, 1, 1.5, 1.5, five outputs from four samples with the ends drawn. Two owned facts make it so: sums pass through (the weighted sum is linear — the dice), and the same rule holds at every stop (the window never changes). | This is why a room, a microphone or a cable is fully described by its response to one click, and why the next scene can ask what a filter does to every tone at once: a tone is a signal, and the answer is a sum of responses. |
| 3 | `TheFlip` | $\sum_m h[m]\,x[n-m]$ vs $\sum_m h[m]\,x[n+m]$ | Slide a pattern the probe's way and an echo lands *before* the click; flip the pattern first and it lands after. The flip is what turns "does the signal match this pattern here" into "what does this system do to a click". | The echo kernel 1, 0, 0, ½ on a single click: slid as the probe slides, the half lands at stop −3 — a pre-echo nobody hears; flipped, at +3 — the echo the kernel meant. Same numbers, one list reversed; ⅓ ⅓ ⅓ reversed is itself, which is why the moving average hid it. Then a step through the centred window comes out smoothed in place, 0, 0, ⅓, ⅔, 1, 1, 1, 1 — but the window read one stop ahead; a window reading only the past gives the same numbers one stop late. | Correlation asks a detector's question, convolution a filter's — Smith's "very different DSP procedures". Delay is the price of causality, not a defect. And convolutional layers slide without flipping yet say "convolution": a learned kernel does not mind which. |
| 4 | `AMovingAverageIsALowPass` | $\lvert H_k\rvert = \tfrac13\lvert 1 + 2\cos(2\pi k/8)\rvert$ | Every whole-lap tone comes out of the moving average as the same tone, scaled — slow ones barely, fast ones a lot, two with their sign flipped. A low-pass scales; it does not remove. Gain 0 is the special case. | The spectrum series' bank reads each tone before and after the ⅓ ⅓ ⅓ window: 1000 Hz comes out 0.80 as tall (the reading 4 became 3.22), 2000 Hz exactly ⅓ (1.33), 3000 Hz 0.14 and upside down (4 became 0.55), 4000 Hz ⅓ and upside down (the end row reads ÷ 8: 8 became 2.67), a constant unchanged. The ½ ½ window on the 4000 Hz tone gives all eight outputs exactly 0 — 1, −1, 1, −1 averages to 0 — and on 2000 Hz gives 0.71 as tall, half a sample late: the pair turned 45°. | "Low-pass" defined honestly: slow tones pass, fast tones shrink, and a tone is removed only when its gain happens to be 0. Smith's verdict on the moving average — the best smoother and a poor frequency separator (row 3 quieter than row 4) — is read straight off the bars. |
| 5 | `TheKernelsOwnReading` | $Y_k = X_k \cdot H_k$ (on the pair: magnitudes multiply, angles add) | Feed the kernel itself to the bank and its readings are the gains — because a delay turns a tone's pair, sums pass through, and the kernel is a sum of delayed clicks. Filtering in time multiplies the readings, row by row: the convolution theorem. | The kernel as a signal on the ring (⅓ at stops 7, 0, 1) reads 1, 0.80, 0.33, 0.14, 0.33 — the previous scene's gains, with rows 3 and 4 negative. Why, on the probe's pair plane: delaying a tone by one sample turns its pair by 45° × the row number; the kernel is three clicks, ⅓ early, ⅓ now, ⅓ late, each giving the tone turned; sums pass through — so add three arrows of length ⅓ head to tail: row 1 leans forward to 0.80, row 2's side arrows cancel to ⅓, row 3 leans backward to −0.14, row 4 both backward to −⅓. Checked on one kernel and four rows; for every kernel and every N the proof needs Euler's formula — `calculus/`'s promise. The ½ ½ window's row-2 reading (½, ½), length 0.71 turned 45°, is the previous scene's turn explained. | Read the kernel on the bank and you have read what it does to every tone at once — the design step behind every filter, and the reason a long impulse response can be applied by multiplying spectra instead of sliding (the FFT's other job, parked in `algorithms/`). |
| 6 | `MultiplyingInTime` | $x \cdot w \;\leftrightarrow\; \tfrac{1}{N}\, X \circledast W$ | The other half of the theorem, stated and checked once: multiply two signals stop by stop and their readings convolve — each line of one takes copies of the other's lines. Every frame is such a multiplication, by a rectangle of ones. | A 2000 Hz tone (row 2 reads 4) times a 1000 Hz cosine (row 1 reads 4): row 2 empties and rows 1 and 3 read 2 each — 4 × 4 ÷ 8 = 2, for this pair; times all ones (a window that reads only on row 0) nothing moves. Then the hook: the 8 samples are an endless tone × a rectangle of eight ones; a whole-lap tone does not notice, having no neighbouring line to copy onto; the spectrum series' 1500 Hz sine does — its bars 1.5, 2.85, 2.41, 0.85, 0.67 are the rectangle's lines copied onto its own. | Leakage, by the theorem — and the promise that a window with quieter lines copies less, which is the windowing series' whole subject. |
| 7 | `WhereConvolutionLives` | $y_i = \sum_j s_j * h_{ij}$ | A room, a learned layer and a vocal tract are all the sliding weighted sum — and, read on the bank, the multiplication it hides. | A room's impulse response is the echo kernel grown long: 2 s of tail at 50 000 samples a second is 100 000 taps, 100 000 multiply-adds per output sample, which is why long kernels are applied by multiplying spectra (the FFT — an algorithm story, parked in `algorithms/`). A convolutional layer slides kernels whose weights are learned, not designed ("the kernel of the convolution is the set of connection weights"). Speech: a 115 Hz buzz from the glottis is a comb of lines at 230, 345, 460 Hz …; the vocal tract is a filter whose own reading, drawn over the comb, makes the vowel — the source–filter model. | Slide the probe and the detector's one number becomes a signal: the bank becomes a filterbank, its kernels the probes reversed — the windowing series' opening move. The closing map: reverb, a kernel's own reading and convolutional layers are met here — one built, two named as where the walk lives; windowing, the short-time transform and mel are the road ahead. |

Renders are numbered to match:
`01_TheSlidingWeightedSum.mp4` … `07_WhereConvolutionLives.mp4`.

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
The spectrum series' fifty-two entries came out of the plan-019 research
pass and were verified by the maintainer, who directed the ticks
(2026-09-19). The convolution series' twenty-eight entries (plan 020) were
likewise verified by the maintainer, who directed the ticks (2026-09-24).
Notes such as "not opened by the research pass" record what the agents
could reach, not the maintainer's check. Future entries start unchecked
until a human does the same.

The formulation — the DFT as correlation with real probes:

- [X] [Smith, *Guide to DSP*, ch. 8 "The DFT"](https://www.dspguide.com/ch8.htm)
      — Steven W. Smith, *The Scientist and Engineer's Guide to Digital
      Signal Processing* (California Technical Publishing): the real
      sine-and-cosine formulation this series follows.
- [X] [Smith, ch. 8, "DFT Basis Functions"](https://www.dspguide.com/ch8/4.htm)
      — the cosine and sine probes; the sine probes at 0 and N/2 laps
      are all zeros.
- [X] [Smith, ch. 8, "Analysis, Calculating the DFT"](https://www.dspguide.com/ch8/6.htm)
      — the DFT by correlation: multiply, add; Fig. 8-8 is the match and
      mismatch of `TheProbe`, rebuilt at N = 8.
- [X] [Smith, ch. 8, "Synthesis"](https://www.dspguide.com/ch8/5.htm)
      — the N/2 normalisation and its exception at the two end rows.
- [X] [Smith, ch. 8, "Notation and Format of the Real DFT"](https://www.dspguide.com/ch8/2.htm)
      — N samples in, N/2 + 1 cosine and N/2 + 1 sine amplitudes out.
- [X] [Smith, ch. 8, "The Frequency Domain's Independent Variable"](https://www.dspguide.com/ch8/3.htm)
      — four ways to label the frequency axis; this series uses Hz.
- [X] [Lyons, *Understanding DSP*, 3rd ed. — contents](https://ptgmedia.pearsoncmg.com/images/9780137027415/samplepages/0137027419.pdf)
      — Richard G. Lyons, *Understanding Digital Signal Processing*, 3rd
      ed., Prentice Hall, © 2011: §3.1's worked example (8 samples at
      8000 Hz) is the mix this series uses; §2.1 aliasing. The publisher's
      sample carries the contents pages only — the numbers on screen are
      computed (plan 019, anchor R), not quoted.
- [X] [Lyons, "Using the DFT as a Filter" (2013)](https://www.dsprelated.com/showarticle/187.php)
      — Rick Lyons, DSPRelated blog, 18 Feb 2013: what is and is not true
      of "a bin is a bandpass filter" — behind the choice of "detector".
- [X] [J. O. Smith, *Mathematics of the DFT* — "The DFT"](https://ccrma.stanford.edu/~jos/mdft/Discrete_Fourier_Transform_DFT.html)
      — Julius O. Smith III, *Mathematics of the Discrete Fourier
      Transform*, 2nd ed., W3K Publishing, 2007: the definition; "the DFT
      is proportional to the set of coefficients of projection onto the
      sinusoidal basis set".
- [X] [J. O. Smith, MDFT, "Orthogonality of the DFT Sinusoids"](https://ccrma.stanford.edu/~jos/mdft/Orthogonality_DFT_Sinusoids.html)
      — the all-N orthogonality proof (complex form) that
      `NoDoubleCounting` checks at N = 8 and does not prove.
- [X] [J. O. Smith, MDFT, "Norm of the DFT Sinusoids"](https://ccrma.stanford.edu/~jos/mdft/Norm_DFT_Sinusoids.html)
      — the diagonal of the probe table.
- [X] [J. O. Smith, MDFT, "Frequencies in the Cracks"](https://ccrma.stanford.edu/~jos/mdft/Frequencies_Cracks.html)
      — each bin as a length-N filter read at one instant; deaf exactly
      at the other bins' frequencies, and only there.
- [X] [J. O. Smith, MDFT, "Spectral Bin Numbers"](https://ccrma.stanford.edu/~jos/mdft/Spectral_Bin_Numbers.html)
      — bin k ↔ k·sr/N.
- [X] [J. O. Smith, *Spectral Audio Signal Processing*, "DFT Filter Bank"](https://ccrma.stanford.edu/~jos/sasp/DFT_Filter_Bank.html)
      — Julius O. Smith III, W3K Publishing, 2011: "taking a snapshot of
      all filter-bank channels at time N−1 yields the DFT" — the sliding
      view the windowing series will build.
- [X] [J. O. Smith, SASP, "Filter Bank Summation Interpretation"](https://ccrma.stanford.edu/~jos/sasp/Filter_Bank_Summation_FBS_Interpretation.html)
      — each STFT bin as heterodyne-then-lowpass; windowing-series
      material, read for the wording of "detector".
- [X] [J. O. Smith, MDFT, "Sampling Theorem"](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html)
      — the strict band limit: below sr/2, not up to it.
- [X] [Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed.](https://ocw.mit.edu/courses/res-6-dtsp-discrete-time-signal-processing/resources/mitres_6-dtsp_s26_thirdedition_pdf/)
      — Alan V. Oppenheim and Ronald W. Schafer, Pearson, 2010: §8.5 the
      DFT (eq. 8.67); §4.2 aliasing and the "Nyquist frequency" usage
      this series avoids; §10.3.2 the filter-bank interpretation.
- [X] [Chaudhari, "DFT as a Filter Bank" (2020)](https://wirelesspi.com/discrete-fourier-transform-dft-as-a-filter-bank/)
      — Qasim Chaudhari, Wireless Pi, 19 Mar 2020: the bank-of-N-filters
      figure.
- [X] [MIT OCW 6.341, Lecture 21 "Short-Time Fourier Analysis"](https://ocw.mit.edu/courses/6-341-discrete-time-signal-processing-fall-2005/3634773c2eb17d84e4f5de0c1446a374_lec21.pdf)
      — spectrum analyzers as banks of filters; a windowing-series
      source first seen here.
- [X] [Allen & Rabiner, "A Unified Approach to Short-Time Fourier Analysis"](https://doi.org/10.1109/PROC.1977.10770)
      — J. B. Allen and L. R. Rabiner, Proceedings of the IEEE 65(11),
      1977: citation confirmed, text not opened by the research pass.

How it is taught:

- [X] [Schaedler, "Seeing Circles, Sines and Signals"](https://jackschaedler.github.io/circles-sines-signals/)
      — Jack Schaedler: the sampled rotation; the detector fooled by a
      shifted tone and rescued by a second probe
      ([dotproduct3](https://jackschaedler.github.io/circles-sines-signals/dotproduct3.html),
      [dotproduct4](https://jackschaedler.github.io/circles-sines-signals/dotproduct4.html)).
- [X] [Sanderson, "But what is the Fourier Transform?" (2018)](https://www.3blue1brown.com/lessons/fourier-transforms/)
      — Grant Sanderson (3Blue1Brown): the winding-machine visual this
      series deliberately does not remake.
- [X] [Swanson, "An Interactive Introduction to Fourier Transforms"](https://www.jezzamon.com/fourier/)
      — Jez Swanson: the synthesis-first camp.
- [X] [Azad, "Intuitive Understanding of Sine Waves"](https://betterexplained.com/articles/intuitive-understanding-of-sine-waves/)
      — Kalid Azad, BetterExplained: the dissent — sine as its own
      motion, not a circle's by-product.
- [X] [Weber, "Students' understanding of trigonometric functions" (2005)](https://link.springer.com/article/10.1007/BF03217423)
      — Keith Weber, Mathematics Education Research Journal 17: the
      unit circle as a process; abstract only.
- [X] [Wage et al., "The Signals and Systems Concept Inventory" (2002)](https://peer.asee.org/the-signals-and-systems-concept-inventory.pdf)
      — Kathleen E. Wage, John R. Buck, Thad B. Welch, Cameron H. G.
      Wright, ASEE 2002: why the bank scenes keep the 8 samples beside
      their readings (`TheBankOfDetectors`, and the leakage beat of
      `WhatSetsTheSpacing`).
- [X] [Montgomery, "Digital Show and Tell" (2013)](https://wiki.xiph.org/Videos/Digital_Show_and_Tell)
      — Christopher "Monty" Montgomery, Xiph.Org: "the stairsteps aren't
      really there" — stems, never staircases.
- [X] [comp.dsp, "The inherent periodicity of the DFT" (2011)](https://www.dsprelated.com/showthread/comp.dsp/135472-5.php)
      — experts disagreeing in public, which is why the word "assumes"
      stays off screen.
- [X] [Wikipedia, "Aliasing"](https://en.wikipedia.org/wiki/Aliasing)
      — the folding diagram; the wagon-wheel effect.

Speech front ends:

- [X] [Jurafsky & Martin, *Speech and Language Processing*, ch. 15](https://web.stanford.edu/~jurafsky/slp3/15.pdf)
      — Daniel Jurafsky and James H. Martin, 3rd ed. draft: sampling
      ("at least two samples in each cycle"), 8 and 16 kHz, dB, the DFT
      with its details deliberately omitted, the mel filter bank.
- [X] [Jurafsky & Martin, SLP3, ch. 16 "Automatic Speech Recognition"](https://web.stanford.edu/~jurafsky/slp3/16.pdf)
      — Whisper's front end: 25 ms windows, 10 ms stride, 80 channels.
- [X] [Radford et al., "Robust Speech Recognition…" (2022)](https://arxiv.org/abs/2212.04356)
      — Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine
      McLeavey, Ilya Sutskever, arXiv:2212.04356, §2.2: 16 000 Hz,
      25 ms windows, 10 ms stride.
- [X] [OpenAI, `whisper/audio.py` at 8609812](https://github.com/openai/whisper/blob/86098128c0b4f24f0e2aa2994de830614b474227/whisper/audio.py)
      — N_FFT 400, HOP_LENGTH 160; power, log₁₀, the floor 8 decades
      below the maximum.
- [X] [OpenAI, whisper-large-v3 model card](https://huggingface.co/openai/whisper-large-v3)
      — 128 mel bins (not in the 2022 paper).
- [X] [Hugging Face Audio Course, "Introduction to audio data"](https://huggingface.co/learn/audio-course/chapter1/audio_data)
      — the trumpet spectrum the decibel scene's real-note beat follows.
- [X] [Sorohan, "solo trumpet -06in F - 90bpm.wav" (Freesound)](https://freesound.org/people/sorohanro/sounds/77711/)
      — Mihai Sorohan (sorohanro), CC BY 4.0 on Freesound today
      (librosa's bundled metadata says CC BY 3.0). The series shows five
      levels measured from librosa's converted copy (mono, 22 050 Hz),
      first 4096 samples, Hann window — never the audio.
- [X] [Creative Commons, Attribution 4.0 deed](https://creativecommons.org/licenses/by/4.0/)
      — credit, a link to the licence, and an indication of changes.
- [X] [librosa, "Example files"](https://librosa.org/doc/latest/recordings.html)
      — the `trumpet` example's provenance.

Sampling theorem and decibels:

- [X] [Shannon, "Communication in the Presence of Noise" (1949)](https://doi.org/10.1109/JRPROC.1949.232969)
      — Claude E. Shannon, Proceedings of the IRE 37(1): Theorem 1
      (p. 11); the "Nyquist interval" named on p. 12.
- [X] [Lüke, "The Origins of the Sampling Theorem" (1999)](https://doi.org/10.1109/35.755459)
      — Hans Dieter Lüke, IEEE Communications Magazine 37(4): E. T.
      Whittaker 1915, Kotelnikov 1933; Nyquist 1928 is not a source for
      the theorem.
- [X] [Nyquist, "Certain Topics in Telegraph Transmission Theory" (1928)](https://doi.org/10.1109/T-AIEE.1928.5055024)
      — Harry Nyquist, Transactions of the AIEE 47(2): the name, not the
      theorem; not opened by the research pass.
- [X] [Wikipedia, "Nyquist–Shannon sampling theorem"](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem)
      — used only to locate Lüke; no claim rests on it.
- [X] [Martin, "Decibel — The Name for the Transmission Unit" (1929)](https://archive.org/details/bstj8-1-1)
      — W. H. Martin, Bell System Technical Journal 8(1): "ten times the
      common logarithm of that ratio" — a power ratio only.
- [X] [J. O. Smith, MDFT, "Decibels"](https://ccrma.stanford.edu/~jos/mdft/Decibels.html)
      — the 20 × log₁₀ amplitude form derived from power ∝ amplitude²;
      [properties](https://ccrma.stanford.edu/~jos/mdft/Properties_DB_Scales.html):
      6.0206 and 3.0103.
- [X] [NIST SP 811, §8.7 "Logarithmic quantities and units"](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-8)
      — Ambler Thompson and Barry N. Taylor, 2008: L = 20 lg(F/F₀) dB and
      10 lg(P/P₀) dB.

The other log scales, and history:

- [X] [Pogson, "Magnitudes of Thirty-six of the Minor Planets" (1856)](https://articles.adsabs.harvard.edu/pdf/1856MNRAS..17...12P)
      — N. Pogson, Monthly Notices of the RAS 17(1): the ratio 2.512 —
      five magnitudes = × 100 is the modern reading, implicit there.
- [X] [Buck et al., "Measurement of pH" (IUPAC, 2002)](https://doi.org/10.1351/pac200274112169)
      — R. P. Buck and eleven co-authors, Pure and Applied Chemistry
      74(11): pH in terms of hydrogen-ion *activity*; not opened by the
      research pass.
- [X] [Stevens, "On the psychophysical law" (1957)](https://doi.org/10.1037/h0046162)
      — S. S. Stevens, Psychological Review 64(3): the power-law rival
      to Fechner; not opened by the research pass.
- [X] [Wikipedia, "Weber–Fechner law"](https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law)
      — secondary; behind "an approximate motivation, not a law".
- [X] [Heideman, Johnson & Burrus, "Gauss and the History of the FFT"](https://doi.org/10.1109/MASSP.1984.1162257)
      — Michael T. Heideman, Don H. Johnson, C. Sidney Burrus, IEEE ASSP
      Magazine 1(4), 1984: Clairaut 1754 (cosine-only), Gauss c. 1805
      (the general formula, published 1866).
- [X] [Cooley & Tukey, "An Algorithm for the Machine Calculation…" (1965)](https://doi.org/10.1090/S0025-5718-1965-0178586-1)
      — James W. Cooley and John W. Tukey, Mathematics of Computation
      19: the FFT — named here, parked in `algorithms/`; not opened.
- [X] [J J O'Connor and E F Robertson, "Jean Baptiste Joseph Fourier"](https://mathshistory.st-andrews.ac.uk/Biographies/Fourier/)
      — MacTutor: the memoir read 21 December 1807; *Théorie analytique
      de la chaleur*, 1822.

### Convolution (plan 020)

The formulation:

- [X] [Smith, ch. 6 "Convolution"](https://www.dspguide.com/ch6.htm)
      — Steven W. Smith, *The Scientist and Engineer's Guide to Digital
      Signal Processing*, ch. 6: the impulse response, the input-side
      and output-side views this series puts on one screen.
- [X] [Smith, ch. 6, "The Sum of Weighted Inputs"](https://www.dspguide.com/ch6/5.htm)
      — "each point in the output signal receives a contribution from
      many points in the input signal, multiplied by a flipped impulse
      response" — the weighted-sum reading this series grounds in
      expectation.
- [X] [Smith, ch. 7, "Common Impulse Responses"](https://www.dspguide.com/ch7/1.htm)
      — the echo ("the input signal plus a delayed version of the input
      signal"), the first difference, and the sum rule: *if* the DC gain
      is one, the kernel's points sum to one.
- [X] [Smith, ch. 7, "Correlation"](https://www.dspguide.com/ch7/3.htm)
      — "the signal inside of the convolution machine is flipped
      left-for-right"; "very different DSP procedures".
- [X] [Smith, ch. 9, "Convolution via the Frequency Domain"](https://www.dspguide.com/ch9/3.htm)
      — magnitudes multiply, phases add; the wrap-around and
      zero-padding this series meets but does not teach.
- [X] [Smith, ch. 15 "Moving Average Filters"](https://www.dspguide.com/ch15.htm)
      — eq. 15-2 for the gains; "an exceptionally good smoothing filter
      … but an exceptionally bad low-pass filter".
- [X] [Lyons, *Understanding DSP*, 3rd ed. — ch. 5 (contents)](https://ptgmedia.pearsoncmg.com/images/9780137027415/samplepages/0137027419.pdf)
      — Richard G. Lyons, Prentice Hall, © 2011: §5.1 "An Introduction
      to FIR Filters" (the 5-tap averager), §5.2 "Convolution in FIR
      Filters". Contents pages only; the chapter was not opened by the
      research pass.
- [X] [J. O. Smith, *Filters*, "The Simplest Lowpass Filter"](https://ccrma.stanford.edu/~jos/filters/Simplest_Lowpass_Filter.html)
      — Julius O. Smith III, W3K, 2007: y = x[n] + x[n−1] as the
      teaching vehicle; ["Sine-Wave Analysis"](https://ccrma.stanford.edu/~jos/filters/Sine_Wave_Analysis.html):
      a sinusoid in, the same sinusoid out, scaled and shifted.
- [X] [J. O. Smith, MDFT, "Convolution"](https://ccrma.stanford.edu/~jos/mdft/Convolution.html)
      — the cyclic definition; convolution as the probe's inner product
      with the shifted, flipped kernel.
- [X] [J. O. Smith, MDFT, "Convolution Example 1"](https://ccrma.stanford.edu/~jos/mdft/Convolution_Example_1_Smoothing.html)
      — ⅓ ⅓ ⅓ on a pulse gives ⅓, ⅔, 1; "smeared to the 'right'
      (forward in time) because the filter impulse response starts at
      time zero. Such a filter is said to be causal".
- [X] [J. O. Smith, MDFT, "Convolution Theorem"](https://ccrma.stanford.edu/~jos/mdft/Convolution_Theorem.html)
      — x ⊛ y ↔ X·Y, "perhaps the most important single Fourier theorem
      of all"; the [dual](https://ccrma.stanford.edu/~jos/mdft/Dual_Convolution_Theorem.html):
      x·y ↔ (1/N) X ⊛ Y — series D's statement.
- [X] [Oppenheim & Schafer, DTSP 3rd ed. — ch. 2, §8.6–8.7](https://ocw.mit.edu/courses/res-6-dtsp-discrete-time-signal-processing/mitres_6-dtsp_s26_thirdedition.pdf)
      — §2.2–2.3 (linearity, time invariance, the convolution sum derived
      from both, eq. 2.49); §8.6.5 circular convolution (eq. 8.114) and
      the theorem (8.126–8.127); §8.7.2: circular equals linear when
      N ≥ L + P − 1.
- [X] [MIT OCW 6.341, Lecture 16 "Circular Convolution"](https://ocw.mit.edu/courses/6-341-discrete-time-signal-processing-fall-2005/6e5190ef6e0d66c78bfdce2be6ce7125_lec16.pdf)
      — circular as linear wrapped mod N.
- [X] [Wikipedia, "Convolution"](https://en.wikipedia.org/wiki/Convolution)
      — the reflect-offset-slide picture; the term's history (pointers
      only).

How it is taught:

- [X] [Sanderson, "But what is a convolution?" (2022)](https://www.3blue1brown.com/lessons/convolutions)
      — Grant Sanderson (3Blue1Brown), 18 Nov 2022: the two-dice table
      with its flipped row, image kernels, polynomial multiplication and
      the FFT speed-up — the pictures this series does not remake.
- [X] [Azad, "Intuitive Guide to Convolution"](https://betterexplained.com/articles/intuitive-convolution/)
      — Kalid Azad, BetterExplained: "fancy multiplication"; the flipped
      patient list.
- [X] [Wilczek, "Circular vs. Linear Convolution"](https://thewolfsound.com/circular-vs-linear-convolution-whats-the-difference/)
      — Jan Wilczek, WolfSound: a delay by one on four samples, the
      last one wrapping to the front.
- [X] [Wage, Buck & Hjalmarson, "Analyzing Misconceptions…" (2006)](https://ieeexplore.ieee.org/document/4041044/)
      — Kathleen E. Wage, John R. Buck, Margret A. Hjalmarson, IEEE DSP
      Workshop 2006: students compute convolution without seeing it
      rests on linearity and time invariance — why the two facts are
      named on screen. Abstract only.
- [X] [Goodfellow, Bengio & Courville, *Deep Learning*, ch. 9](https://www.deeplearningbook.org/contents/convnets.html)
      — MIT Press, 2016, p. 328: "many neural network libraries
      implement a related function called the cross-correlation, which
      is the same as convolution but without flipping the kernel".

When it is useful:

- [X] [J. O. Smith, "Artificial Reverberation and Spatialization"](https://ccrma.stanford.edu/~jos/Reverb/Reverb_4up.pdf)
      — Julius O. Smith III, MUS420/EE367A: "the output is given by six
      convolutions"; t60 = 2 s at 50 kHz → "100,000 multiplies and
      additions per sample"; "In principle, this is an exact
      computational model".
- [X] [J. O. Smith, PASP, "Exact Reverb via Transfer-Function Modeling"](https://ccrma.stanford.edu/~jos/pasp/Exact_Reverb_Transfer_Function_Modeling.html)
      — *Physical Audio Signal Processing*, W3K, 2010: sources convolved
      with source-to-ear impulse responses.
- [X] [Allen & Berkley, "Image method for … small-room acoustics" (1979)](https://doi.org/10.1121/1.382599)
      — Jont B. Allen and David A. Berkley, J. Acoust. Soc. Am. 65(4):
      the simulated impulse response, convolved with speech; not opened
      by the research pass.
- [X] [LeCun et al., "Gradient-Based Learning Applied to Document Recognition" (1998)](https://doi.org/10.1109/5.726791)
      — Yann LeCun, Léon Bottou, Yoshua Bengio, Patrick Haffner, Proc.
      IEEE 86(11), §II.A: "The kernel of the convolution is the set of
      connection weights"; TDNNs for phoneme recognition. Read from the
      [preprint](http://leon.bottou.org/publications/pdf/ieee-1998.pdf).
- [X] [Jurafsky & Martin, SLP3, §15.4.6 "The Source-Filter Model"](https://web.stanford.edu/~jurafsky/slp3/15.pdf)
      — draft of 19 Aug 2026: "a 115 Hz glottal fold vibration leads to
      harmonics … of 230 Hz, 345 Hz, 460 Hz"; Fig. 15.24, the vocal
      tract as a filter.
- [X] [Wikipedia, "Source–filter model"](https://en.wikipedia.org/wiki/Source%E2%80%93filter_model)
      — the impulse-train source shaped by the tract; Fant credited.
- [X] [Fant, *Acoustic Theory of Speech Production* (1960) — preview](https://api.pageplace.de/preview/DT0400.9783110873429_A20720807/preview-9783110873429_A20720807.pdf)
      — Gunnar Fant, Mouton & Co., The Hague, © 1960 (the publisher's
      preview, second printing 1970; ISBN 978-3-11-087342-9): the
      source–filter theory in the original — "simple resonator systems
      and the theory of sound sources in speech". Front matter opened;
      the body not.

History:

- [X] [Domínguez, "A History of the Convolution Operation" (2015)](https://www.embs.org/pulse/articles/history-convolution-operation/)
      — Alejandro Domínguez, IEEE Pulse, 24 Jan 2015: Laplace 1778;
      "Faltung" (Doetsch 1923); the theorem in Borel 1899 — secondary,
      and the only source for the credit.
- [X] [Domínguez-Torres, "The Origin and History of Convolution I" (2010)](https://slideshare.net/Alexdfar/origin-adn-history-of-convolution)
      — the discrete operation's history; secondary.

## Ideas not yet built

- **Windowing → STFT → spectrogram** — the road's next series:
  `MultiplyingInTime` has stated the mechanism (every frame is a
  multiplication by a rectangle; leakage by the theorem; a window with
  quieter lines copies less) and `WhereConvolutionLives` the opening
  move (slide the probe and the bank becomes a filterbank, its kernels
  the probes reversed); left to build: the Hann window's lines, framing
  and hop, the time–frequency tradeoff, the spectrogram.
- **Mel** — a matrix of triangles regrouping Whisper's 201 rows into
  80, a log on top: the log-mel spectrogram. The natural on-ramp for
  the parked `linear_algebra/` topic (to be returned to): the bank is a
  projection onto probes, the mel filterbank a matrix.
- **The source–filter model of speech** — `WhereConvolutionLives` draws
  it once, not to scale (a 115 Hz comb under a formant envelope); a
  series would build the vocal tract's own reading from a real vowel,
  and the cepstrum that separates the two.
- **The inverse** — `NoDoubleCounting` promises that 8 readings rebuild
  8 samples; synthesis ("signals are sums of sines") is unbuilt.
- **The complex form** — one complex number per row instead of a pair;
  the all-N reason for the 28 zeros; and the convolution theorem for
  every kernel and every N (`TheKernelsOwnReading` checks one kernel on
  four rows): all wait on Euler's formula in
  [`calculus/`](../calculus/README.md).
- **The FFT** — the same readings in N log N steps, and the reason a
  100 000-tap room can be applied at all (multiply spectra, do not
  slide): the second example the divide-and-conquer Idea in
  [`algorithms/`](../algorithms/README.md) is waiting for (Cooley &
  Tukey 1965; Gauss c. 1805).
- **Circular convolution as a concept** — the DFT's theorem is circular
  and this road meets it only where circular and linear agree (Scope);
  the wrap, zero-padding and overlap-add are unbuilt.
- **Other kernels** — the first difference [1, −1] as a high-pass (gains
  0, 0.77, 1.41, 1.85, 2 on this grid) and as S. W. Smith's discrete
  derivative — [`calculus/`](../calculus/README.md)'s
  `TheSlopeIsAFunction` run on stems, the slope born as a signal;
  [1, 2, 1]/4 as the ½ ½ window squared (the theorem re-checked: gains
  multiply): pinned in plan 020, not on screen.
- **Quantization** — bit depth as noise; 16 bits span
  20 × log₁₀(2¹⁶) = 96.33 dB from full range to one step.
