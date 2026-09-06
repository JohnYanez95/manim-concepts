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
    SMALL_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    on_frame,
    palette,
    render_cli,
    token,
)

_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _sub(n: int) -> str:
    """``x₁₂``-style index for ``Text`` — Pango draws ``_`` literally."""
    return str(n).translate(_SUB)


# Anchor L (plan 017): the seven listed points, first eight digits, truncated.
# Row 7 is the same point as row 2 under its other expansion — on purpose.
_ROWS = [
    ("π − 3", "14159265"),
    ("1/2", "50000000"),
    ("1/3", "33333333"),
    ("√2 − 1", "41421356"),
    ("1/e", "36787944"),
    ("e − 2", "71828182"),
    ("1/2", "49999999"),
]
_DIAGONAL = "1032719"  # digit n of row n
_Y = "2111121"  # d_n = 1 unless a_n^n = 1, then 2
# Anchor M: y prepended, the seven rows shifted down one.
_RERUN_DIAGONAL = "24031989"
_Y_PRIME = "11112111"


def _stamp(p: int, q: int) -> int:
    """Anchor O: position of cell (p, q) on the anti-diagonal walk that starts at
    the top row of each anti-diagonal."""
    s = p + q
    return (s - 2) * (s - 1) // 2 + p


class _DigitTable(VGroup):
    """Listed numbers as rows of digits: a name, ``0.``, the digits, ``…``.

    ``table.digit(r, k)`` is digit k (0-based) of row r; ``table.box(r, k)`` frames
    it. The diagonal is boxed cell by cell, never drawn as a line — the claim is
    "one cell per row", not "a diagonal".
    """

    def __init__(
        self,
        rows,
        top_y: float,
        cell: float = 0.5,
        name_x: float = -5.2,
        digit_x0: float = -1.4,
        font_size: int = LABEL_SIZE,
    ):
        super().__init__()
        self.cell = cell
        self.digit_x0 = digit_x0
        self.names, self.prefixes, self.rows, self.dots = VGroup(), VGroup(), [], VGroup()
        for r, (name, digits) in enumerate(rows):
            y = top_y - r * cell
            label = Text(name, font_size=font_size)
            label.move_to(np.array([name_x, y, 0.0]), aligned_edge=LEFT)
            prefix = Text("0.", font_size=font_size, color=MUTED)
            prefix.move_to(np.array([digit_x0 - 0.5, y, 0.0]))
            row = VGroup(
                *[
                    Text(d, font_size=font_size).move_to(np.array([digit_x0 + k * cell, y, 0.0]))
                    for k, d in enumerate(digits)
                ]
            )
            dots = Text("…", font_size=font_size, color=MUTED)
            dots.move_to(np.array([digit_x0 + len(digits) * cell, y, 0.0]))
            self.names.add(label)
            self.prefixes.add(prefix)
            self.rows.append(row)
            self.dots.add(dots)
        self.digits = VGroup(*self.rows)
        self.add(self.names, self.prefixes, self.digits, self.dots)

    def digit(self, r: int, k: int) -> Text:
        return self.rows[r][k]

    def box(self, r: int, k: int, color: str = ACCENT) -> SurroundingRectangle:
        return SurroundingRectangle(self.digit(r, k), color=color, buff=0.07, stroke_width=2.5)

    def column_x(self, k: int) -> float:
        return self.digit_x0 + k * self.cell


def _y_row(table: _DigitTable, digits: str, y: float, label: str = "y") -> VGroup:
    """The constructed number under the table, digit k under column k."""
    name = Text(f"{label} =", font_size=LABEL_SIZE, color=ACCENT)
    name.move_to(np.array([table.names[0].get_left()[0], y, 0.0]), aligned_edge=LEFT)
    prefix = Text("0.", font_size=LABEL_SIZE, color=ACCENT)
    prefix.move_to(np.array([table.prefixes[0].get_x(), y, 0.0]))
    cells = VGroup(
        *[
            Text(d, font_size=LABEL_SIZE, color=ACCENT).move_to(
                np.array([table.column_x(k), y, 0.0])
            )
            for k, d in enumerate(digits)
        ]
    )
    dots = Text("…", font_size=LABEL_SIZE, color=ACCENT)
    dots.move_to(np.array([table.column_x(len(digits) - 1) + table.cell, y, 0.0]))
    return VGroup(name, prefix, cells, dots)


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
        new.move_to(np.array([naturals[0].get_x(), integers.get_y(), 0.0]))
        step = naturals[1].get_x() - naturals[0].get_x()
        self.play(FadeOut(arrows), integers.animate.shift(step * RIGHT), run_time=0.8)
        shifted = _pairing_arrows(naturals, VGroup(new, *integers[:9]))
        self.play(FadeIn(new, scale=0.6), FadeIn(shifted), run_time=0.5)
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


