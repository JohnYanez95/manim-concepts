"""Convolution — the sliding weighted sum, and what it does to every tone at once.

Seven scenes, the second series of the road from sound to the log-mel
spectrogram: the probe's multiply-and-sum walked along a signal (a filter
turns a signal into a signal), what one click becomes, the flip and what it
is for, a moving average read on the bank before and after, the kernel's own
reading as the theorem, multiplying in time, and where convolution lives.

    TheSlidingWeightedSum     the window walks: a moving average, and the word "filter"
    WhatOneClickBecomes       the impulse response; sums pass through, the same rule at every stop
    TheFlip                   the echo kernel: correlation asks, convolution answers
    AMovingAverageIsALowPass  tones through the kernel: scaled, never removed
    TheKernelsOwnReading      the kernel on the bank — filtering in time multiplies the readings
    MultiplyingInTime         the dual, checked once; every frame is a multiplication
    WhereConvolutionLives     reverb, learned kernels, source and filter, the road ahead

Grid and devices are the spectrum series' (N = 8 samples at 8000 Hz; the
helpers below are copied from ``spectrum_manim.py`` — topic directories are
not packages). Every number on screen is exact and machine-verified in
plan 020.

Render:
    uv run python signal_processing/convolution_manim.py
    uv run python signal_processing/convolution_manim.py --scene TheFlip --quality draft
"""

import numpy as np
from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    GOOD,
    LABEL_SIZE,
    MUTED,
    SMALL_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    render_cli,
)

_N = 8  # samples per frame — 1 ms at _SR
_SR = 8000  # samples per second


def _probe(k: int, kind: str) -> np.ndarray:
    """Plan 019 anchor E: probe k at the 8 stops — ``"s"`` the height, ``"c"`` the shadow."""
    angles = 2 * np.pi * k * np.arange(_N) / _N
    return np.sin(angles) if kind == "s" else np.cos(angles)


def _reading(samples, k: int) -> tuple[float, float, float]:
    """Plan 019 anchor A: detector k's pair (cosine sum, sine sum) and its distance — plus-signed,
    so the sine sum is the negative of numpy's imaginary part."""
    a = float(np.dot(samples, _probe(k, "c")))
    b = float(np.dot(samples, _probe(k, "s")))
    return a, b, float(np.hypot(a, b))


def _weight(value: float) -> str:
    """A kernel weight as one glyph where one exists: ⅓, ½ — otherwise ``_fmt``."""
    if abs(value - 1 / 3) < 1e-9:
        return "⅓"
    if abs(value - 0.5) < 1e-9:
        return "½"
    return _fmt(value)


def _fmt(value: float) -> str:
    """Two decimals, trailing zeros dropped, a true minus: 0.7071 → ``0.71``, −1 → ``−1``."""
    rounded = round(float(value), 2)
    if rounded == 0:
        return "0"
    digits = f"{abs(rounded):.2f}".rstrip("0").rstrip(".")
    return f"−{digits}" if rounded < 0 else digits


class _Stems(VGroup):
    """Samples as lollipops on a baseline — a value at an instant, never a staircase.

    ``stems[n]`` is sample n; ``stems.x(n)`` its column, so number strips and probe
    rows line up under it.
    """

    def __init__(
        self,
        values,
        x0: float,
        dx: float,
        y0: float,
        scale: float,
        color: str = COOL,
        radius: float = 0.07,
    ):
        super().__init__()
        # Not ``self.scale``: that would shadow Mobject.scale and break FadeIn.
        self.x0, self.dx, self.y0 = x0, dx, y0
        for n, value in enumerate(values):
            foot = np.array([x0 + n * dx, y0, 0.0])
            head = foot + scale * float(value) * UP
            stem = VGroup(Dot(head, radius=radius, color=color))
            if abs(value) > 1e-9:
                stem.add_to_back(Line(foot, head, color=color, stroke_width=3))
            self.add(stem)

    def x(self, n: int) -> float:
        return self.x0 + n * self.dx


def _number_strip(
    values, stems: _Stems, y: float, color: str | None = None, size: int = SMALL_SIZE
) -> VGroup:
    """One number under each stem."""
    strip = VGroup()
    for n, value in enumerate(values):
        number = Text(_fmt(value), font_size=size)
        if color is not None:
            number.set_color(color)
        strip.add(number.move_to(np.array([stems.x(n), y, 0.0])))
    return strip


def _swap_caption(scene: ConceptScene, old: Text | None, new: Text) -> Text:
    """Replaced text leaves before its replacement arrives."""
    if old is not None:
        scene.play(FadeOut(old), run_time=0.4)
    scene.play(FadeIn(new), run_time=0.5)
    return new


def _takeaway(scene: ConceptScene, text: str, size: int = 25) -> None:
    takeaway = Text(text, font_size=size, line_spacing=1.1).move_to(0.2 * DOWN)
    scene.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
    scene.wait(2)


class _Bank(VGroup):
    """Five detector rows — 0 to 4000 Hz — each a probe pair, a Σ node and a slot for its bar.

    The end rows carry one probe: at 0 and 4 laps the sine probe is all zeros (plan 019 anchor C),
    so it is not drawn.
    """

    ROWS_Y = (1.9, 1.0, 0.1, -0.8, -1.7)
    BAR_X = 0.95
    BAR_UNIT = 0.55

    def __init__(self, feed: np.ndarray):
        super().__init__()
        self.labels, self.thumbs, self.nodes, self.wires, self.fan = (
            VGroup(),
            VGroup(),
            VGroup(),
            VGroup(),
            VGroup(),
        )
        for k, y in enumerate(self.ROWS_Y):
            label = Text(f"{k * _SR // _N} Hz", font_size=SMALL_SIZE)
            label.move_to(np.array([-3.25, y, 0.0]), aligned_edge=LEFT)
            pair = VGroup(_Stems(_probe(k, "c"), -1.7, 0.1, y, 0.22, color=MUTED, radius=0.025))
            if 0 < k < _N // 2:
                pair.add(_Stems(_probe(k, "s"), -0.8, 0.1, y, 0.22, color=MUTED, radius=0.025))
            node = VGroup(
                Circle(radius=0.27, color=MUTED, stroke_width=2),
                Text("Σ", font_size=16, color=MUTED),
            ).move_to(np.array([0.45, y, 0.0]))
            wire = Line(np.array([0.0, y, 0.0]), node[0].get_left(), color=MUTED, stroke_width=1.5)
            self.fan.add(Line(feed, np.array([-3.35, y, 0.0]), color=MUTED, stroke_width=1.5))
            self.labels.add(label)
            self.thumbs.add(pair)
            self.nodes.add(node)
            self.wires.add(wire)
        self.add(self.fan, self.labels, self.thumbs, self.wires, self.nodes)

    def readout(self, samples) -> tuple[VGroup, VGroup]:
        """The bars and their readings for one frame of samples."""
        bars, numbers = VGroup(), VGroup()
        for k, y in enumerate(self.ROWS_Y):
            distance = _reading(samples, k)[2]
            length = max(self.BAR_UNIT * distance, 0.02)
            bar = Rectangle(width=length, height=0.32, stroke_width=0)
            bar.set_fill(ACCENT if distance > 1e-9 else MUTED, opacity=0.9)
            bar.move_to(np.array([self.BAR_X, y, 0.0]), aligned_edge=LEFT)
            number = Text(_fmt(distance), font_size=SMALL_SIZE)
            number.set_color(ACCENT if distance > 1e-9 else MUTED)
            number.next_to(bar, RIGHT, buff=0.15)
            bars.add(bar)
            numbers.add(number)
        return bars, numbers


