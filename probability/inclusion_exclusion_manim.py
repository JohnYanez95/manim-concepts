"""Inclusion–exclusion — the union rule, from two sets to n.

Seven scenes on the repo's own cells: the overlap counted twice on a die
strip and removed on the unit square, the per-cell ledger on the two-dice
grid that forces the three-set signs, the picture that breaks at four
sets and the two examples that share a coefficient row, the n-set formula
proved by pairing subsets, the matching problem climbing to 1 − 1/e, the
truncated sum as a bound, and the decision rule for reaching for any of it.

    TwoSetsOneOverlap       |A ∪ B| = |A| + |B| − |A ∩ B|, then as area
    ThreeSetsOneLedger      every cell stamped +1, −1, +1 — counted once
    FourSetsNoPicture       four circles make 14 regions; 4, 6, 4, 1 remain
    EveryPointCountedOnce   the n-set formula; the toggle pairing proves it
    TheMatchingLimit        1 − 1/2! + 1/3! − ⋯ → 1 − 1/e
    BracketsAndBounds       stop early and hold a bound — Boole, Bonferroni
    WhenToReachForIt        add, complement, sieve, or bound

Every number on screen is exact and machine-verified in plan 016.

Render:
    uv run python probability/inclusion_exclusion_manim.py
    uv run python probability/inclusion_exclusion_manim.py --scene TwoSetsOneOverlap --quality draft
"""

import numpy as np
from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    FORMULA_SIZE,
    GOOD,
    LABEL_SIZE,
    MUTED,
    RESULT_SIZE,
    SMALL_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    chip,
    on_frame,
    palette,
    render_cli,
)

# Sets are distinct things with no ranking between them — the categorical
# cycle, in the same assignment the independence and conditional series use,
# so "the teal region is A" stays true across the whole topic.
A_COLOR = palette(0)
B_COLOR = palette(1)
C_COLOR = palette(2)
D_COLOR = palette(3)


def _die_strip(side: float = 1.05) -> VGroup:
    """A fair die as six equal cells in a row (the sibling modules' device —
    local on purpose: topic furniture, not repo-wide vocabulary).

    Cell i is ``strip[i]``; its face number is the second submobject.
    """
    cells = VGroup()
    for face in range(1, 7):
        square = Square(side_length=side, stroke_width=2, color=MUTED)
        label = Text(str(face), font_size=LABEL_SIZE).move_to(square)
        cells.add(VGroup(square, label))
    return cells.arrange(RIGHT, buff=0)


def _tint(cell: VGroup, color: str, opacity: float = 0.35) -> None:
    cell[0].set_fill(color, opacity=opacity)


def _overlay(cells, color: str, opacity: float = 0.25) -> VGroup:
    """Translucent squares over already-tinted cells.

    A second ``set_fill`` would replace the first colour; a cell in two events
    must visibly carry both — that is the whole point of the series.
    """
    return VGroup(
        *[
            Square(
                side_length=c.width, stroke_width=0, fill_color=color, fill_opacity=opacity
            ).move_to(c)
            for c in cells
        ]
    )


def _dice_grid(cell: float = 0.48, center=(0.0, 0.0)) -> VGroup:
    """The 36 outcomes of two dice as a grid; ``grid[6 * (a - 1) + (b - 1)]``
    is first die a (rows, 1 at the top) and second die b (columns)."""
    grid = VGroup()
    for a in range(6):
        for b in range(6):
            square = Square(side_length=cell, stroke_width=1.2, color=MUTED)
            square.move_to(
                np.array([(b - 2.5) * cell + center[0], (2.5 - a) * cell + center[1], 0])
            )
            grid.add(square)
    return grid


def _cells(grid: VGroup, pairs) -> list:
    return [grid[6 * (a - 1) + (b - 1)] for a, b in pairs]


def _takeaway(scene: ConceptScene, text: str, size: int = 25) -> None:
    takeaway = Text(text, font_size=size, line_spacing=1.1).move_to(0.2 * DOWN)
    scene.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
    scene.wait(2)


