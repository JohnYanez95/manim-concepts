"""Independence — when multiplying probabilities is legitimate.

Six scenes on the aligned unit square: probability as area, the product
rule as the definition of independence, the jewel example on a single die,
the mutual-exclusivity confusion, the chain over independent trials, and
the decision rule for assuming any of it.

    ProbabilityAsArea     the unit square: event = region, P = area
    TheProductRule        P(A and B) = P(A) P(B) — straight cuts
    OneDieTwoEvents       independent events on one roll; one pip flips it
    NotMutualExclusivity  disjoint means maximally dependent
    ChainsOfTrials        the product over a sequence — CTC's borrowed step
    WhenToUseIt           what installs independence, what breaks it

Every number on screen is exact and machine-verified in plan 002.

Render:
    uv run python probability/independence_manim.py
    uv run python probability/independence_manim.py --scene TheProductRule --quality draft
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
    palette,
    render_cli,
)

# Events A and B are two distinct things with no ranking between them, which
# is exactly what the categorical cycle is for. One assignment, used by every
# scene, so "the teal region is A" stays true across the whole series.
A_COLOR = palette(0)
B_COLOR = palette(1)


def _die_strip(side: float = 1.05) -> VGroup:
    """A fair die as six equal cells in a row — the sample space, drawn.

    Returns the strip; cell i is ``strip[i]`` with the face number as its
    second submobject, so scenes can tint outcomes without rebuilding it.
    """
    cells = VGroup()
    for face in range(1, 7):
        square = Square(side_length=side, stroke_width=2, color=MUTED)
        label = Text(str(face), font_size=LABEL_SIZE).move_to(square)
        cells.add(VGroup(square, label))
    return cells.arrange(RIGHT, buff=0)


def _tint(cell: VGroup, color: str, opacity: float = 0.35) -> None:
    cell[0].set_fill(color, opacity=opacity)


class ProbabilityAsArea(ConceptScene):
    """The sample space is a unit square; probability is a region's share."""

    def construct(self):
        self.play(FadeIn(self.title("Probability as Area"), shift=0.3 * DOWN))

        prompt = Text("One roll of a fair die — six outcomes, equally likely", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        strip = _die_strip().move_to(1.2 * UP)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in strip], lag_ratio=0.08))
        self.wait(0.4)

        # --- counting first, the way combinatorics left it --------------------
        for i in (1, 3, 5):  # faces 2, 4, 6
            _tint(strip[i], A_COLOR)
        even_tag = Text("A = even", font_size=LABEL_SIZE, color=A_COLOR)
        even_tag.next_to(strip, UP, buff=0.3)
        self.play(FadeIn(even_tag))
        count = MathTex(
            r"P(A) = \frac{3}{6} = \frac{1}{2}", font_size=RESULT_SIZE, color=ACCENT
        ).next_to(strip, DOWN, buff=0.55)
        origin_note = caption("count the cells, divide by the total — counting already did this")
        origin_note.next_to(count, DOWN, buff=0.3)
        self.play(Write(count))
        self.play(FadeIn(origin_note))
        self.wait(0.8)

        # --- forget the cells: region and area ---------------------------------
        self.play(FadeOut(VGroup(count, origin_note, even_tag, prompt)))
        square = Square(side_length=3.1, stroke_width=3, color=MUTED).move_to(0.85 * DOWN)
        band = Rectangle(
            width=3.1 / 2,
            height=3.1,
            stroke_width=0,
            fill_color=A_COLOR,
            fill_opacity=0.4,
        ).align_to(square, DL)
        band_tag = MathTex(r"A", font_size=44, color=A_COLOR).move_to(band)
        half = MathTex(r"\tfrac{1}{2}", font_size=36, color=ACCENT)
        half.next_to(square, RIGHT, buff=0.5)
        self.play(strip.animate.scale(0.75).to_edge(UP, buff=1.35))
        self.play(Create(square))
        self.play(FadeIn(band), FadeIn(band_tag))
        self.play(FadeIn(half, shift=0.2 * LEFT))
        self.wait(0.5)

        widen = caption("any event is a region — probability is its share of the square")
        widen.next_to(square, DOWN, buff=0.35)
        self.play(FadeIn(widen))
        self.wait(0.8)

        self.play(FadeOut(VGroup(strip, square, band, band_tag, half, widen)))
        claim = MathTex(r"P(A) = \text{area}(A)", font_size=FORMULA_SIZE, color=ACCENT)
        claim.move_to(0.3 * UP)
        gloss = caption("the math of probability is the math of proportions")
        gloss.next_to(claim, DOWN, buff=0.5)
        self.play(Write(claim), Create(boxed(claim, buff=0.35)))
        self.play(FadeIn(gloss))
        self.wait(2)