def _uprights(heights, tops, ticks, left: float, base_y: float, pitch: float, width: float = 0.4):
    """An upright bar chart: floor, bars, a label over each bar and a tick under it."""
    floor = Line(
        np.array([left - 0.5, base_y, 0.0]),
        np.array([left + (len(heights) - 1) * pitch + 0.5, base_y, 0.0]),
        color=MUTED,
        stroke_width=2,
    )
    bars, over, under = VGroup(), VGroup(), VGroup()
    for k, (height, top, tick) in enumerate(zip(heights, tops, ticks, strict=True)):
        live = height > 1e-9
        bar = Rectangle(width=width, height=max(height, 0.02), stroke_width=0)
        bar.set_fill(ACCENT if live else MUTED, opacity=0.9)
        bar.move_to(np.array([left + k * pitch, base_y, 0.0]), aligned_edge=DOWN)
        bars.add(bar)
        over.add(
            Text(top, font_size=SMALL_SIZE, color=ACCENT if live else MUTED).next_to(
                bar, UP, buff=0.12
            )
        )
        under.add(caption(tick).next_to(bar, DOWN, buff=0.15))
    return VGroup(floor, bars, over, under)


# Plan 020 anchor C / R: the flagship kernels. Centred kernels are drawn centred.
_K3 = np.array([1 / 3, 1 / 3, 1 / 3])
_K2 = np.array([0.5, 0.5])
_SPIKE = np.array([2, 2, 2, 8, 2, 2, 2, 2], dtype=float)


def _slide(values, kernel, centred: bool, edge: float = 0.0) -> np.ndarray:
    """Linear convolution on a strip whose neighbours beyond both ends equal ``edge``.

    ``centred`` puts the kernel's middle tap on the current stop; otherwise the
    kernel is causal (its first tap on the current stop, the rest on earlier ones).
    Symmetric kernels give the same answer flipped or not — asymmetric ones do not,
    which is scene 3's whole point, so the flip is applied here explicitly.
    """
    values = np.asarray(values, dtype=float)
    taps = len(kernel)
    offset = taps // 2 if centred else 0
    padded = np.concatenate([np.full(taps, edge), values, np.full(taps, edge)])
    out = np.zeros(len(values))
    for n in range(len(values)):
        for m, weight in enumerate(kernel):
            out[n] += weight * padded[n + taps + offset - m]
    return out


def _ring(values, kernel, centred: bool) -> np.ndarray:
    """Circular convolution on the 8-stop ring — a whole-lap tone's own repetition."""
    values = np.asarray(values, dtype=float)
    taps = len(kernel)
    offset = taps // 2 if centred else 0
    out = np.zeros(_N)
    for n in range(_N):
        for m, weight in enumerate(kernel):
            out[n] += weight * values[(n + offset - m) % _N]
    return out


def _strip(values, x0, dx, y, scale, color=COOL, size=18, label=None, numbers=True):
    """A stem strip on its own axis with (optionally) its numbers under it and a tag left."""
    values = np.asarray(values, dtype=float)
    stems = _Stems(values, x0, dx, y, scale, color=color, radius=0.055)
    axis = Line(
        np.array([x0 - 0.35, y, 0.0]),
        np.array([x0 + (len(values) - 1) * dx + 0.35, y, 0.0]),
        color=MUTED,
        stroke_width=1.5,
    )
    group = VGroup(axis, stems)
    if numbers:
        drop = 0.42 + scale * max(0.0, -float(values.min()))
        group.add(_number_strip(values, stems, y - drop, color=color, size=size))
    if label is not None:
        tag = Text(label, font_size=SMALL_SIZE, color=color)
        group.add(tag.move_to(np.array([x0 - 0.75, y, 0.0]), aligned_edge=RIGHT))
    return group