class TwoSetsOneOverlap(ConceptScene):
    """Two sets: the overlap is counted twice, so subtract it once — as counts, then as area."""

    def construct(self):
        self.play(FadeIn(self.title("Two sets, one overlap"), shift=0.3 * DOWN))
        prompt = Text("A or B — is it P(A) + P(B)?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 1: count the cells ------------------------------------------
        strip = _die_strip().move_to(0.9 * UP)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in strip], lag_ratio=0.08))
        tags = VGroup(
            Text("A = even", font_size=LABEL_SIZE, color=A_COLOR),
            Text("B = at most 4", font_size=LABEL_SIZE, color=B_COLOR),
        ).arrange(RIGHT, buff=1.0)
        tags.next_to(strip, UP, buff=0.22)
        for face in (2, 4, 6):
            _tint(strip[face - 1], A_COLOR)
        self.play(FadeIn(tags[0]))
        b_over = _overlay([strip[i][0] for i in range(4)], B_COLOR)
        self.play(FadeIn(b_over), FadeIn(tags[1]))
        twice = VGroup(*[SurroundingRectangle(strip[i], color=WARM, buff=0.04) for i in (1, 3)])
        count = MathTex(
            r"|A \cup B|", r"=", r"3", r"+", r"4", r"-", r"2", r"=", r"5", font_size=RESULT_SIZE
        ).move_to(0.9 * DOWN)
        count[2].set_color(A_COLOR)
        count[4].set_color(B_COLOR)
        count[6].set_color(WARM)
        count[8].set_color(ACCENT)
        twice_note = caption("cells 2 and 4 sit in both — counted twice, subtract them once")
        twice_note.next_to(count, DOWN, buff=0.35)
        self.play(Write(count[:5]))
        self.play(Create(twice))
        self.play(Write(count[5:7]), FadeIn(twice_note))
        self.play(Write(count[7:]))
        self.wait(0.9)

        # --- the alarm: the naive sum is not even a probability ----------------
        self.play(FadeOut(VGroup(count, twice_note)))
        alarm = MathTex(
            r"P(A) + P(B) = \tfrac{1}{2} + \tfrac{2}{3} = \tfrac{7}{6}",
            r"> 1",
            font_size=RESULT_SIZE,
            color=WARM,
        ).move_to(0.9 * DOWN)
        alarm_note = caption("a probability above 1 — the sum is wrong before the picture says why")
        alarm_note.next_to(alarm, DOWN, buff=0.35)
        self.play(Write(alarm))
        self.play(FadeIn(alarm_note))
        self.wait(0.9)

        # --- level 2: the same rule as area --------------------------------------
        self.play(FadeOut(VGroup(strip, tags, b_over, twice, alarm, alarm_note, prompt)))
        side = 3.0
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.7 * LEFT + 0.3 * DOWN
        )
        a_band = Rectangle(
            width=side * 0.5, height=side, stroke_width=0, fill_color=A_COLOR, fill_opacity=0.35
        ).align_to(square, DL)
        b_band = Rectangle(
            width=side, height=side * 2 / 3, stroke_width=0, fill_color=B_COLOR, fill_opacity=0.3
        ).align_to(square, DL)
        overlap = Rectangle(
            width=side * 0.5,
            height=side * 2 / 3,
            stroke_width=3,
            color=WARM,
            fill_color=WARM,
            fill_opacity=0.45,
        ).align_to(square, DL)
        a_lab = MathTex(r"P(A) = \tfrac{1}{2}", font_size=30, color=A_COLOR)
        a_lab.next_to(a_band, UP, buff=0.15)
        b_lab = MathTex(r"P(B) = \tfrac{2}{3}", font_size=30, color=B_COLOR)
        b_lab.next_to(b_band, LEFT, buff=0.2)
        formula = MathTex(
            r"P(A \cup B)", r"=", r"P(A)", r"+", r"P(B)", r"-", r"P(A \cap B)", font_size=40
        ).move_to(2.9 * RIGHT + 0.7 * UP)
        formula[2].set_color(A_COLOR)
        formula[4].set_color(B_COLOR)
        formula[6].set_color(WARM)
        numbers = MathTex(
            r"= \tfrac{1}{2} + \tfrac{2}{3} - \tfrac{1}{3}", r"= \tfrac{5}{6}", font_size=40
        ).next_to(formula, DOWN, buff=0.45)
        numbers[1].set_color(ACCENT)
        area_note = caption("under both bands —\ncounted twice, removed once")
        area_note.next_to(numbers, DOWN, buff=0.45)
        self.play(Create(square))
        self.play(FadeIn(a_band), FadeIn(a_lab), Write(formula[:3]))
        self.play(FadeIn(b_band), FadeIn(b_lab), Write(formula[3:5]))
        self.play(FadeIn(overlap), Write(formula[5:]), FadeIn(area_note))
        self.wait(0.5)
        # "removed once" is a claim the picture must perform, not just caption.
        self.play(FadeOut(overlap), run_time=0.7)
        self.play(Write(numbers))
        self.wait(1.0)

        # --- level 3: the three readings of the overlap --------------------------
        stage = VGroup(square, a_band, b_band, a_lab, b_lab, formula, numbers, area_note)
        self.play(FadeOut(stage))
        rows = VGroup(
            VGroup(
                Text("disjoint — {1, 2} and {5, 6}", font_size=SMALL_SIZE, color=GOOD),
                MathTex(r"\tfrac{2}{6} + \tfrac{2}{6} = \tfrac{4}{6}", font_size=32),
                caption("no overlap: the sum is exact"),
            ),
            VGroup(
                Text("independent — this pair is", font_size=SMALL_SIZE, color=COOL),
                MathTex(
                    r"\tfrac{1}{3} = \tfrac{1}{2}\cdot\tfrac{2}{3}, \quad "
                    r"P(A \cup B) = 1 - \tfrac{1}{2}\cdot\tfrac{1}{3} = \tfrac{5}{6}",
                    font_size=32,
                ),
                caption("the overlap is a product; the complement route agrees"),
            ),
            VGroup(
                Text("exactly one, not at least one — {1, 3, 6}", font_size=SMALL_SIZE, color=WARM),
                MathTex(
                    r"\tfrac{1}{2} + \tfrac{2}{3} - 2\cdot\tfrac{1}{3} = \tfrac{1}{2}", font_size=32
                ),
                caption("the overlap subtracted twice, not once"),
            ),
        )
        for row in rows:
            row.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(LEFT, buff=0.9).shift(0.2 * DOWN)
        for row in rows:
            self.play(FadeIn(row, shift=0.2 * RIGHT), run_time=0.7)
            self.wait(0.5)
        # The headline misconception, answered in one line: disjoint and
        # independent are not the same thing — they are the two ends of the
        # overlap (NotMutualExclusivity drew the same two ends as a step).
        ends = caption(
            "disjoint and independent are the two ends of the overlap —\n"
            "zero, or a product; never the same thing"
        ).move_to(2.75 * DOWN)
        self.play(FadeIn(ends))
        self.wait(1.0)

        # --- the two-dice closer: one cell carries both sixes --------------------
        self.play(FadeOut(VGroup(rows, ends)))
        grid = _dice_grid(cell=0.42, center=(-3.4, -0.2))
        for c in grid[30:36]:
            c.set_fill(A_COLOR, opacity=0.35)
        col_over = _overlay([grid[6 * r + 5] for r in range(6)], B_COLOR)
        row_note = Text("first die 6", font_size=SMALL_SIZE, color=A_COLOR)
        row_note.next_to(grid[30], LEFT, buff=0.3)
        col_note = Text("second die 6", font_size=SMALL_SIZE, color=B_COLOR)
        col_note.next_to(grid[5], UP, buff=0.2)
        both = SurroundingRectangle(grid[35], color=WARM, buff=0.03)
        two = MathTex(
            r"\tfrac{6}{36} + \tfrac{6}{36} - \tfrac{1}{36}", r"= \tfrac{11}{36}", font_size=40
        ).move_to(2.8 * RIGHT + 0.4 * UP)
        two[1].set_color(ACCENT)
        two_note = caption("12/36 is the overcount, not the answer —\none cell carries both sixes")
        two_note.next_to(two, DOWN, buff=0.4)
        self.play(FadeIn(grid, lag_ratio=0.005, run_time=1.0), FadeIn(row_note), FadeIn(col_note))
        self.play(FadeIn(col_over), Create(both))
        self.play(Write(two), FadeIn(two_note))
        self.wait(1.0)

        self.play(FadeOut(VGroup(grid, col_over, row_note, col_note, both, two, two_note)))
        rule = MathTex(
            r"P(A \cup B) = P(A) + P(B) - P(A \cap B)", font_size=FORMULA_SIZE, color=ACCENT
        ).move_to(0.4 * UP)
        gloss = caption("counted twice, subtracted once — the sum rule, the product rule's sibling")
        gloss.next_to(rule, DOWN, buff=0.5)
        self.play(Write(rule), Create(boxed(rule, buff=0.35)))
        self.play(FadeIn(gloss))
        self.wait(2)


