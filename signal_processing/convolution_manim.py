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


class _Window(VGroup):
    """The kernel's weights as tokens under ``taps`` adjacent stems, with a Σ node."""

    def __init__(self, kernel, stems: _Stems, at: int, centred: bool, y: float):
        super().__init__()
        taps = len(kernel)
        first = at - (taps // 2 if centred else taps - 1)
        self.tokens = VGroup()
        for m, weight in enumerate(kernel):
            n = first + m
            token = VGroup(
                RoundedRectangle(width=0.5, height=0.36, corner_radius=0.08, stroke_width=1.5)
                .set_stroke(MUTED)
                .set_fill(MUTED, opacity=0.18),
                Text(_fmt(weight) if weight != 1 / 3 else "⅓", font_size=18, color=MUTED),
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


if __name__ == "__main__":
    raise SystemExit(render_cli())
