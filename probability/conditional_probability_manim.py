"""Conditional probability — re-measuring inside what you now know.

Six scenes on the same unit square as the independence series:
restriction and renormalization, the stepped cut finally named, the
multiplication rule as a rectangle identity, total probability and trees,
the inversion fallacy, and what conditioning is actually for.

    TheRestrictedSquare      dim what B rules out, re-inflate the band
    IndependenceRevisited    the step's height was P(A|B) all along
    TheMultiplicationRule    P(A and B) = P(B) P(A|B) — the aces license
    TotalProbabilityAndTrees add up the columns; the square drawn as a tree
    TwoSlicesOneSquare       same overlap, two denominators — the inversion
    WhenToCondition          what you condition on, and the CTC residual

Every number on screen is exact and machine-verified in plan 003.

Render:
    uv run python probability/conditional_probability_manim.py
    uv run python probability/conditional_probability_manim.py -s TwoSlicesOneSquare -q draft
"""

import numpy as np
from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    FORMULA_SIZE,
    GOOD,
    LABEL_SIZE,
    MUTED,
    RESULT_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    chip,
    palette,
    render_cli,
)

# Same assignment as the independence module, deliberately: A stays teal and
# B stays pink across the whole topic, so the conditional series reads as a
# continuation of the same picture rather than a new one.
A_COLOR = palette(0)
B_COLOR = palette(1)


def _die_strip(side: float = 1.05) -> VGroup:
    """A fair die as six equal cells in a row (same device as the sibling
    independence module — local on purpose: topic furniture, not repo-wide
    vocabulary like `utils.mobjects`)."""
    cells = VGroup()
    for face in range(1, 7):
        square = Square(side_length=side, stroke_width=2, color=MUTED)
        label = Text(str(face), font_size=LABEL_SIZE).move_to(square)
        cells.add(VGroup(square, label))
    return cells.arrange(RIGHT, buff=0)


