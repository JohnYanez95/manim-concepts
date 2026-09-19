"""The spectrum — eight samples, a bank of detectors, and what each one hears.

Seven scenes on the discrete Fourier transform read as a bank of detectors:
sound sampled into numbers, one detector built from a sine-and-cosine probe
pair, five of them listening to the same eight samples, why they never
double-count, what sets the spacing between them, the readings in decibels,
and the fold at half the sample rate where the bank has to stop.

    PressureIntoNumbers      a tone is a point going round; sampling keeps 8 heights
    TheProbe                 multiply and sum: one detector is a sine-and-cosine pair
    TheBankOfDetectors       five detectors on the same 8 samples — the spectrum
    NoDoubleCounting         why a mix splits cleanly: 28 zeros in the probe table
    WhatSetsTheSpacing       spacing is sr/N — listening longer, not sampling faster
    TheSpectrumInDecibels    a tone 100× quieter is invisible until the axis is a log
    TheFoldAtNyquist         probe 7 is probe 1: why the bank stops at half the rate

All arithmetic runs on N = 8 samples at sr = 8000 Hz. Every number on screen
is exact and machine-verified in plan 019 (anchors A–Z).

Render:
    uv run python signal_processing/spectrum_manim.py
    uv run python signal_processing/spectrum_manim.py --scene PressureIntoNumbers --quality draft
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
    """Anchor E: probe k at the 8 stops — ``"s"`` the height, ``"c"`` the shadow."""
    angles = 2 * np.pi * k * np.arange(_N) / _N
    return np.sin(angles) if kind == "s" else np.cos(angles)


# Anchor R: Lyons' Example 1 — a 1 kHz sine plus a half-size 2 kHz tone started at 135°.
_MIX = _probe(1, "s") + 0.5 * np.sin(2 * np.pi * 2 * np.arange(_N) / _N + 3 * np.pi / 4)


def _reading(samples, k: int) -> tuple[float, float, float]:
    """Anchor A: detector k's pair (cosine sum, sine sum) and its distance — plus-signed,
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

    The end rows carry one probe: at 0 and 4 laps the sine probe is all zeros (anchor C),
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


