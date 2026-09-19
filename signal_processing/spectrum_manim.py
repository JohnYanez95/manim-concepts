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
    MUTED,
    SMALL_SIZE,
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
        self.x0, self.dx, self.y0, self.scale = x0, dx, y0, scale
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


if __name__ == "__main__":
    raise SystemExit(render_cli())