class TheRestrictedSquare(ConceptScene):
    """Conditioning is restriction then renormalization — the formula comes last."""

    def construct(self):
        self.play(FadeIn(self.title("The Restricted Square"), shift=0.3 * DOWN))

        prompt = Text("Three flips of a fair coin. P(all heads)?", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- recount inside the smaller world ----------------------------------
        outcomes = ["HHH", "HHT", "HTH", "HTT", "THH", "THT", "TTH", "TTT"]
        chips = VGroup(*[chip(o, MUTED, width=1.4) for o in outcomes])
        chips.arrange_in_grid(rows=2, cols=4, buff=0.3).move_to(0.9 * UP)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.08))
        target = SurroundingRectangle(chips[0], color=ACCENT, buff=0.05)
        eighth = MathTex(r"P(\text{HHH}) = \tfrac{1}{8}", font_size=RESULT_SIZE, color=ACCENT)
        eighth.next_to(chips, DOWN, buff=0.5)
        self.play(Create(target), Write(eighth))
        self.wait(0.6)

        news = Text(
            "Now you learn: the first flip was heads.", font_size=BODY_SIZE, color=B_COLOR
        ).next_to(eighth, DOWN, buff=0.4)
        self.play(FadeIn(news))
        # The T-first half of the world is ruled out — it leaves, in WARM, the
        # same way cancelled orderings and dropped blanks always have.
        ruled_out = VGroup(*[chips[i] for i in range(4, 8)])
        self.play(*[c.animate.set_color(WARM) for c in ruled_out], run_time=0.5)
        self.play(FadeOut(ruled_out, shift=0.3 * DOWN), run_time=0.8)
        recount = MathTex(
            r"P(\text{HHH} \mid \text{first is H}) = \tfrac{1}{4}",
            font_size=RESULT_SIZE,
            color=ACCENT,
        ).move_to(eighth)
        # news leaves WITH the old equation: the recount's caption lands in
        # news's spot, and motion discipline says the space must be empty
        # before the replacement arrives.
        self.play(FadeOut(eighth), FadeOut(news), run_time=0.4)
        self.play(Write(recount))
        smaller = caption("a smaller world — recount inside it").next_to(recount, DOWN, buff=0.3)
        self.play(FadeIn(smaller))
        self.wait(0.9)

        # --- the same move on the square ---------------------------------------
        remaining = VGroup(*[chips[i] for i in range(4)])
        self.play(FadeOut(VGroup(remaining, target, recount, smaller, prompt)))

        side = 3.0
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.6 * LEFT + 0.3 * DOWN
        )
        band = Rectangle(
            width=side * 0.5, height=side, stroke_width=0, fill_color=B_COLOR, fill_opacity=0.4
        ).align_to(square, DL)
        b_tag = MathTex(r"B", font_size=40, color=B_COLOR).next_to(band, UP, buff=0.2)
        overlap = Rectangle(
            width=side * 0.5,
            height=side * 0.3,
            stroke_width=0,
            fill_color=ACCENT,
            fill_opacity=0.55,
        ).align_to(square, DL)
        ab_tag = MathTex(r"A \cap B", font_size=30, color=ACCENT).move_to(overlap)
        # The discarded half needs to read as discarded next to a bright B —
        # at draft the two halves were nearly the same value on the dark
        # canvas and the "dim it" line had nothing visible to point at.
        outside = Rectangle(
            width=side * 0.5, height=side, stroke_width=0, fill_color=WARM, fill_opacity=0.45
        ).align_to(square, DR)
        self.play(Create(square), FadeIn(band), FadeIn(b_tag))
        self.play(FadeIn(overlap), FadeIn(ab_tag))
        self.wait(0.4)

        dim_note = Text(
            "B rules the right half out —\ndim it, and re-measure inside B",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.9)
        self.play(FadeIn(outside), FadeIn(dim_note))
        self.wait(0.6)
        self.play(FadeOut(outside), square.animate.set_stroke(opacity=0.3), run_time=0.6)

        # Re-inflate: a straight band stretched uniformly multiplies every
        # enclosed area by exactly 1/P(B) — the stretch IS the renormalization,
        # which is why this animation is honest only for bands.
        stretched_band = Rectangle(
            width=side, height=side, stroke_width=0, fill_color=B_COLOR, fill_opacity=0.18
        ).move_to(square)
        stretched_overlap = Rectangle(
            width=side, height=side * 0.3, stroke_width=0, fill_color=ACCENT, fill_opacity=0.55
        ).align_to(square, DL)
        new_note = Text(
            "stretch the slice back to a full square:\nevery share inside B scales by 1/P(B)",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.9)
        self.play(FadeOut(dim_note), run_time=0.3)
        self.play(
            Transform(band, stretched_band),
            Transform(overlap, stretched_overlap),
            ab_tag.animate.move_to(stretched_overlap),
            run_time=1.2,
        )
        self.play(FadeIn(new_note))
        self.wait(0.9)

        # --- the definition, last -----------------------------------------------
        self.play(FadeOut(VGroup(square, band, overlap, ab_tag, b_tag, new_note)))
        definition = MathTex(
            r"P(A \mid B) = \frac{P(A \cap B)}{P(B)}", font_size=FORMULA_SIZE, color=ACCENT
        ).move_to(0.55 * UP)
        conditions = VGroup(
            caption("defined only when P(B) > 0"),
            caption("the slice is a genuine probability space —"),
            caption("conditional probabilities are probabilities"),
        ).arrange(DOWN, buff=0.2)
        conditions.next_to(definition, DOWN, buff=0.5)
        self.play(Write(definition), Create(boxed(definition, buff=0.35)))
        self.play(LaggedStart(*[FadeIn(c) for c in conditions], lag_ratio=0.3))
        self.wait(2)