class ThreeSetsOneLedger(ConceptScene):
    """Three sets: stamp every cell as the terms arrive — the signs are forced by counting once."""

    def construct(self):
        self.play(FadeIn(self.title("Three sets, one ledger"), shift=0.3 * DOWN))

        # --- level 1: three events on the two-dice grid ---------------------------
        grid = _dice_grid(cell=0.48, center=(-2.3, 0.3))
        a_cells = list(grid[30:36])
        b_cells = [grid[6 * r + 5] for r in range(6)]
        c_pairs = [(4, 6), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)]
        c_cells = _cells(grid, c_pairs)
        a_tag = Text("A: first die 6", font_size=SMALL_SIZE, color=A_COLOR)
        a_tag.next_to(grid[30], LEFT, buff=0.3)
        b_tag = Text("B: second die 6", font_size=SMALL_SIZE, color=B_COLOR)
        b_tag.next_to(grid[5], UP, buff=0.2)
        c_tag = Text("C: sum ≥ 10", font_size=SMALL_SIZE, color=C_COLOR)
        c_tag.next_to(grid, DOWN, buff=0.25)
        self.play(FadeIn(grid, lag_ratio=0.005, run_time=1.0))
        self.play(*[c.animate.set_fill(A_COLOR, opacity=0.35) for c in a_cells], FadeIn(a_tag))
        b_over = _overlay(b_cells, B_COLOR)
        self.play(FadeIn(b_over), FadeIn(b_tag))
        c_over = _overlay(c_cells, C_COLOR)
        self.play(FadeIn(c_over), FadeIn(c_tag))
        answer = MathTex(
            r"P(A \cup B \cup C) = \tfrac{12}{36} = \tfrac{1}{3}", font_size=38, color=ACCENT
        ).move_to(3.2 * RIGHT + 1.7 * UP)
        answer_note = caption("count them: 12 cells — the answer, this time")
        answer_note.next_to(answer, DOWN, buff=0.3)
        self.play(Write(answer), FadeIn(answer_note))
        self.wait(0.8)

        # --- level 2: the ledger ----------------------------------------------------
        union = {6 * (a - 1) + (b - 1) for a, b in c_pairs}
        union |= set(range(30, 36)) | {6 * r + 5 for r in range(6)}
        values = dict.fromkeys(union, 0)
        stamps = {}
        steps = [
            (r"+\,P(A)", [30, 31, 32, 33, 34, 35], +1),
            (r"+\,P(B)", [5, 11, 17, 23, 29, 35], +1),
            (r"+\,P(C)", [23, 28, 29, 33, 34, 35], +1),
            (r"-\,P(A \cap B)", [35], -1),
            (r"-\,P(A \cap C)", [33, 34, 35], -1),
            (r"-\,P(B \cap C)", [23, 29, 35], -1),
            (r"+\,P(A \cap B \cap C)", [35], +1),
        ]
        terms = MathTex(
            r"\tfrac{6}{36}",
            r"+\tfrac{6}{36}",
            r"+\tfrac{6}{36}",
            r"-\tfrac{1}{36}",
            r"-\tfrac{3}{36}",
            r"-\tfrac{3}{36}",
            r"+\tfrac{1}{36}",
            r"= \tfrac{12}{36}",
            font_size=34,
        ).move_to(2.45 * DOWN)
        for i in range(3, 6):
            terms[i].set_color(WARM)
        terms[7].set_color(ACCENT)
        ledger_note = caption("every cell in the union must end at 1, every cell outside at 0")
        ledger_note.move_to(3.25 * DOWN)
        zeros = VGroup(
            *[
                Text("0", font_size=18, color=MUTED).move_to(grid[c])
                for c in range(36)
                if c not in union
            ]
        )
        self.play(FadeOut(answer_note), FadeIn(ledger_note), FadeIn(zeros))
        step_label = None
        for i, (tex, cells, delta) in enumerate(steps):
            new_label = MathTex(tex, font_size=34, color=WARM if delta < 0 else MUTED)
            new_label.move_to(3.2 * RIGHT + 0.7 * UP)
            outs = [step_label] if step_label else []
            olds = [stamps[c] for c in cells if c in stamps]
            if outs or olds:
                self.play(*[FadeOut(m) for m in outs + olds], run_time=0.3)
            ins = []
            for c in cells:
                values[c] += delta
                colour = COOL if values[c] > 0 else WARM
                stamps[c] = Text(str(values[c]), font_size=18, color=colour).move_to(grid[c])
                ins.append(stamps[c])
            step_label = new_label
            self.play(FadeIn(step_label), *[FadeIn(s) for s in ins], Write(terms[i]), run_time=0.6)
            if i == 5:
                gone = caption("(6, 6) reads 0 — it has vanished\nfrom a union it belongs to")
                gone.move_to(3.2 * RIGHT + 0.4 * DOWN)
                flash = SurroundingRectangle(grid[35], color=WARM, buff=0.03)
                self.play(Create(flash), FadeIn(gone))
                self.wait(0.9)
                self.play(FadeOut(gone), FadeOut(flash), run_time=0.3)
            elif i == 6:
                stamps[35].set_color(GOOD)
                back = caption(
                    "the last term is the only one that knows\nabout the centre — add it back"
                )
                back.move_to(3.2 * RIGHT + 0.4 * DOWN)
                self.play(FadeIn(back))
            else:
                self.wait(0.35)
        self.play(Write(terms[7]))
        empty = caption("A∩B without C is empty — a region that costs the formula nothing")
        self.play(FadeOut(ledger_note), run_time=0.3)
        empty.move_to(3.25 * DOWN)
        self.play(FadeIn(empty))
        self.wait(1.0)

        # --- Bernstein's coins: an empty centre, and the licence ------------------
        self.play(
            FadeOut(
                VGroup(
                    grid,
                    b_over,
                    c_over,
                    a_tag,
                    b_tag,
                    c_tag,
                    answer,
                    terms,
                    empty,
                    step_label,
                    back,
                    zeros,
                    *stamps.values(),
                )
            )
        )
        outcomes = [["HH", "HT"], ["TH", "TT"]]
        cells = VGroup()
        for r in range(2):
            for c in range(2):
                square = Square(side_length=1.35, stroke_width=2, color=MUTED)
                square.move_to(np.array([(c - 0.5) * 1.35 - 2.8, (0.5 - r) * 1.35 + 0.3, 0]))
                label = Text(outcomes[r][c], font_size=BODY_SIZE).move_to(square)
                cells.add(VGroup(square, label))
        for i in (0, 1):
            _tint(cells[i], A_COLOR, 0.25)
        b_coin = _overlay([cells[i][0] for i in (0, 2)], B_COLOR)
        c_coin = _overlay([cells[i][0] for i in (1, 2)], C_COLOR)
        a_coin_tag = Text("A: first H", font_size=LABEL_SIZE, color=A_COLOR)
        a_coin_tag.next_to(cells[0], LEFT, buff=0.4)
        b_coin_tag = Text("B: second H", font_size=LABEL_SIZE, color=B_COLOR)
        b_coin_tag.next_to(VGroup(cells[0], cells[2]), UP, buff=0.25)  # the left column IS B
        c_coin_tag = Text("C: exactly one head", font_size=LABEL_SIZE, color=C_COLOR)
        c_coin_tag.next_to(VGroup(cells[2], cells[3]), DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.1))
        self.play(FadeIn(a_coin_tag), FadeIn(b_coin), FadeIn(b_coin_tag))
        self.play(FadeIn(c_coin), FadeIn(c_coin_tag))
        bern = MathTex(
            r"\tfrac{1}{2} + \tfrac{1}{2} + \tfrac{1}{2}",
            r"- \tfrac{1}{4} - \tfrac{1}{4} - \tfrac{1}{4}",
            r"+ \, 0",
            r"= \tfrac{3}{4}",
            font_size=36,
        ).move_to(3.0 * RIGHT + 1.3 * UP)
        bern[1].set_color(WARM)
        bern[3].set_color(ACCENT)
        bern_note = caption(
            "no outcome is in all three — the centre is empty,\nand the formula does not mind"
        )
        bern_note.next_to(bern, DOWN, buff=0.35)
        self.play(Write(bern), FadeIn(bern_note))
        self.wait(0.9)
        shortcut = MathTex(
            r"1 - \left(\tfrac{1}{2}\right)^3 = \tfrac{7}{8}", r"\neq \tfrac{3}{4}", font_size=36
        ).next_to(bern_note, DOWN, buff=0.5)
        shortcut[1].set_color(WARM)
        licence = caption(
            "every pair term was a product; the triple was not —\n"
            "the error 1/8 is exactly the missing product;\n"
            "'multiply the complements' needs mutual independence"
        ).next_to(shortcut, DOWN, buff=0.3)
        self.play(Write(shortcut))
        self.play(FadeIn(licence))
        self.wait(1.2)

        self.play(
            FadeOut(
                VGroup(
                    cells,
                    b_coin,
                    c_coin,
                    a_coin_tag,
                    b_coin_tag,
                    c_coin_tag,
                    bern,
                    bern_note,
                    shortcut,
                    licence,
                )
            )
        )
        rule = MathTex(
            r"P(A \cup B \cup C) = \sum_i P(A_i) - \sum_{i<j} P(A_i \cap A_j) + P(A \cap B \cap C)",
            font_size=44,
            color=ACCENT,
        ).move_to(0.4 * UP)
        gloss = caption("every cell counted once: +1 per set, −1 per pair, +1 for the triple")
        gloss.next_to(rule, DOWN, buff=0.5)
        self.play(Write(rule), Create(boxed(rule, buff=0.35)))
        self.play(FadeIn(gloss))
        self.wait(2)


