"""e and the natural logarithm — the base whose stride is exactly 1.

Six scenes closing the repo's oldest on-screen debt: `algebra/`'s strip
promised that calculus makes one base natural, and `TheUnderflowCliff`
rendered ln before any series taught it. Compounding poses the question
(a ceiling between 2 and 3), the zoom builds an honest local growth
rate, the mystery constants obey the strip's laws before they are named
as ln, and the payoffs run from e^(rt) to the log-add identity re-read.

    TheSplitYear         Bernoulli's split year; the table crowds a ceiling
    ZoomUntilStraight    slope, three honest beats; the readout settles
    TheMysteryConstants  0.6931, 1.0986 — and base 8's is three of base 2's
    TheNaturalStride     ln is the counter row in nature's units; the bridge
    RateTimesTime        e^(rt); 69.3 vs 72; ln as time-to-grow
    TheDebtRepaid        the underflow identity re-read; the inverse graph

Every number on screen traces to plan 006's verified anchors; slope
tables are the one-sided ratio (the symmetric quotient's rows differ
visibly, and float cancellation bends it below h = 1e-5 — the recorded
hazard).

Render:
    uv run python calculus/e_and_ln_manim.py
    uv run python calculus/e_and_ln_manim.py -s TheSplitYear -q draft
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


def _strip(counters, values, cell_width=1.15, highlight=()):
    """The two-row strip from `algebra/`: a counter row (COOL) over values.

    Reprised here on purpose — scene 4's whole claim is that this exact
    device was secretly ruled in natural units all along. ``highlight``
    marks columns whose value cell gets the ACCENT frame.
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


