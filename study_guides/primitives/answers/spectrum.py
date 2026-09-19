"""Answer anchors for the spectrum problem set (plan 019, ADR 008).

Two routes per answer, the same two plan 019's verifier used. Exact: the
probes at the 8 stops take values in {0, ±1, ±√2/2}, so every pair is
computed in Q(√2) with Fractions — a number p + q·√2 is the tuple (p, q).
Numeric: numpy, cross-checked against ``np.fft.rfft``. The chapter's sine
sum is plus-signed, so numpy's X[k] = a_k − i·b_k: its imaginary part is the
NEGATIVE of the b computed here, and ``_check_fft`` asserts exactly that.
Run: prints `problem_id: answer`.
"""

from fractions import Fraction
from math import log10, sqrt

import numpy as np

N = 8
SR = 8000
ZERO = (Fraction(0), Fraction(0))
HALF_ROOT2 = (Fraction(0), Fraction(1, 2))  # √2/2


def _neg(x):
    return (-x[0], -x[1])


def _mul(x, y):
    """(p + q√2)(r + s√2) = (pr + 2qs) + (ps + qr)√2."""
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def _add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def _rational(x) -> Fraction:
    assert x[1] == 0, f"{x} is not rational"
    return x[0]


ONE = (Fraction(1), Fraction(0))
_COS = [ONE, HALF_ROOT2, ZERO, _neg(HALF_ROOT2), _neg(ONE), _neg(HALF_ROOT2), ZERO, HALF_ROOT2]
_SIN = _COS[6:] + _COS[:6]  # sin θ = cos(θ − 90°): the same ring, a quarter-turn behind


def _probe_exact(k: int, kind: str):
    """Probe k at the 8 stops, exact; defined for every k (the fold needs k > 4)."""
    table = _COS if kind == "c" else _SIN
    return [table[(k * n) % N] for n in range(N)]


def _lift(samples):
    """Rationals into Q(√2)."""
    return [s if isinstance(s, tuple) else (Fraction(s), Fraction(0)) for s in samples]


def _pair_exact(samples, k: int):
    """Detector k's (cosine sum, sine sum), exact in Q(√2)."""
    xs = _lift(samples)
    a = b = ZERO
    for x, c, s in zip(xs, _probe_exact(k, "c"), _probe_exact(k, "s"), strict=True):
        a = _add(a, _mul(x, c))
        b = _add(b, _mul(x, s))
    return a, b


def _float(x) -> float:
    return float(x[0]) + float(x[1]) * sqrt(2)


def _pair(samples, k: int, n: int = N) -> tuple[float, float]:
    """The same pair in floats, for any window length n."""
    t = np.arange(n)
    x = np.asarray(samples, dtype=float)
    return (
        float(np.dot(x, np.cos(2 * np.pi * k * t / n))),
        float(np.dot(x, np.sin(2 * np.pi * k * t / n))),
    )