# Region centroids of the symmetric four-circle flower (centres (±d, ±d),
# radius r, with r/d = 12/7), sampled at build time — see plan 016 phase 2.
# Thirteen inside regions plus the outside make 14; the two "opposite pairs
# only" regions do not exist. Coordinates are in units of d.
_CIRCLE_REGIONS = [
    (-1.54, 1.54),
    (1.54, 1.54),
    (1.54, -1.54),
    (-1.54, -1.54),
    (0.0, 1.31),
    (1.31, 0.0),
    (0.0, -1.31),
    (-1.31, 0.0),
    (0.39, 0.39),
    (-0.39, 0.39),
    (-0.39, -0.39),
    (0.39, -0.39),
    (0.0, 0.0),
]


class FourSetsNoPicture(ConceptScene):
    """Four sets: circles stop at 14 regions — the ledger takes over, two examples share one row."""

    def construct(self):
        self.play(FadeIn(self.title("Four sets, no picture"), shift=0.3 * DOWN))
        prompt = Text("Draw four overlapping circles and count the regions", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 1: the picture breaks ------------------------------------------
        d, r = 1.05, 1.05 * 12 / 7
        centre = np.array([-3.7, -0.75, 0])
        circles = VGroup(
            *[
                Circle(radius=r, color=col, stroke_width=3).move_to(
                    centre + np.array([sx * d, sy * d, 0])
                )
                for (sx, sy), col in zip(
                    [(-1, 1), (1, 1), (1, -1), (-1, -1)],
                    [A_COLOR, B_COLOR, C_COLOR, D_COLOR],
                    strict=True,
                )
            ]
        )
        self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio=0.2))
        numbers = VGroup(
            *[
                Text(str(i + 1), font_size=16 if i < 8 else 12, color=MUTED).move_to(
                    centre + np.array([x * d, y * d, 0])
                )
                for i, (x, y) in enumerate(_CIRCLE_REGIONS)
            ]
        )
        self.play(LaggedStart(*[FadeIn(n) for n in numbers], lag_ratio=0.08, run_time=1.6))
        tally = VGroup(
            Text("13 inside + the outside = 14 regions", font_size=BODY_SIZE),
            MathTex(r"2^4 = 16 \text{ needed}", font_size=40, color=WARM),
            caption(
                "the two missing: opposite pairs only —\nin A and C but not B or D, and the mirror"
            ),
        ).arrange(DOWN, buff=0.3)
        tally.move_to(3.3 * RIGHT + 0.9 * UP)
        for part in tally:
            self.play(FadeIn(part))
        self.wait(0.6)
        venn = caption(
            "“four circles cannot be so drawn as to intersect\n"
            "one another in the way required” — Venn, 1881"
        ).move_to(3.3 * RIGHT + 1.5 * DOWN)
        self.play(FadeIn(venn))
        self.wait(1.0)

        # --- Venn's own fix, as a still: four ellipses, sixteen regions ------------
        self.play(FadeOut(VGroup(circles, numbers, tally)))
        s = 0.72
        ellipses = VGroup(
            *[
                Ellipse(width=6.0 * s, height=2.6 * s, color=col, stroke_width=3)
                .rotate(np.deg2rad(ang))
                .move_to(centre + np.array([cx * s, cy * s, 0]))
                for (cx, cy, ang), col in zip(
                    [(-0.7, 0.0, 35), (0.7, 0.0, -35), (-1.4, 0.5, 35), (1.4, 0.5, -35)],
                    [A_COLOR, B_COLOR, C_COLOR, D_COLOR],
                    strict=True,
                )
            ]
        )
        fix = VGroup(
            Text("four ellipses: all 16 — Venn's own fix", font_size=BODY_SIZE),
            caption(
                "Venn stopped at four; five took\n"
                "Grünbaum (1975) — and never area-true:\n"
                "the grid was, so the ledger stays"
            ),
        ).arrange(DOWN, buff=0.3)
        fix.move_to(3.3 * RIGHT + 0.9 * UP)
        self.play(LaggedStart(*[Create(e) for e in ellipses], lag_ratio=0.2))
        self.play(FadeIn(fix))
        self.wait(1.2)

        # --- level 2: four hats — dependent events, counted -------------------------
        self.play(FadeOut(VGroup(ellipses, fix, venn, prompt)))
        hats_prompt = Text(
            "Four hats handed back at random — someone gets their own?", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(hats_prompt))
        perms = [
            "1234", "1243", "1324", "1342", "1423", "1432",
            "2134", "2143", "2314", "2341", "2413", "2431",
            "3124", "3142", "3214", "3241", "3412", "3421",
            "4123", "4132", "4213", "4231", "4312", "4321",
        ]  # fmt: skip
        derangements = {"2143", "2341", "2413", "3142", "3412", "3421", "4123", "4312", "4321"}
        chips = VGroup(
            *[chip(p, GOOD if p in derangements else MUTED, width=0.95, height=0.5) for p in perms]
        )
        chips.arrange_in_grid(rows=4, cols=6, buff=0.14).move_to(0.75 * UP)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.03, run_time=1.6))
        chips_note = caption("9 derangements (no hat home) — 15 of 24 keep at least one match")
        chips_note.next_to(chips, DOWN, buff=0.3)
        self.play(FadeIn(chips_note))
        hats = MathTex(
            r"4\cdot\tfrac{1}{4}",
            r"- 6\cdot\tfrac{1}{12}",
            r"+ 4\cdot\tfrac{1}{24}",
            r"- 1\cdot\tfrac{1}{24}",
            r"= \tfrac{15}{24}",
            font_size=38,
        ).move_to(1.85 * DOWN)
        hats[4].set_color(ACCENT)
        hats_note = caption("each term C(4,k)·(4−k)!/4! — dependent events, no product anywhere")
        hats_note.next_to(hats, DOWN, buff=0.3)
        self.play(Write(hats))
        self.play(FadeIn(hats_note))
        self.wait(1.0)

        # --- the rolls beside the hats: one coefficient row ----------------------------
        self.play(FadeOut(VGroup(chips, chips_note, hats_note, hats_prompt)))
        rolls_prompt = Text(
            "Four rolls of a die — at least one six? (de Méré's bet)", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(rolls_prompt))
        hats_head = Text("four hats", font_size=SMALL_SIZE, color=MUTED)
        rolls_head = Text("four rolls", font_size=SMALL_SIZE, color=MUTED)
        rolls = MathTex(
            r"4\cdot\tfrac{1}{6}",
            r"- 6\cdot\tfrac{1}{36}",
            r"+ 4\cdot\tfrac{1}{216}",
            r"- 1\cdot\tfrac{1}{1296}",
            r"= \tfrac{671}{1296}",
            font_size=38,
        )
        rolls[4].set_color(ACCENT)
        self.play(hats.animate.move_to(1.45 * UP), run_time=0.7)
        hats_head.next_to(hats, LEFT, buff=0.5)
        rolls.move_to(0.45 * UP)
        rolls_head.next_to(rolls, LEFT, buff=0.5)
        self.play(FadeIn(hats_head), Write(rolls), FadeIn(rolls_head))
        for tex in (hats, rolls):
            for i in range(4):
                tex[i][0 if i == 0 else 1].set_color(ACCENT)
        self.play(
            *[
                Indicate(tex[i][0 if i == 0 else 1], color=ACCENT)
                for tex in (hats, rolls)
                for i in range(4)
            ]
        )
        row_note = VGroup(
            Text(
                "the same row both times: 4, 6, 4, 1 — the sorted square's columns",
                font_size=SMALL_SIZE,
            ),
            MathTex(r"4 - 6 + 4 - 1 = 1", font_size=34, color=GOOD),
            caption("any outcome in all four events is counted once — the ledger, unchanged"),
        ).arrange(DOWN, buff=0.25)
        row_note.move_to(0.9 * DOWN)
        for part in row_note:
            self.play(FadeIn(part))
        self.wait(1.0)
        which = caption(
            "rolls: p_k = (1/6)^k, and 1 − (5/6)⁴ says the same in one line — independent only;\n"
            "hats: p_k = (4 − k)!/4!, and no shortcut exists"
        ).move_to(2.6 * DOWN)
        self.play(FadeIn(which))
        self.wait(1.2)

        # --- level 3: the symmetric collapse ---------------------------------------------
        self.play(
            FadeOut(VGroup(hats, rolls, hats_head, rolls_head, row_note, which, rolls_prompt))
        )
        rule = MathTex(
            r"P\Big(\bigcup_{i=1}^{n} A_i\Big) = \sum_{k=1}^{n} (-1)^{k+1} \binom{n}{k}\, p_k",
            font_size=FORMULA_SIZE,
            color=ACCENT,
        ).move_to(0.4 * UP)
        gloss = caption(
            "when every k-fold intersection has the same probability p_k —\n"
            "the coefficients are Pascal's row, and n stops being frightening"
        ).next_to(rule, DOWN, buff=0.5)
        self.play(Write(rule), Create(boxed(rule, buff=0.35)))
        self.play(FadeIn(gloss))
        self.wait(2)