class IndependenceRevisited(ConceptScene):
    """The stepped cut had a name: its height inside the band is P(A|B)."""

    def construct(self):
        self.play(FadeIn(self.title("Independence, Revisited"), shift=0.3 * DOWN))

        recall = Text(
            "The independence series drew dependence as a cut that steps.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))

        # --- the broken square, named -------------------------------------------
        side = 2.9
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.6 * LEFT + 0.35 * DOWN
        )
        corner = square.get_corner(DL)
        x_cut = side * 0.5

        def a_region(left_h: float, right_h: float) -> VGroup:
            left = Rectangle(
                width=x_cut,
                height=side * left_h,
                stroke_width=0,
                fill_color=A_COLOR,
                fill_opacity=0.4,
            ).align_to(square, DL)
            right = Rectangle(
                width=side - x_cut,
                height=side * right_h,
                stroke_width=0,
                fill_color=A_COLOR,
                fill_opacity=0.4,
            )
            right.next_to(left, RIGHT, buff=0, aligned_edge=DOWN)
            return VGroup(left, right)

        v_cut = Line(
            corner + np.array([x_cut, 0, 0]),
            corner + np.array([x_cut, side, 0]),
            color=B_COLOR,
            stroke_width=4,
        )
        b_tag = MathTex(r"B", font_size=36, color=B_COLOR)
        b_tag.next_to(square, UP, buff=0.2).shift(0.7 * LEFT)
        region = a_region(0.62, 0.25)
        self.play(Create(square), Create(v_cut), FadeIn(b_tag))
        self.play(FadeIn(region))

        inside = MathTex(r"P(A \mid B)", font_size=32, color=A_COLOR)
        inside.next_to(square, LEFT, buff=0.35).shift(0.35 * DOWN)
        arrow_in = Arrow(
            inside.get_right(),
            region[0].get_left() + 0.2 * RIGHT,
            buff=0.08,
            color=MUTED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )
        named = Text(
            "the step's height inside the band\nis a conditional probability —\n"
            "it had a name all along",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.9)
        self.play(FadeIn(inside), GrowArrow(arrow_in))
        self.play(FadeIn(named))
        self.wait(0.9)

        flat_note = Text(
            "the step flattening is\nP(A|B) = P(A): conditioning\n"
            "on B changed nothing — independence",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(square, RIGHT, buff=0.9)
        self.play(FadeOut(named), run_time=0.3)
        self.play(Transform(region, a_region(0.4, 0.4)), FadeIn(flat_note))
        self.wait(0.9)

        # --- the die, recounted --------------------------------------------------
        self.play(
            FadeOut(VGroup(square, v_cut, b_tag, region, inside, arrow_in, flat_note, recall))
        )
        strip = _die_strip(0.95).move_to(1.5 * UP)
        for i in (1, 3, 5):
            strip[i][0].set_fill(A_COLOR, opacity=0.35)
        a_lab = Text("A = even", font_size=LABEL_SIZE, color=A_COLOR)
        a_lab.next_to(strip, UP, buff=0.25).align_to(strip, LEFT)
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.8) for c in strip], lag_ratio=0.06), FadeIn(a_lab)
        )

        first = MathTex(
            r"P(A \mid \{1,2,3,4\}) = \tfrac{2}{4} = \tfrac{1}{2} = P(A)\ \checkmark",
            font_size=40,
        ).move_to(0.15 * DOWN)
        first[0][-1].set_color(GOOD)
        self.play(Write(first))
        jewel = caption("the jewel example, re-read: recount inside B, nothing moved")
        jewel.next_to(first, DOWN, buff=0.3)
        self.play(FadeIn(jewel))
        self.wait(0.8)

        second = MathTex(
            r"P(A \mid \{1,2,3\}) = \tfrac{1}{3} \neq \tfrac{1}{2}\ \times",
            font_size=40,
        ).next_to(jewel, DOWN, buff=0.45)
        second[0][-1].set_color(WARM)
        pip = caption("one pip, again — and disjoint B gives P(A|B) = 0: maximal information")
        pip.next_to(second, DOWN, buff=0.3)
        self.play(Write(second))
        self.play(FadeIn(pip))
        self.wait(0.9)

        # --- the takeaway ---------------------------------------------------------
        self.play(FadeOut(VGroup(strip, a_lab, first, jewel, second, pip)))
        takeaway = Text(
            "Independence: the conditional answer matches the unconditional one\n"
            "(on P(B) > 0 — the product form stays the definition)",
            font_size=24,
            line_spacing=1.1,
        ).move_to(0.35 * UP)
        note = caption("P(A) itself never changed — P(A|B) answers in a different measure")
        note.next_to(takeaway, DOWN, buff=0.5)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.play(FadeIn(note))
        self.wait(2)