def _readings(samples) -> list[float]:
    return [float(np.hypot(*_pair(samples, k))) for k in range(N // 2 + 1)]


def _check_fft(samples) -> None:
    """The bank IS rfft: X[k] = a_k − i·b_k on every row, 0 to N/2."""
    spectrum = np.fft.rfft(np.asarray(samples, dtype=float))
    assert len(spectrum) == N // 2 + 1
    for k, value in enumerate(spectrum):
        a, b = _pair(samples, k)
        assert np.isclose(value.real, a, atol=1e-9), (k, value, a)
        assert np.isclose(value.imag, -b, atol=1e-9), (k, value, b)


def _tone(amplitude: float, hz: float, degrees: float = 0.0, kind: str = "sin", sr: int = SR):
    t = np.arange(N) / sr
    angle = 2 * np.pi * hz * t + np.deg2rad(degrees)
    return amplitude * (np.sin(angle) if kind == "sin" else np.cos(angle))


TONE = [5, 12, -5, -12, 5, 12, -5, -12]  # 5·c₂ + 12·s₂ — a 5-12-13 tone at 2000 Hz


def p1_pair_and_reading() -> str:
    """The 2000 Hz detector on the 5-12-13 tone: pair, reading, amplitude."""
    a, b = (_rational(v) for v in _pair_exact(TONE, 2))
    assert (a, b) == (20, 48)
    reading_squared = a * a + b * b
    assert reading_squared == 52**2
    amplitude = Fraction(52, N // 2)  # interior rows: reading ÷ (N/2)
    assert amplitude == 13 and max(abs(s) for s in TONE) == 12 < amplitude
    assert amplitude**2 == 5**2 + 12**2  # the tone is 5·cos + 12·sin
    assert _pair_exact(TONE, 1) == (ZERO, ZERO)  # the 1000 Hz detector hears nothing
    _check_fft(TONE)
    assert np.allclose(_readings(TONE), [0, 0, 52, 0, 0])
    return "pair (20, 48); reading 52; amplitude 52/4 = 13 > largest sample 12; row 1 pair (0, 0)"


def p2_which_row_fires() -> str:
    """A bin-centred tone lights one row at A·N/2, at every phase; a mix splits."""
    single = _tone(2.5, 3000, 50)
    assert np.allclose(_readings(single), [0, 0, 0, 10, 0], atol=1e-9)
    for degrees in range(360):  # the reading ignores the starting angle on interior rows
        assert np.allclose(_readings(_tone(2.5, 3000, degrees)), [0, 0, 0, 10, 0], atol=1e-9)
    _check_fft(single)
    # The mix, exactly: 3·s₁ + ½·c₃.
    mix = [
        _add(_mul((Fraction(3), Fraction(0)), s), _mul((Fraction(1, 2), Fraction(0)), c))
        for s, c in zip(_probe_exact(1, "s"), _probe_exact(3, "c"), strict=True)
    ]
    pairs = [_pair_exact(mix, k) for k in range(N // 2 + 1)]
    assert [tuple(_rational(v) for v in p) for p in pairs] == [
        (0, 0),
        (0, 12),
        (0, 0),
        (2, 0),
        (0, 0),
    ]
    mix_float = _tone(3, 1000) + _tone(0.5, 3000, kind="cos")
    assert np.allclose(mix_float, [_float(v) for v in mix])
    # Linearity: the mix's pair is the sum of the parts' pairs, row by row.
    for k in range(N // 2 + 1):
        parts = np.add(_pair(_tone(3, 1000), k), _pair(_tone(0.5, 3000, kind="cos"), k))
        assert np.allclose(_pair(mix_float, k), parts)
    _check_fft(mix_float)
    return "(a) row 3 (3000 Hz) reads 10, the rest 0; (b) readings 0, 12, 0, 2, 0"


def _bank(sr: int, n: int) -> tuple[Fraction, Fraction, int, Fraction]:
    """(duration in ms, spacing in Hz, rows, reach in Hz) — spacing = sr/N = 1/duration."""
    duration = Fraction(n, sr)
    spacing = Fraction(sr, n)
    assert spacing == 1 / duration
    rows = n // 2 + 1
    assert len(np.fft.rfftfreq(n, d=1 / sr)) == rows
    assert np.isclose(np.fft.rfftfreq(n, d=1 / sr)[1], float(spacing))
    reach = spacing * (rows - 1)
    assert reach == Fraction(sr, 2)
    return duration * 1000, spacing, rows, reach


def p3_spacing_rows_reach() -> str:
    """Spacing, row count and reach from sr and N."""
    assert _bank(8000, 8) == (1, 1000, 5, 4000)  # the chapter's own bank
    assert _bank(16000, 400) == (25, 40, 201, 8000)
    assert _bank(48000, 960) == (20, 50, 481, 24000)
    n = Fraction(16000, 10)  # spacing 10 Hz at sr 16 000
    assert n == 1600 and _bank(16000, 1600) == (100, 10, 801, 8000)
    assert _bank(48000, 1600)[1] == 30  # same N, faster rate: COARSER
    assert _bank(48000, 4800)[:2] == (100, 10)  # 10 Hz costs 100 ms at any rate
    return (
        "(a) 25 ms, 40 Hz, 201 rows, to 8000 Hz; (b) 20 ms, 50 Hz, 481 rows, to 24 000 Hz; "
        "(c) N = 1600 (100 ms); at 48 000 Hz the same N gives 30 Hz — 4800 samples, still 100 ms"
    )


def _db_amplitude(ratio: float) -> float:
    return 20 * log10(ratio)


def _db_power(ratio: float) -> float:
    return 10 * log10(ratio)


def p4_decibels() -> str:
    """Reading ratios to dB and back; the two routes (amplitude, power) agree."""
    a = _db_amplitude(0.5 / 4)
    assert round(a, 2) == -18.06 and np.isclose(a, _db_power((0.5 / 4) ** 2))
    assert round(-20 * 3 * 0.301, 2) == -18.06  # 1/8 is three halvings, on the repo's 0.301
    ratio = 10 ** (-12.04 / 20)
    assert round(ratio, 3) == 0.25 and round(_db_amplitude(1 / 4), 2) == -12.04
    assert round(_db_power(1 / 16), 2) == -12.04  # a quarter the amplitude, 1/16 the power
    assert _db_amplitude(1 / 10) == -20.0 and _db_power(1 / 10) == -10.0
    half_power = _db_power(1 / 2)
    assert round(half_power, 2) == -3.01
    assert np.isclose(_db_amplitude(1 / sqrt(2)), half_power) and round(1 / sqrt(2), 3) == 0.707
    reading = 4 * 10 ** (-26.02 / 20)
    assert round(reading, 3) == 0.2 and round(_db_amplitude(1 / 20), 2) == -26.02
    assert round(-20 - 20 * 0.301, 2) == -26.02  # a tenth, then a half
    return (
        "(a) −18.06 dB; (b) amplitude ratio 1/4 (power 1/16); (c) −20 dB, and −10 dB for power; "
        "(d) −3.01 dB, amplitude ratio 1/√2 ≈ 0.707; (e) 0.2"
    )


def _lands(hz: int, sr: int) -> int:
    """Where a tone between 0 and sr is heard after sampling at sr."""
    assert 0 <= hz < sr
    return hz if hz < sr / 2 else sr - hz


def p5_the_fold() -> str:
    """Tones above sr/2 land at sr − f; the cosine unchanged, the sine negated."""
    assert [_lands(f, 8000) for f in (5000, 6000, 7000)] == [3000, 2000, 1000]  # the ruler
    assert _lands(5000, 16000) == 5000  # below sr/2: no fold
    assert _lands(9000, 16000) == 7000 and _lands(10000, 16000) == 6000
    for k in (5, 6, 7):  # probe N−k IS probe k at the stops (sine negated), exactly
        assert _probe_exact(k, "c") == _probe_exact(N - k, "c")
        assert _probe_exact(k, "s") == [_neg(v) for v in _probe_exact(N - k, "s")]
    sine = _probe_exact(7, "s")
    assert [round(_float(v), 2) for v in sine] == [0, -0.71, -1, -0.71, 0, 0.71, 1, 0.71]
    assert np.allclose(_tone(1, 7000), [_float(v) for v in sine])
    assert np.allclose(_tone(1, 7000), -_tone(1, 1000))
    assert _pair_exact(sine, 1) == (ZERO, (Fraction(-4), Fraction(0)))
    cosine = _probe_exact(7, "c")
    assert np.allclose(_tone(1, 7000, kind="cos"), _tone(1, 1000, kind="cos"))
    assert _pair_exact(cosine, 1) == ((Fraction(4), Fraction(0)), ZERO)
    assert np.allclose(_readings(_tone(1, 7000)), [0, 4, 0, 0, 0])
    assert np.allclose(_readings(_tone(1, 5000)), [0, 0, 0, 4, 0])
    # 16 samples at 16 000 Hz: rows 1000 Hz apart to 8000; 10 000 Hz fires the 6000 Hz row.
    t = np.arange(16) / 16000
    fast = np.abs(np.fft.rfft(np.sin(2 * np.pi * 10000 * t)))
    assert int(np.argmax(fast)) == 6 and np.isclose(fast[6], 8) and np.isclose(fast.sum(), 8)
    _check_fft(_tone(1, 7000))
    return (
        "(a) 3000 Hz; (b) 5000 stays 5000, 9000 → 7000, 10 000 → 6000; (c) samples "
        "0, −0.71, −1, −0.71, 0, 0.71, 1, 0.71 = −sin at 1000 Hz, pair (0, −4), reading 4; "
        "(d) pair (4, 0), reading 4"
    )


def p6_the_end_row() -> str:
    """At exactly sr/2 the sine probe is all zeros: the reading depends on the start."""
    assert _probe_exact(4, "s") == [ZERO] * N and _probe_exact(0, "s") == [ZERO] * N
    cosine = [(-1) ** n for n in range(N)]
    assert np.allclose(_tone(1, 4000, kind="cos"), cosine)
    assert tuple(_rational(v) for v in _pair_exact(cosine, 4)) == (8, 0)
    assert Fraction(8, N) == 1  # the end rows read ÷ N, not ÷ N/2
    silent = _tone(1, 4000)
    assert np.allclose(silent, 0) and np.allclose(_readings(silent), 0)
    shifted = [Fraction(3, 2) * (-1) ** n for n in range(N)]
    assert np.allclose(_tone(3, 4000, 60, kind="cos"), [float(s) for s in shifted])
    assert tuple(_rational(v) for v in _pair_exact(shifted, 4)) == (12, 0)
    assert np.isclose(3 * N * abs(np.cos(np.deg2rad(60))), 12)  # A·N·|cos φ|
    assert Fraction(12, N) == Fraction(3, 2)  # ÷ 8 returns 1.5 — half the true amplitude 3
    for samples in (cosine, [float(s) for s in shifted]):
        _check_fft(samples)
        assert np.allclose(_readings(samples)[:4], 0)
    return (
        "(a) 1, −1, 1, −1, …: row 4 reads 8, amplitude 8/8 = 1; (b) all zeros — every row reads "
        "0; (c) ±1.5 alternating: row 4 reads 12 = 3·8·cos 60°, so ÷ 8 gives 1.5, not 3"
    )


def p7_spot_the_false_claims() -> str:
    """Five claims, one true. Each verdict is tied to a computation."""
    # (b) 8 at 8000 and 16 at 16 000 are both 1 ms and both 1000 Hz apart.
    assert _bank(8000, 8)[:2] == _bank(16000, 16)[:2] == (1, 1000)
    assert _bank(16000, 16)[3] == 8000 and _bank(8000, 16)[1] == 500
    # (c) 0 dB is a ratio of 1; silence has no finite level.
    assert _db_amplitude(1.0) == 0.0
    with np.errstate(divide="ignore"):
        assert np.log10(0.0) == -np.inf
    # (d) the alias is one clean row, not a smear.
    assert np.allclose(_readings(_tone(1, 7000)), [0, 4, 0, 0, 0])
    # (e) a quarter-lap later: the pair turns, the reading stays.
    early, late = _tone(1, 2000), _tone(1, 2000, 90)
    assert not np.allclose(_pair(early, 2), _pair(late, 2))
    assert np.isclose(_readings(early)[2], 4) and np.isclose(_readings(late)[2], 4)
    return "only (e) is true; (a), (b), (c), (d) are false"


def p8_the_delayed_tone() -> str:
    """The 5-12-13 tone at four starts: a quarter-turn of the pair per sample."""
    pairs, sines = [], []
    for delay in range(4):
        delayed = TONE[-delay:] + TONE[:-delay] if delay else list(TONE)
        assert delayed == list(np.roll(TONE, delay))
        a, b = (_rational(v) for v in _pair_exact(delayed, 2))
        assert a * a + b * b == 52**2
        pairs.append((int(a), int(b)))
        sines.append(int(b))
    assert pairs == [(20, 48), (-48, 20), (-20, -48), (48, -20)]
    for (a, b), (c, d) in zip(pairs, pairs[1:], strict=False):
        assert (c, d) == (-b, a)  # a quarter-turn anticlockwise
    assert sines == [48, 20, -48, -20]  # the sine probe alone is fooled
    # A 1000 Hz tone turns 45° per sample on the 1000 Hz detector: 1 lap / 8 samples.
    tone = _tone(1, 1000, 20)
    before, after = _pair(tone, 1), _pair(np.roll(tone, 1), 1)
    turn = np.rad2deg(np.arctan2(after[1], after[0]) - np.arctan2(before[1], before[0]))
    assert np.isclose(turn % 360, 45)
    assert np.isclose(360 * 2000 / SR, 90) and np.isclose(360 * 1000 / SR, 45)
    return (
        "pairs (−48, 20), (−20, −48), (48, −20); reading 52 every time; sine probe alone "
        "reads 48, 20, −48, −20; 90° per sample at 2000 Hz, 45° at 1000 Hz"
    )


ANSWERS = {
    "spectrum.1": p1_pair_and_reading,
    "spectrum.2": p2_which_row_fires,
    "spectrum.3": p3_spacing_rows_reach,
    "spectrum.4": p4_decibels,
    "spectrum.5": p5_the_fold,
    "spectrum.6": p6_the_end_row,
    "spectrum.7": p7_spot_the_false_claims,
    "spectrum.8": p8_the_delayed_tone,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