def _subset_chip(members, color):
    label = "{" + ",".join(str(m) for m in members) + "}"
    return chip(label, color, width=0.5 + 0.28 * len(members), height=0.5)


class EveryPointCountedOnce(ConceptScene):
    """The n-set formula, and why the signs alternate: pair the subsets and one survivor remains."""

    def construct(self):
        self.play(FadeIn(self.title("Every point counted once"), shift=0.3 * DOWN))

        # --- level 1: the formula for n sets --------------------------------------------
        formula = MathTex(
            r"P\Big(\bigcup_{i=1}^{n} A_i\Big) = \sum_{k=1}^{n} (-1)^{k+1} "
            r"\sum_{|S| = k} P\Big(\bigcap_{i \in S} A_i\Big)",
            font_size=44,
            color=ACCENT,
        ).move_to(1.7 * UP)
        terms_note = caption("one term per non-empty S: 2ⁿ − 1 of them — 1, 3, 7, 15, …")
        terms_note.next_to(formula, DOWN, buff=0.35)
        self.play(Write(formula))
        self.play(FadeIn(terms_note))
        self.wait(0.8)

        # --- level 2: one point, counted -------------------------------------------------
        ask = Text(
            "Take one outcome that lies in exactly k of the sets. How often is it counted?",
            font_size=BODY_SIZE,
        ).move_to(0.1 * DOWN)
        ledger3 = MathTex(
            r"k = 3: \quad \binom{3}{1} - \binom{3}{2} + \binom{3}{3} = 3 - 3 + 1 = 1",
            font_size=40,
        ).next_to(ask, DOWN, buff=0.45)
        ledger_note = caption(
            "once per set it is in, minus once per pair, plus once for the triple"
        )
        ledger_note.next_to(ledger3, DOWN, buff=0.3)
        self.play(FadeIn(ask))
        self.play(Write(ledger3), FadeIn(ledger_note))
        self.wait(0.9)

        # --- the pairing: why the alternating sum is 1, with no binomial theorem ----------
        self.play(FadeOut(VGroup(formula, terms_note, ask, ledger3, ledger_note)))
        heads = VGroup(
            Text("+ odd-size subsets", font_size=SMALL_SIZE, color=COOL),
            Text("− even-size subsets", font_size=SMALL_SIZE, color=WARM),
        )
        heads[0].move_to(2.0 * LEFT + 2.3 * UP)
        heads[1].move_to(2.0 * RIGHT + 2.3 * UP)
        left = [(1,), (2,), (3,), (1, 2, 3)]
        right = [None, (1, 2), (1, 3), (2, 3)]
        left_chips = VGroup(*[_subset_chip(m, COOL) for m in left])
        right_chips = VGroup(*[_subset_chip(m, WARM) for m in right if m])
        for i, c in enumerate(left_chips):
            c.move_to(2.0 * LEFT + (1.5 - 0.75 * i) * UP)
        for i, c in enumerate(right_chips):
            c.move_to(2.0 * RIGHT + (1.5 - 0.75 * (i + 1)) * UP)
        self.play(FadeIn(heads), LaggedStart(*[FadeIn(c) for c in left_chips], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(c) for c in right_chips], lag_ratio=0.1))
        toggle = Text(
            "toggle 1: S ↔ S △ {1} flips the size's parity — and the sign", font_size=SMALL_SIZE
        )
        toggle.move_to(1.95 * DOWN)
        self.play(FadeIn(toggle))
        links = VGroup(
            *[
                Line(
                    left_chips[i].get_right(),
                    right_chips[i - 1].get_left(),
                    color=WARM,
                    stroke_width=3,
                )
                for i in (1, 2, 3)
            ]
        )
        self.play(LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.25))
        self.play(
            *[c.animate.set_opacity(0.35) for c in list(left_chips[1:]) + list(right_chips)],
            run_time=0.7,
        )
        survivor = SurroundingRectangle(left_chips[0], color=GOOD, buff=0.08)
        survive_note = VGroup(
            Text("every subset has a partner across the sign — except {1}", font_size=SMALL_SIZE),
            MathTex(r"3 - 3 + 1 = 1", font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.2)
        survive_note.move_to(2.85 * DOWN)
        self.play(Create(survivor), FadeOut(toggle), run_time=0.5)
        self.play(FadeIn(survive_note))
        self.wait(1.2)

        # --- k = 4, in one line; the partial sums as counts ----------------------------------
        self.play(FadeOut(VGroup(heads, left_chips, right_chips, links, survivor, survive_note)))
        four = VGroup(
            Text("k = 4: seven pairs, one survivor", font_size=BODY_SIZE),
            MathTex(
                r"\{2\}\leftrightarrow\{1,2\}\quad \{3\}\leftrightarrow\{1,3\}\quad "
                r"\{4\}\leftrightarrow\{1,4\}\quad \{2,3\}\leftrightarrow\{1,2,3\}",
                font_size=30,
                color=MUTED,
            ),
            MathTex(
                r"\{2,4\}\leftrightarrow\{1,2,4\}\quad \{3,4\}\leftrightarrow\{1,3,4\}\quad "
                r"\{2,3,4\}\leftrightarrow\{1,2,3,4\}",
                font_size=30,
                color=MUTED,
            ),
            MathTex(r"4 - 6 + 4 - 1 = 1", font_size=40, color=GOOD),
            caption(
                "running count 4, −2, 2, 1 — counts, not probabilities; "
                "that sign pattern returns as a bound"
            ),
        ).arrange(DOWN, buff=0.35)
        four.move_to(0.5 * UP)
        for part in four:
            self.play(FadeIn(part), run_time=0.6)
        self.wait(1.0)

        # --- level 3: the two roads not taken, named ---------------------------------------------
        self.play(FadeOut(four))
        pointers = VGroup(
            caption(
                "(1 − 1)^k = 0 says the same thing — "
                "that is the binomial theorem, queued in combinatorics/"
            ),
            caption(
                "indicators do it too: 1 − ∏(1 − 1_A) expanded, then linearity —\n"
                "SameOutcomesAdd's, which needed no independence either"
            ),
        ).arrange(DOWN, buff=0.3)
        pointers.move_to(1.6 * DOWN)
        rule = MathTex(
            r"P\Big(\bigcup_{i=1}^{n} A_i\Big) = \sum_{k=1}^{n} (-1)^{k+1} "
            r"\sum_{|S| = k} P\Big(\bigcap_{i \in S} A_i\Big)",
            font_size=44,
            color=ACCENT,
        ).move_to(0.6 * UP)
        gloss = caption("every point of the union counted exactly once — that is all the signs do")
        gloss.next_to(rule, DOWN, buff=0.45)
        self.play(Write(rule), Create(boxed(rule, buff=0.35)))
        self.play(FadeIn(gloss))
        self.play(FadeIn(pointers))
        self.wait(2)


class TheMatchingLimit(ConceptScene):
    """n hats returned at random: the chance of a match settles at 1 − 1/e, never at 1."""

    def construct(self):
        self.play(FadeIn(self.title("The matching limit"), shift=0.3 * DOWN))
        prompt = Text(
            "n hats handed back at random — does anyone get their own?", font_size=BODY_SIZE
        )
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 1: the series ----------------------------------------------------------------
        series = MathTex(
            r"P(\text{at least one match}) = "
            r"1 - \tfrac{1}{2!} + \tfrac{1}{3!} - \cdots \pm \tfrac{1}{n!}",
            font_size=42,
            color=ACCENT,
        ).move_to(1.6 * UP)
        why = MathTex(r"\binom{n}{k} \cdot \frac{(n-k)!}{n!} = \frac{1}{k!}", font_size=36).move_to(
            0.55 * UP
        )
        why_note = caption(
            "C(n,k) equal terms, each (n−k)!/n! — the count cancels against the coefficient"
        )
        why_note.next_to(why, DOWN, buff=0.25)
        self.play(Write(series))
        self.play(Write(why), FadeIn(why_note))
        self.wait(0.9)

        # --- level 2: the values oscillate and land ----------------------------------------------
        ns = [2, 3, 4, 5, 6, 7, 8]
        vals = [0.5, 2 / 3, 5 / 8, 19 / 30, 91 / 144, 177 / 280, 3641 / 5760]
        shown = ["0.5000", "0.6667", "0.6250", "0.6333", "0.6319", "0.6321", "0.6321"]
        table = VGroup(
            VGroup(*[MathTex(f"n = {n}", font_size=26, color=MUTED) for n in ns]).arrange(
                RIGHT, buff=0.55
            ),
            VGroup(*[MathTex(s, font_size=26) for s in shown]).arrange(RIGHT, buff=0.55),
        ).arrange(DOWN, buff=0.2)
        for top, bottom in zip(table[0], table[1], strict=True):
            bottom.match_x(top)
        table.move_to(0.9 * DOWN)
        self.play(FadeOut(why), FadeOut(why_note), run_time=0.3)
        self.play(FadeIn(table))
        x0, x1, lo, hi, y_axis = -5.0, 5.0, 0.45, 0.70, 2.6

        def to_x(v):
            return x0 + (v - lo) / (hi - lo) * (x1 - x0)

        axis = Line([x0, -y_axis, 0], [x1, -y_axis, 0], color=MUTED, stroke_width=2)
        limit_x = to_x(1 - np.exp(-1))
        limit = DashedLine([limit_x, -y_axis - 0.35, 0], [limit_x, -y_axis + 0.12, 0], color=ACCENT)
        dots = VGroup(*[Dot([to_x(v), -y_axis, 0], radius=0.07, color=COOL) for v in vals])
        dot_labels = VGroup(
            *[
                Text(str(n), font_size=16, color=MUTED).next_to(dots[i], UP, buff=0.12)
                for i, n in enumerate(ns[:4])
            ]
        )
        limit_tag = MathTex(r"1 - \tfrac{1}{e}", font_size=28, color=ACCENT).move_to(
            [limit_x + 0.8, -y_axis - 0.4, 0]
        )
        self.play(Create(axis), Create(limit), FadeIn(limit_tag))
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2), FadeIn(dot_labels)
        )
        osc = caption(
            "above the limit at n = 3, below at n = 4 — never monotone;\n"
            "each error is smaller than the next term"
        )
        osc.move_to(3.5 * DOWN)
        self.play(FadeIn(osc))
        self.wait(1.2)

        # --- level 3: the limit, and the two roads to 1/e ---------------------------------------
        self.play(
            FadeOut(VGroup(table, axis, limit, limit_tag, dots, dot_labels, osc, series, prompt))
        )
        limit_line = MathTex(
            r"\longrightarrow\ 1 - \tfrac{1}{e} \approx 0.6321", font_size=RESULT_SIZE, color=ACCENT
        ).move_to(2.0 * UP)
        e_note = caption(
            "e is calculus/'s compound-interest ceiling; 1/e already appeared as the binomial's\n"
            "zero-success limit — the series Σ(−1)^k/k! = 1/e is a fact this repo has not built"
        ).next_to(limit_line, DOWN, buff=0.35)
        roads = VGroup(
            Text(
                "two roads to 1/e — no match vs. no success in n tries at 1/n", font_size=SMALL_SIZE
            ),
            MathTex(
                r"n = 4:\ \tfrac{3}{8} = 0.375 \text{ vs } "
                r"\left(1 - \tfrac{1}{4}\right)^4 = 0.3164",
                font_size=32,
            ),
            MathTex(
                r"n = 8:\ 0.3679 \text{ vs } \left(1 - \tfrac{1}{8}\right)^8 = 0.3436",
                font_size=32,
            ),
            caption(
                "same limit; one road is n independent trials, the other has no independence in it"
            ),
        ).arrange(DOWN, buff=0.25)
        roads.move_to(0.7 * DOWN)
        history = caption(
            "Montmort posed it in 1708 (the game of Treize); "
            "de Moivre stated the general case in 1718"
        ).move_to(2.75 * DOWN)
        self.play(Write(limit_line), FadeIn(e_note))
        for part in roads:
            self.play(FadeIn(part), run_time=0.6)
        self.play(FadeIn(history))
        self.wait(1.2)

        self.play(FadeOut(VGroup(limit_line, e_note, roads, history)))
        _takeaway(
            self,
            "More hats do not make a match certain —\n"
            "the probability settles at 1 − 1/e ≈ 0.6321, never at 1",
        )