class TheProductRule(ConceptScene):
    """Independence defined: the joint probability factors, cuts run straight."""

    def construct(self):
        self.play(FadeIn(self.title("The Product Rule"), shift=0.3 * DOWN))

        prompt = Text("Two coins — four outcomes, one grid", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- the 2x2 grid ------------------------------------------------------
        outcomes = [["HH", "HT"], ["TH", "TT"]]
        cells = VGroup()
        for r in range(2):
            for c in range(2):
                square = Square(side_length=1.35, stroke_width=2, color=MUTED)
                square.move_to(np.array([(c - 0.5) * 1.35, (0.5 - r) * 1.35 + 0.55, 0]))
                label = Text(outcomes[r][c], font_size=BODY_SIZE).move_to(square)
                cells.add(VGroup(square, label))
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.1))

        a_tag = Text("A: first is H", font_size=LABEL_SIZE, color=A_COLOR)
        a_tag.next_to(cells[0], LEFT, buff=0.5).shift(0.1 * LEFT)
        b_tag = Text("B: second is H", font_size=LABEL_SIZE, color=B_COLOR)
        b_tag.next_to(VGroup(cells[0], cells[2]), UP, buff=0.3)
        for i in (0, 1):  # top row = A
            _tint(cells[i], A_COLOR, 0.25)
        self.play(FadeIn(a_tag))
        # B is an overlay rather than a second _tint: set_fill would replace
        # HH's A-colour, and the overlap cell must visibly carry both.
        b_overlay = VGroup(
            *[
                Square(
                    side_length=1.35, stroke_width=0, fill_color=B_COLOR, fill_opacity=0.25
                ).move_to(cells[i])
                for i in (0, 2)
            ]
        )
        self.play(FadeIn(b_overlay), FadeIn(b_tag))
        overlap = SurroundingRectangle(cells[0], color=ACCENT, buff=0.03)
        product = MathTex(
            r"P(A \cap B) = \tfrac{1}{4} = \tfrac{1}{2}\times\tfrac{1}{2}",
            font_size=40,
            color=ACCENT,
        ).next_to(cells, DOWN, buff=0.5)
        self.play(Create(overlap))
        self.play(Write(product))
        self.wait(0.8)

        # --- the same picture at 6x6 -------------------------------------------
        self.play(FadeOut(VGroup(cells, a_tag, b_tag, b_overlay, overlap, product, prompt)))
        grid = VGroup()
        for r in range(6):
            for c in range(6):
                square = Square(side_length=0.52, stroke_width=1.2, color=MUTED)
                square.move_to(np.array([(c - 2.5) * 0.52 - 2.6, (2.5 - r) * 0.52 + 0.3, 0]))
                grid.add(square)
        row_note = Text("first die = 6", font_size=SMALL_SIZE, color=A_COLOR)
        row_note.next_to(grid[30], LEFT, buff=0.35)
        col_note = Text("second die = 6", font_size=SMALL_SIZE, color=B_COLOR)
        col_note.next_to(grid[5], UP, buff=0.25)
        self.play(FadeIn(grid, lag_ratio=0.005, run_time=1.2))
        self.play(
            *[grid[30 + c].animate.set_fill(A_COLOR, opacity=0.35) for c in range(6)],
            FadeIn(row_note),
        )
        self.play(
            *[grid[6 * r + 5].animate.set_fill(B_COLOR, opacity=0.35) for r in range(6)],
            FadeIn(col_note),
        )
        cell_box = SurroundingRectangle(grid[35], color=ACCENT, buff=0.02)
        cell_math = (
            MathTex(r"\tfrac{1}{36} = \tfrac{1}{6}\times\tfrac{1}{6}", font_size=38, color=ACCENT)
            .next_to(grid, RIGHT, buff=1.2)
            .shift(0.9 * UP)
        )
        # Left-aligned under the equation: the note is wider than it, and
        # centring would push its left edge back over the tinted column.
        rect_note = caption("any rows × any columns:\na rectangle — width × height")
        rect_note.next_to(cell_math, DOWN, buff=0.4).align_to(cell_math, LEFT)
        self.play(Create(cell_box))
        self.play(Write(cell_math), FadeIn(rect_note))
        self.wait(0.9)

        # --- the unit square, cuts straight ------------------------------------
        self.play(FadeOut(VGroup(grid, row_note, col_note, cell_box, cell_math, rect_note)))
        side = 3.0
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.4 * LEFT + 0.15 * DOWN
        )
        corner = square.get_corner(DL)
        v_cut = Line(
            corner + np.array([side * 0.55, 0, 0]),
            corner + np.array([side * 0.55, side, 0]),
            color=A_COLOR,
            stroke_width=4,
        )
        h_cut = Line(
            corner + np.array([0, side * 0.4, 0]),
            corner + np.array([side, side * 0.4, 0]),
            color=B_COLOR,
            stroke_width=4,
        )
        joint = Rectangle(
            width=side * 0.55,
            height=side * 0.4,
            stroke_width=0,
            fill_color=ACCENT,
            fill_opacity=0.35,
        )
        joint.align_to(square, DL)
        a_lab = MathTex(r"P(A)", font_size=30, color=A_COLOR).next_to(v_cut, UP, buff=0.15)
        b_lab = MathTex(r"P(B)", font_size=30, color=B_COLOR).next_to(h_cut, LEFT, buff=0.2)
        straight = Text(
            "both cuts run straight across —\nthat is what independence looks like",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.8)
        self.play(Create(square))
        self.play(Create(v_cut), FadeIn(a_lab))
        self.play(Create(h_cut), FadeIn(b_lab))
        self.play(FadeIn(joint))
        self.play(FadeIn(straight))
        self.wait(0.9)

        stage = VGroup(square, v_cut, h_cut, joint, a_lab, b_lab, straight)
        self.play(FadeOut(stage))
        definition = MathTex(
            r"A \perp B \iff P(A \cap B) = P(A)\,P(B)",
            font_size=FORMULA_SIZE,
            color=ACCENT,
        ).move_to(0.4 * UP)
        gloss = caption("this is the definition — no conditioning required")
        gloss.next_to(definition, DOWN, buff=0.5)
        self.play(Write(definition), Create(boxed(definition, buff=0.35)))
        self.play(FadeIn(gloss))
        self.wait(2)