class TheMultiplicationRule(ConceptScene):
    """The definition rewritten: P(A and B) = P(B) P(A|B), one rectangle."""

    def construct(self):
        self.play(FadeIn(self.title("The Multiplication Rule"), shift=0.3 * DOWN))

        flip = MathTex(
            r"P(A \mid B) = \frac{P(A \cap B)}{P(B)}",
            r"\quad\Longrightarrow\quad",
            r"P(A \cap B) = P(B)\,P(A \mid B)",
            font_size=44,
        ).move_to(1.7 * UP)
        flip[2].set_color(ACCENT)
        self.play(Write(flip))
        rectangle_note = caption("a joint probability is a width times a conditional height —")
        rectangle_note.next_to(flip, DOWN, buff=0.35)
        counting = caption("the counting rule of product, carrying probabilities")
        counting.next_to(rectangle_note, DOWN, buff=0.2)
        self.play(FadeIn(rectangle_note), FadeIn(counting))
        self.wait(0.8)

        # --- the aces payoff ------------------------------------------------------
        self.play(FadeOut(rectangle_note), FadeOut(counting))
        # The earlier scene priced the aces by counting alone (1/221 vs the
        # product-rule 1/169); the factorization below is THIS scene's new
        # object — claim only what was shown.
        owed = Text(
            "Independence priced the aces with no license shown — now factor it:",
            font_size=BODY_SIZE,
        ).move_to(0.45 * UP)
        debt = MathTex(
            r"P(\text{both aces}) = \tfrac{4}{52}\cdot\tfrac{3}{51} = \tfrac{1}{221}",
            font_size=RESULT_SIZE,
        ).next_to(owed, DOWN, buff=0.4)
        self.play(FadeIn(owed))
        self.play(Write(debt))
        self.wait(0.5)
        license_tex = MathTex(
            r"= P(A_1)\cdot P(A_2 \mid A_1)",
            font_size=RESULT_SIZE,
            color=GOOD,
        ).next_to(debt, DOWN, buff=0.35)
        paid = caption("the second factor was a conditional probability all along —")
        paid2 = caption("the shrinking pool, made rigorous")
        paid.next_to(license_tex, DOWN, buff=0.3)
        paid2.next_to(paid, DOWN, buff=0.18)
        self.play(Write(license_tex))
        self.play(FadeIn(paid), FadeIn(paid2))
        self.wait(1.0)

        # --- chain rule and time reversal ----------------------------------------
        self.play(FadeOut(VGroup(owed, debt, license_tex, paid, paid2)))
        chain = MathTex(
            r"P(A \cap B \cap C) = P(A)\,P(B \mid A)\,P(C \mid A \cap B)",
            font_size=40,
        ).move_to(0.55 * UP)
        hearts = MathTex(
            r"P(\text{3 hearts}) = \tfrac{13}{52}\cdot\tfrac{12}{51}\cdot\tfrac{11}{50}"
            r" = \tfrac{11}{850}",
            font_size=38,
            color=ACCENT,
        ).next_to(chain, DOWN, buff=0.4)
        tworoutes = caption("counting agrees: C(13,3) / C(52,3) = 11/850 — two routes, one answer")
        tworoutes.next_to(hearts, DOWN, buff=0.3)
        nfact = caption('every expansion order is valid — "n! theorems in one"')
        nfact.next_to(tworoutes, DOWN, buff=0.18)
        self.play(Write(chain))
        self.play(Write(hearts))
        self.play(FadeIn(tworoutes), FadeIn(nfact))
        self.wait(1.0)

        self.play(FadeOut(VGroup(chain, hearts, tworoutes, nfact)))
        reverse = MathTex(
            r"P(S_1 \mid S_2) = \tfrac{12}{51} = P(S_2 \mid S_1)",
            font_size=40,
        ).move_to(0.55 * UP)
        rev_note = Text(
            "conditioning on the second card tells you about the first —",
            font_size=BODY_SIZE,
        ).next_to(reverse, DOWN, buff=0.4)
        rev_note2 = Text(
            "re-measuring, not re-running: information flows backwards fine",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).next_to(rev_note, DOWN, buff=0.25)
        self.play(Write(reverse))
        self.play(FadeIn(rev_note))
        self.play(FadeIn(rev_note2))
        self.wait(1.0)

        self.play(FadeOut(VGroup(flip, reverse, rev_note, rev_note2)))
        formula = MathTex(
            r"P(A \cap B) = P(B)\,P(A \mid B) = P(A)\,P(B \mid A)",
            font_size=48,
            color=ACCENT,
        ).move_to(0.3 * UP)
        self.play(Write(formula), Create(boxed(formula, buff=0.32)))
        self.wait(2)