class BracketsAndBounds(ConceptScene):
    """Stop the sum early and you hold a bound — upper, lower, upper — Boole and Bonferroni."""

    def construct(self):
        self.play(FadeIn(self.title("Brackets and bounds"), shift=0.3 * DOWN))
        prompt = Text("Stop the sum early — what do you hold?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- level 1: the ladder of inequalities -------------------------------------------
        ladder = VGroup(
            MathTex(r"P\Big(\bigcup A_i\Big) \le S_1", r"\quad\text{(Boole)}", font_size=36),
            MathTex(r"P\Big(\bigcup A_i\Big) \ge S_1 - S_2", font_size=36),
            MathTex(r"P\Big(\bigcup A_i\Big) \le S_1 - S_2 + S_3", font_size=36),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ladder[0][1].set_color(MUTED)
        ladder.move_to(1.0 * UP)
        ladder_note = caption("one term: an upper bound; two: lower; three: upper — and so on")
        ladder_note.next_to(ladder, DOWN, buff=0.3)
        for line in ladder:
            self.play(Write(line), run_time=0.7)
        self.play(FadeIn(ladder_note))
        self.wait(0.9)

        # --- level 2: the two four-set ladders as bars -------------------------------------
        self.play(FadeOut(VGroup(ladder, ladder_note, prompt)))
        base_y, scale, bw, gap = -2.4, 2.4, 0.5, 0.3

        def bars(values, labels, exact, cx, title):
            group = VGroup()
            n = len(values)
            for i, (v, lab) in enumerate(zip(values, labels, strict=True)):
                x = cx + (i - (n - 1) / 2) * (bw + gap)
                bar = Rectangle(
                    width=bw,
                    height=v * scale,
                    stroke_width=0,
                    fill_color=GOOD if i == n - 1 else MUTED,
                    fill_opacity=0.8,
                ).move_to([x, base_y + v * scale / 2, 0])
                tag = MathTex([r"\ge", r"\le", r"\ge", r"="][i], lab, font_size=24)
                tag[0].set_color(MUTED)
                tag.next_to(bar, DOWN, buff=0.12)
                group.add(VGroup(bar, tag))
            half = (n - 1) / 2 * (bw + gap) + bw / 2 + 0.2
            line = DashedLine(
                [cx - half, base_y + exact * scale, 0],
                [cx + half, base_y + exact * scale, 0],
                color=ACCENT,
            )
            head = Text(title, font_size=SMALL_SIZE).move_to([cx, base_y - 1.0, 0])
            return group, line, head

        hats, hats_line, hats_head = bars(
            [1, 0.5, 2 / 3, 5 / 8],
            [r"1", r"\tfrac{1}{2}", r"\tfrac{2}{3}", r"\tfrac{5}{8}"],
            5 / 8,
            -3.3,
            "four hats: exact 5/8",
        )
        rolls, rolls_line, rolls_head = bars(
            [2 / 3, 0.5, 14 / 27, 671 / 1296],
            [r"\tfrac{2}{3}", r"\tfrac{1}{2}", r"\tfrac{14}{27}", r"\tfrac{671}{1296}"],
            671 / 1296,
            3.3,
            "four rolls: exact 671/1296",
        )
        for group, line, head in ((hats, hats_line, hats_head), (rolls, rolls_line, rolls_head)):
            self.play(Create(line), FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=0.2 * UP) for g in group], lag_ratio=0.25))
        bracket_note = caption("over, under, over — and the last term lands exactly")
        bracket_note.move_to(2.45 * UP)
        self.play(FadeIn(bracket_note))
        self.wait(1.0)
        why = VGroup(
            MathTex(
                r"\sum_{j=1}^{m} (-1)^{j+1} \binom{k}{j} = 1 - (-1)^m \binom{k-1}{m}",
                font_size=32,
            ),
            caption(
                "a truncated ledger over- or under-counts every point with the sign\n"
                "of its last term kept — at k = 4 this reads 4, −2, 2, 1"
            ),
        ).arrange(DOWN, buff=0.2)
        why.move_to(2.0 * UP)
        self.play(FadeOut(bracket_note), run_time=0.3)
        self.play(FadeIn(why))
        self.wait(1.2)

        # --- level 3: where the first rung is the whole tool -------------------------------
        self.play(FadeOut(VGroup(hats, hats_line, hats_head, rolls, rolls_line, rolls_head, why)))
        rare = VGroup(
            Text("four rare events, each 0.01", font_size=BODY_SIZE),
            MathTex(
                r"P\Big(\bigcup A_i\Big) \le 4 \times 0.01 = 0.04",
                r"\qquad 1 - 0.99^4 = 0.0394 \text{ if independent}",
                font_size=34,
            ),
            caption(
                "on rare events the first rung is nearly exact — "
                "and it needs no independence at all"
            ),
        ).arrange(DOWN, buff=0.3)
        rare[1][0].set_color(ACCENT)
        rare.move_to(1.2 * UP)
        useless = VGroup(
            Text("on four hats the same rung says ≤ 1", font_size=BODY_SIZE),
            caption("honest and useless — the union bound bites only when ΣP(Aᵢ) < 1"),
            caption("Boole named the first rung; Bonferroni (1936) the whole ladder"),
        ).arrange(DOWN, buff=0.25)
        useless.move_to(1.4 * DOWN)
        for part in rare:
            self.play(FadeIn(part), run_time=0.6)
        self.wait(0.6)
        for part in useless:
            self.play(FadeIn(part), run_time=0.6)
        self.wait(1.2)

        self.play(FadeOut(VGroup(rare, useless)))
        _takeaway(
            self,
            "Stop early and you hold a bound —\nwith the sign of the first term you dropped",
        )


