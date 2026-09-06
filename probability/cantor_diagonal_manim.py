"""Cantor's diagonal — the interval [0, 1] cannot be arranged in a sequence.

Seven scenes in the language of Bertsekas & Tsitsiklis's Problem 4*: what
"arranged in a sequence" means and how much a sequence can hold, every
point of the interval as a row of digits, the diagonal rule that builds a
point no row can be, why its digits are 1 or 2, the same diagonal run on
subsets, and the closer that lands in this topic — a sequence of points
has probability 0 + 0 + ⋯ = 0, so "probability is area" was never a sum
over points.

    ArrangedInASequence     every element gets a finite position number
    TheZigzag               pairs and fractions are sequences too
    EveryPointHasDigits     a point is a row of digits; a few own two rows
    TheDiagonalRule         y differs from row n at digit n — for every n
    WhyOneOrTwo             the rule that beats every list, and the ones that fail
    TheSameDiagonalTwice    no list of subsets is complete either
    AreaNotSums             the additivity axiom is stated for sequences

Every number on screen is exact and machine-verified in plan 017.

Render:
    uv run python probability/cantor_diagonal_manim.py
    uv run python probability/cantor_diagonal_manim.py --scene ArrangedInASequence --quality draft
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
    ConceptScene,
    boxed,
    caption,
    palette,
    render_cli,
    token,
)


def _takeaway(scene: ConceptScene, text: str, size: int = 25) -> None:
    takeaway = Text(text, font_size=size, line_spacing=1.1).move_to(0.2 * DOWN)
    scene.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
    scene.wait(2)


def _pairing_arrows(top: VGroup, bottom: VGroup, color: str = MUTED) -> VGroup:
    """One arrow per column, from an element of ``top`` to the one below it.

    Stacked lists with arrows, never side-by-side sets: the layout itself says
    "one-to-one", which is the whole content of "arranged in a sequence".
    """
    return VGroup(
        *[
            Arrow(
                t.get_bottom(),
                b.get_top(),
                buff=0.08,
                color=color,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.3,
            )
            for t, b in zip(top, bottom, strict=True)
        ]
    )


class ArrangedInASequence(ConceptScene):
    """ "Arranged in a sequence" means every element gets a finite position number — and a
    sequence can hold more than it looks: the integers, and always one more."""

    def construct(self):
        self.play(FadeIn(self.title("Arranged in a Sequence"), shift=0.3 * DOWN))
        prompt = Text("[0, 1] — can its points be arranged in a sequence?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 1: what the words mean ---------------------------------------------
        objects = VGroup(*[token(letter, palette(i)) for i, letter in enumerate("abcdef")])
        objects.arrange(RIGHT, buff=0.42).move_to(0.6 * UP)
        self.play(LaggedStart(*[FadeIn(o, scale=0.8) for o in objects], lag_ratio=0.1))
        positions = VGroup(
            *[Text(str(i + 1), font_size=LABEL_SIZE, color=ACCENT) for i in range(6)]
        )
        for pos, obj in zip(positions, objects, strict=True):
            pos.next_to(obj, UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(p, shift=0.15 * DOWN) for p in positions], lag_ratio=0.1))
        meaning = caption("arranged in a sequence: every element gets a finite position number")
        meaning.next_to(objects, DOWN, buff=0.45)
        self.play(FadeIn(meaning))
        self.wait(1.2)

        # The row keeps going — a sequence never runs out of positions.
        more = VGroup(*[token(letter, palette(i + 6)) for i, letter in enumerate("gh")])
        more.arrange(RIGHT, buff=0.42).next_to(objects, RIGHT, buff=0.42)
        dots = Text("…", font_size=BODY_SIZE).next_to(more, RIGHT, buff=0.3)
        more_pos = VGroup(*[Text(str(i + 7), font_size=LABEL_SIZE, color=ACCENT) for i in range(2)])
        for pos, obj in zip(more_pos, more, strict=True):
            pos.next_to(obj, UP, buff=0.3)
        row = VGroup(objects, positions, more, more_pos, dots)
        self.play(row.animate.move_to(np.array([0.0, 0.7, 0.0])), run_time=0.6)
        self.play(FadeIn(more), FadeIn(more_pos), FadeIn(dots))
        repeats = caption("repeats are allowed — a sequence may name a point twice")
        repeats.next_to(meaning, DOWN, buff=0.22)
        self.play(FadeIn(repeats))
        self.wait(1.4)

        # --- the integers are a sequence: stacked, paired, never side by side -------
        self.play(FadeOut(VGroup(row, meaning, repeats)))
        naturals = VGroup(*[Text(str(n), font_size=BODY_SIZE, color=COOL) for n in range(1, 11)])
        naturals.arrange(RIGHT, buff=0.62).move_to(1.35 * UP)
        # Anchor P: even n ↦ n/2, odd n ↦ −(n − 1)/2 — 0, 1, −1, 2, −2, …
        integers = VGroup(
            *[
                Text(str(n // 2 if n % 2 == 0 else -(n - 1) // 2), font_size=BODY_SIZE)
                for n in range(1, 11)
            ]
        )
        for z, n in zip(integers, naturals, strict=True):
            z.move_to(np.array([n.get_x(), -0.15, 0.0]))
        arrows = _pairing_arrows(naturals, integers)
        n_tag = Text("positions", font_size=LABEL_SIZE, color=COOL)
        n_tag.next_to(naturals, LEFT, buff=0.5)
        z_tag = Text("the integers", font_size=LABEL_SIZE).next_to(integers, LEFT, buff=0.5)
        self.play(FadeIn(naturals), FadeIn(n_tag))
        self.play(FadeIn(z_tag))
        for arrow, z in zip(arrows, integers, strict=True):
            self.play(GrowArrow(arrow), FadeIn(z, shift=0.1 * DOWN), run_time=0.3)
        rule = caption("even n ↦ n/2, odd n ↦ −(n − 1)/2 — every integer has one position")
        rule.next_to(integers, DOWN, buff=0.45)
        self.play(FadeIn(rule))
        self.wait(1.4)

        # --- the objection answered before it is raised --------------------------
        # Hilbert's hotel: shift every element one place and a new one fits.
        new = Text("★", font_size=BODY_SIZE, color=GOOD)
        new.move_to(np.array([naturals[0].get_x() - 0.9, integers.get_y(), 0.0]))
        self.play(
            integers.animate.shift(0.62 * RIGHT),
            arrows.animate.shift(0.31 * RIGHT),
            FadeIn(new, scale=0.6),
            run_time=0.8,
        )
        shifted = _pairing_arrows(naturals, VGroup(new, *integers[:9]))
        self.play(FadeOut(arrows), FadeIn(shifted), run_time=0.5)
        room = caption("a list can always take one more: shift everything one place", color=GOOD)
        room.next_to(rule, DOWN, buff=0.22)
        self.play(FadeIn(room))
        self.wait(1.4)

        self.play(FadeOut(VGroup(naturals, integers, shifted, n_tag, z_tag, rule, room, new)))
        _takeaway(
            self,
            "A sequence gives every element a finite position —\n"
            "running out of room is never the obstacle",
        )


if __name__ == "__main__":
    raise SystemExit(render_cli())