class OneDieTwoEvents(ConceptScene):
    """Two events on one roll can be independent — and one pip decides it."""

    def construct(self):
        self.play(FadeIn(self.title("One Die, Two Events"), shift=0.3 * DOWN))

        prompt = Text(
            "Same roll, two questions: is it even? is it at most 4?", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        strip = _die_strip().move_to(1.35 * UP)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in strip], lag_ratio=0.08))

        for i in (1, 3, 5):
            _tint(strip[i], A_COLOR)
        a_tag = Text("A = even", font_size=LABEL_SIZE, color=A_COLOR)
        a_tag.next_to(strip, UP, buff=0.28).align_to(strip, LEFT)
        self.play(FadeIn(a_tag))

        # B drawn as a bar under the strip rather than a second tint, so the
        # overlap stays legible where both events cover a cell.
        def b_bar(count: int) -> Line:
            left = strip[0][0].get_corner(DL) + 0.28 * DOWN
            right = strip[count - 1][0].get_corner(DR) + 0.28 * DOWN
            return Line(left, right, color=B_COLOR, stroke_width=7)

        bar = b_bar(4)
        b_tag = Text("B = at most 4", font_size=LABEL_SIZE, color=B_COLOR)
        b_tag.next_to(bar, DOWN, buff=0.2).align_to(strip, LEFT)
        self.play(Create(bar), FadeIn(b_tag))
        self.wait(0.4)

        check = MathTex(
            r"P(A)\,P(B)",
            r"= \tfrac{1}{2}\cdot\tfrac{2}{3} = \tfrac{1}{3}",
            r"= P(\{2,4\})\ \checkmark",
            font_size=RESULT_SIZE,
        ).move_to(0.75 * DOWN)
        check[2].set_color(GOOD)
        verdict = Text(
            "independent — two facts about the same roll", font_size=BODY_SIZE, color=GOOD
        ).next_to(check, DOWN, buff=0.4)
        self.play(Write(check))
        self.play(FadeIn(verdict))
        self.wait(1.0)

        # --- one pip decides it -------------------------------------------------
        self.play(FadeOut(check), FadeOut(verdict))
        # The bar morph is geometry — the boundary visibly sliding one pip is
        # the point. The label is text, so per motion discipline it leaves
        # before its replacement arrives rather than crossfading in place.
        new_bar = b_bar(3)
        new_tag = Text("B = at most 3", font_size=LABEL_SIZE, color=B_COLOR)
        new_tag.next_to(new_bar, DOWN, buff=0.2).align_to(strip, LEFT)
        self.play(FadeOut(b_tag), run_time=0.4)
        self.play(Transform(bar, new_bar))
        b_tag = new_tag
        self.play(FadeIn(b_tag), run_time=0.4)
        recheck = MathTex(
            r"\tfrac{1}{2}\cdot\tfrac{1}{2} = \tfrac{1}{4}",
            r"\neq \tfrac{1}{6} = P(\{2\})\ \times",
            font_size=RESULT_SIZE,
        ).move_to(0.75 * DOWN)
        recheck[1].set_color(WARM)
        new_verdict = Text("one pip flipped the verdict", font_size=BODY_SIZE, color=WARM)
        new_verdict.next_to(recheck, DOWN, buff=0.4)
        self.play(Write(recheck))
        self.play(FadeIn(new_verdict))
        self.wait(1.0)

        # --- and the measure decides it too -------------------------------------
        self.play(FadeOut(recheck), FadeOut(new_verdict))
        biased = Text(
            "bias the die (double weight on 6) and even the first pair breaks:",
            font_size=BODY_SIZE,
        ).move_to(0.55 * DOWN)
        broken = MathTex(
            r"P(A)\,P(B) = \tfrac{16}{49} \neq \tfrac{2}{7} = P(A \cap B)",
            font_size=40,
            color=WARM,
        ).next_to(biased, DOWN, buff=0.4)
        measure = caption("independence belongs to the measure, not to the events")
        measure.next_to(broken, DOWN, buff=0.35)
        self.play(FadeIn(biased))
        self.play(Write(broken))
        self.play(FadeIn(measure))
        self.wait(1.0)

        self.play(FadeOut(VGroup(strip, a_tag, bar, b_tag, prompt, biased, broken, measure)))
        takeaway = Text(
            "Check independence by multiplying — mechanism tells you nothing",
            font_size=26,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class NotMutualExclusivity(ConceptScene):
    """Mutually exclusive events are not independent; they are maximally dependent."""

    def construct(self):
        self.play(FadeIn(self.title("Not Mutual Exclusivity"), shift=0.3 * DOWN))

        prompt = Text(
            "Even and odd can never happen together. Unrelated, then?", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        strip = _die_strip().move_to(1.35 * UP)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in strip], lag_ratio=0.08))
        for i in (1, 3, 5):
            _tint(strip[i], A_COLOR)
        for i in (0, 2, 4):
            _tint(strip[i], B_COLOR)
        tags = VGroup(
            Text("A = even", font_size=LABEL_SIZE, color=A_COLOR),
            Text("B = odd", font_size=LABEL_SIZE, color=B_COLOR),
        ).arrange(RIGHT, buff=1.0)
        tags.next_to(strip, UP, buff=0.28)
        self.play(FadeIn(tags))
        self.wait(0.4)

        test = MathTex(
            r"P(A \cap B) = 0",
            r"\qquad P(A)\,P(B) = \tfrac{1}{4}",
            font_size=RESULT_SIZE,
        ).move_to(0.35 * DOWN)
        fails = Text(
            "0 ≠ 1/4 — the product test fails as loudly as possible",
            font_size=BODY_SIZE,
            color=WARM,
        ).next_to(test, DOWN, buff=0.4)
        info = Text(
            "seeing one happen tells you the other did not: maximal information, not none",
            font_size=SMALL_SIZE,
        ).next_to(fails, DOWN, buff=0.35)
        self.play(Write(test))
        self.play(FadeIn(fails))
        self.play(FadeIn(info))
        self.wait(1.0)

        # --- the broken square --------------------------------------------------
        self.play(FadeOut(VGroup(strip, tags, prompt, test, fails, info)))
        side = 2.9
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.5 * LEFT + 0.35 * DOWN
        )
        corner = square.get_corner(DL)
        x_cut = side * 0.5

        def b_region(left_h: float, right_h: float) -> VGroup:
            left = Rectangle(
                width=x_cut,
                height=side * left_h,
                stroke_width=0,
                fill_color=B_COLOR,
                fill_opacity=0.4,
            )
            left.align_to(square, DL)
            right = Rectangle(
                width=side - x_cut,
                height=side * right_h,
                stroke_width=0,
                fill_color=B_COLOR,
                fill_opacity=0.4,
            )
            right.next_to(left, RIGHT, buff=0, aligned_edge=DOWN)
            return VGroup(left, right)

        v_cut = Line(
            corner + np.array([x_cut, 0, 0]),
            corner + np.array([x_cut, side, 0]),
            color=A_COLOR,
            stroke_width=4,
        )
        region = b_region(0.62, 0.25)
        step_note = Text(
            "dependence: B's share differs\ninside A and outside it",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.8)
        self.play(Create(square), Create(v_cut))
        self.play(FadeIn(region), FadeIn(step_note))
        self.wait(0.8)

        flat_note = Text(
            "independence: the knife-edge\nwhere the cut runs straight",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.8)
        self.play(Transform(region, b_region(0.4, 0.4)), FadeOut(step_note))
        self.play(FadeIn(flat_note))
        self.wait(0.8)

        slam_note = Text(
            "disjoint: the step at its\nmost extreme — zero inside A",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.8)
        self.play(Transform(region, b_region(0.001, 0.75)), FadeOut(flat_note))
        self.play(FadeIn(slam_note))
        self.wait(1.0)

        self.play(FadeOut(VGroup(square, v_cut, region, slam_note)))
        takeaway = Text(
            "Mutually exclusive means dependent — disjointness is set theory,\n"
            "independence is arithmetic about the measure",
            font_size=24,
            line_spacing=1.1,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class ChainsOfTrials(ConceptScene):
    """A sequence of independent trials multiplies — one factor per step."""

    def construct(self):
        self.play(FadeIn(self.title("Chains of Trials"), shift=0.3 * DOWN))

        prompt = Text("Flip a fair coin four times. P(HHTH)?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- the square subdividing --------------------------------------------
        side = 3.2
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.4 * LEFT + 0.35 * DOWN
        )
        self.play(Create(square))
        corner = square.get_corner(DL)

        splits = VGroup()
        split_specs = [
            # (orientation, positions as fractions) — flip k halves each cell
            ("v", [0.5]),
            ("h", [0.5]),
            ("v", [0.25, 0.75]),
            ("h", [0.25, 0.75]),
        ]
        step_labels = ["flip 1", "flip 2", "flip 3", "flip 4"]
        label = caption(step_labels[0]).next_to(square, UP, buff=0.25)
        self.play(FadeIn(label))
        for k, (orientation, positions) in enumerate(split_specs):
            new_lines = VGroup()
            for fraction in positions:
                if orientation == "v":
                    line = Line(
                        corner + np.array([side * fraction, 0, 0]),
                        corner + np.array([side * fraction, side, 0]),
                        color=COOL,
                        stroke_width=2.5,
                        stroke_opacity=0.8,
                    )
                else:
                    line = Line(
                        corner + np.array([0, side * fraction, 0]),
                        corner + np.array([side, side * fraction, 0]),
                        color=COOL,
                        stroke_width=2.5,
                        stroke_opacity=0.8,
                    )
                new_lines.add(line)
            if k > 0:
                new_label = caption(step_labels[k]).next_to(square, UP, buff=0.25)
                self.play(FadeOut(label), run_time=0.3)
                label = new_label
                self.play(FadeIn(label), Create(new_lines), run_time=0.7)
            else:
                self.play(Create(new_lines), run_time=0.7)
            splits.add(new_lines)
        self.wait(0.4)

        # HHTH: H halves left, H bottom, T right-of-pair, H bottom — one cell of
        # the 16. The exact cell is unimportant; its size is the point.
        cell = Rectangle(
            width=side * 0.25,
            height=side * 0.25,
            stroke_width=0,
            fill_color=ACCENT,
            fill_opacity=0.55,
        )
        cell.move_to(corner + np.array([side * 0.375, side * 0.125, 0]), aligned_edge=ORIGIN)
        cell_math = (
            MathTex(
                r"P(\text{HHTH}) = \left(\tfrac{1}{2}\right)^4 = \tfrac{1}{16}",
                font_size=40,
                color=ACCENT,
            )
            .next_to(square, RIGHT, buff=0.8)
            .shift(1.1 * UP)
        )
        each = caption("each flip splits every cell —\n16 cells, all equal").next_to(
            cell_math, DOWN, buff=0.35
        )
        self.play(FadeIn(cell))
        self.play(Write(cell_math), FadeIn(each))
        self.wait(0.9)

        chain = MathTex(
            r"P(A_1 \cap \cdots \cap A_n) = \prod_{i=1}^{n} P(A_i)",
            font_size=44,
            color=ACCENT,
        ).next_to(each, DOWN, buff=0.5)
        self.play(Write(chain))
        self.wait(0.8)

        # --- pairwise is not enough ---------------------------------------------
        self.play(
            FadeOut(VGroup(square, splits, cell, label, cell_math, each, prompt)),
            chain.animate.move_to(2.3 * UP).scale(0.85),
        )
        warning = Text(
            "the chain needs mutual independence — pairwise is not enough:",
            font_size=BODY_SIZE,
        ).move_to(1.1 * UP)
        bernstein = MathTex(
            r"P(A\cap B) = P(A\cap C) = P(B\cap C) = \tfrac{1}{4}",
            r"\qquad P(A\cap B\cap C) = 0 \neq \tfrac{1}{8}",
            font_size=36,
        ).move_to(0.25 * UP)
        bernstein[1].set_color(WARM)
        bern_note = caption(
            "two coins: A = first H, B = second H, C = exactly one head\n"
            "— any two of them determine the third"
        ).next_to(bernstein, DOWN, buff=0.3)
        self.play(FadeIn(warning))
        self.play(Write(bernstein))
        self.play(FadeIn(bern_note))
        self.wait(1.0)

        # --- the bridge ---------------------------------------------------------
        self.play(FadeOut(VGroup(warning, bernstein, bern_note)))
        bridge = MathTex(
            r"y_1(\pi_1)\, y_2(\pi_2)\, y_3(\pi_3)\, y_4(\pi_4)",
            font_size=44,
            color=COOL,
        ).move_to(0.35 * UP)
        bridge_note = Text(
            "the per-frame product in the CTC loss is this exact move",
            font_size=BODY_SIZE,
        ).next_to(bridge, DOWN, buff=0.4)
        honest = caption(
            "legitimate exactly when the model's measure factorizes —\n"
            "an assumption, purchased per frame"
        ).next_to(bridge_note, DOWN, buff=0.3)
        self.play(Write(bridge))
        self.play(FadeIn(bridge_note))
        self.play(FadeIn(honest))
        self.wait(2)


class WhenToUseIt(ConceptScene):
    """What installs independence, what silently breaks it, and how to tell."""

    def construct(self):
        self.play(FadeIn(self.title("When to Assume It"), shift=0.3 * DOWN))

        # Level three: the first five scenes define and stress-test the product
        # rule; this one is the field guide for assuming it outside the examples.
        cases = [
            ("Two draws, with replacement", "independent", True),
            ("Two draws, no replacement — 1/221 ≠ 1/169", "dependent", False),
            ("Heat and smoke — fire is the common cause", "dependent", False),
            ("A fair coin after five heads — no memory", "independent", True),
        ]
        questions = VGroup(*[Text(q, font_size=21) for q, _, _ in cases])
        questions.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        questions.to_edge(LEFT, buff=0.8).shift(1.4 * UP)
        verdicts = VGroup(
            *[
                Text(v, font_size=22, weight=BOLD, color=ACCENT if ok else WARM)
                for _, v, ok in cases
            ]
        )
        verdicts.arrange(DOWN, buff=0.55, aligned_edge=LEFT).to_edge(RIGHT, buff=1.1)
        for question, verdict in zip(questions, verdicts, strict=True):
            verdict.match_y(question)

        start_x = questions.get_right()[0] + 0.35
        end_x = verdicts.get_left()[0] - 0.35
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
                run_time=0.6,
            )
        self.wait(0.6)

        # The gambler's fallacy is the last row misread, so it goes here: the
        # law of large numbers dilutes a surplus, it never repays one.
        dilution = VGroup(
            Text("10 extra heads are never repaid — they get diluted:", font_size=BODY_SIZE),
            MathTex(
                r"\tfrac{15}{20} = 75\%",
                r"\qquad\longrightarrow\qquad",
                r"\tfrac{5{,}005}{10{,}000} = 50.05\%",
                font_size=38,
            ),
            caption("the law of large numbers swamps; it does not compensate"),
        ).arrange(DOWN, buff=0.35)
        dilution.move_to(1.7 * DOWN)
        dilution[1][2].set_color(ACCENT)
        self.play(FadeIn(dilution[0]))
        self.play(Write(dilution[1]))
        self.play(FadeIn(dilution[2]))
        self.wait(1.0)

        self.play(FadeOut(VGroup(questions, arrows, verdicts, dilution)))
        takeaway = Text(
            "Independence is an assumption about the measure —\n"
            "know what you paid before you multiply",
            font_size=25,
            line_spacing=1.1,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