class WhenToReachForIt(ConceptScene):
    """Add, complement, sieve, or bound — which move an 'A or B' question needs."""

    def construct(self):
        self.play(FadeIn(self.title("When to Reach for It"), shift=0.3 * DOWN))

        # Level three: six scenes build the union rule; this one is the field
        # guide for choosing it — or choosing something cheaper.
        cases = [
            ("disjoint events — 'A or B'", "add: the sum is exact"),
            ("independent events — 'at least one'", "complement: 1 − ∏(1 − pᵢ)"),
            ("dependent but symmetric — hats, matches", "inclusion–exclusion, C(n,k)·pₖ"),
            ("many rare events — a guarantee", "the union bound, first term only"),
            ("'exactly m of n'", "the sieve (Feller IV.3) — not built here"),
        ]
        questions = VGroup(*[Text(q, font_size=20) for q, _ in cases])
        questions.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        questions.to_edge(LEFT, buff=0.7).shift(0.7 * UP)
        verdicts = VGroup(
            *[
                Text(v, font_size=20, weight=BOLD, color=MUTED if "not built" in v else ACCENT)
                for _, v in cases
            ]
        )
        verdicts.arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6)
        for question, verdict in zip(questions, verdicts, strict=True):
            verdict.match_y(question)
        start_x = questions.get_right()[0] + 0.3
        end_x = verdicts.get_left()[0] - 0.3
        arrows = VGroup(
            *[
                Arrow(
                    np.array([start_x, q.get_y(), 0]),
                    np.array([end_x, q.get_y(), 0]),
                    buff=0,
                    color=MUTED,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.18,
                )
                for q in questions
            ]
        )
        for question, arrow, verdict in zip(questions, arrows, verdicts, strict=True):
            self.play(
                FadeIn(question, shift=0.2 * RIGHT),
                GrowArrow(arrow),
                FadeIn(verdict, shift=0.2 * LEFT),
                run_time=0.8,
            )
            self.wait(0.3)
        self.wait(1.0)

        # The sieve is the same formula read as a count — the pointer the
        # combinatorics queue is owed.
        sieve = VGroup(
            Text("the same rule as a sieve — 1..30 divisible by 2, 3 or 5:", font_size=SMALL_SIZE),
            MathTex(r"15 + 10 + 6 - 5 - 3 - 2 + 1 = 22", font_size=36),
            caption("8 survivors — {1, 7, 11, 13, 17, 19, 23, 29}, Euler's φ(30)"),
        ).arrange(DOWN, buff=0.22)
        sieve.move_to(2.55 * DOWN)
        sieve[1][0][-2:].set_color(ACCENT)
        for part in sieve:
            self.play(FadeIn(part), run_time=0.7)
            self.wait(0.4)
        self.wait(1.2)

        self.play(FadeOut(VGroup(questions, arrows, verdicts, sieve)))
        last = caption(
            "Blitzstein & Hwang: try the other tools first — inclusion–exclusion is the last resort"
        )
        last.move_to(1.5 * DOWN)
        takeaway = Text(
            "Count what is there, correct what you counted twice —\n"
            "and stop when a bound is enough",
            font_size=25,
            line_spacing=1.1,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.play(FadeIn(on_frame(last)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
