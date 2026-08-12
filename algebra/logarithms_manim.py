"""Logarithms — counting multiplicative steps, so multiplying becomes adding.

Six scenes on the two-row strip (a counter row over a value row): the
definition as reading the counter, the notation honesty beat, the product
law as hops, negative logs as shrink counts on the repo's own unit
square, and the two payoffs this series was built to deliver — the
evidence ruler for Bayes and the underflow cliff for CTC.

    TheCountingStrip     a logarithm reads the counter row
    OneFactThreeNotations  (2, 6, 64) asked three ways; undo, never cancel
    MultiplyIsAdd        hops add; the slide rule; the base is a unit
    ShrinkCounts         probabilities are shrink counts; log 0 is -inf
    TheEvidenceRuler     each head adds exactly +2 — evidence as length
    TheUnderflowCliff    0.1^324 is exactly zero; the counter walks on

Every number on screen is exact and machine-verified in plan 005; every
integer log is written from its exponent, never computed by a float log
call (math.log(243, 3) returns 4.999999999999999 — the recorded hazard).

Render:
    uv run python algebra/logarithms_manim.py
    uv run python algebra/logarithms_manim.py -s TheEvidenceRuler -q draft
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
    render_cli,
)


def _strip(counters, values, cell_width=1.15, highlight=()):
    """The two-row strip: a counter row (COOL) over a value row.

    The device the whole series stands on — the counter row is the log.
    ``highlight`` marks columns whose value cell gets the ACCENT frame.
    """
    columns = VGroup()
    for i, (c, v) in enumerate(zip(counters, values, strict=True)):
        counter = Text(str(c), font_size=LABEL_SIZE, color=COOL)
        value = Text(str(v), font_size=LABEL_SIZE)
        box = RoundedRectangle(
            width=cell_width,
            height=0.62,
            corner_radius=0.1,
            stroke_width=2,
            color=ACCENT if i in highlight else MUTED,
        )
        value.move_to(box)
        counter.next_to(box, UP, buff=0.22)
        columns.add(VGroup(counter, box, value))
    return columns.arrange(RIGHT, buff=0.16)


class TheCountingStrip(ConceptScene):
    """A logarithm reads the counter row: the exponent is a count of steps."""

    def construct(self):
        self.play(FadeIn(self.title("The Counting Strip"), shift=0.3 * DOWN))

        prompt = Text("Keep doubling. Count as you go.", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        strip = _strip(range(9), [2**k for k in range(9)], cell_width=1.25)
        strip.scale(0.92).move_to(0.9 * UP)
        row_tags = VGroup(
            Text("count", font_size=SMALL_SIZE, color=COOL),
            Text("value", font_size=SMALL_SIZE, color=MUTED),
        )
        row_tags[0].next_to(strip[0][0], LEFT, buff=0.45)
        row_tags[1].next_to(strip[0][1], LEFT, buff=0.45)
        self.play(
            LaggedStart(*[FadeIn(c, shift=0.15 * UP) for c in strip], lag_ratio=0.08),
            FadeIn(row_tags),
            run_time=1.6,
        )
        self.wait(0.5)

        # --- invert the question ------------------------------------------------
        question = Text("2 to the what is 64?", font_size=BODY_SIZE, color=ACCENT)
        question.move_to(0.75 * DOWN)
        self.play(FadeIn(question))
        target = SurroundingRectangle(strip[6][1], color=ACCENT, buff=0.05)
        up_arrow = Arrow(
            strip[6][1].get_top() + 0.55 * UP,
            strip[6][0].get_bottom(),
            buff=0.06,
            color=ACCENT,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.3,
        )
        self.play(Create(target))
        self.play(GrowArrow(up_arrow))
        answer = MathTex(r"\log_2 64 = 6", font_size=RESULT_SIZE, color=ACCENT)
        answer.next_to(question, DOWN, buff=0.4)
        read_note = caption("a logarithm just reads the counter row").next_to(
            answer, DOWN, buff=0.3
        )
        self.play(Write(answer))
        self.play(FadeIn(read_note))
        self.wait(1.0)

        # --- the definition, with its conditions --------------------------------
        self.play(FadeOut(VGroup(prompt, question, answer, read_note, target, up_arrow)))
        definition = MathTex(
            r"\log_b x = y \iff b^y = x", font_size=FORMULA_SIZE, color=ACCENT
        ).move_to(0.55 * DOWN)
        conditions = VGroup(
            caption("b > 0 and b ≠ 1 — the ladder of 1s never moves"),
            caption("x > 0 — a positive base never leaves the positives"),
        ).arrange(DOWN, buff=0.2)
        conditions.next_to(definition, DOWN, buff=0.45)
        self.play(Write(definition), Create(boxed(definition, buff=0.32)))
        self.play(LaggedStart(*[FadeIn(c) for c in conditions], lag_ratio=0.3))
        self.wait(2)


class OneFactThreeNotations(ConceptScene):
    """One triple, three questions — and logs undo, they never cancel."""

    def construct(self):
        self.play(FadeIn(self.title("One Fact, Three Notations"), shift=0.3 * DOWN))

        prompt = Text(
            "Three notations. One fact about the triple (2, 6, 64).", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        forms = VGroup(
            MathTex(r"2^6 = 64", font_size=44),
            MathTex(r"\log_2 64 = 6", font_size=44),
            MathTex(r"\sqrt[6]{64} = 2", font_size=44),
        ).arrange(RIGHT, buff=1.1)
        forms.move_to(1.35 * UP)
        self.play(LaggedStart(*[Write(f) for f in forms], lag_ratio=0.25))
        questions = VGroup(
            caption("what do I reach?"),
            caption("how many steps?"),
            caption("what's the stride?"),
        )
        for q, f in zip(questions, forms, strict=True):
            q.next_to(f, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(q) for q in questions], lag_ratio=0.25))
        self.wait(0.8)

        # --- undo, never cancel -------------------------------------------------
        undo = MathTex(r"b^{\log_b x} = x", font_size=44, color=GOOD).move_to(0.3 * DOWN)
        undo_note = Text(
            'ask "how many steps to x?", then take that many steps: you are at x',
            font_size=BODY_SIZE,
        ).next_to(undo, DOWN, buff=0.35)
        never = caption('an inverse question, answered — logs undo; they never "cancel"')
        never.next_to(undo_note, DOWN, buff=0.25)
        self.play(Write(undo))
        self.play(FadeIn(undo_note))
        self.play(FadeIn(never))
        self.wait(1.0)

        # --- the classic trap, refuted in the right base ------------------------
        self.play(FadeOut(VGroup(undo, undo_note, never)))
        trap = MathTex(r"\log(a + b) \neq \log a + \log b", font_size=44, color=WARM).move_to(
            0.15 * DOWN
        )
        refute = MathTex(
            r"\log_{10}(10 + 10) \approx 1.301 \neq 2 = \log_{10}10 + \log_{10}10",
            font_size=36,
        ).next_to(trap, DOWN, buff=0.4)
        beware = caption("refuted in base 10 on purpose — in base 2 the instance log₂(2+2) = 2")
        beware2 = caption("is coincidentally TRUE, which is how this trap survives")
        beware.next_to(refute, DOWN, buff=0.3)
        beware2.next_to(beware, DOWN, buff=0.18)
        self.play(Write(trap))
        self.play(Write(refute))
        self.play(FadeIn(beware), FadeIn(beware2))
        self.wait(1.2)

        self.play(FadeOut(VGroup(prompt, forms, questions, trap, refute, beware, beware2)))
        takeaway = Text(
            "Power, log, and root ask three questions about one triple",
            font_size=27,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class MultiplyIsAdd(ConceptScene):
    """Multiplying values is adding counters — the slide rule made a law of it."""

    def construct(self):
        self.play(FadeIn(self.title("Multiply Is Add"), shift=0.3 * DOWN))

        prompt = Text("8 × 16, without multiplying", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        strip = _strip(range(9), [2**k for k in range(9)], cell_width=1.25)
        strip.scale(0.92).move_to(1.1 * UP)
        self.play(
            LaggedStart(*[FadeIn(c, shift=0.15 * UP) for c in strip], lag_ratio=0.06),
            run_time=1.3,
        )

        # 8 is hop 3, 16 is hop 4 — arcs above the counter row land on hop 7.
        hop_a = SurroundingRectangle(strip[3][1], color=ACCENT, buff=0.05)
        hop_b = SurroundingRectangle(strip[4][1], color=ACCENT, buff=0.05)
        hop_c = SurroundingRectangle(strip[7][1], color=GOOD, buff=0.05)
        hops = MathTex(
            r"8 \times 16",
            r"\;=\; 2^{3} \cdot 2^{4}",
            r"\;=\; 2^{3+4}",
            r"\;=\; 128",
            font_size=RESULT_SIZE,
        ).move_to(0.75 * DOWN)
        hops[3].set_color(GOOD)
        self.play(Create(hop_a), Create(hop_b))
        self.play(Write(hops[0]), Write(hops[1]))
        self.play(Write(hops[2]))
        self.play(Create(hop_c), Write(hops[3]))
        add_note = caption("hop 3, then hop 4 — seven hops: multiplying values adds counters")
        add_note.next_to(hops, DOWN, buff=0.3)
        self.play(FadeIn(add_note))
        self.wait(1.0)

        # --- the law, the slide rule, the unit ----------------------------------
        self.play(FadeOut(VGroup(strip, hop_a, hop_b, hop_c, hops, add_note, prompt)))
        law = MathTex(
            r"\log_b(xy) = \log_b x + \log_b y", font_size=FORMULA_SIZE, color=ACCENT
        ).move_to(1.5 * UP)
        self.play(Write(law), Create(boxed(law, buff=0.3)))

        slide = VGroup(
            Text("the slide rule made it physical:", font_size=25),
            Text("two log-scaled rulers — sliding one adds lengths,", font_size=25),
            Text("and lengths are logs (Gunter 1620, Oughtred ~1622)", font_size=25),
        ).arrange(DOWN, buff=0.18)
        slide.move_to(0.1 * UP)
        self.play(FadeIn(slide))
        self.wait(0.8)

        unit = VGroup(
            MathTex(r"\log_4 64 = \tfrac{\log_2 64}{\log_2 4} = \tfrac{6}{2} = 3", font_size=36),
            caption("changing base is changing the stride — the base is a unit"),
            caption("ten doublings ≈ three digits (1024 ≈ 1000), which is why log₁₀2 ≈ 0.301"),
            caption("calculus later makes one base natural — that story waits"),
        ).arrange(DOWN, buff=0.24)
        unit.move_to(1.95 * DOWN)
        self.play(Write(unit[0]))
        self.play(LaggedStart(*[FadeIn(u) for u in unit[1:]], lag_ratio=0.25))
        self.wait(2)


class ShrinkCounts(ConceptScene):
    """Probabilities are shrink counts: negative logs fall out of the square."""

    def construct(self):
        self.play(FadeIn(self.title("Shrink Counts"), shift=0.3 * DOWN))

        recall = Text(
            "You have seen this cell before: HHTH, area (1/2)⁴", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))

        # The ChainsOfTrials square, quartered twice — the cell is 4 halvings.
        side = 2.7
        square = Square(side_length=side, stroke_width=3, color=MUTED).move_to(
            2.7 * LEFT + 0.3 * DOWN
        )
        corner = square.get_corner(DL)
        cuts = VGroup(
            *[
                Line(
                    corner + np.array([side * f, 0, 0]),
                    corner + np.array([side * f, side, 0]),
                    color=COOL,
                    stroke_width=2,
                    stroke_opacity=0.7,
                )
                for f in (0.25, 0.5, 0.75)
            ],
            *[
                Line(
                    corner + np.array([0, side * f, 0]),
                    corner + np.array([side, side * f, 0]),
                    color=COOL,
                    stroke_width=2,
                    stroke_opacity=0.7,
                )
                for f in (0.25, 0.5, 0.75)
            ],
        )
        cell = Rectangle(
            width=side / 4,
            height=side / 4,
            stroke_width=0,
            fill_color=ACCENT,
            fill_opacity=0.6,
        ).move_to(corner + np.array([side * 0.375, side * 0.125, 0]))
        self.play(Create(square))
        self.play(Create(cuts, lag_ratio=0.1, run_time=1.2), FadeIn(cell))

        count = VGroup(
            MathTex(r"\left(\tfrac{1}{2}\right)^4 = \tfrac{1}{16}", font_size=40),
            MathTex(r"\log_2 \tfrac{1}{16} = -4", font_size=40, color=ACCENT),
            caption("four halvings — the minus sign is\nthe direction of the count"),
        ).arrange(DOWN, buff=0.35)
        count.next_to(square, RIGHT, buff=0.9)
        self.play(Write(count[0]))
        self.play(Write(count[1]))
        self.play(FadeIn(count[2]))
        self.wait(1.0)

        # --- the strip runs both ways -------------------------------------------
        self.play(FadeOut(VGroup(square, cuts, cell, count, recall)))
        strip = _strip(
            [-3, -2, -1, 0, 1, 2, 3],
            ["1/8", "1/4", "1/2", 1, 2, 4, 8],
            cell_width=1.15,
        ).move_to(1.2 * UP)
        self.play(
            LaggedStart(*[FadeIn(c, shift=0.15 * UP) for c in strip], lag_ratio=0.08),
            run_time=1.2,
        )
        both_ways = caption("the counter row is all of ℤ — growth right, shrinkage left")
        both_ways.next_to(strip, DOWN, buff=0.45)
        self.play(FadeIn(both_ways))

        facts = VGroup(
            Text("pH is the everyday version: −log₁₀ of a tiny concentration", font_size=BODY_SIZE),
            Text(
                "log 0 = −∞: a zero prior sits infinitely far down the ruler", font_size=BODY_SIZE
            ),
            Text(
                "and slow is not bounded — name any N, 2^N sits on the strip", font_size=BODY_SIZE
            ),
        ).arrange(DOWN, buff=0.3)
        facts.move_to(1.5 * DOWN)
        self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.3))
        self.wait(1.2)

        self.play(FadeOut(VGroup(strip, both_ways, facts)))
        takeaway = Text(
            "A negative log is a count of shrinkings — content, not error",
            font_size=27,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class TheEvidenceRuler(ConceptScene):
    """The odds ladder on a base-3 ruler: each head adds exactly the same length."""

    def construct(self):
        self.play(FadeIn(self.title("The Evidence Ruler"), shift=0.3 * DOWN))

        recall = Text(
            "The Bayes coins again: each head multiplies the odds by 9 = 3²",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))

        # The ruler: log3(odds) axis, ticks -2..6, odds labels under key ticks.
        axis = NumberLine(
            x_range=[-2, 6, 1],
            length=10.5,
            color=MUTED,
            include_numbers=True,
            font_size=24,
        ).move_to(0.55 * UP)
        axis_tag = MathTex(r"\log_3(\text{odds})", font_size=30, color=COOL)
        axis_tag.next_to(axis, UP, buff=0.35).align_to(axis, LEFT)
        odds_tags = VGroup(
            *[
                MathTex(tex, font_size=26, color=MUTED).next_to(
                    axis.number_to_point(x), DOWN, buff=0.55
                )
                for x, tex in [(0, r"1{:}1"), (2, r"9{:}1"), (4, r"81{:}1")]
            ]
        )
        self.play(Create(axis), FadeIn(axis_tag))
        self.play(FadeIn(odds_tags))

        marker = Dot(axis.number_to_point(0), radius=0.09, color=ACCENT)
        self.play(FadeIn(marker, scale=0.5))

        def step(frm, to, label, color):
            arc = CurvedArrow(
                axis.number_to_point(frm) + 0.15 * UP,
                axis.number_to_point(to) + 0.15 * UP,
                angle=-1.1,
                color=color,
                stroke_width=3.5,
                tip_length=0.18,
            )
            tag = Text(label, font_size=SMALL_SIZE, color=color)
            tag.next_to(arc, UP, buff=0.12)
            return arc, tag

        arc1, tag1 = step(0, 2, "H: +2", GOOD)
        self.play(Create(arc1), FadeIn(tag1), marker.animate.move_to(axis.number_to_point(2)))
        arc2, tag2 = step(2, 4, "H: +2", GOOD)
        self.play(Create(arc2), FadeIn(tag2), marker.animate.move_to(axis.number_to_point(4)))
        same = Text(
            "each head adds the same length — evidence is a distance",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).move_to(1.8 * DOWN)
        self.play(FadeIn(same))
        self.wait(0.8)

        arc3, tag3 = step(4, 2, "T: −2", WARM)
        self.play(Create(arc3), FadeIn(tag3), marker.animate.move_to(axis.number_to_point(2)))
        arc4, tag4 = step(2, 0, "T: −2", WARM)
        self.play(Create(arc4), FadeIn(tag4), marker.animate.move_to(axis.number_to_point(0)))
        cancel = caption("two heads out, two tails back — the marker returns to exactly 0")
        cancel.next_to(same, DOWN, buff=0.3)
        self.play(FadeIn(cancel))
        self.wait(0.9)

        deciban = caption(
            "Turing weighed evidence this way — decibans; about one deciban is\n"
            "the smallest weight a person can feel"
        )
        deciban.next_to(cancel, DOWN, buff=0.3)
        self.play(FadeIn(deciban))
        self.wait(0.9)

        stage = VGroup(
            axis,
            axis_tag,
            odds_tags,
            marker,
            arc1,
            tag1,
            arc2,
            tag2,
            arc3,
            tag3,
            arc4,
            tag4,
            same,
            cancel,
            deciban,
            recall,
        )
        self.play(FadeOut(stage))
        takeaway = Text(
            "On a log ruler, updating is walking — evidence adds",
            font_size=28,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class TheUnderflowCliff(ConceptScene):
    """Products die at float's floor; sums of logs walk on forever."""

    def construct(self):
        self.play(FadeIn(self.title("The Underflow Cliff"), shift=0.3 * DOWN))

        recall = Text(
            "CTC multiplies one probability per frame. Frames add up.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))

        # --- the cliff -----------------------------------------------------------
        cliff = VGroup(
            MathTex(r"0.1^{323} = 1\times 10^{-323}\quad\checkmark", font_size=38),
            MathTex(r"0.1^{324} = 0.0\ \text{exactly}\quad\times", font_size=38, color=WARM),
            caption("float64's floor is 2⁻¹⁰⁷⁴ ≈ 5×10⁻³²⁴ — one more frame and the"),
            caption("product is not small, it is GONE (float32 dies at 46 frames)"),
        ).arrange(DOWN, buff=0.3)
        cliff.move_to(0.85 * UP)
        self.play(Write(cliff[0]))
        self.play(Write(cliff[1]))
        self.play(FadeIn(cliff[2]), FadeIn(cliff[3]))
        graves = caption(
            'Graves, on the CTC recursions: they "soon lead to underflows on any digital computer"'
        ).next_to(cliff, DOWN, buff=0.4)
        self.play(FadeIn(graves))
        self.wait(1.0)

        walker = MathTex(
            r"\sum_{t=1}^{324} \log_{10}(0.1) = -324\ \text{exactly}",
            font_size=40,
            color=GOOD,
        ).move_to(1.75 * DOWN)
        walk_note = caption("the counter row never falls off anything")
        walk_note.next_to(walker, DOWN, buff=0.28)
        self.play(Write(walker))
        self.play(FadeIn(walk_note))
        self.wait(1.0)

        # --- the one thing log space loses, restored ----------------------------
        self.play(FadeOut(VGroup(cliff, graves, walker, walk_note, recall)))
        need = Text(
            "But the trellis ADDS α's — and log space cannot add by adding.",
            font_size=BODY_SIZE,
        ).move_to(1.7 * UP)
        self.play(FadeIn(need))
        lse = MathTex(
            r"\ln(a + b) = \ln a + \ln\!\left(1 + e^{\ln b - \ln a}\right) \quad (a \ge b)",
            font_size=44,
            color=ACCENT,
        ).move_to(0.7 * UP)
        exact_bit = MathTex(
            r"\log_2(2^{-10} + 2^{-10}) = -9\ \text{exactly}", font_size=36
        ).next_to(lse, DOWN, buff=0.4)
        safe = caption(
            "the convention a ≥ b makes a the max — it factors out, and the\n"
            "shifted term lives in (0, 1]: nothing can overflow"
        )
        safe.next_to(exact_bit, DOWN, buff=0.3)
        attribution = caption(
            "the 2006 CTC paper rescaled (Rabiner-style); log space is the 2012 book,"
        )
        attribution2 = caption('which calls rescaling "less robust" — credit where it is due')
        attribution.next_to(safe, DOWN, buff=0.28)
        attribution2.next_to(attribution, DOWN, buff=0.18)
        lse_box = boxed(lse, buff=0.3)
        self.play(Write(lse), Create(lse_box))
        self.play(Write(exact_bit))
        self.play(FadeIn(safe))
        self.play(FadeIn(attribution), FadeIn(attribution2))
        self.wait(1.2)

        self.play(FadeOut(VGroup(need, lse, exact_bit, safe, attribution, attribution2, lse_box)))
        wild = caption(
            "the same ruler everywhere the world multiplies: decibels, pH,\n"
            "earthquake magnitudes, semitones — and every per-frame product"
        ).move_to(0.9 * UP)
        takeaway = Text(
            "Whenever the world multiplies and you would rather add — take logs",
            font_size=26,
        ).move_to(0.5 * DOWN)
        self.play(FadeIn(wild))
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