class TheSplitYear(ConceptScene):
    """Split one year of 100% growth into smaller hops; a ceiling appears."""

    def construct(self):
        self.play(FadeIn(self.title("The Split Year"), shift=0.3 * DOWN))

        promise = caption('algebra/ left a promise on the strip: "calculus later')
        promise2 = caption('makes one base natural — that story waits." The wait ends here.')
        promise.next_to(self.head, DOWN, buff=0.3)
        promise2.next_to(promise, DOWN, buff=0.15)
        self.play(FadeIn(promise), FadeIn(promise2))
        self.wait(0.8)

        question = Text(
            "Jacob Bernoulli, 1683: $1 grows at 100% for one year.",
            font_size=BODY_SIZE,
        ).move_to(1.6 * UP)
        self.play(FadeIn(question))

        # One hop, then the year splits into more, smaller multiplicative hops.
        splits = VGroup(
            MathTex(r"1\ \text{hop}:\ (1+1)^{1} = 2", font_size=38),
            MathTex(r"2\ \text{hops}:\ \left(1+\tfrac{1}{2}\right)^{2} = 2.25", font_size=38),
            MathTex(r"4\ \text{hops}:\ \left(1+\tfrac{1}{4}\right)^{4} = 2.4414", font_size=38),
            MathTex(r"12\ \text{hops}:\ \left(1+\tfrac{1}{12}\right)^{12} = 2.6130", font_size=38),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        splits.move_to(2.6 * LEFT + 0.35 * DOWN)
        self.play(LaggedStart(*[Write(s) for s in splits], lag_ratio=0.35), run_time=3.0)
        interest = caption("each split: the interest starts earning interest sooner")
        interest.next_to(splits, DOWN, buff=0.35)
        self.play(FadeIn(interest))
        self.wait(0.8)

        # Two wrong intuitions, raced — the table kills both.
        guess_up = Text("more hops → endless money?", font_size=BODY_SIZE, color=WARM)
        guess_down = Text("1 + 1/n → 1, so the power → 1?", font_size=BODY_SIZE, color=WARM)
        guesses = VGroup(guess_up, guess_down).arrange(DOWN, buff=0.3)
        guesses.move_to(3.3 * RIGHT + 0.35 * DOWN)
        self.play(FadeIn(guess_up, shift=0.2 * UP))
        self.play(FadeIn(guess_down, shift=0.2 * DOWN))
        self.wait(1.0)

        self.play(FadeOut(VGroup(question, splits, interest, guesses, promise, promise2)))

        # The table crowds a ceiling: dots climb, the dashed line is unnamed.
        ns = ["1", "2", "4", "12", "52", "365", "8760"]
        vals = [2.0, 2.25, 2.4414, 2.6130, 2.6926, 2.7146, 2.7181]
        labels = ["2", "2.25", "2.4414", "2.6130", "2.6926", "2.7146", "2.7181"]
        e_val = 2.7183

        def height(v):
            return (v - 2.0) / (e_val - 2.0) * 2.9 - 1.6

        columns = VGroup()
        for i, (n, v, s) in enumerate(zip(ns, vals, labels, strict=True)):
            x = -4.8 + i * 1.6
            dot = Dot([x, height(v), 0], color=COOL)
            # The last three labels hang below their dots: nothing may sit
            # above the ceiling line, or the picture contradicts the claim.
            side = DOWN if v > 2.65 else UP
            val = Text(s, font_size=SMALL_SIZE).next_to(dot, side, buff=0.14)
            n_tag = Text(n, font_size=SMALL_SIZE, color=MUTED).move_to([x, -2.15, 0])
            columns.add(VGroup(dot, val, n_tag))
        n_label = Text("hops:", font_size=SMALL_SIZE, color=MUTED)
        n_label.next_to(columns[0][2], LEFT, buff=0.35)
        ceiling = DashedLine([-5.4, height(e_val), 0], [5.6, height(e_val), 0], color=ACCENT)
        ceiling_tag = MathTex(r"?", font_size=44, color=ACCENT)
        ceiling_tag.next_to(ceiling, RIGHT, buff=0.15)
        self.play(FadeIn(n_label))
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in columns], lag_ratio=0.2))
        self.play(Create(ceiling), FadeIn(ceiling_tag))
        crowd = caption("always climbing, never past 3 — Bernoulli proved the ceiling")
        crowd2 = caption("sits between 2 and 3, and never named it")
        crowd.move_to(2.7 * DOWN)
        crowd2.next_to(crowd, DOWN, buff=0.15)
        self.play(FadeIn(crowd), FadeIn(crowd2))
        self.wait(1.2)

        first = Text(
            "The first number in history defined as a limit",
            font_size=26,
        ).move_to(2.85 * DOWN)
        self.play(FadeOut(crowd), FadeOut(crowd2))
        self.play(FadeIn(first, shift=0.2 * UP), Create(boxed(first, buff=0.28)))
        self.wait(2)