class TotalProbabilityAndTrees(ConceptScene):
    """Total probability adds the columns; a tree is the same square drawn."""

    def construct(self):
        self.play(FadeIn(self.title("Total Probability, and Trees"), shift=0.3 * DOWN))

        prompt = Text(
            "Split the die: B = {1,2,3} or not. What is P(even)?", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- columns on the square ----------------------------------------------
        side = 2.9
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.6 * LEFT + 0.4 * DOWN
        )
        left_col = Rectangle(
            width=side / 2,
            height=side,
            stroke_width=1.5,
            color=B_COLOR,
            fill_opacity=0.08,
            fill_color=B_COLOR,
        ).align_to(square, DL)
        right_col = Rectangle(
            width=side / 2,
            height=side,
            stroke_width=1.5,
            color=MUTED,
            fill_opacity=0.05,
            fill_color=MUTED,
        ).align_to(square, DR)
        col_tags = VGroup(
            MathTex(r"B", font_size=30, color=B_COLOR).next_to(left_col, UP, buff=0.15),
            MathTex(r"B^{c}", font_size=30, color=MUTED).next_to(right_col, UP, buff=0.15),
        )
        even_left = Rectangle(
            width=side / 2, height=side / 3, stroke_width=0, fill_color=A_COLOR, fill_opacity=0.5
        ).align_to(square, DL)
        even_right = Rectangle(
            width=side / 2,
            height=2 * side / 3,
            stroke_width=0,
            fill_color=A_COLOR,
            fill_opacity=0.5,
        ).align_to(square, DR)
        h_tags = VGroup(
            MathTex(r"\tfrac{1}{3}", font_size=28, color=A_COLOR).move_to(even_left),
            MathTex(r"\tfrac{2}{3}", font_size=28, color=A_COLOR).move_to(even_right),
        )
        self.play(Create(square), FadeIn(left_col), FadeIn(right_col), FadeIn(col_tags))
        heights = caption("each column carries A at its own\nconditional height P(A | column)")
        heights.next_to(square, RIGHT, buff=0.9)
        self.play(FadeIn(even_left), FadeIn(even_right), FadeIn(h_tags), FadeIn(heights))
        self.wait(0.7)

        lotp = (
            MathTex(
                r"P(A) = \tfrac{1}{2}\cdot\tfrac{1}{3} + \tfrac{1}{2}\cdot\tfrac{2}{3}"
                r" = \tfrac{1}{2}",
                font_size=38,
                color=ACCENT,
            )
            .next_to(heights, DOWN, buff=0.5)
            .align_to(heights, LEFT)
        )
        addup = (
            caption("total probability is: add up the rectangles")
            .next_to(lotp, DOWN, buff=0.3)
            .align_to(lotp, LEFT)
        )
        self.play(Write(lotp))
        self.play(FadeIn(addup))
        self.wait(0.9)

        # --- the same square, drawn as a tree ------------------------------------
        stage = VGroup(
            square,
            left_col,
            right_col,
            col_tags,
            even_left,
            even_right,
            h_tags,
            heights,
            lotp,
            addup,
            prompt,
        )
        self.play(FadeOut(stage))
        tree_note = Text("A tree is the same square drawn sideways", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        self.play(FadeIn(tree_note))

        root = Dot(np.array([-4.6, 0.3, 0]), radius=0.07, color=MUTED)
        b_node = np.array([-1.9, 1.45, 0])
        bc_node = np.array([-1.9, -0.85, 0])
        leaves_y = {"be": 2.0, "bo": 0.9, "bce": -0.3, "bco": -1.4}
        leaf_x = 1.1
        edges = VGroup(
            Line(root.get_center(), b_node, color=B_COLOR, stroke_width=3),
            Line(root.get_center(), bc_node, color=MUTED, stroke_width=3),
            Line(b_node, np.array([leaf_x, leaves_y["be"], 0]), color=A_COLOR, stroke_width=2.5),
            Line(b_node, np.array([leaf_x, leaves_y["bo"], 0]), color=MUTED, stroke_width=2.5),
            Line(bc_node, np.array([leaf_x, leaves_y["bce"], 0]), color=A_COLOR, stroke_width=2.5),
            Line(bc_node, np.array([leaf_x, leaves_y["bco"], 0]), color=MUTED, stroke_width=2.5),
        )
        branch_labels = VGroup(
            MathTex(r"\tfrac{1}{2}", font_size=26, color=B_COLOR).next_to(edges[0], UP, buff=0.1),
            MathTex(r"\tfrac{1}{2}", font_size=26, color=MUTED).next_to(edges[1], DOWN, buff=0.1),
            MathTex(r"\tfrac{1}{3}", font_size=26, color=A_COLOR).next_to(edges[2], UP, buff=0.08),
            MathTex(r"\tfrac{2}{3}", font_size=26, color=MUTED).next_to(edges[3], DOWN, buff=0.08),
            MathTex(r"\tfrac{2}{3}", font_size=26, color=A_COLOR).next_to(edges[4], UP, buff=0.08),
            MathTex(r"\tfrac{1}{3}", font_size=26, color=MUTED).next_to(edges[5], DOWN, buff=0.08),
        )
        node_tags = VGroup(
            MathTex(r"B", font_size=30, color=B_COLOR).next_to(b_node, UP, buff=0.15),
            MathTex(r"B^{c}", font_size=30, color=MUTED).next_to(bc_node, DOWN, buff=0.15),
        )
        # Leaves are intersections — labelled precisely once, because the
        # shorthand ("even") is exactly how trees teach the wrong thing.
        leaf_labels = VGroup(
            MathTex(r"B \cap A:\ \tfrac{1}{2}\cdot\tfrac{1}{3} = \tfrac{1}{6}", font_size=28),
            MathTex(r"B \cap A^{c}", font_size=28, color=MUTED),
            MathTex(r"B^{c} \cap A:\ \tfrac{1}{2}\cdot\tfrac{2}{3} = \tfrac{1}{3}", font_size=28),
            MathTex(r"B^{c} \cap A^{c}", font_size=28, color=MUTED),
        )
        for label, key in zip(leaf_labels, ["be", "bo", "bce", "bco"], strict=True):
            label.move_to(np.array([leaf_x + 0.3, leaves_y[key], 0]), aligned_edge=LEFT)

        self.play(FadeIn(root))
        self.play(
            Create(edges[0]),
            Create(edges[1]),
            FadeIn(node_tags),
            FadeIn(branch_labels[0]),
            FadeIn(branch_labels[1]),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[Create(e) for e in edges[2:]], lag_ratio=0.15),
            LaggedStart(*[FadeIn(b) for b in branch_labels[2:]], lag_ratio=0.15),
            run_time=1.1,
        )
        self.play(LaggedStart(*[FadeIn(label) for label in leaf_labels], lag_ratio=0.15))
        branches_note = caption(
            "branches carry conditional probabilities;\n"
            "leaves are intersections — products along the path"
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(branches_note))
        self.wait(0.7)

        circles = VGroup(
            SurroundingRectangle(leaf_labels[0], color=ACCENT, buff=0.1, corner_radius=0.08),
            SurroundingRectangle(leaf_labels[2], color=ACCENT, buff=0.1, corner_radius=0.08),
        )
        summed = MathTex(
            r"P(A) = \tfrac{1}{6} + \tfrac{1}{3} = \tfrac{1}{2}", font_size=34, color=ACCENT
        ).next_to(branches_note, UP, buff=0.35)
        self.play(Create(circles))
        self.play(Write(summed))
        self.wait(0.9)

        tree = VGroup(
            root,
            edges,
            branch_labels,
            node_tags,
            leaf_labels,
            circles,
            summed,
            branches_note,
            tree_note,
        )
        self.play(FadeOut(tree))
        formula = MathTex(
            r"P(A) = \sum_i P(B_i)\,P(A \mid B_i)", font_size=FORMULA_SIZE, color=ACCENT
        ).move_to(0.4 * UP)
        partition = caption("over any partition — disjoint columns that tile the square")
        partition.next_to(formula, DOWN, buff=0.5)
        self.play(Write(formula), Create(boxed(formula, buff=0.35)))
        self.play(FadeIn(partition))
        self.wait(2)