class _Window(VGroup):
    """The kernel's weights as tokens under ``taps`` adjacent stems, with a Σ node."""

    def __init__(self, kernel, stems: _Stems, at: int, centred: bool, y: float):
        super().__init__()
        taps = len(kernel)
        width = min(0.5, stems.dx - 0.14)
        first = at - (taps // 2 if centred else taps - 1)
        self.tokens = VGroup()
        for m, weight in enumerate(kernel):
            n = first + m
            token = VGroup(
                RoundedRectangle(width=width, height=0.36, corner_radius=0.08, stroke_width=1.5)
                .set_stroke(MUTED)
                .set_fill(MUTED, opacity=0.18),
                Text(_weight(weight), font_size=18, color=MUTED),
            ).move_to(np.array([stems.x(n), y, 0.0]))
            self.tokens.add(token)
        self.frame = SurroundingRectangle(
            VGroup(*[stems[first + m] for m in range(taps)], self.tokens),
            color=ACCENT,
            buff=0.12,
            corner_radius=0.1,
            stroke_width=2,
        )
        self.add(self.frame, self.tokens)


class TheSlidingWeightedSum(ConceptScene):
    """The probe's multiply-and-sum walked along a signal: at every stop one output —
    a moving average, and the word "filter": it turns a signal into a signal."""

    def construct(self):
        self.play(FadeIn(self.title("The Sliding Weighted Sum"), shift=0.3 * DOWN))
        prompt = Text(
            "The detector gave one number. What if the window moves?", font_size=BODY_SIZE
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))
        self.wait(1.2)
        self.play(FadeOut(prompt))

        # --- level 1: the spike, and the window that walks -----------------------------
        x0, dx, scale = -3.3, 1.0, 0.16
        top_y, out_y = 1.3, -1.1
        # The strip carries one neighbour beyond each end (the steady 2), drawn muted,
        # so the window has something to read at the edges.
        with_edges = np.concatenate([[2.0], _SPIKE, [2.0]])
        signal = _Stems(with_edges, x0 - dx, dx, top_y, scale)
        for ghost in (signal[0], signal[-1]):
            ghost.set_color(MUTED).set_opacity(0.5)
        axis = Line(
            np.array([x0 - 1.5, top_y, 0.0]),
            np.array([x0 + 8 * dx + 0.5, top_y, 0.0]),
            color=MUTED,
            stroke_width=1.5,
        )
        inner = _Stems(_SPIKE, x0, dx, top_y, scale)
        numbers = _number_strip(_SPIKE, inner, top_y - 0.4, color=COOL)
        in_tag = caption("the signal", COOL).move_to(np.array([x0 - 2.35, top_y, 0.0]))
        self.play(FadeIn(axis), FadeIn(signal), FadeIn(numbers), FadeIn(in_tag))
        note = _swap_caption(
            self,
            None,
            caption(
                "a spike in a steady signal: 2, 2, 2, 8, 2, 2, 2, 2 — and 2 beyond both ends"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.2)

        out_axis = Line(
            np.array([x0 - 1.5, out_y, 0.0]),
            np.array([x0 + 8 * dx + 0.5, out_y, 0.0]),
            color=MUTED,
            stroke_width=1.5,
        )
        out_tag = caption("the output", ACCENT).move_to(np.array([x0 - 2.35, out_y, 0.0]))
        self.play(FadeIn(out_axis), FadeIn(out_tag))
        result = _slide(_SPIKE, _K3, centred=True, edge=2.0)
        out_stems = _Stems(result, x0, dx, out_y, scale, color=ACCENT)
        out_numbers = _number_strip(result, out_stems, out_y - 0.4, color=ACCENT)

        window = _Window(_K3, signal, 1, True, top_y - 0.85)
        self.play(FadeIn(window))
        note = _swap_caption(
            self,
            note,
            caption(
                "three weights of ⅓: multiply the three samples under the window, then add"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.0)
        for n in range(_N):
            if n:
                target = _Window(_K3, signal, n + 1, True, top_y - 0.85)
                self.play(Transform(window, target), run_time=0.45)
            arrow = Arrow(
                window.frame.get_bottom(),
                np.array([out_stems.x(n), out_y + 0.25, 0.0]),
                color=ACCENT,
                buff=0.05,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            )
            self.play(GrowArrow(arrow), FadeIn(out_stems[n]), FadeIn(out_numbers[n]), run_time=0.4)
            self.remove(arrow)
            if n == 1:
                note = _swap_caption(
                    self,
                    note,
                    caption(
                        "the probe's multiply-and-sum, now walking: one output at every stop"
                    ).move_to(3.2 * DOWN),
                )
        self.wait(1.0)
        note = _swap_caption(
            self,
            note,
            caption(
                "the spike spread over three stops and lowered: 8 became 4, 4, 4 — a moving average"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)

        # --- the word: a filter turns a signal into a signal -----------------------------
        definition = Text(
            "a filter turns a signal into a signal",
            font_size=LABEL_SIZE,
            color=ACCENT,
        ).move_to(2.4 * DOWN)
        self.play(FadeIn(definition), Create(boxed(definition, buff=0.2)))
        note = _swap_caption(
            self,
            note,
            caption(
                "the detector gave one number per frame; slide the window and they form a signal"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        # --- the weights sum to 1: nothing is added or lost ------------------------------
        totals = VGroup(
            Text("in: 22", font_size=SMALL_SIZE, color=COOL),
            Text("out: 22", font_size=SMALL_SIZE, color=ACCENT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        totals.move_to(np.array([x0 + 8 * dx + 1.15, (top_y + out_y) / 2, 0.0]))
        self.play(FadeIn(totals))
        note = _swap_caption(
            self,
            note,
            caption(
                "⅓ + ⅓ + ⅓ = 1, so the totals agree: the window spreads, it does not add"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.4)
        heavy = _slide(_SPIKE, np.array([1.0, 1.0, 1.0]), centred=True, edge=2.0)
        heavy_numbers = _number_strip(heavy, out_stems, out_y - 0.4, color=WARM)
        heavy_tokens = _Window(np.array([1.0, 1.0, 1.0]), signal, 8, True, top_y - 0.85)
        self.play(
            FadeOut(out_numbers),
            FadeOut(out_stems),
            FadeOut(totals[1]),
            Transform(window, heavy_tokens),
            run_time=0.5,
        )
        self.play(FadeIn(heavy_numbers))
        heavier = Text("out: 66", font_size=SMALL_SIZE, color=WARM).move_to(totals[1])
        self.play(FadeIn(heavier))
        note = _swap_caption(
            self,
            note,
            caption(
                "weights 1, 1, 1 instead: three times as loud — the weights' sum is the gain"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        self.play(
            FadeOut(
                VGroup(
                    axis,
                    signal,
                    numbers,
                    in_tag,
                    out_axis,
                    out_tag,
                    heavy_numbers,
                    window,
                    definition,
                    totals[0],
                    heavier,
                    note,
                )
            )
        )
        _takeaway(
            self,
            "Slide a window of weights along a signal, multiplying and adding at\n"
            "every stop — the output is a signal too. That is a filter, and the\n"
            "window is its kernel",
        )


class WhatOneClickBecomes(ConceptScene):
    """One click through the kernel gives the kernel back — the impulse response — and a
    signal is a sum of scaled, shifted clicks, so its output is the same sum of scaled,
    shifted responses: sums pass through, and the same rule holds at every stop."""

    def construct(self):
        self.play(FadeIn(self.title("What One Click Becomes"), shift=0.3 * DOWN))
        x0, dx, scale = -4.6, 0.8, 0.9
        click = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=float)
        top_y, out_y = 1.7, -0.3

        # --- level 1: the click comes out as the kernel -------------------------------
        signal = _strip(click, x0, dx, top_y, scale, label="in")
        output = _strip(
            _slide(click, _K3, centred=False), x0, dx, out_y, scale, color=ACCENT, label="out"
        )
        self.play(FadeIn(signal))
        note = _swap_caption(
            self,
            None,
            caption("one click — a single 1 in a run of zeros — through the ⅓ ⅓ ⅓ window").move_to(
                3.2 * DOWN
            ),
        )
        self.play(FadeIn(output))
        note = _swap_caption(
            self,
            note,
            caption(
                "out comes the kernel itself, ⅓ ⅓ ⅓ — the impulse response: what one click becomes"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)

        # A scaled click, a later click.
        for values, line in (
            (-2 * click, "a click of −2: the same shape, −2 as tall"),
            (np.roll(click, 3), "a click three stops later: the same shape, three stops later"),
        ):
            new_in = _strip(values, x0, dx, top_y, scale, label="in")
            new_out = _strip(
                _slide(values, _K3, centred=False), x0, dx, out_y, scale, color=ACCENT, label="out"
            )
            self.play(FadeOut(signal), FadeOut(output), run_time=0.35)
            signal, output = new_in, new_out
            self.play(FadeIn(signal), FadeIn(output))
            note = _swap_caption(self, note, caption(line).move_to(3.2 * DOWN))
            self.wait(1.3)
        rule = Text(
            "scaled in → scaled out · later in → later out", font_size=LABEL_SIZE, color=ACCENT
        )
        rule.move_to(2.3 * DOWN)
        self.play(FadeIn(rule))
        self.wait(1.4)
        self.play(FadeOut(VGroup(signal, output, rule, note)))

        # --- level 2: a signal is a sum of clicks, so its output is a sum of responses ---
        four = np.array([1, 2, 0, 3], dtype=float)
        kernel = _K2
        result = np.array([0.5, 1.5, 1.0, 1.5, 1.5])  # anchor P: length 4 + 2 − 1 = 5
        lx0, ldx, lscale = -4.9, 0.6, 0.16
        left_in = _strip(np.append(four, 0.0), lx0, ldx, 2.05, lscale, label="in")
        for ghost in (left_in[1][-1],):
            ghost.set_color(MUTED).set_opacity(0.5)
        self.play(FadeIn(left_in))
        note = _swap_caption(
            self,
            None,
            caption(
                "1, 2, 0, 3 through the window ½ ½ — read as three clicks, each with a response"
            ).move_to(3.2 * DOWN),
        )
        copies = VGroup()
        ys = (1.1, 0.2, -0.7)
        for (stop, amount), y in zip(((0, 1.0), (1, 2.0), (3, 3.0)), ys, strict=True):
            piece = np.zeros(5)
            piece[stop : stop + 2] = amount * kernel
            copy = _strip(piece, lx0, ldx, y, lscale, color=MUTED, size=16)
            tag = Text(f"{_fmt(amount)}× at {stop}", font_size=16, color=MUTED)
            tag.move_to(np.array([lx0 - 0.55, y, 0.0]), aligned_edge=RIGHT)
            copies.add(VGroup(copy, tag))
        self.play(LaggedStart(*[FadeIn(c) for c in copies], lag_ratio=0.3))
        self.wait(1.0)
        left_out = _strip(result, lx0, ldx, -1.6, lscale, color=GOOD, label="sum")
        self.play(FadeIn(left_out))
        note = _swap_caption(
            self,
            note,
            caption(
                "stack the responses and add by column: 0.5, 1.5, 1, 1.5, 1.5 — five from four"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)

        # The other view: one output at a time, the window read over the input.
        rx0 = 1.9
        right_in = _strip(np.append(four, 0.0), rx0, ldx, 2.05, lscale, label="in", numbers=False)
        right_in[1][-1].set_color(MUTED).set_opacity(0.5)
        right_out = _strip(result, rx0, ldx, -1.6, lscale, color=ACCENT, label="out")
        self.play(FadeIn(right_in))
        window = _Window(kernel, right_in[1], 1, False, 1.35)
        self.play(FadeIn(window))
        for n in range(5):
            if n:
                self.play(
                    Transform(window, _Window(kernel, right_in[1], n, False, 1.35)), run_time=0.35
                )
            self.play(FadeIn(right_out[1][n]), FadeIn(right_out[2][n]), run_time=0.3)
        self.play(FadeIn(right_out[0]), FadeIn(right_out[3]))
        note = _swap_caption(
            self,
            note,
            caption(
                "or walk the window as before: one output at a time — the same five numbers"
            ).move_to(3.2 * DOWN),
        )
        match = Text("the same answer, two ways", font_size=SMALL_SIZE, color=GOOD)
        match.move_to(np.array([rx0 + 1.2, 0.0, 0.0]))
        self.play(FadeIn(match))
        self.wait(1.6)

        facts = VGroup(
            Text(
                "sums pass through — the response of a sum is the sum of the responses",
                font_size=SMALL_SIZE,
            ),
            Text(
                "the same rule at every stop — a later click gets a later response",
                font_size=SMALL_SIZE,
            ),
        ).arrange(DOWN, buff=0.22)
        facts.move_to(0.6 * UP)
        self.play(
            FadeOut(VGroup(left_in, copies, left_out, right_in, window, match, note)), run_time=0.5
        )
        self.play(FadeIn(facts))
        note = _swap_caption(
            self,
            None,
            caption(
                "two owned facts: the weighted sum is linear (the dice); the window never changes"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)

        self.play(FadeOut(VGroup(right_out, facts, note)))
        _takeaway(
            self,
            "A filter is known by what one click becomes. A signal is a sum\n"
            "of scaled, shifted clicks — so its output is the same sum of\n"
            "scaled, shifted responses",
        )


class TheFlip(ConceptScene):
    """Slide a pattern the probe's way and an echo lands before the click; flip it and the
    echo lands after — the flip is what makes the sliding sum answer "what does this system
    do to a click", and a symmetric kernel hides it."""

    def construct(self):
        self.play(FadeIn(self.title("The Flip"), shift=0.3 * DOWN))
        prompt = Text(
            "The probe never flipped anything. Why does convolution?", font_size=BODY_SIZE
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))
        self.wait(1.2)
        self.play(FadeOut(prompt))

        # A strip from stop −4 to stop 4, the click at 0.
        stops = np.arange(-4, 5)
        x0, dx, scale = -3.4, 0.7, 1.0
        click = (stops == 0).astype(float)
        echo = np.array([1.0, 0.0, 0.0, 0.5])
        top_y, mid_y, low_y = 1.7, 0.1, -1.5

        def strip_with_stops(values, y, color, label):
            group = _strip(values, x0, dx, y, scale, color=color, label=label, numbers=False)
            ticks = VGroup(
                *[
                    caption(str(stop)).move_to(np.array([x0 + i * dx, y - 0.35, 0.0]))
                    for i, stop in enumerate(stops)
                ]
            )
            return VGroup(group, ticks)

        signal = strip_with_stops(click, top_y, COOL, "the click")
        kernel_tokens = VGroup(
            *[
                VGroup(
                    RoundedRectangle(width=0.5, height=0.36, corner_radius=0.08, stroke_width=1.5)
                    .set_stroke(MUTED)
                    .set_fill(MUTED, opacity=0.18),
                    Text(_weight(w), font_size=18, color=MUTED),
                )
                for w in echo
            ]
        ).arrange(RIGHT, buff=0.12)
        kernel_tag = Text("the echo kernel\n1, 0, 0, ½", font_size=SMALL_SIZE, line_spacing=1.0)
        kernel_tag.next_to(kernel_tokens, UP, buff=0.15)
        VGroup(kernel_tokens, kernel_tag).move_to(np.array([5.1, top_y + 0.1, 0.0]))
        self.play(FadeIn(signal), FadeIn(kernel_tokens), FadeIn(kernel_tag))
        note = _swap_caption(
            self,
            None,
            caption("a kernel with a memory: the click now, and half of it three stops on").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.4)

        # The probe's way: the pattern slid unreversed — the half-click lands early.
        pre = np.zeros(9)
        pre[4] = 1.0
        pre[1] = 0.5
        probe_way = strip_with_stops(pre, mid_y, WARM, "slid as is")
        self.play(FadeIn(probe_way))
        note = _swap_caption(
            self,
            note,
            caption(
                "slide the pattern as the probe did, multiply and add: the half lands at −3"
            ).move_to(3.2 * DOWN),
        )
        pre_tag = Text("a pre-echo?", font_size=SMALL_SIZE, color=WARM)
        pre_tag.move_to(np.array([5.1, mid_y, 0.0]))
        self.play(FadeIn(pre_tag))
        self.wait(1.6)

        post = np.zeros(9)
        post[4] = 1.0
        post[7] = 0.5
        flipped_way = strip_with_stops(post, low_y, ACCENT, "flipped")
        self.play(FadeIn(flipped_way))
        note = _swap_caption(
            self,
            note,
            caption(
                "flip the pattern first and the half lands at +3 — an echo after the click"
            ).move_to(3.2 * DOWN),
        )
        post_tag = Text("the echo, after", font_size=SMALL_SIZE, color=ACCENT)
        post_tag.move_to(np.array([5.1, low_y, 0.0]))
        self.play(FadeIn(post_tag))
        self.wait(1.8)

        verdict = VGroup(
            Text(
                "correlation asks: how much does the signal look like this pattern, here?",
                font_size=SMALL_SIZE,
            ),
            Text(
                "convolution asks: what does this system do to a click?",
                font_size=SMALL_SIZE,
                color=ACCENT,
            ),
        ).arrange(DOWN, buff=0.18)
        verdict.move_to(2.5 * DOWN)
        self.play(FadeOut(note), run_time=0.3)
        self.play(FadeIn(verdict))
        self.wait(2.0)
        self.play(FadeOut(verdict))
        note = _swap_caption(
            self,
            None,
            caption(
                "same numbers, one list reversed — ⅓ ⅓ ⅓ reversed is itself, so the average hid it"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        # --- causality: the centred window peeks ahead --------------------------------
        self.play(
            FadeOut(
                VGroup(
                    signal,
                    probe_way,
                    flipped_way,
                    kernel_tokens,
                    kernel_tag,
                    pre_tag,
                    post_tag,
                    note,
                )
            )
        )
        step = np.array([0, 0, 0, 1, 1, 1, 1, 1], dtype=float)
        sx0, sdx, sscale = -3.0, 0.9, 0.9
        s_in = _strip(np.append(step, 1.0), sx0, sdx, 1.6, sscale, label="a step")
        s_in[1][-1].set_color(MUTED).set_opacity(0.5)
        # Anchor U: the strip continues at 1 beyond its right end (drawn), at 0 before it.
        centred_vals = np.array([0, 0, 1 / 3, 2 / 3, 1, 1, 1, 1])
        causal_vals = np.array([0, 0, 0, 1 / 3, 2 / 3, 1, 1, 1])
        centred = _strip(centred_vals, sx0, sdx, 0.0, sscale, color=ACCENT, label="centred")
        causal = _strip(causal_vals, sx0, sdx, -1.6, sscale, color=ACCENT, label="causal")
        self.play(FadeIn(s_in))
        self.play(FadeIn(centred))
        note = _swap_caption(
            self,
            None,
            caption(
                "a step through the centred window: smoothed in place — but it read one stop ahead"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        self.play(FadeIn(causal))
        note = _swap_caption(
            self,
            note,
            caption(
                "reading only the past gives the same numbers a stop late: delay is the price"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        aside = caption(
            'conv layers slide unflipped yet say "convolution" — a learned kernel does not mind'
        )
        aside.move_to(2.5 * DOWN)
        self.play(FadeIn(aside))
        self.wait(1.8)

        self.play(FadeOut(VGroup(s_in, centred, causal, note, aside)))
        _takeaway(
            self,
            'The flip turns "does the signal match this pattern here" into\n'
            '"what does this system do to a click" — a symmetric kernel\n'
            "cannot tell the two apart",
        )


def _bank_readout(bank: _Bank, samples, x: float, unit: float = 0.2, color=ACCENT):
    """Bars for one ring of samples at column ``x`` — ``unit`` scene units per reading."""
    bars, numbers = VGroup(), VGroup()
    for k, y in enumerate(bank.ROWS_Y):
        distance = _reading(samples, k)[2]
        live = distance > 1e-9
        bar = Rectangle(width=max(unit * distance, 0.02), height=0.32, stroke_width=0)
        bar.set_fill(color if live else MUTED, opacity=0.9)
        bar.move_to(np.array([x, y, 0.0]), aligned_edge=LEFT)
        number = Text(_fmt(distance), font_size=SMALL_SIZE, color=color if live else MUTED)
        number.next_to(bar, RIGHT, buff=0.12)
        bars.add(bar)
        numbers.add(number)
    return bars, numbers


class AMovingAverageIsALowPass(ConceptScene):
    """Every whole-lap tone comes out of the moving average as the same tone, scaled — slow
    ones barely, fast ones a lot, two with their sign flipped: a low-pass scales, it does
    not remove. Gain 0 is the special case."""

    def construct(self):
        self.play(FadeIn(self.title("A Moving Average Is a Low-Pass"), shift=0.3 * DOWN))
        prompt = Text("What does the ⅓ ⅓ ⅓ window do to a tone?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))
        self.wait(1.0)
        self.play(FadeOut(prompt))

        # Left: the tone in and out on the ring. Right: the bank read before and after.
        x0, dx, scale = -5.7, 0.32, 0.5
        in_y, out_y = 1.4, -0.6
        feed = np.array([x0 + 7 * dx + 0.25, 0.4, 0.0])
        bank = _Bank(feed)
        bank.shift(0.3 * RIGHT)
        self.play(FadeIn(bank.labels), FadeIn(bank.thumbs), FadeIn(bank.wires), FadeIn(bank.nodes))
        heads = VGroup(
            caption("before", COOL).move_to(np.array([2.0, 2.55, 0.0])),
            caption("after", ACCENT).move_to(np.array([4.5, 2.55, 0.0])),
        )
        self.play(FadeIn(heads))
        note = _swap_caption(
            self,
            None,
            caption(
                "the bank from the spectrum series reads the tone before and after the window"
            ).move_to(3.2 * DOWN),
        )

        # Anchor D (centred 3-tap): 1000 Hz → 0.80, 2000 → ⅓, 3000 → 0.14 flipped, 4000 → ⅓ flipped.
        cases = [
            (1, "s", "1000 Hz: the same tone, 0.80 as tall — the reading 4 became 3.22"),
            (2, "s", "2000 Hz: the same tone, exactly ⅓ as tall — 4 became 1.33"),
            (3, "s", "3000 Hz: 0.14 as tall, and upside down — the sign flipped"),
            (4, "c", "4000 Hz: ⅓ as tall and upside down — the end row reads ÷ 8: 8 became 2.67"),
            (0, "c", "0 Hz — a constant: unchanged. Slow tones pass, fast tones shrink"),
        ]
        in_strip = out_strip = before = after = None
        for k, kind, line in cases:
            tone = _probe(k, kind)
            out = _ring(tone, _K3, centred=True)
            flipped = k in (3, 4)
            new_in = _strip(tone, x0, dx, in_y, scale, label="in", numbers=False)
            new_out = _strip(
                out,
                x0,
                dx,
                out_y,
                scale,
                color=WARM if flipped else ACCENT,
                label="out",
                numbers=False,
            )
            new_before = _bank_readout(bank, tone, 1.25, color=COOL)
            new_after = _bank_readout(bank, out, 3.75, color=WARM if flipped else ACCENT)
            olds = [m for m in (in_strip, out_strip) if m is not None]
            if before is not None:
                olds += [before[0], before[1], after[0], after[1]]
            # The old caption leaves with the old tone, so the words never lag the picture.
            self.play(FadeOut(VGroup(*olds, note)), run_time=0.4)
            in_strip, out_strip, before, after = new_in, new_out, new_before, new_after
            self.play(FadeIn(in_strip), FadeIn(before[0]), FadeIn(before[1]))
            self.play(FadeIn(out_strip), FadeIn(after[0]), FadeIn(after[1]))
            note = _swap_caption(self, None, caption(line).move_to(3.2 * DOWN))
            self.wait(1.6)

        verdict = Text("a low-pass scales — it does not remove", font_size=LABEL_SIZE, color=ACCENT)
        verdict.move_to(2.5 * DOWN)
        verdict_box = boxed(verdict, buff=0.2)
        self.play(FadeIn(verdict), Create(verdict_box))
        self.wait(1.6)
        self.play(
            FadeOut(
                VGroup(
                    in_strip,
                    out_strip,
                    before[0],
                    before[1],
                    after[0],
                    after[1],
                    verdict,
                    verdict_box,
                    note,
                )
            )
        )

        # --- the special case: gain 0 -----------------------------------------------------
        tone = _probe(4, "c")
        out = _ring(tone, _K2, centred=False)
        in_strip = _strip(tone, x0, dx, in_y, scale, label="in", numbers=False)
        out_strip = _strip(out, x0, dx, out_y, scale, color=MUTED, label="out", numbers=False)
        before = _bank_readout(bank, tone, 1.25, color=COOL)
        after = _bank_readout(bank, out, 3.75, color=ACCENT)
        self.play(FadeIn(in_strip), FadeIn(before[0]), FadeIn(before[1]))
        note = _swap_caption(
            self,
            None,
            caption(
                "a two-weight window, ½ ½, on the 4000 Hz tone: 1, −1, 1, −1 … averages to 0"
            ).move_to(3.2 * DOWN),
        )
        self.play(FadeIn(out_strip), FadeIn(after[0]), FadeIn(after[1]))
        note = _swap_caption(
            self,
            note,
            caption(
                "all eight outputs exactly 0 — removed, because its gain happens to be 0"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        self.play(
            FadeOut(VGroup(in_strip, out_strip, before[0], before[1], after[0], after[1])),
            run_time=0.4,
        )
        tone = _probe(2, "s")
        out = _ring(tone, _K2, centred=False)
        in_strip = _strip(tone, x0, dx, in_y, scale, label="in", numbers=False)
        out_strip = _strip(out, x0, dx, out_y, scale, color=ACCENT, label="out", numbers=False)
        before = _bank_readout(bank, tone, 1.25, color=COOL)
        after = _bank_readout(bank, out, 3.75, color=ACCENT)
        self.play(FadeIn(in_strip), FadeIn(before[0]), FadeIn(before[1]))
        self.play(FadeIn(out_strip), FadeIn(after[0]), FadeIn(after[1]))
        note = _swap_caption(
            self,
            note,
            caption(
                "same window on 2000 Hz: 0.71 as tall, half a sample late — the pair turned 45°"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        smith = caption(
            "the best smoother and a poor frequency separator: row 3 is quieter than row 4"
        )
        smith.move_to(2.5 * DOWN)
        self.play(FadeIn(smith))
        self.wait(1.8)

        self.play(
            FadeOut(
                VGroup(
                    in_strip,
                    out_strip,
                    before[0],
                    before[1],
                    after[0],
                    after[1],
                    bank,
                    heads,
                    note,
                    smith,
                )
            )
        )
        _takeaway(
            self,
            "A tone through a filter is the same tone, scaled — by a number\n"
            "that depends on the frequency. Low-pass: slow tones pass, fast\n"
            "tones shrink. Gain 0 is the one case where a tone is removed",
        )


class TheKernelsOwnReading(ConceptScene):
    """Feed the kernel itself to the bank and its readings are the gains — because a delay
    turns a tone's pair, sums pass through, and the kernel is a sum of delayed clicks:
    filtering in time multiplies the readings, row by row."""

    def construct(self):
        self.play(FadeIn(self.title("The Kernel's Own Reading"), shift=0.3 * DOWN))
        prompt = Text("Where did 0.80, ⅓, 0.14, ⅓ come from?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))
        self.wait(1.0)
        self.play(FadeOut(prompt))

        # --- the kernel on the bank -------------------------------------------------------
        x0, dx, scale = -5.7, 0.32, 0.9
        kernel_ring = np.zeros(_N)
        kernel_ring[[7, 0, 1]] = 1 / 3
        feed = np.array([x0 + 7 * dx + 0.25, 0.4, 0.0])
        bank = _Bank(feed)
        bank.shift(0.3 * RIGHT)
        strip = _strip(kernel_ring, x0, dx, 0.4, scale, color=MUTED, numbers=False)
        strip_tag = caption("the kernel, as a signal").move_to(np.array([x0 + 3.5 * dx, 1.75, 0.0]))
        self.play(FadeIn(bank.labels), FadeIn(bank.thumbs), FadeIn(bank.wires), FadeIn(bank.nodes))
        self.play(FadeIn(strip))
        note = _swap_caption(
            self,
            None,
            caption(
                "the kernel as a signal: ⅓ at stops 7, 0, 1 — on the ring, the stop before 0 is 7"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.2)
        bars, numbers = _bank_readout(bank, kernel_ring, 1.25, unit=0.55)
        # The sine sums are all 0 here, so the cosine sum carries the sign: show it.
        signed = VGroup()
        for k, number in enumerate(numbers):
            a = _reading(kernel_ring, k)[0]
            label = Text(_fmt(a), font_size=SMALL_SIZE, color=WARM if a < 0 else ACCENT)
            signed.add(label.move_to(number, aligned_edge=LEFT))
        self.play(*[GrowFromEdge(bar, LEFT) for bar in bars], FadeIn(numbers))
        self.play(FadeOut(numbers), run_time=0.3)
        self.play(FadeIn(signed), run_time=0.4)
        note = _swap_caption(
            self,
            note,
            caption(
                "its readings 1, 0.80, 0.33, 0.14, 0.33: the previous scene's gains, signs and all"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(bank, strip, strip_tag, bars, signed, note)))

        # --- why: on the pair plane, a delay is a turn, and sums pass through --------------
        origin = np.array([-3.4, -0.2, 0.0])
        unit = 1.9
        plane = VGroup(
            Line(origin + 2.2 * LEFT, origin + 2.2 * RIGHT, color=MUTED, stroke_width=2),
            Line(origin + 2.2 * DOWN, origin + 2.2 * UP, color=MUTED, stroke_width=2),
            Circle(radius=unit, color=MUTED, stroke_width=1.5).move_to(origin),
        )
        plane_tag = caption("the pair plane: across cosine sum, up sine sum").move_to(
            np.array([-3.4, -2.65, 0.0])
        )
        self.play(Create(plane), FadeIn(plane_tag))
        note = _swap_caption(
            self,
            None,
            caption(
                "recall: delaying a tone by one sample turns its pair — by 45° × the row number"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.4)
        facts = VGroup(
            Text("the kernel is three clicks:\n⅓ early, ⅓ now, ⅓ late", font_size=SMALL_SIZE),
            Text("each click's copy of the tone\nis the tone, turned", font_size=SMALL_SIZE),
            Text("sums pass through — so add\nthree arrows of length ⅓", font_size=SMALL_SIZE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        facts.move_to(np.array([3.6, 1.3, 0.0]))
        for line in facts:
            self.play(FadeIn(line, shift=0.1 * UP), run_time=0.5)
        self.wait(1.0)

        readout = Text("", font_size=LABEL_SIZE)
        arrows = VGroup()
        for k in range(1, 5):
            angle = np.pi / 4 * k
            steps = [(1 / 3, -angle), (1 / 3, 0.0), (1 / 3, angle)]
            tip = origin.copy()
            new_arrows = VGroup()
            for length, theta in steps:
                head = tip + unit * length * np.array([np.cos(theta), np.sin(theta), 0.0])
                new_arrows.add(
                    Arrow(
                        tip,
                        head,
                        buff=0,
                        color=ACCENT,
                        stroke_width=3,
                        max_tip_length_to_length_ratio=0.25,
                    )
                )
                tip = head
            total = (tip - origin)[0] / unit
            resultant = Line(origin, tip, color=GOOD, stroke_width=4)
            label = Text(f"row {k}: {_fmt(total)}", font_size=LABEL_SIZE, color=GOOD)
            label.move_to(np.array([3.4, -0.2, 0.0]))
            if arrows:
                self.play(FadeOut(arrows), FadeOut(readout), run_time=0.3)
            arrows = VGroup(new_arrows, resultant)
            readout = label
            self.play(LaggedStart(*[GrowArrow(a) for a in new_arrows], lag_ratio=0.4), run_time=1.0)
            self.play(Create(resultant), FadeIn(readout))
            lines = {
                1: "row 1: the side arrows lean forward — ⅓ + 2 × ⅓ × cos 45° = 0.80",
                2: "row 2: the side arrows point straight up and down and cancel — ⅓",
                3: "row 3: they lean backward — 0.14 the wrong way: the flipped sign",
                4: "row 4: both side arrows point backward — −⅓",
            }
            note = _swap_caption(self, note, caption(lines[k]).move_to(3.2 * DOWN))
            self.wait(1.6)

        rule = Text(
            "filtering in time = multiplying the readings, row by row",
            font_size=LABEL_SIZE,
            color=ACCENT,
        ).move_to(2.45 * DOWN)
        rule_box = boxed(rule, buff=0.2)
        self.play(FadeOut(plane_tag), run_time=0.3)
        self.play(FadeIn(rule), Create(rule_box))
        note = _swap_caption(
            self,
            note,
            caption(
                "the output's pair is the input's pair times the kernel's reading: the theorem"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        debt = caption(
            "checked on one kernel and four rows; for every kernel and N, the proof needs Euler"
        )
        debt.move_to(3.2 * DOWN)
        self.play(FadeOut(note), run_time=0.3)
        self.play(FadeIn(debt))
        self.wait(1.8)
        self.play(FadeOut(debt))
        note = _swap_caption(
            self,
            None,
            caption(
                "½ ½ reads (½, ½) on row 2: length 0.71, turned 45° — the previous scene's turn"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        self.play(FadeOut(VGroup(plane, facts, arrows, readout, rule, rule_box, note)))
        _takeaway(
            self,
            "Read the kernel on the bank and you have read what it does to\n"
            "every tone: filtering in time is multiplying the readings,\n"
            "row by row — checked here, proved with Euler's formula",
        )


class MultiplyingInTime(ConceptScene):
    """The dual: multiply two signals stop by stop and their readings convolve — each line of
    one gets a copy of the other's lines. Every frame is such a multiplication, by a
    rectangle of ones: a whole-lap tone does not notice, the 1500 Hz tone does — leakage."""

    def construct(self):
        self.play(FadeIn(self.title("Multiplying in Time"), shift=0.3 * DOWN))
        prompt = Text(
            "Filtering multiplies the readings. What multiplies the samples?", font_size=BODY_SIZE
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))
        self.wait(1.2)
        self.play(FadeOut(prompt))

        # --- the dual, checked once (anchor T) ------------------------------------------
        x0, dx, scale = -5.9, 0.34, 0.55
        feed = np.array([x0 + 7 * dx + 0.25, 0.4, 0.0])
        bank = _Bank(feed)
        bank.shift(0.3 * RIGHT)
        self.play(FadeIn(bank.labels), FadeIn(bank.thumbs), FadeIn(bank.wires), FadeIn(bank.nodes))
        tone = _probe(2, "s")
        window = _probe(1, "c")
        product = tone * window
        strip_a = _strip(tone, x0, dx, 1.6, scale, numbers=False)
        strip_b = _strip(window, x0, dx, 0.4, scale, color=MUTED, label="×", numbers=False)
        strip_c = _strip(product, x0, dx, -0.9, scale, color=ACCENT, label="=", numbers=False)
        col_a = _bank_readout(bank, tone, 1.25, color=COOL)
        col_b = _bank_readout(bank, window, 2.6, color=MUTED)
        col_c = _bank_readout(bank, product, 3.95, color=ACCENT)
        heads = VGroup(
            caption("tone", COOL).move_to(np.array([1.7, 2.55, 0.0])),
            caption("× window", MUTED).move_to(np.array([3.0, 2.55, 0.0])),
            caption("= product", ACCENT).move_to(np.array([4.75, 2.55, 0.0])),
        )
        self.play(FadeIn(strip_a), FadeIn(col_a[0]), FadeIn(col_a[1]), FadeIn(heads[0]))
        note = _swap_caption(
            self,
            None,
            caption(
                "a 2000 Hz tone: row 2 reads 4. Multiply it, stop by stop, by a 1000 Hz cosine"
            ).move_to(3.2 * DOWN),
        )
        self.play(FadeIn(strip_b), FadeIn(col_b[0]), FadeIn(col_b[1]), FadeIn(heads[1]))
        self.wait(1.0)
        self.play(FadeIn(strip_c), FadeIn(col_c[0]), FadeIn(col_c[1]), FadeIn(heads[2]))
        note = _swap_caption(
            self,
            note,
            caption(
                "row 2 empties; rows 1 and 3 read 2 each — the tone's line took the window's lines"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        arithmetic = Text("4 × 4 ÷ 8 = 2, for this pair", font_size=SMALL_SIZE, color=ACCENT)
        arithmetic.move_to(np.array([3.1, -2.45, 0.0]))
        self.play(FadeIn(arithmetic))
        note = _swap_caption(
            self,
            note,
            caption(
                "multiply in time and the readings convolve — the theorem's other half, stated"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        self.play(
            FadeOut(VGroup(strip_b, strip_c, col_b[0], col_b[1], col_c[0], col_c[1], arithmetic)),
            run_time=0.4,
        )
        ones = _probe(0, "c")
        strip_b = _strip(ones, x0, dx, 0.4, scale, color=MUTED, label="×", numbers=False)
        strip_c = _strip(tone * ones, x0, dx, -0.9, scale, color=ACCENT, label="=", numbers=False)
        col_b = _bank_readout(bank, ones, 2.6, unit=0.1, color=MUTED)
        col_c = _bank_readout(bank, tone * ones, 3.95, color=ACCENT)
        self.play(FadeIn(strip_b), FadeIn(col_b[0]), FadeIn(col_b[1]))
        self.play(FadeIn(strip_c), FadeIn(col_c[0]), FadeIn(col_c[1]))
        note = _swap_caption(
            self,
            note,
            caption(
                "multiply by all ones — a window that reads only on row 0 — and nothing moves"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)

        # --- every frame is a multiplication: the hook to series D (anchor T of plan 019) --
        self.play(
            FadeOut(
                VGroup(
                    strip_a,
                    strip_b,
                    strip_c,
                    col_a[0],
                    col_a[1],
                    col_b[0],
                    col_b[1],
                    col_c[0],
                    col_c[1],
                    heads,
                    bank,
                    note,
                )
            )
        )
        between = np.sin(2 * np.pi * 1.5 * np.arange(_N) / _N)
        long_x0, long_dx = -3.6, 0.36
        long_t = np.arange(-8, 24)
        endless = np.sin(2 * np.pi * 1.5 * long_t / 8)
        wave = _Stems(endless, long_x0 - 8 * long_dx, long_dx, 1.5, 0.55, color=MUTED, radius=0.04)
        frame_box = Rectangle(width=8 * long_dx + 0.2, height=1.5, stroke_width=2, color=ACCENT)
        frame_box.move_to(np.array([long_x0 + 3.5 * long_dx, 1.5, 0.0]))
        # Only the stems inside the frame are kept; the rest is what the rectangle of ones zeroed.
        for n, stem in enumerate(wave):
            if 8 <= n < 16:
                stem.set_color(COOL)
        self.play(FadeIn(wave))
        self.play(Create(frame_box))
        note = _swap_caption(
            self,
            None,
            caption(
                "every frame is a multiplication: an endless tone × a rectangle of eight ones"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.4)
        readings = [_reading(between, k)[2] for k in range(_N // 2 + 1)]
        chart = _uprights(
            [0.5 * r for r in readings],
            [_fmt(r) for r in readings],
            [f"{k * _SR // _N}" for k in range(_N // 2 + 1)],
            left=1.2,
            base_y=-1.6,
            pitch=1.05,
        )
        chart_tag = caption("Hz").next_to(chart[3], RIGHT, buff=0.25)
        whole = caption(
            "a whole-lap tone × the rectangle: unchanged — no neighbouring line to copy onto"
        )
        whole.move_to(2.45 * DOWN)
        self.play(FadeIn(whole))
        self.wait(1.6)
        self.play(FadeOut(whole), run_time=0.3)
        self.play(FadeIn(chart), FadeIn(chart_tag))
        note = _swap_caption(
            self,
            note,
            caption(
                "the spectrum series' 1500 Hz sine: the rectangle's lines, copied onto its own"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        leak = Text("leakage — by the theorem", font_size=LABEL_SIZE, color=ACCENT).move_to(
            np.array([3.4, 0.6, 0.0])
        )
        self.play(FadeIn(leak))
        note = _swap_caption(
            self,
            note,
            caption(
                "a window with quieter lines copies less: the windowing series' whole subject"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        self.play(FadeOut(VGroup(wave, frame_box, chart, chart_tag, leak, note)))
        _takeaway(
            self,
            "Multiply two signals and their readings convolve — so cutting a\n"
            "frame out of a sound is a multiplication too, and its readings\n"
            "smear by exactly the rectangle's own",
        )


class WhereConvolutionLives(ConceptScene):
    """A room, a learned kernel, a vocal tract: where the sliding weighted sum shows up, and
    the two roads it opens — the sliding detector, and the window behind every frame."""

    def construct(self):
        self.play(FadeIn(self.title("Where Convolution Lives"), shift=0.3 * DOWN))

        # --- reverb: the echo kernel grown long (anchor W) -----------------------------
        x0, dx = -4.6, 0.52
        taps = 16
        decay = np.array(
            [1.0]
            + [0.0] * 3
            + [0.5]
            + [0.0] * 2
            + [0.3, 0.0, 0.2, 0.15, 0.0, 0.1, 0.08, 0.05, 0.03]
        )
        room = _Stems(decay, x0, dx, 1.0, 1.1, color=MUTED, radius=0.05)
        room_axis = Line(
            np.array([x0 - 0.3, 1.0, 0.0]),
            np.array([x0 + (taps - 1) * dx + 0.3, 1.0, 0.0]),
            color=MUTED,
            stroke_width=1.5,
        )
        room_tag = caption(
            "a room's impulse response: one clap, and everything it becomes"
        ).move_to(np.array([-0.5, 2.65, 0.0]))
        self.play(FadeIn(room_axis), FadeIn(room), FadeIn(room_tag))
        note = _swap_caption(
            self,
            None,
            caption(
                "reverb is the echo kernel grown long — a hall's is two seconds of taps"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.4)
        cost = VGroup(
            Text("2 s of tail at 50 000 samples a second: 100 000 taps", font_size=SMALL_SIZE),
            Text("100 000 multiply-adds for every output sample", font_size=SMALL_SIZE),
            Text(
                "— which is why long kernels are applied by multiplying spectra",
                font_size=SMALL_SIZE,
                color=ACCENT,
            ),
        ).arrange(DOWN, buff=0.2)
        cost.move_to(0.0 * UP + 0.1 * DOWN)
        for line in cost:
            self.play(FadeIn(line, shift=0.1 * UP), run_time=0.5)
        note = _swap_caption(
            self,
            note,
            caption(
                "the fast way to those spectra is the FFT — an algorithm story, parked elsewhere"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        self.play(FadeOut(VGroup(room, room_axis, room_tag, cost, note)))

        # --- learned kernels, and the source shaped by a filter (anchors L, W) ----------
        conv = (
            VGroup(
                Text("a convolutional layer: kernels slid over the input —", font_size=LABEL_SIZE),
                Text("their weights learned, not designed", font_size=LABEL_SIZE, color=ACCENT),
            )
            .arrange(DOWN, buff=0.2)
            .move_to(1.4 * UP)
        )
        self.play(FadeIn(conv))
        note = _swap_caption(
            self,
            None,
            caption(
                "the kernel of the convolution is the set of connection weights — LeCun, 1998"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        comb_x0, comb_dx = -3.6, 0.9
        harmonics = [115 * (k + 1) for k in range(8)]
        envelope = np.array([0.55, 0.9, 1.0, 0.7, 0.35, 0.5, 0.6, 0.3])
        comb = _Stems(envelope, comb_x0, comb_dx, -1.3, 1.1, color=COOL, radius=0.05)
        comb_axis = Line(
            np.array([comb_x0 - 0.4, -1.3, 0.0]),
            np.array([comb_x0 + 7 * comb_dx + 0.4, -1.3, 0.0]),
            color=MUTED,
            stroke_width=1.5,
        )
        ticks = VGroup(
            *[
                caption(str(h)).move_to(np.array([comb_x0 + k * comb_dx, -1.65, 0.0]))
                for k, h in enumerate(harmonics)
            ]
        )
        hz = caption("Hz").next_to(ticks, RIGHT, buff=0.2)
        curve = ParametricFunction(
            lambda t: np.array(
                [
                    comb_x0 + 7 * comb_dx * t,
                    -1.3
                    + 1.1
                    * (
                        0.45
                        + 0.55 * np.exp(-((t - 0.28) ** 2) / 0.035)
                        + 0.3 * np.exp(-((t - 0.82) ** 2) / 0.03)
                    )
                    * 0.92,
                    0.0,
                ]
            ),
            t_range=[0, 1],
            color=WARM,
            stroke_width=2.5,
        )
        self.play(FadeIn(comb_axis), FadeIn(comb), FadeIn(ticks), FadeIn(hz))
        note = _swap_caption(
            self,
            note,
            caption(
                "speech: a 115 Hz buzz from the glottis is a comb of lines — 230, 345, 460 Hz …"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.2)
        self.play(Create(curve))
        note = _swap_caption(
            self,
            note,
            caption(
                "the vocal tract is a filter: its own reading, drawn over the comb, makes the vowel"
            ).move_to(3.2 * DOWN),
        )
        source_tag = caption("the source–filter model (a picture, not to scale)").move_to(
            np.array([-0.5, -2.35, 0.0])
        )
        self.play(FadeIn(source_tag))
        self.wait(1.8)
        self.play(FadeOut(VGroup(conv, comb, comb_axis, ticks, hz, curve, source_tag, note)))

        # --- the sliding detector, and the closing map --------------------------------
        slide = (
            VGroup(
                Text(
                    "slide the probe and the detector's one number becomes a signal:",
                    font_size=SMALL_SIZE,
                ),
                Text(
                    "the bank becomes a filterbank — its kernels the probes, reversed",
                    font_size=SMALL_SIZE,
                    color=ACCENT,
                ),
            )
            .arrange(DOWN, buff=0.18)
            .move_to(1.9 * UP)
        )
        self.play(FadeIn(slide))
        self.wait(1.6)
        road = VGroup(
            Text("echoes and rooms?  →  reverb, one long kernel", font_size=LABEL_SIZE, color=GOOD),
            Text(
                "smoothing and sharpening?  →  a kernel's own reading",
                font_size=LABEL_SIZE,
                color=GOOD,
            ),
            Text(
                "kernels a network chooses?  →  convolutional layers",
                font_size=LABEL_SIZE,
                color=GOOD,
            ),
            Text("a tone between rows?  →  windowing", font_size=LABEL_SIZE, color=MUTED),
            Text(
                "tones that change over time?  →  the short-time transform",
                font_size=LABEL_SIZE,
                color=MUTED,
            ),
            Text("the ear's own grouping?  →  mel", font_size=LABEL_SIZE, color=MUTED),
        ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        road.move_to(0.45 * DOWN)
        self.play(LaggedStart(*[FadeIn(line, shift=0.15 * UP) for line in road], lag_ratio=0.25))
        note = _swap_caption(
            self,
            None,
            caption(
                "built here — next on the road: the window behind every frame, then the spectrogram"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.2)
        self.play(FadeOut(VGroup(slide, road, note)))
        _takeaway(
            self,
            "A sliding weighted sum is a room, a learned layer and a vocal\n"
            "tract — and, read on the bank, the multiplication it hides",
        )


if __name__ == "__main__":
    raise SystemExit(render_cli())