class ZoomUntilStraight(ConceptScene):
    """Zoom until the curve is straight, and the slope readout settles."""

    def construct(self):
        self.play(FadeIn(self.title("Zoom Until Straight"), shift=0.3 * DOWN))

        prompt = Text("How fast is 2ˣ growing, right here at x = 0?", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        self.play(FadeIn(prompt))

        # Three zoom panels: the same curve over a shrinking span, stretched to
        # the same width — curvature dies, the dashed chord closes the gap.
        def panel(span, center, zoom_label):
            width, height_u = 3.1, 2.0

            def to_point(t):
                y = (2.0**t - 2.0**-span) / (2.0**span - 2.0**-span) - 0.5
                return center + RIGHT * (t / span) * (width / 2) + UP * y * height_u

            curve = ParametricFunction(
                to_point, t_range=[-span, span, span / 40], color=COOL, stroke_width=4
            )
            chord = DashedLine(to_point(-span), to_point(span), color=MUTED)
            frame = RoundedRectangle(
                width=width + 0.5,
                height=height_u + 0.7,
                corner_radius=0.12,
                stroke_width=2,
                color=MUTED,
            ).move_to(center)
            tag = caption(zoom_label).next_to(frame, DOWN, buff=0.18)
            return VGroup(frame, chord, curve, tag)

        panels = VGroup(
            panel(1.0, 4.1 * LEFT + 0.55 * UP, "zoom ×1"),
            panel(0.25, 0.0 * RIGHT + 0.55 * UP, "zoom ×4"),
            panel(0.0625, 4.1 * RIGHT + 0.55 * UP, "zoom ×16"),
        )
        self.play(LaggedStart(*[FadeIn(p, shift=0.2 * UP) for p in panels], lag_ratio=0.35))
        straight = caption("zoomed far enough, a smooth curve is straight — so")
        straight2 = caption('"the slope right here" is a number you can read off')
        straight.move_to(2.0 * DOWN)
        straight2.next_to(straight, DOWN, buff=0.15)
        self.play(FadeIn(straight), FadeIn(straight2))
        self.wait(1.2)

        # The readout: rise over run with dt a real number, settling.
        self.play(FadeOut(VGroup(panels, straight, straight2)))
        ratio = MathTex(r"\frac{2^{dt} - 1}{dt}", font_size=48).move_to(4.6 * LEFT + 0.3 * UP)
        rows = VGroup(
            MathTex(r"dt = 1:\quad 1.0", font_size=36),
            MathTex(r"dt = 0.1:\quad 0.7177", font_size=36),
            MathTex(r"dt = 0.01:\quad 0.6956", font_size=36),
            MathTex(r"dt = 0.001:\quad 0.69339", font_size=36),
        ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        rows.move_to(0.9 * LEFT + 0.3 * UP)
        settle = MathTex(r"\rightarrow\ 0.6931\ldots", font_size=44, color=ACCENT)
        settle.move_to(3.6 * RIGHT + 0.3 * UP)
        self.play(Write(ratio))
        self.play(LaggedStart(*[Write(r) for r in rows], lag_ratio=0.35), run_time=2.6)
        self.play(Write(settle))
        honest = caption('the readout settles — no "instant" needed, just as')
        honest2 = caption("close-up as you like; dt stays a real number throughout")
        honest.move_to(1.6 * DOWN)
        honest2.next_to(honest, DOWN, buff=0.15)
        self.play(FadeIn(honest), FadeIn(honest2))
        self.wait(1.2)

        # One strip-law step: a hop is the same length everywhere.
        self.play(FadeOut(VGroup(ratio, rows, settle, honest, honest2, prompt)))
        law = MathTex(r"2^{x + dt} = 2^{x} \cdot 2^{dt}", font_size=RESULT_SIZE)
        law.move_to(1.3 * UP)
        hop_note = caption("the product law again: a hop is the same length everywhere,")
        hop_note2 = caption("so what happens at 0 happens at every x — scaled by the height")
        hop_note.next_to(law, DOWN, buff=0.35)
        hop_note2.next_to(hop_note, DOWN, buff=0.15)
        self.play(Write(law))
        self.play(FadeIn(hop_note), FadeIn(hop_note2))
        slope = MathTex(
            r"\text{slope of } 2^{x} \text{ at } x \;=\; 2^{x} \times 0.6931\ldots",
            font_size=44,
            color=ACCENT,
        ).move_to(1.0 * DOWN)
        prop = caption("growth rate proportional to amount — the constant is the slope at 0")
        prop.next_to(slope, DOWN, buff=0.5)
        self.play(Write(slope), Create(boxed(slope, buff=0.3)))
        self.play(FadeIn(prop))
        self.wait(2)


class TheMysteryConstants(ConceptScene):
    """Each base grows at a constant times itself — and the constants obey the strip."""

    def construct(self):
        self.play(FadeIn(self.title("The Mystery Constants"), shift=0.3 * DOWN))

        prompt = Text(
            "Measure the slope at 0 for other bases. A pattern appears.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # A categorical lineup: four bases, four constants, no ranking.
        lineup = VGroup(
            MathTex(r"2^{x}:\ 0.6931", font_size=42, color=palette(0)),
            MathTex(r"3^{x}:\ 1.0986", font_size=42, color=palette(1)),
            MathTex(r"8^{x}:\ 2.0794", font_size=42, color=palette(2)),
            MathTex(r"10^{x}:\ 2.3026", font_size=42, color=palette(3)),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        lineup.move_to(3.4 * LEFT + 0.35 * DOWN)
        self.play(LaggedStart(*[Write(row) for row in lineup], lag_ratio=0.3), run_time=2.6)
        self.wait(0.6)

        spot = MathTex(r"2.0794 = 3 \times 0.6931", font_size=40).move_to(2.9 * RIGHT + 0.25 * UP)
        spot2 = MathTex(r"8 = 2^{3}", font_size=40).next_to(spot, DOWN, buff=0.3)
        stride_note = caption("three doublings — three strides: the constants obey")
        stride_note2 = caption("the strip's own law before anyone has named them")
        stride_note.next_to(spot2, DOWN, buff=0.4)
        stride_note2.next_to(stride_note, DOWN, buff=0.15)
        self.play(Write(spot))
        self.play(Write(spot2))
        self.play(FadeIn(stride_note), FadeIn(stride_note2))
        unit_line = Text(
            "They are stride lengths — in a unit nobody has disclosed.",
            font_size=BODY_SIZE,
        ).move_to(2.5 * DOWN)
        self.play(FadeIn(unit_line))
        self.wait(1.2)

        # The squeeze: between 2 and 3 sits the base whose constant is 1.
        self.play(
            FadeOut(VGroup(prompt, lineup, spot, spot2, stride_note, stride_note2, unit_line))
        )
        squeeze = MathTex(r"0.6931 \;<\; 1 \;<\; 1.0986", font_size=RESULT_SIZE).move_to(1.5 * UP)
        between = Text(
            "Between 2 and 3 sits the base whose constant is exactly 1.",
            font_size=BODY_SIZE,
        ).next_to(squeeze, DOWN, buff=0.4)
        self.play(Write(squeeze))
        self.play(FadeIn(between))
        e_rows = VGroup(
            MathTex(r"\frac{e^{dt}-1}{dt}:\quad 1.0517,\ \ 1.0050,\ \ 1.0005", font_size=36),
            MathTex(r"\rightarrow\ 1\ \text{exactly}", font_size=36, color=GOOD),
        ).arrange(RIGHT, buff=0.5)
        e_rows.move_to(0.35 * DOWN)
        self.play(Write(e_rows[0]))
        self.play(Write(e_rows[1]))
        named = MathTex(r"e = 2.718281828459\ldots", font_size=RESULT_SIZE, color=ACCENT)
        named.move_to(1.6 * DOWN)
        ceiling_back = caption("the ceiling from the split year — back, from a different question")
        ceiling_back.next_to(named, DOWN, buff=0.5)
        not_big = caption("e is not big (3ˣ outruns eˣ) — e is the self-paced base:")
        not_big2 = caption("its growth rate is its own height")
        not_big.next_to(ceiling_back, DOWN, buff=0.3)
        not_big2.next_to(not_big, DOWN, buff=0.15)
        self.play(Write(named), Create(boxed(named, buff=0.3)))
        self.play(FadeIn(ceiling_back))
        self.play(FadeIn(not_big), FadeIn(not_big2))
        self.wait(2)


class TheNaturalStride(ConceptScene):
    """The unit disclosed: ln is the counter row in nature's units."""

    def construct(self):
        self.play(FadeIn(self.title("The Natural Stride"), shift=0.3 * DOWN))

        naming = MathTex(
            r"\text{slope of } b^{x} \text{ at } 0 \;=\; \log_e b \;=\; \ln b",
            font_size=44,
            color=ACCENT,
        ).next_to(self.head, DOWN, buff=0.45)
        naming_box = boxed(naming, buff=0.3)
        disclosed = caption("the undisclosed unit was the e-stride: change of base, one step —")
        disclosed2 = caption("0.6931 = ln 2, 1.0986 = ln 3, 2.0794 = ln 8 = 3 ln 2")
        disclosed.next_to(naming, DOWN, buff=0.5)
        disclosed2.next_to(disclosed, DOWN, buff=0.15)
        self.play(Write(naming), Create(naming_box))
        self.play(FadeIn(disclosed), FadeIn(disclosed2))
        self.wait(1.0)

        # The strip returns, ruled in its native unit.
        strip = _strip(
            ["0", "0.693", "1", "1.386", "2.079"],
            ["1", "2", "e", "4", "8"],
            cell_width=1.3,
            highlight=(2,),
        )
        strip.scale(0.95).move_to(0.55 * DOWN)
        native = caption("ln is the counter row in nature's units — every log you have")
        native2 = caption("met was this row, read in a stretched unit")
        native.next_to(strip, DOWN, buff=0.4)
        native2.next_to(native, DOWN, buff=0.15)
        self.play(
            LaggedStart(*[FadeIn(c, shift=0.15 * UP) for c in strip], lag_ratio=0.1),
            run_time=1.4,
        )
        self.play(FadeIn(native), FadeIn(native2))
        self.wait(1.2)

        # A tiny hop costs about its own size in strides.
        self.play(
            FadeOut(VGroup(naming, naming_box, disclosed, disclosed2, strip, native, native2))
        )
        tiny = VGroup(
            MathTex(r"\ln 1.1 = 0.0953", font_size=38),
            MathTex(r"\ln 1.01 = 0.0099503", font_size=38),
            MathTex(r"\ln 1.001 = 0.0009995", font_size=38),
        ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        tiny.move_to(3.3 * LEFT + 1.35 * UP)
        approx = MathTex(r"\ln(1+x) \approx x", font_size=44).move_to(2.9 * RIGHT + 1.35 * UP)
        small_print = caption("one tiny hop costs about its own size in natural strides")
        small_print2 = caption("(honest below x ≈ 0.1 — the error grows like x²/2)")
        small_print.move_to(0.15 * DOWN)
        small_print2.next_to(small_print, DOWN, buff=0.15)
        self.play(LaggedStart(*[Write(t) for t in tiny], lag_ratio=0.3), run_time=2.2)
        self.play(Write(approx))
        self.play(FadeIn(small_print), FadeIn(small_print2))
        self.wait(1.0)

        # The bridge: the ceiling's natural counter is exactly 1.
        bridge = MathTex(
            r"\ln\!\left(\left(1+\tfrac{1}{n}\right)^{n}\right)"
            r" = n \ln\!\left(1+\tfrac{1}{n}\right)"
            r" \approx n \cdot \tfrac{1}{n} = 1",
            font_size=40,
            color=ACCENT,
        ).move_to(1.35 * DOWN)
        bridge_box = boxed(bridge, buff=0.28)
        walked = caption("n = 10, 100, 1000: 0.9531, 0.99503, 0.99950 → 1 — the ceiling's")
        walked2 = caption("natural counter is exactly 1: both definitions of e are one number")
        walked3 = caption("(that the meeting is guaranteed is analysis — here it is watched)")
        walked.next_to(bridge, DOWN, buff=0.45)
        walked2.next_to(walked, DOWN, buff=0.15)
        walked3.next_to(walked2, DOWN, buff=0.15)
        self.play(Write(bridge), Create(bridge_box))
        self.play(FadeIn(walked), FadeIn(walked2))
        self.play(FadeIn(walked3))
        self.wait(2)


class RateTimesTime(ConceptScene):
    """Growth has one dial — rate times time — and e is its unit."""

    def construct(self):
        self.play(FadeIn(self.title("Rate Times Time"), shift=0.3 * DOWN))

        dial = MathTex(r"e^{rt}", font_size=FORMULA_SIZE, color=ACCENT)
        dial.next_to(self.head, DOWN, buff=0.45)
        dial_box = boxed(dial, buff=0.32)
        merge = MathTex(r"e^{0.03 \times 10} = e^{0.3}", font_size=40).next_to(dial, DOWN, buff=0.5)
        merge_note = caption("10 years at 3% is one year at 30% — the dial's two knobs multiply")
        merge_note.next_to(merge, DOWN, buff=0.25)
        self.play(Write(dial), Create(dial_box))
        self.play(Write(merge))
        self.play(FadeIn(merge_note))
        self.wait(0.8)

        double = MathTex(
            r"e^{rt} = 2 \;\iff\; rt = \ln 2 = 0.6931\ldots",
            font_size=40,
        ).move_to(0.35 * DOWN)
        at_five = MathTex(
            r"r = 5\%:\quad t = \tfrac{0.693}{0.05} = 13.86\ \text{years}",
            font_size=38,
            color=GOOD,
        ).next_to(double, DOWN, buff=0.35)
        rule_note = caption("69.3 is the mathematics; 72 is the convention with friendlier")
        rule_note2 = caption("divisors (it answers 14.4) — keep the two numbers apart")
        rule_note.next_to(at_five, DOWN, buff=0.3)
        rule_note2.next_to(rule_note, DOWN, buff=0.15)
        self.play(Write(double))
        self.play(Write(at_five))
        self.play(FadeIn(rule_note), FadeIn(rule_note2))
        self.wait(1.2)

        self.play(FadeOut(VGroup(merge, merge_note, double, at_five, rule_note, rule_note2)))
        grow = MathTex(
            r"e^{3} = 20.0855 \quad\Longleftrightarrow\quad \ln 20.08 = 2.99972",
            font_size=40,
        ).move_to(0.55 * UP)
        grow_note = caption("ln answers: how long, in natural units, to grow that much?")
        grow_note.next_to(grow, DOWN, buff=0.3)
        self.play(Write(grow))
        self.play(FadeIn(grow_note))
        self.wait(0.8)

        ledger = MathTex(
            r"\left(1+\tfrac{0.05}{365}\right)^{365} = 1.0512675"
            r"\qquad e^{0.05} = 1.0512711",
            font_size=36,
        ).move_to(0.9 * DOWN)
        ledger_note = caption("Bernoulli's ledger, closed: a year of daily 5% is already")
        ledger_note2 = caption("within 3.6 × 10⁻⁶ of the limit — the ceiling is a working tool")
        ledger_note.next_to(ledger, DOWN, buff=0.3)
        ledger_note2.next_to(ledger_note, DOWN, buff=0.15)
        self.play(Write(ledger))
        self.play(FadeIn(ledger_note), FadeIn(ledger_note2))
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(dial, dial_box, grow, grow_note, ledger, ledger_note, ledger_note2))
        )
        takeaway = Text(
            "Growth has one dial — rate × time — and e is its unit",
            font_size=27,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class TheDebtRepaid(ConceptScene):
    """The underflow identity re-read, and the inverse graph earned at last."""

    def construct(self):
        self.play(FadeIn(self.title("The Debt Repaid"), shift=0.3 * DOWN))

        recall = Text("The repo's oldest forward reference —", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        recall2 = Text("rendered before ln meant anything:", font_size=BODY_SIZE).next_to(
            recall, DOWN, buff=0.15
        )
        self.play(FadeIn(recall), FadeIn(recall2))

        identity = MathTex(
            r"\ln(a + b) = \ln a + \ln\!\left(1 + e^{\ln b - \ln a}\right)",
            font_size=44,
            color=ACCENT,
        ).move_to(1.15 * UP)
        identity_box = boxed(identity, buff=0.3)
        self.play(Write(identity), Create(identity_box))
        reads = VGroup(
            caption("ln — the natural counter row, nature's stride"),
            caption("e to a counter — undo, never cancel: the same number, other corner"),
            caption("1 + e^(ln b − ln a) — the small term, kept safe inside (0, 1]"),
        ).arrange(DOWN, buff=0.2)
        reads.move_to(0.55 * DOWN)
        self.play(LaggedStart(*[FadeIn(r) for r in reads], lag_ratio=0.4), run_time=2.2)
        earned = Text(
            "Every symbol on the cliff rope now means something.",
            font_size=BODY_SIZE,
        ).move_to(2.0 * DOWN)
        self.play(FadeIn(earned))
        self.wait(1.2)

        # The cliff's own scale: the naive route dies, the identity survives.
        self.play(FadeOut(VGroup(recall, recall2, reads, earned)))
        naive = MathTex(
            r"\text{float64: } 1 + e^{-40} = 1.0\ \text{exactly}"
            r"\ \Rightarrow\ \log(1+e^{-40}) = 0.0\quad\times",
            font_size=36,
            color=WARM,
        ).move_to(0.1 * UP)
        survives = MathTex(
            r"\ln\!\left(1+e^{-40}\right) = 4.248\times 10^{-18}\quad\checkmark",
            font_size=36,
            color=GOOD,
        ).next_to(naive, DOWN, buff=0.35)
        cliff_note = caption("the underflow cliff again — the identity is how the value survives")
        cliff_note.next_to(survives, DOWN, buff=0.3)
        self.play(Write(naive))
        self.play(Write(survives))
        self.play(FadeIn(cliff_note))
        self.wait(1.2)

        # The promised payoff, last: the inverse graph, earned.
        self.play(FadeOut(VGroup(identity, identity_box, naive, survives, cliff_note)))
        axes = Axes(
            x_range=[-1.5, 4.2, 1],
            y_range=[-1.5, 4.2, 1],
            x_length=6.4,
            y_length=5.0,
            tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 2},
        ).move_to(2.6 * LEFT + 0.45 * DOWN)
        exp_curve = axes.plot(lambda x: np.exp(x), x_range=[-1.5, 1.42], color=COOL)
        self.play(Create(axes), Create(exp_curve))
        point = Dot(axes.coords_to_point(0.693, 2.0), color=ACCENT)
        point_tag = MathTex(r"\ln 2 = 0.693", font_size=32, color=ACCENT)
        point_tag.next_to(point, LEFT, buff=0.2)
        one_at_a_time = caption("the input that reaches 2 —")
        one_at_a_time2 = caption("the inverse, one point at a time")
        one_at_a_time.move_to(3.8 * RIGHT + 1.9 * UP)
        one_at_a_time2.next_to(one_at_a_time, DOWN, buff=0.15)
        self.play(FadeIn(point, scale=0.5), Write(point_tag))
        self.play(FadeIn(one_at_a_time), FadeIn(one_at_a_time2))
        self.wait(0.8)

        mirror = DashedLine(
            axes.coords_to_point(-1.5, -1.5), axes.coords_to_point(4.2, 4.2), color=MUTED
        )
        ln_curve = axes.plot(lambda x: np.log(x), x_range=[0.23, 4.2], color=GOOD)
        payoff = caption("the flip algebra/ deferred —")
        payoff2 = caption("arriving as a payoff, never the definition")
        payoff.next_to(one_at_a_time2, DOWN, buff=0.35)
        payoff2.next_to(payoff, DOWN, buff=0.15)
        self.play(Create(mirror))
        self.play(Create(ln_curve))
        self.play(FadeIn(payoff), FadeIn(payoff2))
        euler = caption("the name is Euler's: a letter in 1731,")
        euler2 = caption("print in 1736, 18 places by 1748")
        euler.next_to(payoff2, DOWN, buff=0.35)
        euler2.next_to(euler, DOWN, buff=0.15)
        self.play(FadeIn(euler), FadeIn(euler2))
        self.wait(1.0)

        takeaway = Text(
            "e is the base whose stride is 1 — nature's unit for growth",
            font_size=26,
        ).move_to(3.35 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.24)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