class TwoSlicesOneSquare(ConceptScene):
    """P(A|B) and P(B|A) share a numerator and nothing else — the inversion."""

    def construct(self):
        self.play(FadeIn(self.title("Two Slices, One Square"), shift=0.3 * DOWN))

        # --- the geometric point -------------------------------------------------
        side = 2.7
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.7 * LEFT + 0.35 * DOWN
        )
        b_band = Rectangle(
            width=side * 0.45, height=side, stroke_width=0, fill_color=B_COLOR, fill_opacity=0.25
        ).align_to(square, DL)
        # A steps at the B boundary — tall inside B, short outside. Straight
        # perpendicular bands would draw an independent pair (the previous
        # scenes taught exactly that), and the inversion point is stronger
        # when the conditionals differ because the events are dependent, not
        # only because the denominators do.
        a_band = VGroup(
            Rectangle(
                width=side * 0.45,
                height=side * 0.45,
                stroke_width=0,
                fill_color=A_COLOR,
                fill_opacity=0.25,
            ).align_to(square, DL),
            Rectangle(
                width=side * 0.55,
                height=side * 0.18,
                stroke_width=0,
                fill_color=A_COLOR,
                fill_opacity=0.25,
            ).align_to(square, DR),
        )
        overlap = Rectangle(
            width=side * 0.45,
            height=side * 0.45,
            stroke_width=0,
            fill_color=ACCENT,
            fill_opacity=0.6,
        ).align_to(square, DL)
        tags = VGroup(
            MathTex(r"B", font_size=32, color=B_COLOR).next_to(b_band, UP, buff=0.15),
            MathTex(r"A", font_size=32, color=A_COLOR).next_to(a_band, RIGHT, buff=0.15),
        )
        self.play(Create(square), FadeIn(b_band), FadeIn(a_band), FadeIn(overlap), FadeIn(tags))

        readings = VGroup(
            MathTex(
                r"P(A \mid B) = \frac{\text{overlap}}{\text{area}(B)}", font_size=34, color=B_COLOR
            ),
            MathTex(
                r"P(B \mid A) = \frac{\text{overlap}}{\text{area}(A)}", font_size=34, color=A_COLOR
            ),
        ).arrange(DOWN, buff=0.5)
        readings.next_to(square, RIGHT, buff=1.0)
        same = caption("same numerator — different denominators").next_to(readings, DOWN, buff=0.4)
        self.play(Write(readings[0]))
        self.play(Write(readings[1]))
        self.play(FadeIn(same))
        self.wait(0.9)

        quick = MathTex(
            r"P(\text{first H} \mid \text{five H}) = 1",
            r"\qquad P(\text{five H} \mid \text{first H}) = \tfrac{1}{16}",
            font_size=34,
        ).to_edge(DOWN, buff=0.55)
        quick[1].set_color(WARM)
        self.play(Write(quick))
        self.wait(0.9)

        # --- the prevalence pair -------------------------------------------------
        self.play(FadeOut(VGroup(square, b_band, a_band, overlap, tags, readings, same, quick)))
        setup = Text(
            "One test: catches 9 of 10 sick, false-alarms 1 in 10 healthy.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(setup))

        def cohort(total: int, sick: int, tp: int, fp: int, x: float) -> VGroup:
            # Natural frequencies as labelled count chips — whole people, no
            # percentages of percentages.
            healthy = total - sick
            rows = VGroup(
                Text(f"{total} people", font_size=LABEL_SIZE),
                VGroup(
                    chip(f"{sick} sick", A_COLOR, width=2.0),
                    chip(f"{healthy} healthy", MUTED, width=2.4),
                ).arrange(RIGHT, buff=0.25),
                VGroup(
                    chip(f"{tp} +", GOOD, width=1.35),
                    chip(f"{fp} +", WARM, width=1.35),
                ).arrange(RIGHT, buff=0.9),
                MathTex(
                    rf"P(\text{{sick}} \mid +) = \tfrac{{{tp}}}{{{tp + fp}}}",
                    font_size=32,
                ),
            ).arrange(DOWN, buff=0.35)
            rows.move_to(np.array([x, -0.55, 0]))
            return rows

        left = cohort(100, 10, 9, 9, -3.3)
        right = cohort(1000, 10, 9, 99, 3.3)
        left[3][0][-4:].set_color(ACCENT)  # the 1/2-ish tail
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * UP) for r in left], lag_ratio=0.2))
        half = MathTex(r"= \tfrac{1}{2}", font_size=36, color=ACCENT).next_to(
            left[3], RIGHT, buff=0.15
        )
        self.play(Write(half))
        self.wait(0.6)
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * UP) for r in right], lag_ratio=0.2))
        twelfth = MathTex(r"= \tfrac{1}{12}", font_size=36, color=WARM).next_to(
            right[3], RIGHT, buff=0.15
        )
        self.play(Write(twelfth))
        moved = Text(
            "same test — the prior moved the answer by a factor of six",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(moved))
        self.wait(1.1)

        # --- Bayes' front door ----------------------------------------------------
        self.play(FadeOut(VGroup(left, right, half, twelfth, moved, setup)))
        door = MathTex(
            r"P(A)\,P(B \mid A) = P(B)\,P(A \mid B)", font_size=FORMULA_SIZE, color=ACCENT
        ).move_to(0.4 * UP)
        knock = caption("both expansions of the same rectangle — divide either side")
        knock2 = caption("and you are at Bayes' rule. That door opens in the next series.")
        knock.next_to(door, DOWN, buff=0.5)
        knock2.next_to(knock, DOWN, buff=0.2)
        self.play(Write(door), Create(boxed(door, buff=0.35)))
        self.play(FadeIn(knock), FadeIn(knock2))
        self.wait(2)