class TheZigzag(ConceptScene):
    """Pairs of positions — and the fractions — are a sequence too: walk the counting grid
    along its anti-diagonals and every cell gets a finite position number."""

    def construct(self):
        self.play(FadeIn(self.title("The Zigzag"), shift=0.3 * DOWN))
        prompt = Text("pairs of positions (p, q) — are they a sequence too?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- the counting grid, open on two sides ---------------------------------------
        cell = 0.66
        origin = np.array([-4.0, 1.25, 0.0])  # centre of cell (1, 1)
        squares = {}
        grid = VGroup()
        for p in range(1, 6):
            for q in range(1, 6):
                sq = Square(side_length=cell, stroke_width=1.5, color=MUTED)
                sq.move_to(origin + np.array([(q - 1) * cell, -(p - 1) * cell, 0.0]))
                squares[p, q] = sq
                grid.add(sq)
        q_labels = VGroup(
            *[
                Text(str(q), font_size=SMALL_SIZE, color=COOL).next_to(squares[1, q], UP, buff=0.12)
                for q in range(1, 6)
            ]
        )
        p_labels = VGroup(
            *[
                Text(str(p), font_size=SMALL_SIZE, color=COOL).next_to(
                    squares[p, 1], LEFT, buff=0.15
                )
                for p in range(1, 6)
            ]
        )
        q_labels.add(
            Text("q", font_size=SMALL_SIZE, color=COOL).next_to(q_labels[4], RIGHT, buff=0.45)
        )
        p_labels.add(
            Text("p", font_size=SMALL_SIZE, color=COOL).next_to(p_labels[4], DOWN, buff=0.35)
        )
        open_right = Text("…", font_size=BODY_SIZE, color=MUTED).next_to(
            squares[3, 5], RIGHT, buff=0.2
        )
        open_down = Text("⋮", font_size=BODY_SIZE, color=MUTED).next_to(
            squares[5, 3], DOWN, buff=0.15
        )
        self.play(Create(grid), FadeIn(q_labels), FadeIn(p_labels), run_time=1.2)
        self.play(FadeIn(open_right), FadeIn(open_down))
        furniture = caption(
            "the counting grid — the multiplicative rule's rectangle, open on two sides"
        )
        furniture.move_to(2.5 * DOWN)
        self.play(FadeIn(furniture))
        self.wait(1.0)

        # --- stamp the anti-diagonals (anchor O) ------------------------------------------
        order = sorted(
            ((p, q) for p in range(1, 6) for q in range(1, 6) if p + q <= 6),
            key=lambda c: _stamp(*c),
        )
        stamps = {}
        for p, q in order:
            stamps[p, q] = Text(str(_stamp(p, q)), font_size=LABEL_SIZE, color=ACCENT).move_to(
                squares[p, q]
            )
        walk = caption("walk the anti-diagonals: p + q = 2, then 3, then 4, …")
        walk.move_to(2.85 * DOWN)
        self.play(FadeIn(walk))
        self.play(
            LaggedStart(*[FadeIn(stamps[c], scale=0.6) for c in order], lag_ratio=0.9),
            run_time=4.0,
        )
        self.wait(0.8)
        every = caption("every cell gets a finite position number — pairs are a sequence")
        every.move_to(3.2 * DOWN)
        self.play(FadeIn(every))
        self.wait(1.2)

        # --- relabel as fractions; skip what is not in lowest terms ---------------------
        self.play(FadeOut(VGroup(walk, every, furniture)))
        fractions = {}
        for p, q in order:
            fractions[p, q] = Text(f"{p}/{q}", font_size=SMALL_SIZE).move_to(squares[p, q])
        self.play(
            *[FadeOut(stamps[c]) for c in order],
            *[FadeIn(fractions[c]) for c in order],
            run_time=0.8,
        )
        relabel = caption("the same cells, read as fractions p/q")
        relabel.move_to(2.5 * DOWN)
        self.play(FadeIn(relabel))
        skipped = [(2, 2), (2, 4), (3, 3), (4, 2)]
        strikes = VGroup()
        for c in skipped:
            fractions[c].set_color(WARM)
            strikes.add(
                Line(
                    fractions[c].get_left(), fractions[c].get_right(), color=WARM, stroke_width=2.5
                )
            )
        self.play(Create(strikes), run_time=0.8)
        skip = caption(
            "2/2, 2/4, 3/3, 4/2 already appeared in lowest terms — skip them", color=WARM
        )
        skip.move_to(2.85 * DOWN)
        self.play(FadeIn(skip))
        self.wait(0.8)

        kept = [c for c in order if c not in skipped]
        listing = VGroup()
        for i, (p, q) in enumerate(kept):
            pos = Text(str(i + 1), font_size=SMALL_SIZE, color=ACCENT)
            arrow = Text("↦", font_size=SMALL_SIZE, color=MUTED)
            frac = Text(f"{p}/{q}", font_size=SMALL_SIZE, color=GOOD)
            entry = VGroup(pos, arrow, frac).arrange(RIGHT, buff=0.15)
            listing.add(entry)
        listing.arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to(np.array([3.4, 0.0, 0.0]))
        head = Text("positions → fractions", font_size=SMALL_SIZE, color=MUTED)
        head.next_to(listing, UP, buff=0.25)
        self.play(FadeIn(head))
        for entry, c in zip(listing, kept, strict=True):
            self.play(
                FadeIn(entry, shift=0.1 * RIGHT),
                Indicate(fractions[c], color=GOOD, scale_factor=1.3),
                run_time=0.3,
            )
        never = caption(
            "skipping never breaks a list — the next kept cell takes the next position", color=GOOD
        )
        never.move_to(3.2 * DOWN)
        self.play(FadeIn(never))
        self.wait(1.5)

        self.play(
            FadeOut(
                VGroup(
                    grid,
                    q_labels,
                    p_labels,
                    open_right,
                    open_down,
                    strikes,
                    listing,
                    head,
                    relabel,
                    skip,
                    never,
                    *fractions.values(),
                )
            )
        )
        _takeaway(
            self,
            "Pairs and fractions are sequences —\n"
            "every positive fraction has one lowest-terms cell, so one position",
        )


class EveryPointHasDigits(ConceptScene):
    """Every point of [0, 1] is a row of digits — its address by tenths, then hundredths — and a
    few points own two rows: 0.5000… and 0.4999… name the same point."""

    def construct(self):
        self.play(FadeIn(self.title("Every Point Has Digits"), shift=0.3 * DOWN))
        prompt = Text("a point of [0, 1] — what is its name?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- the interval as a sample space, the spinner lands at 1/3 --------------------
        def segment(y: float, lo: str, hi: str, length: float = 9.0) -> VGroup:
            line = Line(LEFT * length / 2, RIGHT * length / 2, stroke_width=3).move_to(y * UP)
            ticks = VGroup()
            for i in range(11):
                x = line.get_left()[0] + i * length / 10
                ticks.add(
                    Line(
                        np.array([x, y - 0.12, 0]),
                        np.array([x, y + 0.12, 0]),
                        stroke_width=2,
                        color=MUTED,
                    )
                )
            left = Text(lo, font_size=SMALL_SIZE).next_to(line.get_left(), DOWN, buff=0.18)
            right = Text(hi, font_size=SMALL_SIZE).next_to(line.get_right(), DOWN, buff=0.18)
            return VGroup(line, ticks, left, right)

        def point_on(seg: VGroup, t: float) -> np.ndarray:
            line = seg[0]
            return line.get_left() + t * (line.get_right() - line.get_left())

        def tenth(seg: VGroup, i: int, color: str) -> Rectangle:
            line = seg[0]
            w = line.get_length() / 10
            rect = Rectangle(
                width=w, height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.35
            )
            rect.move_to(line.get_left() + np.array([(i + 0.5) * w, 0, 0]))
            return rect

        top = segment(1.6, "0", "1")
        self.play(Create(top[0]), FadeIn(top[1]), FadeIn(top[2]), FadeIn(top[3]))
        third = 1 / 3
        dot = Dot(point_on(top, third), color=ACCENT, radius=0.09)
        dot_label = Text("1/3", font_size=LABEL_SIZE, color=ACCENT).next_to(dot, UP, buff=0.15)
        self.play(FadeIn(dot, scale=0.5), FadeIn(dot_label))
        tint1 = tenth(top, 3, COOL)
        digit1 = Text(
            "first digit 3 — it lies in the fourth tenth, [0.3, 0.4)",
            font_size=SMALL_SIZE,
            color=COOL,
        )
        digit1.next_to(top, DOWN, buff=0.35)
        self.play(FadeIn(tint1), FadeIn(digit1))
        self.wait(0.8)

        # zoom: the tenth cut into tenths again
        mid = segment(-0.1, "0.3", "0.4")
        zoom = VGroup(
            DashedLine(tint1.get_corner(DL), mid[0].get_left(), color=MUTED, stroke_width=1.5),
            DashedLine(tint1.get_corner(DR), mid[0].get_right(), color=MUTED, stroke_width=1.5),
        )
        self.play(
            FadeOut(digit1),
            Create(zoom),
            Create(mid[0]),
            FadeIn(mid[1]),
            FadeIn(mid[2]),
            FadeIn(mid[3]),
        )
        dot2 = Dot(point_on(mid, (third - 0.3) * 10), color=ACCENT, radius=0.09)
        tint2 = tenth(mid, 3, COOL)
        digit2 = Text(
            "second digit 3 — the fourth hundredth inside it, [0.33, 0.34)",
            font_size=SMALL_SIZE,
            color=COOL,
        )
        digit2.next_to(mid, DOWN, buff=0.35)
        self.play(FadeIn(dot2, scale=0.5), FadeIn(tint2), FadeIn(digit2))
        self.wait(0.8)
        address = VGroup(
            MathTex(r"\tfrac{1}{3} = 0.333\cdots", font_size=40),
            caption("B&T's own example — the digits are the address, and every point has one"),
        ).arrange(DOWN, buff=0.2)
        address.move_to(2.2 * DOWN)
        self.play(FadeIn(address))
        self.wait(1.5)

        # --- the exception: a point that owns two rows ---------------------------------
        self.play(FadeOut(VGroup(mid, zoom, dot2, tint2, digit2, address, tint1, dot, dot_label)))
        half = Dot(point_on(top, 0.5), color=ACCENT, radius=0.09)
        half_label = Text("1/2", font_size=LABEL_SIZE, color=ACCENT).next_to(half, UP, buff=0.15)
        left_tenth = tenth(top, 4, WARM)
        right_tenth = tenth(top, 5, COOL)
        self.play(FadeIn(half, scale=0.5), FadeIn(half_label))
        self.play(FadeIn(right_tenth), FadeIn(left_tenth))
        edge = Text(
            "1/2 sits on a tick — the edge of [0.4, 0.5) and of [0.5, 0.6)", font_size=SMALL_SIZE
        )
        edge.next_to(top, DOWN, buff=0.35)
        self.play(FadeIn(edge))
        two_rows = VGroup(
            MathTex(r"0.5000\cdots", font_size=40, color=COOL),
            MathTex(r"0.4999\cdots", font_size=40, color=WARM),
        ).arrange(RIGHT, buff=1.2)
        two_rows.move_to(0.0 * UP)
        self.play(FadeIn(two_rows))
        why = VGroup(
            MathTex(
                r"3 \times 0.333\cdots = 0.999\cdots",
                r"\quad\text{and}\quad",
                r"3 \times \tfrac{1}{3} = 1",
                font_size=36,
            ),
            caption("so 0.999… = 1 — two rows for one point, and 0.4999… = 0.5000… the same way"),
        ).arrange(DOWN, buff=0.2)
        why.move_to(1.2 * DOWN)
        self.play(FadeIn(why[0]))
        self.wait(0.6)
        self.play(FadeIn(why[1]))
        only = caption(
            'B&T: "this is the only kind of exception" — all zeros or all nines',
            color=ACCENT,
        )
        only.move_to(2.4 * DOWN)
        self.play(FadeIn(only))
        self.wait(1.8)

        self.play(
            FadeOut(
                VGroup(top, half, half_label, left_tenth, right_tenth, edge, two_rows, why, only)
            )
        )
        _takeaway(
            self,
            "Every point of [0, 1] is a row of digits —\nand a few points own two rows",
        )


class TheDiagonalRule(ConceptScene):
    """Suppose the points are arranged in a sequence: read digit n of row n, choose a different
    digit, and the number built from the choices differs from every row — at digit n."""

    def construct(self):
        self.play(FadeIn(self.title("The Diagonal Rule"), shift=0.3 * DOWN))
        prompt = Text(
            "suppose [0, 1] is arranged in a sequence x₁, x₂, x₃, …",
            font_size=BODY_SIZE,
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        table = _DigitTable(
            [(f"x{_sub(i + 1)} = {name}", digits) for i, (name, digits) in enumerate(_ROWS)],
            top_y=1.65,
        )
        self.play(FadeIn(table.names), FadeIn(table.prefixes), FadeIn(table.dots))
        self.wait(0.4)

        # --- diagonal first: one cell per row, before the rows are filled --------------
        boxes = VGroup(*[table.box(n, n) for n in range(7)])
        diag_digits = VGroup(*[table.digit(n, n) for n in range(7)])
        one_cell = caption("digit n of row n — one cell per row", color=ACCENT)
        one_cell.next_to(table, DOWN, buff=0.25)
        for n in range(7):
            self.play(FadeIn(diag_digits[n], scale=0.6), Create(boxes[n]), run_time=0.35)
        self.play(FadeIn(one_cell))
        self.wait(0.8)

        rule = MathTex(
            r"d_n = \begin{cases} 1 & a_n^n \neq 1 \\ 2 & a_n^n = 1 \end{cases}",
            font_size=34,
        )
        rule.move_to(np.array([5.1, 0.6, 0.0]))
        rule_words = caption("a digit the cell is not")
        rule_words.next_to(rule, DOWN, buff=0.25)
        self.play(FadeIn(rule), FadeIn(on_frame(rule_words)))
        y_row = _y_row(table, _Y, y=table.digit(6, 0).get_y() - 0.75)
        self.play(FadeOut(one_cell), FadeIn(y_row[0]), FadeIn(y_row[1]), FadeIn(y_row[3]))
        for n in range(7):
            self.play(
                Indicate(diag_digits[n], color=ACCENT, scale_factor=1.2),
                FadeIn(y_row[2][n], shift=0.15 * DOWN),
                run_time=0.4,
            )
        self.wait(0.8)

        # --- now the rows: the other digits never mattered ------------------------------
        others = VGroup(*[table.digit(r, k) for r in range(7) for k in range(8) if k != r])
        self.play(FadeIn(others, lag_ratio=0.01), run_time=1.2)
        never = caption("the other digits never mattered — they arrive after y is built")
        never.next_to(y_row, DOWN, buff=0.25)
        self.play(FadeIn(never))
        self.wait(1.0)

        # --- compare y with every row at its own column -------------------------------
        self.play(FadeOut(never))
        compare = None
        for n in range(7):
            row_hit = SurroundingRectangle(table.digit(n, n), color=WARM, buff=0.07, stroke_width=3)
            y_hit = SurroundingRectangle(y_row[2][n], color=GOOD, buff=0.07, stroke_width=3)
            line = caption(
                f"row {n + 1}: digit {n + 1} is {_DIAGONAL[n]}, y's is {_Y[n]} — different",
                color=GOOD,
            )
            line.next_to(y_row, DOWN, buff=0.25)
            anims = [Create(row_hit), Create(y_hit), FadeIn(line)]
            if compare is not None:
                self.play(FadeOut(compare), run_time=0.15)
            self.play(*anims, run_time=0.35)
            self.wait(0.35)
            self.play(FadeOut(row_hit), FadeOut(y_hit), run_time=0.15)
            compare = line
        self.play(FadeOut(compare))
        every_n = caption(
            "y differs from row n at digit n — for every n, by the rule", color=ACCENT
        )
        every_n.next_to(y_row, DOWN, buff=0.25)
        self.play(FadeIn(every_n))
        self.wait(1.2)

        # --- the diagonal is bookkeeping, not geometry -----------------------------------
        self.play(FadeOut(boxes), FadeOut(every_n))
        permuted = [(0, 2), (1, 0), (2, 4), (3, 1), (4, 6), (5, 3), (6, 5)]
        other_boxes = VGroup(*[table.box(r, k, color=COOL) for r, k in permuted])
        self.play(Create(other_boxes), run_time=0.8)
        bookkeeping = caption(
            "one cell per row, at most one per column — any such choice works alike",
            color=COOL,
        )
        bookkeeping.next_to(y_row, DOWN, buff=0.25)
        self.play(FadeIn(on_frame(bookkeeping)))
        self.wait(1.4)

        self.play(FadeOut(VGroup(table, other_boxes, y_row, rule, rule_words, bookkeeping)))
        _takeaway(
            self,
            "y differs from row n at digit n — for every n —\nso y is on no row of the sequence",
        )


class WhyOneOrTwo(ConceptScene):
    """Why the digits are 1 or 2: a rule that can write 0 or 9 lands on a listed point under
    its other name; and why the claim survives "add y to the list" — run the rule again."""

    def construct(self):
        self.play(FadeIn(self.title("Why One or Two"), shift=0.3 * DOWN))
        prompt = Text("why 1 or 2 — and why does the rule beat every list?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- (i) a rule that can write 0 or 9 fails (anchor N) --------------------------
        bad = _DigitTable(
            [("x₁ = 1/10", "099999"), ("x₂ = 1", "999999"), ("x₃ = 1", "999999")],
            top_y=1.5,
            name_x=-5.0,
            digit_x0=-1.6,
        )
        self.play(FadeIn(bad))
        bad_boxes = VGroup(*[bad.box(n, n, color=WARM) for n in range(3)])
        self.play(Create(bad_boxes))
        plus_one = Text("rule: add 1 to the digit", font_size=SMALL_SIZE, color=WARM)
        plus_one.move_to(np.array([4.4, 1.5, 0.0]))
        bad_y = _y_row(bad, "1000", y=bad.digit(2, 0).get_y() - 0.7)
        bad_y.set_color(WARM)
        self.play(FadeIn(on_frame(plus_one)), FadeIn(bad_y))
        same = MathTex(
            r"0.1000\cdots = \tfrac{1}{10} = 0.0999\cdots = x_1", font_size=38, color=WARM
        )
        same.move_to(1.2 * DOWN)
        fails = caption("different digits, the same number — a rule writing 0 or 9 proves nothing")
        fails.next_to(same, DOWN, buff=0.25)
        binary = caption("the binary flip fails the same way: 0.0111…₂ = 0.1000…₂ = 1/2")
        binary.next_to(fails, DOWN, buff=0.2)
        self.play(FadeIn(same))
        self.play(FadeIn(fails))
        self.play(FadeIn(binary))
        self.wait(1.6)

        # --- (ii) 1 or 2: y owns exactly one row (anchors B, C, D) --------------------
        self.play(FadeOut(VGroup(bad, bad_boxes, plus_one, bad_y, same, fails, binary)))
        rule = MathTex(r"d_n \in \{1, 2\}", font_size=44, color=GOOD).move_to(1.95 * UP)
        owns = VGroup(
            caption(
                "y ends in neither zeros nor nines — so y owns exactly one row",
                color=GOOD,
            ),
            caption("if y were xₙ, the listed row of xₙ would be a row for y — its only row —"),
            caption("so the two rows agree at digit n — but they differ there"),
            caption("y's digits are 1 or 2, so 1/9 ≤ y ≤ 2/9 — inside [0, 1]"),
            caption("rows 2 and 7, both 1/2, are not even in that range"),
        ).arrange(DOWN, buff=0.22)
        owns.move_to(0.1 * UP)
        self.play(FadeIn(rule))
        for line in owns:
            self.play(FadeIn(line), run_time=0.6)
            self.wait(0.3)
        verdict = Text(
            "different digit ⇒ different number, because y never writes 0 or 9",
            font_size=SMALL_SIZE,
            color=GOOD,
        )
        verdict.move_to(1.7 * DOWN)
        self.play(FadeIn(verdict))
        self.wait(1.6)

        # --- (iii) "just add y to the list" — run the rule again (anchor M) --------------
        self.play(FadeOut(VGroup(rule, owns, verdict)))
        rerun_rows = [("y", _Y)] + [(name, digits) for name, digits in _ROWS]
        table = _DigitTable(
            [(f"x{_sub(i + 1)} = {name}", digits) for i, (name, digits) in enumerate(rerun_rows)],
            top_y=1.75,
            cell=0.44,
            font_size=SMALL_SIZE,
        )
        table.names[0].set_color(ACCENT)
        self.play(FadeIn(table))
        added = VGroup(
            caption("y added at the front,", color=ACCENT),
            caption("every row moved down one", color=ACCENT),
        ).arrange(DOWN, buff=0.1)
        added.move_to(np.array([5.0, 1.55, 0.0]))
        self.play(FadeIn(on_frame(added)))
        boxes = VGroup(*[table.box(n, n) for n in range(8)])
        self.play(Create(boxes), run_time=0.8)
        y2 = _y_row(table, _Y_PRIME, y=table.digit(7, 0).get_y() - 0.6, label="y′")
        y2.set_color(GOOD)
        self.play(FadeIn(y2))
        first = caption(
            "y′ ≠ y at digit 1 — always, d′₁ = 3 − d₁ — and off every row at its digit",
            color=GOOD,
        )
        first.next_to(y2, DOWN, buff=0.25)
        self.play(FadeIn(first))
        self.wait(1.2)
        claim = caption(
            'the claim was never "this list misses y" — it is "every list misses one"',
            color=ACCENT,
        )
        claim.next_to(first, DOWN, buff=0.2)
        self.play(FadeIn(on_frame(claim)))
        self.wait(1.4)

        # --- close: the direct statement, then B&T's sentence ---------------------------
        self.play(FadeOut(VGroup(table, boxes, y2, added, first, claim)))
        direct = Text(
            "for any sequence, the rule finds a point not on it", font_size=BODY_SIZE, color=ACCENT
        )
        direct.move_to(0.9 * UP)
        bt = VGroup(
            caption('"the sequence x₁, x₂, … does not exhaust the elements of [0, 1],'),
            caption('contrary to what was assumed" — Bertsekas & Tsitsiklis'),
        ).arrange(DOWN, buff=0.12)
        bt.move_to(0.0 * UP)
        self.play(FadeIn(direct))
        self.play(FadeIn(bt))
        self.wait(1.8)
        self.play(FadeOut(VGroup(direct, bt)))
        _takeaway(
            self,
            "Different digit means different number —\nonly because y's digits are never 0 or 9",
        )


class TheSameDiagonalTwice(ConceptScene):
    """The same move on other objects: Cantor's own rows of two symbols, and a yes/no table of
    subsets whose flipped diagonal is a subset on no row — no list of subsets is complete."""

    def construct(self):
        self.play(FadeIn(self.title("The Same Diagonal Twice"), shift=0.3 * DOWN))
        prompt = Text("Cantor, 1891: two symbols, no decimals", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- Cantor's rows (anchor H) --------------------------------------------------------
        cantor_rows = [("E¹ =", "mmmmmm"), ("E² =", "wwwwww"), ("E³ =", "mwmwmw")]
        cantor = VGroup()
        for r, (name, symbols) in enumerate(cantor_rows):
            y = 1.5 - r * 0.5
            label = Text(name, font_size=LABEL_SIZE).move_to(
                np.array([-5.0, y, 0.0]), aligned_edge=LEFT
            )
            cells = VGroup(
                *[
                    Text(sym, font_size=LABEL_SIZE).move_to(np.array([-3.4 + k * 0.5, y, 0.0]))
                    for k, sym in enumerate(symbols)
                ]
            )
            dots = Text("…", font_size=LABEL_SIZE, color=MUTED).move_to(
                np.array([-3.4 + 6 * 0.5, y, 0.0])
            )
            cantor.add(VGroup(label, cells, dots))
        self.play(FadeIn(cantor))
        c_boxes = VGroup(
            *[
                SurroundingRectangle(cantor[n][1][n], color=ACCENT, buff=0.07, stroke_width=2.5)
                for n in range(3)
            ]
        )
        self.play(Create(c_boxes))
        new_row = VGroup(
            Text("E₀ =", font_size=LABEL_SIZE, color=ACCENT).move_to(
                np.array([-5.0, -0.25, 0.0]), aligned_edge=LEFT
            ),
            *[
                Text(s, font_size=LABEL_SIZE, color=ACCENT).move_to(
                    np.array([-3.4 + k * 0.5, -0.25, 0.0])
                )
                for k, s in enumerate("wmw")
            ],
            Text("…", font_size=LABEL_SIZE, color=ACCENT).move_to(
                np.array([-3.4 + 3 * 0.5, -0.25, 0.0])
            ),
        )
        self.play(FadeIn(new_row))
        own_words = VGroup(
            caption("the new row's nth symbol differs from row n's nth symbol —"),
            caption("Cantor's 1891 rule, on sequences of m and w; the reals came afterwards"),
        ).arrange(DOWN, buff=0.12)
        own_words.move_to(1.1 * DOWN)
        self.play(FadeIn(own_words))
        self.wait(1.6)

        # --- subsets: the yes/no table (anchor Q) ---------------------------------------
        self.play(FadeOut(VGroup(cantor, c_boxes, new_row, own_words)))
        subsets = Text(
            "list four subsets of {1, 2, 3, 4} — is n in the mth subset?", font_size=LABEL_SIZE
        )
        subsets.move_to(1.9 * UP)
        self.play(FadeIn(subsets))
        f_sets = ["{1, 3}", "{1, 3, 4}", "{ }", "{2, 4}"]
        members = [{1, 3}, {1, 3, 4}, set(), {2, 4}]
        x0, y0, dx, dy = -0.6, 0.95, 0.7, 0.55
        col_heads = VGroup(
            *[
                Text(str(n), font_size=LABEL_SIZE, color=COOL).move_to(
                    np.array([x0 + (n - 1) * dx, y0 + dy, 0.0])
                )
                for n in range(1, 5)
            ]
        )
        row_heads = VGroup()
        entries = []
        for m in range(1, 5):
            y = y0 - (m - 1) * dy
            row_heads.add(
                Text(f"f({m}) = {f_sets[m - 1]}", font_size=LABEL_SIZE).move_to(
                    np.array([-4.6, y, 0.0]), aligned_edge=LEFT
                )
            )
            row = VGroup()
            for n in range(1, 5):
                mark = Text(
                    "yes" if n in members[m - 1] else "no",
                    font_size=SMALL_SIZE,
                    color=GOOD if n in members[m - 1] else MUTED,
                )
                mark.move_to(np.array([x0 + (n - 1) * dx, y, 0.0]))
                row.add(mark)
            entries.append(row)
        self.play(FadeIn(col_heads), FadeIn(row_heads))
        self.play(LaggedStart(*[FadeIn(row) for row in entries], lag_ratio=0.2))
        t_boxes = VGroup(
            *[
                SurroundingRectangle(entries[n][n], color=ACCENT, buff=0.07, stroke_width=2.5)
                for n in range(4)
            ]
        )
        self.play(Create(t_boxes))
        flip = ["no", "yes", "yes", "no"]
        d_y = y0 - 4 * dy - 0.15
        d_row = VGroup(
            Text("D = {2, 3}", font_size=LABEL_SIZE, color=ACCENT).move_to(
                np.array([-4.6, d_y, 0.0]), aligned_edge=LEFT
            ),
            *[
                Text(f, font_size=SMALL_SIZE, color=ACCENT).move_to(
                    np.array([x0 + n * dx, d_y, 0.0])
                )
                for n, f in enumerate(flip)
            ],
        )
        self.play(FadeIn(d_row))
        flipped = caption(
            "flip the diagonal: D holds n exactly when the nth subset does not", color=ACCENT
        )
        flipped.next_to(d_row, DOWN, buff=0.3)
        self.play(FadeIn(flipped))
        none = VGroup(
            caption("D is on no row — it disagrees with row n at n"),
            caption("4 subsets listed, 16 exist — no list of subsets is complete"),
        ).arrange(DOWN, buff=0.12)
        none.next_to(flipped, DOWN, buff=0.2)
        self.play(FadeIn(on_frame(none)))
        self.wait(1.8)

        # --- level 3 pointers, in captions ---------------------------------------------------
        self.play(
            FadeOut(VGroup(subsets, col_heads, row_heads, *entries, t_boxes, d_row, flipped, none))
        )
        pointers = VGroup(
            Text("the same move, elsewhere", font_size=BODY_SIZE),
            caption(
                "Turing (1936): the diagonal on computable sequences — the list is uncomputable",
                color=MUTED,
            ),
            caption(
                "(the undecidability story belongs to algorithms/ — promised, not built here)",
                color=MUTED,
            ),
            caption("names are finite strings, and finite strings are a sequence —", color=MUTED),
            caption("so most points of [0, 1] have no name", color=MUTED),
        ).arrange(DOWN, buff=0.28)
        pointers.move_to(0.3 * UP)
        for line in pointers:
            self.play(FadeIn(line), run_time=0.6)
            self.wait(0.4)
        self.wait(1.2)
        self.play(FadeOut(pointers))
        _takeaway(
            self,
            "One cell per row, changed —\nthe same move breaks every complete list",
        )


class AreaNotSums(ConceptScene):
    """The additivity axiom is stated for sequences: a point has probability 0, a sequence of points
    0 + 0 + ⋯ = 0 — so if [0, 1] were a sequence its probability would be 0, not 1. Probability is
    area because the interval is not a sum over points."""

    def construct(self):
        self.play(FadeIn(self.title("Area, Not Sums"), shift=0.3 * DOWN))
        prompt = Text(
            "the wheel of fortune: what is the probability of one point?",
            font_size=BODY_SIZE,
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        length = 9.0
        line = Line(LEFT * length / 2, RIGHT * length / 2, stroke_width=3).move_to(1.6 * UP)
        ends = VGroup(
            Text("0", font_size=SMALL_SIZE).next_to(line.get_left(), DOWN, buff=0.18),
            Text("1", font_size=SMALL_SIZE).next_to(line.get_right(), DOWN, buff=0.18),
        )

        def at(t: float) -> np.ndarray:
            return line.get_left() + t * (line.get_right() - line.get_left())

        self.play(Create(line), FadeIn(ends))
        point = Dot(at(0.5), color=ACCENT, radius=0.09)
        self.play(FadeIn(point, scale=0.5))

        # --- a point cannot have positive probability (anchor R, B&T Example 1.4) --------
        suppose = Text(
            "suppose one point had p = 0.15 — then so would every other", font_size=LABEL_SIZE
        )
        suppose.move_to(0.55 * UP)
        self.play(FadeIn(suppose))
        unit = 2.4  # scene units per probability 1
        base_y = -2.75
        ref = Line(
            np.array([-4.2, base_y, 0]),
            np.array([-4.2, base_y + unit, 0]),
            stroke_width=3,
            color=MUTED,
        )
        ref_top = Text("1", font_size=SMALL_SIZE, color=MUTED).next_to(
            ref.get_top(), LEFT, buff=0.15
        )
        ref_cap = DashedLine(
            np.array([-4.2, base_y + unit, 0]),
            np.array([0.6, base_y + unit, 0]),
            color=MUTED,
            stroke_width=1.5,
        )
        self.play(Create(ref), FadeIn(ref_top), Create(ref_cap))
        stack = VGroup()
        for i in range(7):
            bar = Rectangle(
                width=0.55,
                height=0.15 * unit,
                stroke_width=1.5,
                color=COOL,
                fill_color=COOL,
                fill_opacity=0.35,
            )
            bar.move_to(np.array([-1.0, base_y + (i + 0.5) * 0.15 * unit, 0]))
            stack.add(bar)
        self.play(
            LaggedStart(*[FadeIn(b, shift=0.1 * UP) for b in stack], lag_ratio=0.15), run_time=1.4
        )
        stack[6].set_color(WARM).set_fill(WARM, opacity=0.45)
        total = MathTex(r"7 \times 0.15 = 1.05 > 1", font_size=40, color=WARM)
        total.move_to(np.array([3.7, base_y + 1.75, 0]))
        self.play(FadeIn(total))
        overflow = VGroup(
            caption("any p > 0 overflows the same way:"),
            caption("N > 1/p points would exceed 1"),
        ).arrange(DOWN, buff=0.12)
        overflow.move_to(np.array([3.7, base_y + 1.05, 0]))
        zero = Text("so one point has probability 0", font_size=LABEL_SIZE, color=GOOD)
        zero.move_to(np.array([3.7, base_y + 0.4, 0]))
        self.play(FadeIn(on_frame(overflow)))
        self.play(FadeIn(on_frame(zero)))
        self.wait(1.6)

        # --- the axiom is stated for sequences (anchor S) --------------------------------
        self.play(FadeOut(VGroup(suppose, ref, ref_top, ref_cap, stack, total, overflow, zero)))
        axiom_words = VGroup(
            Text("Axiom 2 (additivity): if A₁, A₂, … is a", font_size=LABEL_SIZE),
            Text("sequence", font_size=LABEL_SIZE, color=ACCENT),
            Text("of disjoint events, then", font_size=LABEL_SIZE),
        ).arrange(RIGHT, buff=0.18)
        axiom_words.move_to(0.55 * UP)
        axiom = MathTex(r"P(A_1 \cup A_2 \cup \cdots) = P(A_1) + P(A_2) + \cdots", font_size=38)
        axiom.next_to(axiom_words, DOWN, buff=0.25)
        seq_box = SurroundingRectangle(axiom_words[1], color=ACCENT, buff=0.08, stroke_width=2.5)
        self.play(FadeIn(axiom_words), FadeIn(axiom))
        self.play(Create(seq_box))
        same_word = caption("the same word Problem 4* denies to [0, 1]", color=ACCENT)
        same_word.next_to(axiom, DOWN, buff=0.25)
        self.play(FadeIn(same_word))
        self.wait(1.4)

        # --- a sequence of points has probability 0: the halving cover (anchor R) -------
        self.play(
            FadeOut(VGroup(same_word)),
            VGroup(axiom_words, axiom, seq_box).animate.shift(2.05 * DOWN),
        )
        listed = [0.14159, 0.5, 0.33333, 0.41421, 0.36788, 0.71828]
        dots = VGroup(*[Dot(at(t), color=COOL, radius=0.06) for t in listed])
        # Alternating heights: x₃, x₅ and x₄ sit within 0.08 of each other.
        names = VGroup(
            *[
                Text(f"x{_sub(i + 1)}", font_size=SMALL_SIZE, color=COOL).next_to(
                    d, UP, buff=0.18 if i % 2 == 0 else 0.5
                )
                for i, d in enumerate(dots)
            ]
        )
        self.play(FadeOut(point), FadeIn(dots), FadeIn(names))
        covers = VGroup()
        eps = 0.1
        for n, t in enumerate(listed, start=1):
            w = eps / 2**n * length
            cover = Rectangle(
                width=w, height=0.24, stroke_width=0, fill_color=GOOD, fill_opacity=0.45
            )
            cover.move_to(at(t))
            covers.add(cover)
        self.play(LaggedStart(*[FadeIn(c) for c in covers], lag_ratio=0.25), run_time=1.2)
        cover_words = caption("cover x₁ by an interval of length ε/2, x₂ by ε/4, x₃ by ε/8, …")
        cover_words.move_to(0.65 * UP)
        cover_sum = MathTex(
            r"\tfrac{\varepsilon}{2} + \tfrac{\varepsilon}{4} + \tfrac{\varepsilon}{8}"
            r"+ \cdots = \varepsilon",
            font_size=36,
        )
        cover_sum.next_to(cover_words, DOWN, buff=0.2)
        cover_total = caption(
            "total length ε, for any ε — so a sequence of points has probability 0", color=GOOD
        )
        cover_total.next_to(cover_sum, DOWN, buff=0.2)
        self.play(FadeIn(cover_words))
        self.play(FadeIn(cover_sum))
        self.play(FadeIn(cover_total))
        self.wait(1.6)

        # --- the contradiction, in B&T's own words (anchor I) ----------------------------
        self.play(
            FadeOut(
                VGroup(
                    cover_words,
                    cover_sum,
                    cover_total,
                    covers,
                    dots,
                    names,
                    axiom_words,
                    axiom,
                    seq_box,
                )
            )
        )
        if_seq = MathTex(
            r"\text{if } [0,1] = \{x_1, x_2, \ldots\}:\quad P([0,1]) = 0 + 0 + \cdots = 0 \neq 1",
            font_size=38,
            color=WARM,
        )
        if_seq.move_to(0.5 * UP)
        footnote = VGroup(
            caption('"if the unit interval had a countable number of elements, with each'),
            caption("element having zero probability, the additivity axiom would imply that"),
            caption("the whole interval has zero probability, which would contradict the"),
            caption('normalization axiom" — Bertsekas & Tsitsiklis, Chapter 1'),
        ).arrange(DOWN, buff=0.12)
        footnote.next_to(if_seq, DOWN, buff=0.35)
        self.play(FadeIn(if_seq))
        self.play(FadeIn(footnote))
        why_area = Text(
            "probability is area — the interval is not a sum over points",
            font_size=LABEL_SIZE,
            color=ACCENT,
        )
        why_area.next_to(footnote, DOWN, buff=0.4)
        self.play(FadeIn(why_area))
        self.wait(1.8)

        # --- two guards ----------------------------------------------------------------------
        self.play(FadeOut(VGroup(if_seq, footnote, why_area)))
        guards = VGroup(
            caption("consistency, not existence: that length is a probability law at all"),
            caption('is B&T\'s "more advanced treatment" (Lebesgue) — this scene needed only "if"'),
            caption("and uncountable does not mean positive area — the Cantor set has length 0"),
        ).arrange(DOWN, buff=0.22)
        guards.move_to(0.3 * UP)
        for guard in guards:
            self.play(FadeIn(guard), run_time=0.6)
            self.wait(0.5)
        self.wait(1.0)
        self.play(FadeOut(VGroup(guards, line, ends)))
        _takeaway(
            self,
            "The additivity axiom is stated for sequences —\n"
            "[0, 1] is not one, and that is why probability is area",
        )


if __name__ == "__main__":
    raise SystemExit(render_cli())