class PressureIntoNumbers(ConceptScene):
    """A pure tone is a point going round a circle; sampling keeps its height at 8 stops —
    8 numbers, 1 ms of sound at 8000 samples a second."""

    def construct(self):
        self.play(FadeIn(self.title("Pressure into Numbers"), shift=0.3 * DOWN))
        prompt = Text("Sound is air pressure, changing over time", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 1: a tone is a rotation, read by its height --------------------------
        centre = np.array([-4.75, 0.3, 0.0])
        radius = 1.25
        x0, dx = -2.4, 1.0
        circle = Circle(radius=radius, color=MUTED, stroke_width=2).move_to(centre)
        baseline = Line(
            np.array([x0 - 0.3, centre[1], 0.0]),
            np.array([x0 + _N * dx + 0.25, centre[1], 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        time_tag = caption("time").next_to(baseline, RIGHT, buff=0.12)
        self.play(Create(circle), Create(baseline), FadeIn(time_tag))

        lap = ValueTracker(0.0)

        def on_circle() -> np.ndarray:
            angle = 2 * np.pi * lap.get_value()
            return centre + radius * np.array([np.cos(angle), np.sin(angle), 0.0])

        def on_trace() -> np.ndarray:
            t = lap.get_value()
            return np.array([x0 + _N * dx * t, centre[1] + radius * np.sin(2 * np.pi * t), 0.0])

        point = always_redraw(lambda: Dot(on_circle(), radius=0.09, color=ACCENT))
        pen = always_redraw(lambda: Dot(on_trace(), radius=0.06, color=ACCENT))
        level = always_redraw(
            lambda: DashedLine(on_circle(), on_trace(), color=MUTED, stroke_width=2)
        )
        trace = always_redraw(
            lambda: ParametricFunction(
                lambda t: np.array(
                    [x0 + _N * dx * t, centre[1] + radius * np.sin(2 * np.pi * t), 0.0]
                ),
                t_range=[0, max(lap.get_value(), 1e-3)],
                color=ACCENT,
                stroke_width=3,
            )
        )
        # always_redraw rebuilds its family every frame, so these are added, not faded in.
        self.add(level, trace, pen, point)
        note = _swap_caption(
            self,
            None,
            caption("a pure tone: a point going round steadily — the mic reads its height").move_to(
                3.2 * DOWN
            ),
        )
        self.play(lap.animate.set_value(1.0), run_time=4, rate_func=linear)
        wave = ParametricFunction(
            lambda t: np.array([x0 + _N * dx * t, centre[1] + radius * np.sin(2 * np.pi * t), 0.0]),
            t_range=[0, 1],
            color=ACCENT,
            stroke_width=3,
        )
        self.remove(trace, pen, level)
        self.add(wave)
        ticks = VGroup(
            caption("0 ms").move_to(np.array([x0, -1.4, 0.0])),
            caption("1 ms").move_to(np.array([x0 + _N * dx, -1.4, 0.0])),
        )
        self.play(FadeIn(ticks))
        note = _swap_caption(
            self,
            note,
            caption("one lap per millisecond — 1000 laps a second: a 1000 Hz tone").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.4)

        # --- sampling: the 8 stops on the circle are the 8 samples ---------------------
        note = _swap_caption(
            self,
            note,
            caption(
                "sample rate sr = 8000 per second: 8 samples in this 1 ms, one every 45°"
            ).move_to(3.2 * DOWN),
        )
        self.play(wave.animate.set_stroke(color=MUTED, opacity=0.45), run_time=0.5)
        self.remove(point)
        walker = Dot(centre + radius * RIGHT, radius=0.09, color=ACCENT)
        self.add(walker)
        heights = _probe(1, "s")
        stems = _Stems(heights, x0, dx, centre[1], radius)
        stops = VGroup()
        for n in range(_N):
            if n:
                self.play(Rotate(walker, angle=PI / 4, about_point=centre), run_time=0.35)
            stop = Dot(walker.get_center(), radius=0.05, color=COOL)
            stops.add(stop)
            self.play(FadeIn(stop), FadeIn(stems[n], shift=0.1 * UP), run_time=0.3)
        self.wait(0.8)

        note = _swap_caption(
            self,
            note,
            caption(
                "nothing between the samples is stored — the computer keeps these 8 numbers"
            ).move_to(3.2 * DOWN),
        )
        height_tag = Text("height", font_size=SMALL_SIZE, color=COOL)
        height_tag.move_to(np.array([-3.05, -1.95, 0.0]), aligned_edge=RIGHT)
        height_strip = _number_strip(heights, stems, -1.95, color=COOL)
        self.play(FadeOut(wave), FadeOut(prompt))
        self.play(
            FadeIn(height_tag),
            LaggedStart(
                *[FadeIn(number, shift=0.1 * DOWN) for number in height_strip], lag_ratio=0.1
            ),
        )
        self.wait(1.4)

        # --- the shadow: the same point, read sideways ---------------------------------
        track_y = -1.35
        track = Line(
            np.array([centre[0] - radius, track_y, 0.0]),
            np.array([centre[0] + radius, track_y, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        shadow = Dot(np.array([walker.get_x(), track_y, 0.0]), radius=0.07, color=ACCENT)
        shadow.add_updater(lambda m: m.move_to(np.array([walker.get_x(), track_y, 0.0])))
        plumb = always_redraw(
            lambda: DashedLine(
                walker.get_center(), shadow.get_center(), color=MUTED, stroke_width=2
            )
        )
        self.play(Rotate(walker, angle=PI / 4, about_point=centre), run_time=0.35)
        self.play(Create(track), FadeIn(shadow))
        self.add(plumb)
        note = _swap_caption(
            self,
            note,
            caption(
                "the shadow: the same motion a quarter-turn ahead — two readings of one point"
            ).move_to(3.2 * DOWN),
        )
        self.play(Rotate(walker, angle=TAU, about_point=centre), run_time=3, rate_func=linear)
        shadows = _probe(1, "c")
        shadow_tag = Text("shadow", font_size=SMALL_SIZE)
        shadow_tag.move_to(np.array([-3.05, -2.5, 0.0]), aligned_edge=RIGHT)
        shadow_strip = _number_strip(shadows, stems, -2.5)
        self.play(
            FadeIn(shadow_tag),
            LaggedStart(
                *[FadeIn(number, shift=0.1 * DOWN) for number in shadow_strip], lag_ratio=0.1
            ),
        )
        self.wait(1.4)

        # Planted for the last scene: how many samples a lap needs.
        note = _swap_caption(
            self,
            note,
            caption(
                "8 samples per lap here; a faster tone gets fewer — and needs at least two"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)

        # --- the question the series answers --------------------------------------------
        shadow.clear_updaters()
        self.play(
            FadeOut(
                VGroup(
                    circle,
                    stops,
                    walker,
                    track,
                    shadow,
                    plumb,
                    shadow_tag,
                    shadow_strip,
                    height_tag,
                    height_strip,
                    stems,
                    note,
                )
            )
        )
        mix = _Stems(_MIX, x0, dx, centre[1], radius)
        mix_strip = _number_strip(_MIX, mix, -1.95, color=COOL, size=18)
        self.play(
            LaggedStart(*[FadeIn(stem, shift=0.1 * UP) for stem in mix], lag_ratio=0.08),
            FadeIn(mix_strip),
        )
        question = caption(
            "real sound is a mix — still just 8 numbers. Which tones are hiding in them?"
        ).move_to(3.2 * DOWN)
        self.play(FadeIn(question))
        self.wait(1.8)

        self.play(FadeOut(VGroup(mix, mix_strip, question, baseline, time_tag, ticks)))
        _takeaway(
            self,
            "Sampling keeps sr numbers a second and nothing between —\n"
            "the question is which tones are hiding in them",
        )


class TheProbe(ConceptScene):
    """One detector: multiply the samples by a known tone and add. A match sums to 4, a
    different tone cancels to 0 — and it takes a sine-and-cosine pair not to be fooled by
    when the tone starts."""

    def construct(self):
        self.play(FadeIn(self.title("The Probe"), shift=0.3 * DOWN))
        prompt = Text("Is a 2000 Hz tone hiding in these 8 numbers?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))
        self.wait(1.0)
        self.play(FadeOut(prompt))

        x0, dx, scale = -6.1, 0.78, 0.38
        rows_y = (1.5, 0.2, -1.1)
        tags_x = 0.0

        def row(values, y, color, scale=scale, size=18):
            stems = _Stems(values, x0, dx, y, scale, color=color, radius=0.055)
            axis = Line(
                np.array([x0 - 0.25, y, 0.0]),
                np.array([x0 + 7 * dx + 0.25, y, 0.0]),
                color=MUTED,
                stroke_width=1.5,
            )
            numbers = _number_strip(values, stems, y - 0.62, color=color, size=size)
            return VGroup(axis, stems, numbers)

        def tag(label, y, color):
            text = Text(label, font_size=SMALL_SIZE, color=color)
            return text.move_to(np.array([tags_x, y, 0.0]), aligned_edge=LEFT)

        # --- level 1: a probe is a known tone; multiply, then add -----------------------
        tone = row(_probe(2, "s"), rows_y[0], COOL)
        tone_tag = tag("the samples", rows_y[0], COOL)
        probe = row(_probe(2, "s"), rows_y[1], MUTED)
        probe_tag = tag("probe: 2 laps", rows_y[1], MUTED)
        self.play(FadeIn(tone), FadeIn(tone_tag))
        self.play(FadeIn(probe), FadeIn(probe_tag))
        note = _swap_caption(
            self,
            None,
            caption("a probe is a known tone — k laps in the window; this one does 2").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.2)

        products = row(_probe(2, "s") * _probe(2, "s"), rows_y[2], GOOD)
        products_tag = tag("products", rows_y[2], MUTED)
        self.play(
            LaggedStart(*[FadeIn(stem, shift=0.1 * DOWN) for stem in products[1]], lag_ratio=0.1),
            FadeIn(products[0]),
            FadeIn(products[2]),
            FadeIn(products_tag),
        )
        note = _swap_caption(
            self,
            note,
            caption("multiply stop by stop, then add — the weighted sum expectation built").move_to(
                3.2 * DOWN
            ),
        )
        total = Text("sum = 4", font_size=BODY_SIZE, color=ACCENT).move_to(
            np.array([4.2, rows_y[2], 0.0])
        )
        self.play(FadeIn(total, shift=0.2 * LEFT))
        self.wait(1.0)
        note = _swap_caption(
            self,
            note,
            caption(
                "but these weights can be negative and add to 0: a pattern, not a probability"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.4)
        match = Text(
            "a match: every product\nis a square —\nnothing can cancel", font_size=LABEL_SIZE
        )
        match.set_color(GOOD).move_to(np.array([4.4, 0.9, 0.0]))
        self.play(FadeIn(match))
        self.wait(1.6)

        # --- a different tone cancels exactly -------------------------------------------
        self.play(
            FadeOut(VGroup(tone, probe, products, total, match, probe_tag, note)), run_time=0.6
        )
        tone = row(_probe(1, "s"), rows_y[0], COOL)
        probe = row(_probe(3, "s"), rows_y[1], MUTED)
        probe_tag = tag("probe: 3 laps", rows_y[1], MUTED)
        products = row(_probe(1, "s") * _probe(3, "s"), rows_y[2], WARM)
        self.play(FadeIn(tone), FadeIn(probe), FadeIn(probe_tag))
        note = _swap_caption(
            self,
            None,
            caption("a 1-lap tone against a 3-lap probe: the products take both signs").move_to(
                3.2 * DOWN
            ),
        )
        self.play(FadeIn(products))
        tally = VGroup(
            Text("up: 0.5 + 0.5 + 0.5 + 0.5 = 2", font_size=SMALL_SIZE),
            Text("down: 1 + 1 = 2", font_size=SMALL_SIZE),
            Text("sum = 0", font_size=BODY_SIZE, color=ACCENT),
        )
        tally.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([4.6, 0.2, 0.0]))
        for line in tally:
            self.play(FadeIn(line, shift=0.15 * LEFT), run_time=0.5)
        note = _swap_caption(
            self,
            note,
            caption("four halves up, two wholes down — this detector hears nothing", WARM).move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.8)

        # --- the sine probe alone is fooled by when the tone starts ---------------------
        self.play(
            FadeOut(VGroup(tone, probe, products, tally, probe_tag, products_tag, note)),
            run_time=0.6,
        )
        # Anchor Q: 3·c₂ + 4·s₂ — a 2000 Hz tone of amplitude exactly 5, at four starts.
        starts = [np.roll(3 * _probe(2, "c") + 4 * _probe(2, "s"), shift) for shift in range(4)]
        tone = row(starts[0], rows_y[0], COOL, scale=0.095)
        sine_read = Text("sine probe reads 16", font_size=LABEL_SIZE)
        sine_read.move_to(np.array([-3.4, 0.1, 0.0]))
        self.play(FadeIn(tone))
        note = _swap_caption(
            self,
            None,
            caption("a louder 2000 Hz tone — 3, 4, −3, −4 — on the 2-lap sine probe").move_to(
                3.2 * DOWN
            ),
        )
        self.play(FadeIn(sine_read))
        self.wait(1.0)
        self.play(FadeOut(tone), FadeOut(sine_read), run_time=0.4)
        tone = row(starts[1], rows_y[0], COOL, scale=0.095)
        sine_read = Text("sine probe reads 12", font_size=LABEL_SIZE, color=WARM)
        sine_read.move_to(np.array([-3.4, 0.1, 0.0]))
        self.play(FadeIn(tone), FadeIn(sine_read))
        note = _swap_caption(
            self,
            note,
            caption("the same tone, started one sample later: 16 became 12 — fooled").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.6)

        # --- level 2: the pair — height and shadow — is not fooled ----------------------
        origin = np.array([4.0, -0.1, 0.0])
        unit = 1.6 / 20
        plane = VGroup(
            Line(origin + 1.95 * LEFT, origin + 1.95 * RIGHT, color=MUTED, stroke_width=2),
            Line(origin + 1.95 * DOWN, origin + 1.95 * UP, color=MUTED, stroke_width=2),
            Circle(radius=1.6, color=MUTED, stroke_width=1.5).move_to(origin),
        )
        axis_tags = caption("across: cosine sum · up: sine sum")
        axis_tags.move_to(np.array([origin[0], -2.3, 0.0]))
        self.play(FadeOut(tone), FadeOut(sine_read), run_time=0.4)
        self.play(Create(plane), FadeIn(axis_tags))
        note = _swap_caption(
            self,
            note,
            caption("add the shadow probe and plot the pair: (cosine sum, sine sum)").move_to(
                3.2 * DOWN
            ),
        )

        tone = pair_read = spoke = label = None
        ghosts = VGroup()
        for shift, samples in enumerate(starts):
            a, b, distance = _reading(samples, 2)
            if tone is not None:
                self.play(FadeOut(tone), FadeOut(pair_read), FadeOut(label), run_time=0.4)
                ghosts.add(Dot(spoke.get_end(), radius=0.06, color=MUTED))
                self.add(ghosts[-1])
                self.remove(spoke)
            tone = row(samples, rows_y[0], COOL, scale=0.095)
            pair_read = VGroup(
                Text(f"cosine probe reads {_fmt(a)}", font_size=LABEL_SIZE),
                Text(f"sine probe reads {_fmt(b)}", font_size=LABEL_SIZE),
                Text(f"distance = {_fmt(distance)}", font_size=BODY_SIZE, color=ACCENT),
            )
            pair_read.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            pair_read.move_to(np.array([-3.4, -0.7, 0.0]))
            tip = origin + unit * np.array([a, b, 0.0])
            spoke = VGroup(
                Line(origin, tip, color=ACCENT, stroke_width=3),
                Dot(tip, radius=0.08, color=ACCENT),
            )
            spoke.get_end = lambda tip=tip: tip
            label = Text(f"({_fmt(a)}, {_fmt(b)})", font_size=SMALL_SIZE, color=ACCENT)
            label.next_to(spoke[1], np.array([np.sign(a), np.sign(b), 0.0]), buff=0.1)
            self.play(FadeIn(tone), FadeIn(pair_read), FadeIn(spoke), FadeIn(label))
            if shift == 1:
                note = _swap_caption(
                    self,
                    note,
                    caption(
                        "one sample later is a quarter-turn of the pair — the distance stays 20"
                    ).move_to(3.2 * DOWN),
                )
            self.wait(1.0 if shift else 1.6)

        note = _swap_caption(
            self,
            note,
            caption(
                "true for every starting angle — shown here for four. 20 ÷ 4 = amplitude 5"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.2)
        peak = caption("a peak the samples never touch: the largest sample is 4", GOOD)
        peak.move_to(2.7 * DOWN)
        self.play(FadeIn(peak))
        self.wait(1.8)

        self.play(
            FadeOut(
                VGroup(
                    tone, pair_read, spoke, label, ghosts, plane, axis_tags, note, peak, tone_tag
                )
            )
        )
        _takeaway(
            self,
            "One detector is a pair of probes, height and shadow:\n"
            "multiply, add, take the distance — it ignores when the tone starts",
        )


class TheBankOfDetectors(ConceptScene):
    """Five detectors listen to the same 8 samples, each at its own fixed frequency; a pure
    tone lights one row, a mix lights its parts — and the column of readings is the spectrum."""

    def construct(self):
        self.play(FadeIn(self.title("The Bank of Detectors"), shift=0.3 * DOWN))

        x0, dx, y0, scale = -6.6, 0.36, 0.1, 0.55
        feed = np.array([x0 + 7 * dx + 0.25, y0, 0.0])
        bank = _Bank(feed)
        self.play(FadeIn(bank.labels), FadeIn(bank.thumbs), FadeIn(bank.wires), FadeIn(bank.nodes))
        note = _swap_caption(
            self,
            None,
            caption(
                "one detector for each whole number of laps: addresses fixed before any sound"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)

        def frame(samples):
            stems = _Stems(samples, x0, dx, y0, scale, radius=0.05)
            axis = Line(np.array([x0 - 0.2, y0, 0.0]), feed, color=MUTED, stroke_width=1.5)
            return VGroup(axis, stems)

        samples_tag = caption("the 8 samples", COOL).move_to(np.array([-5.35, -1.15, 0.0]))

        # --- level 1: a pure tone lights exactly one row --------------------------------
        feeds = [
            (_probe(2, "s"), "a 2000 Hz tone: exactly one row answers — and it reads 4"),
            (_probe(3, "c"), "a 3000 Hz tone, started elsewhere: row 3 alone — again 4"),
        ]
        signal = bars = numbers = None
        for samples, line in feeds:
            if signal is not None:
                self.play(FadeOut(signal), FadeOut(bars), FadeOut(numbers), run_time=0.5)
            signal = frame(samples)
            bars, numbers = bank.readout(samples)
            self.play(FadeIn(signal), FadeIn(samples_tag) if signal is not None else Wait(0.1))
            if bank.fan not in self.mobjects:
                self.play(Create(bank.fan), run_time=0.6)
            self.play(
                LaggedStart(
                    *[
                        ShowPassingFlash(wire.copy().set_color(COOL), time_width=0.6)
                        for wire in bank.fan
                    ],
                    lag_ratio=0.05,
                ),
                run_time=0.8,
            )
            self.play(
                *[GrowFromEdge(bar, LEFT) for bar in bars],
                FadeIn(numbers),
            )
            note = _swap_caption(self, note, caption(line).move_to(3.2 * DOWN))
            self.wait(1.4)

        # --- the mix splits into its parts ----------------------------------------------
        self.play(FadeOut(signal), FadeOut(bars), FadeOut(numbers), run_time=0.5)
        signal = frame(_MIX)
        bars, numbers = bank.readout(_MIX)
        self.play(FadeIn(signal))
        self.play(
            LaggedStart(
                *[
                    ShowPassingFlash(wire.copy().set_color(COOL), time_width=0.6)
                    for wire in bank.fan
                ],
                lag_ratio=0.05,
            ),
            run_time=0.8,
        )
        self.play(*[GrowFromEdge(bar, LEFT) for bar in bars], FadeIn(numbers))
        note = _swap_caption(
            self,
            note,
            caption("the mix from the first scene: two rows answer — 4 and 2").move_to(3.2 * DOWN),
        )
        self.wait(1.2)
        a, b, _ = _reading(_MIX, 2)
        pair = Text(f"its pair: ({_fmt(a)}, {_fmt(b)})", font_size=SMALL_SIZE, color=ACCENT)
        pair.next_to(numbers[2], RIGHT, buff=0.35)
        self.play(FadeIn(pair, shift=0.15 * LEFT))
        note = _swap_caption(
            self,
            note,
            caption(
                "each bar is its pair's distance — the last scene's lesson, inside the bank"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.4)
        note = _swap_caption(
            self,
            note,
            caption(
                "reading ÷ 4 = amplitude: a 1000 Hz tone of size 1 plus a 2000 Hz tone of size 0.5"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        # --- the bar column, turned on its side, is the spectrum ------------------------
        self.play(
            FadeOut(VGroup(pair, bank.thumbs, bank.wires, bank.nodes, bank.fan, bank.labels)),
            FadeOut(numbers),
        )
        base_y, left, pitch = -1.7, 0.5, 1.2
        floor = Line(
            np.array([left - 0.5, base_y, 0.0]),
            np.array([left + 4 * pitch + 0.5, base_y, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        uprights, ticks, tops = VGroup(), VGroup(), VGroup()
        for k in range(_N // 2 + 1):
            distance = _reading(_MIX, k)[2]
            upright = Rectangle(
                width=0.4, height=max(_Bank.BAR_UNIT * distance, 0.02), stroke_width=0
            )
            upright.set_fill(ACCENT if distance > 1e-9 else MUTED, opacity=0.9)
            upright.move_to(np.array([left + k * pitch, base_y, 0.0]), aligned_edge=DOWN)
            uprights.add(upright)
            ticks.add(caption(f"{k * _SR // _N}").next_to(upright, DOWN, buff=0.15))
            top = Text(_fmt(distance), font_size=SMALL_SIZE)
            top.set_color(ACCENT if distance > 1e-9 else MUTED)
            tops.add(top.next_to(upright, UP, buff=0.12))
        unit_tag = caption("Hz").next_to(ticks, RIGHT, buff=0.3)
        self.play(
            Create(floor),
            *[
                ReplacementTransform(bar, upright)
                for bar, upright in zip(bars, uprights, strict=True)
            ],
            run_time=1.4,
        )
        self.play(FadeIn(ticks), FadeIn(unit_tag), FadeIn(tops))
        note = _swap_caption(
            self,
            note,
            caption(
                "the bars on their side: the spectrum — a column of weighted sums, nothing new"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(signal, samples_tag, floor, uprights, ticks, unit_tag, tops, note))
        )
        _takeaway(
            self,
            "The spectrum is a bank of detectors on the same samples —\n"
            "each row a fixed address, each bar a weighted sum",
        )


class NoDoubleCounting(ConceptScene):
    """Why the mix split cleanly: a detector's reading of a sum is the sum of its readings,
    and every probe reads exactly 0 on every other probe — all 28 pairs, checked."""

    def construct(self):
        self.play(FadeIn(self.title("No Double Counting"), shift=0.3 * DOWN))
        prompt = Text("Why did the mix split cleanly into 4 and 2?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 2, first half: the weighted sum is linear ----------------------------
        split = VGroup(
            Text("reading of (tone A + tone B)", font_size=LABEL_SIZE),
            Text("= reading of A + reading of B", font_size=LABEL_SIZE, color=ACCENT),
        ).arrange(DOWN, buff=0.3)
        split.move_to(0.6 * UP)
        self.play(FadeIn(split[0]))
        self.play(FadeIn(split[1], shift=0.15 * UP))
        note = _swap_caption(
            self,
            None,
            caption(
                "a weighted sum of a sum is the sum of the weighted sums — owned since dice"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        follow = caption("so it is enough to ask: what does each probe read on every other probe?")
        follow.move_to(0.7 * DOWN)
        self.play(FadeIn(follow))
        self.wait(1.6)
        self.play(FadeOut(VGroup(split, follow, prompt, note)))

        # --- level 2, second half: the probe-against-probe table (anchor U) -------------
        probes = [("c", 0), ("c", 1), ("s", 1), ("c", 2), ("s", 2), ("c", 3), ("s", 3), ("c", 4)]
        names = ["c₀", "c₁", "s₁", "c₂", "s₂", "c₃", "s₃", "c₄"]
        cell, left, top = 0.55, -5.2, 2.15
        heads = VGroup(
            *[
                Text(name, font_size=LABEL_SIZE, color=MUTED).move_to(
                    np.array([left + (j + 1) * cell, top, 0.0])
                )
                for j, name in enumerate(names)
            ],
            *[
                Text(name, font_size=LABEL_SIZE, color=MUTED).move_to(
                    np.array([left, top - (i + 1) * cell, 0.0])
                )
                for i, name in enumerate(names)
            ],
        )
        cells = {}
        for i, (kind_i, k_i) in enumerate(probes):
            for j, (kind_j, k_j) in enumerate(probes):
                value = float(np.dot(_probe(k_i, kind_i), _probe(k_j, kind_j)))
                entry = Text(_fmt(value), font_size=SMALL_SIZE)
                entry.set_color(ACCENT if i == j else MUTED)
                entry.move_to(np.array([left + (j + 1) * cell, top - (i + 1) * cell, 0.0]))
                cells[i, j] = entry
        diagonal = VGroup(*[cells[i, i] for i in range(8)])
        upper = VGroup(*[cells[i, j] for i in range(8) for j in range(8) if i < j])
        lower = VGroup(*[cells[i, j] for i in range(8) for j in range(8) if i > j])
        key = Text(
            "c = cosine probe · s = sine probe\nthe number: laps per window",
            font_size=SMALL_SIZE,
            color=MUTED,
            line_spacing=1.0,
        )
        key.move_to(np.array([3.5, -2.35, 0.0]))
        self.play(FadeIn(heads), FadeIn(key))
        note = _swap_caption(
            self,
            None,
            caption("multiply and add every probe against every probe — 8 probes, 64 sums").move_to(
                3.2 * DOWN
            ),
        )
        self.play(LaggedStart(*[FadeIn(entry) for entry in diagonal], lag_ratio=0.12))
        self.play(LaggedStart(*[FadeIn(entry) for entry in upper], lag_ratio=0.02), run_time=1.6)
        self.play(FadeIn(lower), run_time=0.6)
        count = VGroup(
            Text("C(8, 2) = 28 different pairs", font_size=LABEL_SIZE),
            Text("all 28 read exactly 0", font_size=LABEL_SIZE, color=GOOD),
            Text("computed, not proved", font_size=SMALL_SIZE, color=MUTED),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        count.move_to(np.array([3.6, 1.2, 0.0]))
        for line in count:
            self.play(FadeIn(line, shift=0.15 * LEFT), run_time=0.5)
        note = _swap_caption(
            self,
            note,
            caption(
                "each detector is exactly deaf to the other detectors' tones — so no bar borrows"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)

        # --- why 4 on the diagonal: the raised floor (anchor V) -------------------------
        self.play(FadeOut(count), run_time=0.5)
        squares = VGroup(
            Text("s₁ × s₁:  0   0.5   1   0.5   0   0.5   1   0.5", font_size=SMALL_SIZE),
            Text("c₁ × c₁:  1   0.5   0   0.5   1   0.5   0   0.5", font_size=SMALL_SIZE),
            Text(
                "each stop:  1    1    1    1    1    1    1    1", font_size=SMALL_SIZE, color=COOL
            ),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        squares.move_to(np.array([3.4, 1.2, 0.0]))
        self.play(FadeIn(squares[0]), FadeIn(squares[1]))
        note = _swap_caption(
            self,
            note,
            caption(
                "why 4: squares never cancel — and height² + shadow² = 1 at every stop"
            ).move_to(3.2 * DOWN),
        )
        self.play(FadeIn(squares[2], shift=0.1 * UP))
        share = Text(
            "8 stops share out 8 —\nsame values, different order:\n4 each",
            font_size=LABEL_SIZE,
            line_spacing=1.1,
            color=ACCENT,
        )
        share.move_to(np.array([3.4, -0.7, 0.0]))
        self.play(FadeIn(share))
        self.wait(2.0)

        # --- the end rows keep the whole 8 (anchor C, correction 1) ---------------------
        self.play(FadeOut(squares), FadeOut(share), run_time=0.5)
        ends = VGroup(
            SurroundingRectangle(cells[0, 0], color=ACCENT, buff=0.08, stroke_width=2),
            SurroundingRectangle(cells[7, 7], color=ACCENT, buff=0.08, stroke_width=2),
        )
        lonely = Text(
            "at 0 and 4 laps the sine probe\nis all zeros — no partner:\n"
            "the cosine keeps the whole 8",
            font_size=LABEL_SIZE,
            line_spacing=1.1,
        )
        lonely.move_to(np.array([3.5, 0.9, 0.0]))
        self.play(Create(ends), FadeIn(lonely))
        note = _swap_caption(
            self,
            note,
            caption(
                "so the end rows read ÷ 8, not ÷ 4 — and they do care when the tone starts"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)
        ledger = Text(
            "1 + 2·3 + 1 = 8 readings\nfrom 8 samples — nothing lost",
            font_size=LABEL_SIZE,
            line_spacing=1.1,
            color=GOOD,
        )
        ledger.move_to(np.array([3.5, -1.2, 0.0]))
        self.play(FadeIn(ledger))
        note = _swap_caption(
            self,
            note,
            caption(
                "that the 8 readings rebuild the 8 samples is a promise, not shown here"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)

        self.play(FadeOut(VGroup(heads, key, diagonal, upper, lower, ends, lonely, ledger, note)))
        _takeaway(
            self,
            "Every probe reads 0 on every other probe —\n"
            "so the bank splits a mix without counting anything twice",
        )


class WhatSetsTheSpacing(ConceptScene):
    """Detector k listens at k × sr ÷ N: the spacing is one over how long you listen, so a
    faster sample rate buys reach and only a longer window buys finer spacing."""

    def construct(self):
        self.play(FadeIn(self.title("What Sets the Spacing"), shift=0.3 * DOWN))
        prompt = Text("What decides where the detectors listen?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 2: k laps in a window of N ÷ sr seconds ------------------------------
        steps = VGroup(
            Text("probe k fits k laps into the window", font_size=LABEL_SIZE),
            Text("the window lasts N ÷ sr = 8 ÷ 8000 s = 1 ms", font_size=LABEL_SIZE),
            Text("k laps per millisecond = k × 1000 Hz", font_size=LABEL_SIZE),
        ).arrange(DOWN, buff=0.32)
        steps.move_to(0.9 * UP)
        for step in steps:
            self.play(FadeIn(step, shift=0.15 * UP), run_time=0.6)
            self.wait(0.5)
        rule = MathTex(
            r"f_k = k \cdot \frac{sr}{N}",
            r"\qquad \text{spacing} = \frac{sr}{N} = \frac{1}{\text{duration}}",
        ).scale(0.85)
        rule.move_to(1.1 * DOWN)
        self.play(Write(rule))
        frame = boxed(rule, buff=0.25)
        self.play(Create(frame))
        note = _swap_caption(
            self,
            None,
            caption(
                "the spacing between detectors is one over how long the window listens"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        self.play(FadeOut(VGroup(prompt, steps, rule, frame, note)))

        # --- three banks side by side (anchor X), then Whisper's (anchor L) -------------
        per_khz, floor_y = 0.42, -2.2
        scale_marks = VGroup()
        for khz in (0, 4, 8):
            mark = caption(f"{khz * 1000} Hz")
            mark.move_to(np.array([-6.3, floor_y + khz * per_khz, 0.0]))
            scale_marks.add(mark)

        def ladder(x, rate, count, head_lines):
            rungs = VGroup(
                *[
                    Line(
                        np.array([x - 0.45, floor_y + per_khz * k * rate / count / 1000, 0.0]),
                        np.array([x + 0.45, floor_y + per_khz * k * rate / count / 1000, 0.0]),
                        color=ACCENT,
                        stroke_width=3,
                    )
                    for k in range(count // 2 + 1)
                ]
            )
            head = Text(head_lines, font_size=SMALL_SIZE, line_spacing=1.0)
            head.move_to(np.array([x, 2.05, 0.0]))
            return VGroup(rungs, head)

        first = ladder(-4.2, 8000, 8, "sr 8000 · N 8\n1 ms · 5 rows")
        second = ladder(-1.6, 16000, 16, "sr 16 000 · N 16\n1 ms · 9 rows")
        third = ladder(1.0, 8000, 16, "sr 8000 · N 16\n2 ms · 9 rows")
        self.play(FadeIn(scale_marks), FadeIn(first))
        note = _swap_caption(
            self,
            None,
            caption(
                "the bank so far: 8 samples at 8000 a second — rows 1000 Hz apart, up to 4000"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.2)
        self.play(FadeIn(second))
        note = _swap_caption(
            self,
            note,
            caption(
                "sample twice as fast for the same 1 ms: still 1000 Hz apart — it bought reach"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        self.play(FadeIn(third))
        note = _swap_caption(
            self,
            note,
            caption(
                "listen twice as long instead: 500 Hz apart — only duration buys spacing"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        dense = Rectangle(width=0.9, height=8 * per_khz, stroke_width=0)
        dense.set_fill(ACCENT, opacity=0.55)
        dense.move_to(np.array([4.2, floor_y, 0.0]), aligned_edge=DOWN)
        whisper = Text(
            "Whisper\nsr 16 000 · N 400\n25 ms · 201 rows", font_size=SMALL_SIZE, line_spacing=1.0
        )
        whisper.move_to(np.array([4.2, 2.2, 0.0]))
        self.play(FadeIn(dense), FadeIn(whisper))
        note = _swap_caption(
            self,
            note,
            caption(
                "a speech model's bank: 25 ms windows — 201 rows, 40 Hz apart, up to 8000 Hz"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)

        # --- level 3: what the spacing costs — the one honest teaser (anchor T) ---------
        self.play(FadeOut(VGroup(scale_marks, first, second, third, dense, whisper, note)))
        between = np.sin(2 * np.pi * 1.5 * np.arange(_N) / _N)
        readings = [_reading(between, k)[2] for k in range(_N // 2 + 1)]
        chart = _uprights(
            [0.55 * r for r in readings],
            [_fmt(r) for r in readings],
            [f"{k * _SR // _N}" for k in range(_N // 2 + 1)],
            left=-2.4,
            base_y=-1.5,
            pitch=1.2,
        )
        chart_tag = caption("Hz").next_to(chart[3], RIGHT, buff=0.3)
        self.play(FadeIn(chart), FadeIn(chart_tag))
        note = _swap_caption(
            self,
            None,
            caption(
                "a 1500 Hz sine, starting at 0, sits between two rows — and every row answers"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        note = _swap_caption(
            self,
            note,
            caption(
                "that smear is leakage: the windowing series explains it — and tames it"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        note = _swap_caption(
            self,
            note,
            caption(
                "slide the window along and each detector's output becomes a signal: a filterbank"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        note = _swap_caption(
            self,
            note,
            caption("and a mel filterbank will regroup Whisper's 201 rows into 80").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.6)

        self.play(FadeOut(VGroup(chart, chart_tag, note)))
        _takeaway(
            self,
            "Spacing = sr ÷ N = 1 ÷ how long you listen —\n"
            "sampling faster buys reach, listening longer buys detail",
        )


class TheSpectrumInDecibels(ConceptScene):
    """A tone 100 times quieter is invisible on linear bars and sits at −40 dB on a log axis:
    decibels are 10 × log₁₀ of a power ratio, always against a stated reference."""

    def construct(self):
        self.play(FadeIn(self.title("The Spectrum in Decibels"), shift=0.3 * DOWN))
        prompt = Text("A third tone joins the mix — 100 times quieter", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # Anchor S: Lyons' mix plus 0.01 × a 3000 Hz sine — readings 0, 4, 2, 0.04, 0.
        trio = _MIX + 0.01 * _probe(3, "s")
        readings = [_reading(trio, k)[2] for k in range(_N // 2 + 1)]
        hz = [f"{k * _SR // _N}" for k in range(_N // 2 + 1)]
        linear = _uprights(
            [0.55 * r for r in readings], [_fmt(r) for r in readings], hz, -5.6, -1.4, 1.0
        )
        linear_tag = caption("readings").next_to(linear[0], UP, buff=2.7)
        self.play(FadeIn(linear), FadeIn(linear_tag))
        note = _swap_caption(
            self,
            None,
            caption("readings 4, 2 and 0.04 — on these bars the third tone is invisible").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.8)

        # --- level 2: one definition; the 20 is the log pulling a square out front ------
        define = VGroup(
            Text("decibels = 10 × log₁₀ (power ratio)", font_size=LABEL_SIZE, color=ACCENT),
            Text("power goes as amplitude²", font_size=LABEL_SIZE),
            Text("the log turns the square into × 2:", font_size=LABEL_SIZE),
            Text("20 × log₁₀ (amplitude ratio)", font_size=LABEL_SIZE, color=ACCENT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        define.move_to(np.array([3.2, 0.3, 0.0]))
        credit = caption("Bell System, 1929: ten times the common logarithm of a power ratio")
        credit.move_to(2.7 * DOWN)
        self.play(FadeIn(define[0]), FadeIn(credit))
        self.wait(1.0)
        for line in define[1:]:
            self.play(FadeIn(line, shift=0.15 * UP), run_time=0.6)
        note = _swap_caption(
            self,
            note,
            caption("the log ruler from the logarithm series: multiplying becomes adding").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(2.0)

        # --- the same three readings on the log axis ------------------------------------
        self.play(FadeOut(define), FadeOut(credit), FadeOut(prompt))
        levels = [20 * np.log10(r / max(readings)) if r > 1e-9 else None for r in readings]
        per_db, floor_db = 0.055, -50
        log_chart = _uprights(
            [per_db * (level - floor_db) if level is not None else 0.0 for level in levels],
            [("−∞" if level is None else f"{_fmt(level)} dB") for level in levels],
            hz,
            1.3,
            -1.4,
            1.3,
        )
        log_floor = caption("−50 dB").next_to(log_chart[0], LEFT, buff=0.15)
        log_tag = caption("dB re: the loudest row").next_to(log_chart[0], UP, buff=3.45)
        self.play(FadeIn(log_chart[0]), FadeIn(log_chart[3]), FadeIn(log_tag), FadeIn(log_floor))
        beats = [
            (1, "the loudest row is the reference: ratio 1, and log 1 = 0 dB"),
            (2, "half the reading: 20 × log₁₀(½) = −20 × 0.301 = −6.02 dB"),
            (3, "a hundredth: 20 × log₁₀(1/100) = −40 dB — now the third tone has a bar"),
        ]
        for k, line in beats:
            self.play(GrowFromEdge(log_chart[1][k], DOWN), FadeIn(log_chart[2][k]))
            note = _swap_caption(self, note, caption(line).move_to(3.2 * DOWN))
            self.wait(1.4)
        self.play(
            FadeIn(VGroup(log_chart[1][0], log_chart[1][4], log_chart[2][0], log_chart[2][4]))
        )
        note = _swap_caption(
            self,
            note,
            caption(
                "empty rows: log 0 = −∞. So 0 dB means equal to the reference — not silence"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        note = _swap_caption(
            self,
            note,
            caption(
                "Whisper picks a floor: 8 decades of power below its loudest value — 80 dB"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        # --- level 3: a real note (anchor M) --------------------------------------------
        self.play(FadeOut(VGroup(linear, linear_tag, log_chart, log_tag, log_floor, note)))
        harmonics = [
            (624.46, -1.56),
            (1248.93, 0.0),
            (1873.39, -3.23),
            (2497.85, -7.21),
            (3122.31, -11.98),
        ]
        note_chart = _uprights(
            [0.13 * (level + 20) for _, level in harmonics],
            [_fmt(level) for _, level in harmonics],
            [f"{round(f)}" for f, _ in harmonics],
            -2.6,
            -1.5,
            1.3,
        )
        note_tag = Text(
            "a real trumpet note — 4096 samples at 22 050 a second:\n2049 detectors, 5.4 Hz apart",
            font_size=LABEL_SIZE,
            line_spacing=1.1,
        )
        note_tag.next_to(self.head, DOWN, buff=0.3)
        units = caption("Hz · dB re: the loudest").next_to(note_chart[3], RIGHT, buff=0.3)
        note_floor = caption("−20 dB").next_to(note_chart[0], LEFT, buff=0.15)
        source = caption("trumpet: Mihai Sorohan, freesound.org/s/77711 · CC BY 4.0")
        source.move_to(2.7 * DOWN)
        self.play(
            FadeIn(note_tag), FadeIn(note_chart), FadeIn(units), FadeIn(source), FadeIn(note_floor)
        )
        note = _swap_caption(
            self,
            None,
            caption(
                "its second harmonic is the loudest — the 624 Hz fundamental sits 1.56 dB below"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)
        note = _swap_caption(
            self,
            note,
            caption(
                "a real note lands between rows: a window shaped these levels — a later series"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        # --- the same ruler, elsewhere ----------------------------------------------------
        self.play(FadeOut(VGroup(note_tag, note_chart, units, source, note_floor, note)))
        table = VGroup(
            Text("decibels = 10 × log₁₀ (power ratio)", font_size=LABEL_SIZE, color=ACCENT),
            Text("pH = −log₁₀ (hydrogen-ion activity)", font_size=LABEL_SIZE),
            Text("star magnitude = −2.5 × log₁₀ (brightness ratio)", font_size=LABEL_SIZE),
            Text("semitones = 12 × log₂ (frequency ratio)", font_size=LABEL_SIZE),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        table.move_to(0.4 * UP)
        self.play(LaggedStart(*[FadeIn(line, shift=0.15 * UP) for line in table], lag_ratio=0.3))
        note = _swap_caption(
            self,
            None,
            caption(
                "each one a constant × the log of a ratio — the same ruler with its own stride"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)
        note = _swap_caption(
            self,
            note,
            caption(
                "that the ear itself hears in logs is an approximate motivation, not a law"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.8)

        self.play(FadeOut(VGroup(table, note)))
        _takeaway(
            self,
            "Decibels put loud and quiet on one ruler: 10 × log₁₀ of a\n"
            "power ratio — always measured against a stated reference",
        )


class TheFoldAtNyquist(ConceptScene):
    """At the 8 stops probe 7 is probe 1, so a 7000 Hz tone sampled at 8000 Hz is a 1000 Hz
    tone: the bank stops at half the sample rate because nothing above it can be told apart."""

    def construct(self):
        self.play(FadeIn(self.title("The Fold at Nyquist"), shift=0.3 * DOWN))
        prompt = Text(
            "Why does the bank stop at 4000 Hz — half the sample rate?", font_size=BODY_SIZE
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- probe 7 is probe 1 (anchors H, W) ------------------------------------------
        def strip(label, values, y, color):
            name = Text(label, font_size=SMALL_SIZE, color=color)
            name.move_to(np.array([-5.4, y, 0.0]), aligned_edge=LEFT)
            numbers = VGroup(
                *[
                    Text(_fmt(v), font_size=SMALL_SIZE, color=color).move_to(
                        np.array([-2.6 + 0.95 * n, y, 0.0])
                    )
                    for n, v in enumerate(values)
                ]
            )
            return VGroup(name, numbers)

        rows = VGroup(
            strip("cosine, 1 lap", _probe(1, "c"), 1.5, COOL),
            strip("cosine, 7 laps", _probe(7, "c"), 0.95, COOL),
            strip("sine, 1 lap", _probe(1, "s"), 0.1, MUTED),
            strip("sine, 7 laps", _probe(7, "s"), -0.45, WARM),
        )
        self.play(FadeIn(rows[0]), FadeIn(rows[1]))
        note = _swap_caption(
            self,
            None,
            caption(
                "at the 8 stops, the 7-lap cosine probe is the 1-lap probe — number for number"
            ).move_to(3.2 * DOWN),
        )
        self.wait(1.6)
        self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        note = _swap_caption(
            self,
            note,
            caption("the 7-lap sine probe is the 1-lap one with every sign flipped").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.6)
        pairs = Text("likewise 6 laps is 2, and 5 laps is 3", font_size=LABEL_SIZE, color=ACCENT)
        pairs.move_to(1.4 * DOWN)
        cells = caption(
            "the table of zeros, run past row 4: c₃ × c₅ adds to 4, s₃ × s₅ to −4 — not 0"
        )
        cells.move_to(2.1 * DOWN)
        self.play(FadeIn(pairs))
        self.play(FadeIn(cells))
        note = _swap_caption(
            self,
            note,
            caption("a detector above row 4 would only repeat one below it").move_to(3.2 * DOWN),
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(rows, pairs, cells, prompt, note)))

        # --- why: 7/8 of a lap forward is 1/8 of a lap backward -------------------------
        centre, radius = np.array([-4.4, 0.0, 0.0]), 1.4
        circle = Circle(radius=radius, color=MUTED, stroke_width=2).move_to(centre)
        stops = VGroup(
            *[
                Dot(
                    centre + radius * np.array([np.cos(n * PI / 4), np.sin(n * PI / 4), 0.0]),
                    radius=0.05,
                    color=COOL,
                )
                for n in range(_N)
            ]
        )
        walker = Dot(centre + radius * RIGHT, radius=0.09, color=WARM)
        self.play(Create(circle), FadeIn(stops), FadeIn(walker))
        note = _swap_caption(
            self,
            None,
            caption(
                "a 7000 Hz tone steps 7/8 of a lap between samples — watch where it lands"
            ).move_to(3.2 * DOWN),
        )
        for _ in range(3):
            self.play(Rotate(walker, angle=7 * PI / 4, about_point=centre), run_time=0.9)
            self.wait(0.2)
        note = _swap_caption(
            self,
            note,
            caption(
                "the same stops as 1/8 of a lap backward: same shadow, the height flipped"
            ).move_to(3.2 * DOWN),
        )
        for _ in range(3):
            self.play(Rotate(walker, angle=-PI / 4, about_point=centre), run_time=0.4)
        self.wait(1.0)

        # --- two tones through the same 8 samples ---------------------------------------
        x0, dx, y0, scale = -1.9, 1.0, 0.0, 1.1
        axis = Line(
            np.array([x0 - 0.3, y0, 0.0]),
            np.array([x0 + 7 * dx + 0.4, y0, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        slow = ParametricFunction(
            lambda t: np.array([x0 + 7 * dx * t, y0 + scale * np.cos(2 * np.pi * 7 * t / 8), 0.0]),
            t_range=[0, 1],
            color=COOL,
            stroke_width=3,
        )
        fast = ParametricFunction(
            lambda t: np.array([x0 + 7 * dx * t, y0 + scale * np.cos(2 * np.pi * 49 * t / 8), 0.0]),
            t_range=[0, 1, 0.002],
            color=WARM,
            stroke_width=2,
        )
        samples = _Stems(_probe(1, "c"), x0, dx, y0, scale, color=ACCENT)
        self.play(Create(axis), FadeIn(samples))
        self.play(Create(slow), run_time=1.2)
        self.play(Create(fast), run_time=2.0)
        note = _swap_caption(
            self,
            note,
            caption(
                "1000 Hz and 7000 Hz pass through the same 8 samples — the 1000 Hz row fires"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(circle, stops, walker, axis, slow, fast, samples, note)))

        # --- the ruler folds at half the sample rate ------------------------------------
        left, per_khz, y = -4.0, 2.0, -0.3
        ruler = Line(
            np.array([left, y, 0.0]),
            np.array([left + 4 * per_khz, y, 0.0]),
            color=MUTED,
            stroke_width=3,
        )
        marks = VGroup(
            *[
                Text(f"{k * 1000}", font_size=SMALL_SIZE).move_to(
                    np.array([left + k * per_khz, y - 0.4, 0.0])
                )
                for k in range(5)
            ]
        )
        ghosts = VGroup()
        for above, lands in ((5000, 3), (6000, 2), (7000, 1)):
            ghost = Text(f"{above}", font_size=SMALL_SIZE, color=WARM)
            ghost.move_to(np.array([left + lands * per_khz, y + 1.0, 0.0]))
            arrow = Arrow(
                ghost.get_bottom(),
                np.array([left + lands * per_khz, y + 0.08, 0.0]),
                color=WARM,
                buff=0.08,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2,
            )
            ghosts.add(VGroup(ghost, arrow))
        fold = Text("the fold: sr ÷ 2 = 4000 Hz", font_size=LABEL_SIZE, color=ACCENT)
        fold.move_to(np.array([left + 4 * per_khz, y + 1.0, 0.0]) + 0.6 * LEFT + 0.7 * UP)
        self.play(Create(ruler), FadeIn(marks), FadeIn(fold))
        self.play(
            LaggedStart(*[FadeIn(g, shift=0.2 * DOWN) for g in reversed(ghosts)], lag_ratio=0.4)
        )
        note = _swap_caption(
            self,
            None,
            caption("sampled at 8000 Hz: 5000 lands on 3000, 6000 on 2000, 7000 on 1000").move_to(
                3.2 * DOWN
            ),
        )
        self.wait(1.8)
        lines = [
            "the first scene's promise: more than two samples per lap — strictly below sr ÷ 2",
            "exactly at sr ÷ 2, a sine lands on 0 at every stop: the samples are silence",
            "the impostor is a clean lower tone, not noise — so filter it out before sampling",
            "hence 8000 Hz for telephone speech and 16 000 Hz for speech models",
        ]
        for line in lines:
            note = _swap_caption(self, note, caption(line).move_to(3.2 * DOWN))
            self.wait(1.7)
        credit = caption("sampling theorem: E. T. Whittaker 1915 · Kotelnikov 1933 · Shannon 1949")
        credit.move_to(2.7 * DOWN)
        self.play(FadeIn(credit))
        self.wait(1.6)
        self.play(FadeOut(VGroup(ruler, marks, ghosts, fold, note, credit)))

        # --- where the road goes ----------------------------------------------------------
        road = VGroup(
            Text(
                "which tones are in it?  →  the bank of detectors", font_size=LABEL_SIZE, color=GOOD
            ),
            Text("quiet beside loud?  →  decibels", font_size=LABEL_SIZE, color=GOOD),
            Text("a tone between rows?  →  windowing", font_size=LABEL_SIZE, color=MUTED),
            Text(
                "tones that change over time?  →  the short-time transform",
                font_size=LABEL_SIZE,
                color=MUTED,
            ),
            Text("the ear's own grouping?  →  mel", font_size=LABEL_SIZE, color=MUTED),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        road.move_to(0.2 * UP)
        self.play(LaggedStart(*[FadeIn(line, shift=0.15 * UP) for line in road], lag_ratio=0.25))
        note = _swap_caption(
            self,
            None,
            caption(
                "built here, and still ahead on the road to the spectrogram a speech model reads"
            ).move_to(3.2 * DOWN),
        )
        self.wait(2.2)
        self.play(FadeOut(VGroup(road, note)))
        _takeaway(
            self,
            "Above half the sample rate a tone is its own mirror image —\n"
            "the bank stops at sr ÷ 2 because nothing above it can be told apart",
        )


if __name__ == "__main__":
    raise SystemExit(render_cli())