class WhenToCondition(ConceptScene):
    """What conditioning is for — and what exactly you condition on."""

    def construct(self):
        self.play(FadeIn(self.title("When to Condition"), shift=0.3 * DOWN))

        cases = [
            ("Sequential draws — the pool shrinks", "multiplication rule"),
            ("A positive test — two numbers, not one", "condition on the evidence"),
            ("\u201cAt least one girl\u2026\u201d", "condition on the protocol"),
            ("CTC's per-frame product", "independent given the input"),
        ]
        questions = VGroup(*[Text(q, font_size=21) for q, _ in cases])
        questions.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        questions.to_edge(LEFT, buff=0.8).shift(1.5 * UP)
        verdicts = VGroup(*[Text(v, font_size=21, weight=BOLD, color=ACCENT) for _, v in cases])
        verdicts.arrange(DOWN, buff=0.55, aligned_edge=LEFT).to_edge(RIGHT, buff=0.8)
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

        # The protocol beat: the same fact, two conditioning events — with the
        # four families and the announcement rule drawn, not asserted. The
        # mapping leaves first; this beat needs the room.
        self.play(FadeOut(VGroup(questions, arrows, verdicts)))

        families = VGroup(*[chip(k, MUTED, width=1.15) for k in ["GG", "GB", "BG", "BB"]])
        families.arrange(RIGHT, buff=0.4).move_to(1.55 * UP)
        fam_tag = caption("two children, four equally likely families")
        fam_tag.next_to(families, UP, buff=0.3)
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.8) for c in families], lag_ratio=0.12),
            FadeIn(fam_tag),
        )
        # Conditioning on the bare fact: BB leaves, three cells survive.
        self.play(families[3].animate.set_color(WARM), run_time=0.4)
        self.play(FadeOut(families[3], shift=0.3 * DOWN), run_time=0.6)
        bare = MathTex(
            r"P(\text{GG} \mid \text{at least one girl}) = \tfrac{1}{3}", font_size=32
        ).move_to(0.35 * UP)
        self.play(Write(bare))
        self.wait(0.5)

        # The announcement rule, drawn as weights: a GG parent always mentions
        # a girl; a mixed-family parent only half the time. Weights 1/4, 1/8,
        # 1/8 — and the posterior is 1/2, not 1/3.
        weights = VGroup(
            MathTex(r"\times 1", font_size=28, color=GOOD).next_to(families[0], DOWN, buff=0.22),
            MathTex(r"\times \tfrac{1}{2}", font_size=28, color=WARM).next_to(
                families[1], DOWN, buff=0.22
            ),
            MathTex(r"\times \tfrac{1}{2}", font_size=28, color=WARM).next_to(
                families[2], DOWN, buff=0.22
            ),
        )
        rule_note = caption('the announcement rule: a mixed family says "girl" half the time')
        rule_note.next_to(bare, DOWN, buff=0.35)
        self.play(FadeIn(weights), FadeIn(rule_note))
        protocol_eq = MathTex(
            r"P(\text{GG} \mid \text{parent mentioned a girl})"
            r" = \frac{1/4}{1/4 + 1/8 + 1/8} = \tfrac{1}{2}",
            font_size=32,
            color=ACCENT,
        ).next_to(rule_note, DOWN, buff=0.4)
        lesson = caption("the conditioning event includes how you learned it")
        lesson.next_to(protocol_eq, DOWN, buff=0.3)
        self.play(Write(protocol_eq))
        self.play(FadeIn(lesson))
        self.wait(0.9)

        # The CTC residual, closed with exact numbers.
        self.play(
            FadeOut(
                VGroup(
                    families[0],
                    families[1],
                    families[2],
                    fam_tag,
                    bare,
                    weights,
                    rule_note,
                    protocol_eq,
                    lesson,
                )
            )
        )
        ci_head = Text(
            "And a third kind of independence — conditional:", font_size=BODY_SIZE
        ).move_to(1.55 * UP)
        ci = MathTex(
            r"P(H_1 \cap H_2) = \tfrac{41}{100} \neq \tfrac{1}{4}",
            r"\qquad\text{but}\qquad",
            r"P(H_1 \cap H_2 \mid \text{coin}) = P(H_1 \mid \text{coin})\,P(H_2 \mid \text{coin})",
            font_size=32,
        ).next_to(ci_head, DOWN, buff=0.45)
        ci[0].set_color(WARM)
        ci[2].set_color(GOOD)
        ci_note = caption(
            "two coins (9/10 and 1/10 heads), one picked at random: the flips are\n"
            "dependent marginally — the coin is the common cause — yet independent given it"
        ).next_to(ci, DOWN, buff=0.35)
        ctc = Text(
            "this is CTC\u2019s assumption: frames independent given the input",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).next_to(ci_note, DOWN, buff=0.4)
        monty = caption(
            "(Monty Hall waits for the Bayes series — the host's protocol is the problem)"
        )
        monty.next_to(ctc, DOWN, buff=0.3)
        self.play(FadeIn(ci_head))
        self.play(Write(ci))
        self.play(FadeIn(ci_note))
        self.play(FadeIn(ctc))
        self.play(FadeIn(monty))
        self.wait(1.0)

        self.play(FadeOut(VGroup(ci_head, ci, ci_note, ctc, monty)))
        takeaway = Text(
            "Condition on what you saw, the way you saw it — then multiply",
            font_size=26,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
