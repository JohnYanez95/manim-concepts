"""Softmax and likelihood — one table read two ways, and the machine that fills it.

The bridge series the CTC topic deferred: likelihood as the row lens
on a table the viewer already owns, the peak as the best explanation,
the log as the native scale of accumulating evidence, softmax as the
exp-then-normalize machine forced by shift invariance, temperature and
the base-change answer to "why e", and NLL — the loss that trains the
machine — as a visible gap on the log-sum-exp ruler.

    TheLikelihoodLens      probability and likelihood: one table, two lenses
    TheBestExplanation     the row's peak names the best parameter — MLE
    AddToSurvive           log the likelihood: same peak, additive arithmetic
    TheProbabilityMachine  exp-then-normalize, forced by shift invariance
    TurningTheDial         soft argmax, temperature, why e, the caveat
    TheLossThatTrains      NLL as the LSE gap; independent frames add

Every number on screen traces to plan 008's verified anchors (main
report + addendum); probability arithmetic there ran in exact
fractions, and display roundings are forced manually.

Render:
    uv run python probability/softmax_likelihood_manim.py
    uv run python probability/softmax_likelihood_manim.py -s TheLikelihoodLens -q draft
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
    chip,
    on_frame,
    render_cli,
)

# The two-lens table, P(k | n=4, p) for p = 1/4, 1/2, 3/4 — exact
# fractions over 256 (plan 008 addendum A2), stored as floats for bar
# heights only; every displayed number is written out by hand.
TABLE_P = ["1/4", "1/2", "3/4"]
TABLE_COLS = [
    [81 / 256, 108 / 256, 54 / 256, 12 / 256, 1 / 256],
    [16 / 256, 64 / 256, 96 / 256, 64 / 256, 16 / 256],
    [1 / 256, 12 / 256, 54 / 256, 108 / 256, 81 / 256],
]

# The softmax workhorse z = (2, 1, 0) at temperatures 1, 0.5, 2, and
# its base-2 reading — display values from the verifier's anchors.
SOFTMAX_T1 = [0.6652, 0.2447, 0.0900]
SOFTMAX_T_HALF = [0.8668, 0.1173, 0.0159]
SOFTMAX_T2 = [0.5065, 0.3072, 0.1863]
SOFTMAX_BASE2 = [4 / 7, 2 / 7, 1 / 7]


def _prob_bars(values, tags, bar_width=0.42, gap=0.2, unit=3.0, color=MUTED):
    """Vertical probability bars over small tags, growing from y = 0.

    ``values`` are heights as fractions of ``unit``; the group is built
    around x = 0 and repositioned by the caller. Bars carry no value
    labels — scenes add the numbers they want spoken.
    """
    bars = VGroup()
    span = (len(values) - 1) * (bar_width + gap)
    for i, (v, tag) in enumerate(zip(values, tags, strict=True)):
        x = i * (bar_width + gap) - span / 2
        bar = Rectangle(
            width=bar_width,
            height=max(v * unit, 0.02),
            stroke_width=2,
            color=color,
            fill_color=color,
            fill_opacity=0.35,
        )
        bar.move_to([x, max(v * unit, 0.02) / 2, 0])
        label = Text(tag, font_size=SMALL_SIZE, color=MUTED).move_to([x, -0.3, 0])
        bars.add(VGroup(bar, label))
    return bars


def _likelihood_axes(y_max=0.45, y_step=0.15, x_length=6.2, y_length=3.2):
    """Axes for the p ∈ [0, 1] likelihood curve, quarters marked."""
    ax = Axes(
        x_range=[0, 1, 0.25],
        y_range=[0, y_max, y_step],
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": True},
    )
    return ax


class TheLikelihoodLens(ConceptScene):
    """Probability and likelihood are one table read two ways."""

    def construct(self):
        self.play(FadeIn(self.title("The Likelihood Lens"), shift=0.3 * DOWN))

        opening = Text(
            "Distributions answered: given the coin, what data? Reverse it.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # Three sorted-square pmfs side by side: the two-lens table.
        groups = VGroup()
        headers = VGroup()
        for idx, (p_label, col) in enumerate(zip(TABLE_P, TABLE_COLS, strict=True)):
            bars = _prob_bars(col, [str(k) for k in range(5)], unit=4.2)
            bars.move_to([-4.35 + idx * 4.35, -1.7, 0], aligned_edge=DOWN)
            head = MathTex(rf"p = \tfrac{{{p_label[0]}}}{{{p_label[2]}}}", font_size=34, color=COOL)
            head.move_to([-4.35 + idx * 4.35, 1.25, 0])
            groups.add(bars)
            headers.add(head)
        known = caption("n = 4 flips; the columns you sorted out of the square")
        known.move_to(2.6 * DOWN)
        self.play(FadeIn(known))
        self.play(
            LaggedStart(*[FadeIn(g) for g in groups], lag_ratio=0.2),
            LaggedStart(*[FadeIn(h) for h in headers], lag_ratio=0.2),
        )
        self.wait(0.6)

        # Column lens: pin the coin, sweep the data — a pmf.
        col_frame = SurroundingRectangle(groups[1], color=COOL, buff=0.18, corner_radius=0.1)
        self.play(FadeOut(opening))
        column_read = Text(
            "Pin the coin, sweep the data: a pmf — every column sums to 1.",
            font_size=BODY_SIZE,
            color=COOL,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(column_read), Create(col_frame))
        self.wait(1.0)

        # Row lens: pin the observed data, sweep the coin.
        self.play(FadeOut(column_read), FadeOut(col_frame))
        row_read = Text(
            "Now pin the data — three heads in four flips — and sweep the coin.",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(row_read))
        row_bars = VGroup(*[g[3][0] for g in groups])
        others = VGroup(*[g[k][0] for g in groups for k in range(5) if k != 3])
        row_values = VGroup(
            *[
                MathTex(v, font_size=30, color=ACCENT).next_to(bar, UP, buff=0.12)
                for bar, v in zip(
                    row_bars, [r"\tfrac{3}{64}", r"\tfrac{1}{4}", r"\tfrac{27}{64}"], strict=True
                )
            ]
        )
        self.play(
            others.animate.set_opacity(0.18),
            *[bar.animate.set_color(ACCENT) for bar in row_bars],
        )
        self.play(LaggedStart(*[FadeIn(v, shift=0.15 * UP) for v in row_values], lag_ratio=0.2))
        row_sum = MathTex(
            r"\tfrac{3}{64} + \tfrac{1}{4} + \tfrac{27}{64} = \tfrac{23}{32}",
            font_size=34,
        ).move_to(2.55 * DOWN + 3.1 * LEFT)
        not_one = Text("≠ 1 — not a distribution", font_size=SMALL_SIZE, color=WARM)
        not_one.next_to(row_sum, RIGHT, buff=0.45)
        self.play(FadeOut(known))
        self.play(Write(row_sum))
        self.play(FadeIn(not_one))
        self.wait(1.0)

        # Name the row reading.
        self.play(
            FadeOut(VGroup(row_read, row_sum, not_one, row_values)),
            FadeOut(groups),
            FadeOut(headers),
        )
        name = MathTex(r"L(p) = P(\text{data} \mid p)", font_size=48, color=ACCENT)
        name.move_to(0.9 * UP)
        read_as = caption("read as a function of p — the data are pinned, the coin varies")
        fisher = caption("Fisher named it likelihood in 1921, defined it in general in 1922")
        read_as.next_to(name, DOWN, buff=0.35)
        fisher.next_to(read_as, DOWN, buff=0.15)
        self.play(Write(name))
        self.play(FadeIn(read_as), FadeIn(fisher))
        takeaway = Text(
            "One table, two questions: columns are probability, rows are likelihood",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheBestExplanation(ConceptScene):
    """The likelihood's peak names the parameter that explains the data best."""

    def construct(self):
        self.play(FadeIn(self.title("The Best Explanation"), shift=0.3 * DOWN))

        opening = Text(
            "Three rolls land 6, 6, 3. Which die explains them best?",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))
        rolls = VGroup(*[chip(r, COOL, width=0.8) for r in ["6", "6", "3"]])
        rolls.arrange(RIGHT, buff=0.35).move_to(1.55 * UP)
        self.play(LaggedStart(*[FadeIn(r, scale=0.7) for r in rolls], lag_ratio=0.15))

        # Two candidate dice: the fair one, and the die the viewer owns.
        fair = MathTex(
            r"\text{fair die: } \tfrac16 \cdot \tfrac16 \cdot \tfrac16 = \tfrac{1}{216}"
            r" \approx 0.0046",
            font_size=34,
        ).move_to(0.55 * UP)
        biased = MathTex(
            r"\text{double-weight-on-6 die: } \tfrac27 \cdot \tfrac27 \cdot \tfrac17"
            r" = \tfrac{4}{343} \approx 0.0117",
            font_size=34,
        ).move_to(0.25 * DOWN)
        owned = caption("the biased die from the balance point — you already own it")
        owned.next_to(biased, DOWN, buff=0.3)
        self.play(Write(fair))
        self.play(Write(biased))
        self.play(FadeIn(owned))
        self.wait(0.6)
        ratio = MathTex(
            r"\frac{4/343}{1/216} = \frac{864}{343} \approx 2.52",
            font_size=40,
            color=ACCENT,
        ).move_to(1.85 * DOWN)
        rung = caption("a likelihood ratio — one rung of the posterior ladder:")
        rung2 = caption("the update factor, not a verdict about the die")
        rung.next_to(ratio, DOWN, buff=0.3)
        rung2.next_to(rung, DOWN, buff=0.15)
        self.play(Write(ratio))
        self.play(FadeIn(rung), FadeIn(rung2))
        self.wait(1.2)

        # The coin's whole curve: sweep every p at once.
        self.play(FadeOut(VGroup(opening, rolls, fair, biased, owned, ratio, rung, rung2)))
        sweep = Text(
            "For the coin, sweep every p at once: three heads in four flips.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(sweep))
        ax = _likelihood_axes().move_to(2.6 * LEFT + 0.75 * DOWN)
        curve = ax.plot(lambda p: 4 * p**3 * (1 - p), x_range=[0, 1], color=COOL)
        x_marks = VGroup(
            *[
                MathTex(s, font_size=24, color=MUTED).next_to(ax.c2p(x, 0), DOWN, buff=0.2)
                for s, x in [(r"\tfrac14", 0.25), (r"\tfrac12", 0.5), (r"\tfrac34", 0.75)]
            ]
        )
        formula = MathTex(r"L(p) = 4\,p^{3}(1-p)", font_size=38, color=COOL)
        formula.move_to(3.4 * RIGHT + 1.4 * UP)
        self.play(Create(ax), FadeIn(x_marks))
        self.play(Create(curve), Write(formula))
        dots = VGroup(
            Dot(ax.c2p(0.25, 12 / 256), color=MUTED, radius=0.06),
            Dot(ax.c2p(0.5, 0.25), color=MUTED, radius=0.06),
        )
        vals = VGroup(
            MathTex(r"\tfrac{3}{64}", font_size=26, color=MUTED).next_to(dots[0], UP, buff=0.15),
            MathTex(r"\tfrac{1}{4}", font_size=26, color=MUTED).next_to(dots[1], UP, buff=0.15),
        )
        self.play(FadeIn(dots), FadeIn(vals))
        peak = Dot(ax.c2p(0.75, 108 / 256), color=ACCENT, radius=0.08)
        drop = DashedLine(ax.c2p(0.75, 108 / 256), ax.c2p(0.75, 0), color=ACCENT, stroke_width=2)
        mle = MathTex(r"\hat{p} = \tfrac34 = \tfrac{k}{n}", font_size=40, color=ACCENT).move_to(
            3.4 * RIGHT + 0.3 * UP
        )
        proportion = caption("the observed proportion —")
        proportion2 = caption("proportions converge, so the")
        proportion3 = caption("proportion is the best guess")
        on_frame(proportion.move_to(3.9 * RIGHT + 0.5 * DOWN))
        proportion2.next_to(proportion, DOWN, buff=0.13)
        proportion3.next_to(proportion2, DOWN, buff=0.13)
        self.play(FadeIn(peak, scale=0.6), Create(drop))
        self.play(Write(mle))
        self.play(FadeIn(proportion), FadeIn(proportion2), FadeIn(proportion3))
        self.wait(1.0)

        # Guard: the curve is not a distribution over p.
        area = ax.get_area(curve, x_range=[0, 1], color=WARM, opacity=0.25)
        not_density = MathTex(
            r"\int_0^1 4p^{3}(1-p)\,dp = \tfrac15 \ne 1",
            font_size=32,
            color=WARM,
        ).move_to(3.4 * RIGHT + 1.75 * DOWN)
        bayes = caption("a prior and a renormalization would make it one —")
        bayes2 = caption("that is the Bayes move, and it is not this move")
        on_frame(bayes.next_to(not_density, DOWN, buff=0.28))
        on_frame(bayes2.next_to(bayes, DOWN, buff=0.15))
        self.play(FadeOut(VGroup(proportion, proportion2, proportion3)))
        self.play(FadeIn(area), Write(not_density))
        self.play(FadeIn(bayes), FadeIn(bayes2))
        self.wait(1.0)

        self.play(
            FadeOut(
                VGroup(
                    sweep,
                    ax,
                    curve,
                    x_marks,
                    formula,
                    dots,
                    vals,
                    peak,
                    drop,
                    mle,
                    area,
                    not_density,
                    bayes,
                    bayes2,
                )
            )
        )
        takeaway = Text(
            "Maximum likelihood: the parameter that makes the data most probable",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class AddToSurvive(ConceptScene):
    """Log the likelihood: the answer is untouched, the arithmetic becomes additive."""

    def construct(self):
        self.play(FadeIn(self.title("Add to Survive"), shift=0.3 * DOWN))

        opening = Text(
            "Take the log of the likelihood. What changes? Not the answer.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # Beat 1: L above, ln L below, one line through both peaks.
        top = _likelihood_axes(y_length=1.9).move_to(2.9 * LEFT + 1.1 * UP)
        top_curve = top.plot(lambda p: 4 * p**3 * (1 - p), x_range=[0, 1], color=COOL)
        bottom = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-7, 0, 2],
            x_length=6.2,
            y_length=1.9,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": True},
        ).move_to(2.9 * LEFT + 1.55 * DOWN)
        bottom_curve = bottom.plot(
            lambda p: np.log(4) + 3 * np.log(p) + np.log(1 - p),
            x_range=[0.06, 0.995],
            color=GOOD,
        )
        tags = VGroup(
            MathTex(r"L(p)", font_size=30, color=COOL).next_to(top, RIGHT, buff=0.3),
            MathTex(r"\ln L(p)", font_size=30, color=GOOD).next_to(bottom, RIGHT, buff=0.3),
        )
        self.play(Create(top), Create(bottom), FadeIn(tags))
        self.play(Create(top_curve), Create(bottom_curve))
        spike = DashedLine(
            top.c2p(0.75, 108 / 256) + 0.25 * UP,
            bottom.c2p(0.75, np.log(4) + 3 * np.log(0.75) + np.log(0.25)) + 0.25 * DOWN,
            color=ACCENT,
            stroke_width=2.5,
        )
        monotone = caption("log is monotone: bigger stays")
        monotone2 = caption("bigger — same argmax, 3/4")
        on_frame(monotone.move_to(4.3 * RIGHT + 1.15 * UP))
        on_frame(monotone2.next_to(monotone, DOWN, buff=0.13))
        self.play(Create(spike))
        self.play(FadeIn(monotone), FadeIn(monotone2))
        lift = caption("(the exact HHTH sequence is")
        lift2 = caption("this curve ÷ 4 — ln 4 = 1.3863")
        lift3 = caption("lower: same shape, same peak)")
        on_frame(lift.next_to(monotone2, DOWN, buff=0.35))
        on_frame(lift2.next_to(lift, DOWN, buff=0.13))
        on_frame(lift3.next_to(lift2, DOWN, buff=0.13))
        self.play(FadeIn(lift), FadeIn(lift2), FadeIn(lift3))
        self.wait(1.2)

        # Beat 2: multiplying is adding counters, now carrying likelihood.
        self.play(
            FadeOut(
                VGroup(
                    opening,
                    top,
                    top_curve,
                    bottom,
                    bottom_curve,
                    tags,
                    spike,
                    monotone,
                    monotone2,
                    lift,
                    lift2,
                    lift3,
                )
            )
        )
        frames = Text(
            "Five frames, one probability each — the model's score is the product.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(frames))
        probs = (
            VGroup(*[chip(v, COOL, width=1.0) for v in ["0.9", "0.8", "0.7", "0.9", "0.6"]])
            .arrange(RIGHT, buff=0.3)
            .move_to(1.5 * UP)
        )
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in probs], lag_ratio=0.1))
        product = MathTex(
            r"0.9 \times 0.8 \times 0.7 \times 0.9 \times 0.6 = 0.27216",
            font_size=34,
        ).move_to(0.55 * UP)
        self.play(Write(product))
        logs = VGroup(
            *[
                Text(v, font_size=SMALL_SIZE, color=GOOD)
                for v in ["−0.1054", "−0.2231", "−0.3567", "−0.1054", "−0.5108"]
            ]
        )
        for log_label, p_chip in zip(logs, probs, strict=True):
            log_label.next_to(p_chip, DOWN, buff=1.9)
        counters = caption("each factor's counter, in nature's units: ln")
        counters.move_to(0.35 * DOWN)
        log_sum = MathTex(
            r"\ln L = -0.1054 - 0.2231 - 0.3567 - 0.1054 - 0.5108 = -1.3014",
            font_size=32,
            color=GOOD,
        ).move_to(1.75 * DOWN)
        strip = caption("multiplying is adding counters — the strip carries likelihood now;")
        strip2 = caption("the evidence ruler was a log-likelihood-ratio ruler all along")
        strip.move_to(2.45 * DOWN)
        strip2.next_to(strip, DOWN, buff=0.15)
        self.play(FadeIn(counters))
        self.play(LaggedStart(*[FadeIn(v, shift=0.15 * DOWN) for v in logs], lag_ratio=0.1))
        self.play(Write(log_sum))
        self.play(FadeIn(strip), FadeIn(strip2))
        self.wait(1.2)

        # Beat 3: the cliff, met again in training.
        self.play(FadeOut(VGroup(frames, probs, product, counters, logs, log_sum, strip, strip2)))
        cliff = Text(
            "Real runs have hundreds of frames — and the product hits the cliff.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(cliff))
        dead = MathTex(
            r"\text{float32: } 0.1^{46} \;\to\; 0.0 \text{ exactly}",
            font_size=36,
            color=WARM,
        ).move_to(1.0 * UP)
        dead2 = MathTex(
            r"\text{float64: } 0.1^{324} \;\to\; 0.0 \text{ exactly}",
            font_size=36,
            color=WARM,
        ).move_to(0.2 * UP)
        alive = MathTex(
            r"46 \ln 0.1 = -105.9189 \qquad 324 \log_{10} 0.1 = -324",
            font_size=36,
            color=GOOD,
        ).move_to(0.85 * DOWN)
        reprise = caption("the underflow cliff from the logarithms series — met again,")
        reprise2 = caption("this time as the reason training happens in log space")
        reprise.move_to(1.7 * DOWN)
        reprise2.next_to(reprise, DOWN, buff=0.15)
        self.play(Write(dead))
        self.play(Write(dead2))
        self.play(Write(alive))
        self.play(FadeIn(reprise), FadeIn(reprise2))
        self.wait(1.0)

        self.play(FadeOut(VGroup(cliff, dead, dead2, alive, reprise, reprise2)))
        takeaway = Text(
            "Maximize ln L — and call its negative the loss",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheProbabilityMachine(ConceptScene):
    """Softmax: exp then normalize, and shift invariance is what forces the exp."""

    def construct(self):
        self.play(FadeIn(self.title("The Probability Machine"), shift=0.3 * DOWN))

        opening = Text(
            "A model emits scores. Training needs a distribution.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # Raw scores: legal to be negative, no reason to total 1.
        scores = _prob_bars(
            [2 / 3, 1 / 3, 0.02], ["a", "b", "c"], bar_width=0.6, gap=0.5, unit=2.4, color=COOL
        ).move_to(4.3 * LEFT + 1.25 * DOWN, aligned_edge=DOWN)
        score_vals = VGroup(
            *[
                Text(v, font_size=LABEL_SIZE, color=COOL).next_to(bar[0], UP, buff=0.15)
                for bar, v in zip(scores, ["2", "1", "0"], strict=True)
            ]
        )
        defect = caption("scores: z = (2, 1, 0) — no total of 1, and")
        defect2 = caption("nothing stops a score from being negative")
        on_frame(defect.move_to(3.55 * LEFT + 1.95 * UP))
        on_frame(defect2.next_to(defect, DOWN, buff=0.15))
        self.play(FadeIn(scores), FadeIn(score_vals))
        self.play(FadeIn(defect), FadeIn(defect2))
        self.wait(0.6)

        # The naive repair fails twice.
        naive = MathTex(
            r"\text{divide by the sum? } \tfrac{z_i}{\sum_j z_j}", font_size=34, color=WARM
        ).move_to(2.4 * RIGHT + 1.7 * UP)
        fail1 = MathTex(
            r"(2,1,0) \to (\tfrac23, \tfrac13, 0)"
            r"\qquad (3,2,1) \to (\tfrac12, \tfrac13, \tfrac16)",
            font_size=30,
        ).move_to(2.4 * RIGHT + 0.85 * UP)
        shifted = caption("add 1 to every score and the shares change")
        shifted.move_to(2.4 * RIGHT + 0.3 * UP)
        fail2 = MathTex(
            r"(2,-1,0) \to (2, -1, 0)",
            font_size=30,
        ).move_to(2.4 * RIGHT + 0.35 * DOWN)
        negative = caption("and one negative score makes a negative “probability”")
        negative.move_to(2.4 * RIGHT + 0.9 * DOWN)
        self.play(Write(naive))
        self.play(Write(fail1))
        self.play(FadeIn(shifted))
        self.play(Write(fail2))
        self.play(FadeIn(negative))
        self.wait(1.0)

        # Exp repairs both defects; normalize finishes the job.
        self.play(FadeOut(VGroup(naive, fail1, shifted, fail2, negative)))
        exp_row = MathTex(
            r"e^{2} = 7.389 \quad e^{1} = 2.718 \quad e^{0} = 1",
            font_size=32,
        ).move_to(2.4 * RIGHT + 1.55 * UP)
        norm = MathTex(
            r"\mathrm{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}",
            font_size=40,
            color=ACCENT,
        ).move_to(2.4 * RIGHT + 0.55 * UP)
        self.play(Write(exp_row))
        self.play(Write(norm))
        soft_bars = _prob_bars(
            SOFTMAX_T1, ["a", "b", "c"], bar_width=0.6, gap=0.5, unit=2.4, color=ACCENT
        ).move_to(4.3 * LEFT + 1.25 * DOWN, aligned_edge=DOWN)
        soft_vals = VGroup(
            *[
                Text(v, font_size=SMALL_SIZE, color=ACCENT).next_to(bar[0], UP, buff=0.15)
                for bar, v in zip(soft_bars, ["0.6652", "0.2447", "0.0900"], strict=True)
            ]
        )
        self.play(FadeOut(score_vals))
        self.play(Transform(scores, soft_bars))
        self.play(FadeIn(soft_vals))
        legal = caption("positive, total 1 — a legal pmf, ranking preserved")
        legal.move_to(2.4 * RIGHT + 0.4 * DOWN)
        self.play(FadeIn(legal))
        self.wait(0.8)

        # The forcing argument: shift invariance.
        forced = MathTex(
            r"\frac{e^{z_i + c}}{\sum_j e^{z_j + c}}"
            r" = \frac{e^{c}\, e^{z_i}}{e^{c} \sum_j e^{z_j}}"
            r" = \mathrm{softmax}(z)_i",
            font_size=32,
        ).move_to(2.4 * RIGHT + 1.35 * DOWN)
        forcing = caption("add c to every score: e^c cancels — exactly the same")
        forcing2 = caption("distribution; among per-score recipes, only an")
        forcing3 = caption("exponential turns a shift into a factor that cancels")
        forcing.move_to(2.4 * RIGHT + 2.1 * DOWN)
        forcing2.next_to(forcing, DOWN, buff=0.15)
        forcing3.next_to(forcing2, DOWN, buff=0.15)
        self.play(Write(forced))
        self.play(FadeIn(forcing), FadeIn(forcing2), FadeIn(forcing3))
        self.wait(1.2)

        # The invariance, used: subtract the max and overflow dies.
        self.play(
            FadeOut(
                VGroup(
                    opening,
                    defect,
                    defect2,
                    scores,
                    soft_vals,
                    exp_row,
                    norm,
                    legal,
                    forced,
                    forcing,
                    forcing2,
                    forcing3,
                )
            )
        )
        stability = Text(
            "The invariance is also the stability trick, for free.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(stability))
        blow = MathTex(
            r"z = (1000, 1001, 1002): \quad e^{z} \to (\infty, \infty, \infty)"
            r" \;\to\; \text{NaN}",
            font_size=34,
            color=WARM,
        ).move_to(0.9 * UP)
        rescue = MathTex(
            r"z - \max z = (-2, -1, 0) \;\to\; (0.0900,\ 0.2447,\ 0.6652)",
            font_size=34,
            color=GOOD,
        ).move_to(0.0 * UP)
        mirror = caption("float64 overflows past e^709 — subtracting the max is the")
        mirror2 = caption("shift the distribution cannot feel; the workhorse, reversed")
        mirror.move_to(0.85 * DOWN)
        mirror2.next_to(mirror, DOWN, buff=0.15)
        self.play(Write(blow))
        self.play(Write(rescue))
        self.play(FadeIn(mirror), FadeIn(mirror2))
        bridle = caption('"a differentiable winner-take-all … we like to refer to it')
        bridle2 = caption('as soft max" — John Bridle, 1989, naming it')
        bridle.move_to(1.9 * DOWN)
        bridle2.next_to(bridle, DOWN, buff=0.15)
        self.play(FadeIn(bridle), FadeIn(bridle2))
        self.wait(1.0)

        self.play(FadeOut(VGroup(stability, blow, rescue, mirror, mirror2, bridle, bridle2)))
        takeaway = Text(
            "Exp then normalize — and shift invariance is what forces the exp",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TurningTheDial(ConceptScene):
    """Softmax is a soft argmax with a sharpness dial — and the dial is a caveat."""

    def construct(self):
        self.play(FadeIn(self.title("Turning the Dial"), shift=0.3 * DOWN))

        opening = Text(
            "One knob: divide every score by a temperature T.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))
        dial = MathTex(r"\mathrm{softmax}(z / T), \qquad z = (2, 1, 0)", font_size=38).move_to(
            1.9 * UP
        )
        self.play(Write(dial))

        bars = _prob_bars(
            SOFTMAX_T1, ["a", "b", "c"], bar_width=0.7, gap=0.55, unit=2.6, color=COOL
        ).move_to(3.9 * LEFT + 1.15 * DOWN, aligned_edge=DOWN)
        t_label = MathTex(r"T = 1", font_size=34, color=COOL).move_to(3.9 * LEFT + 1.75 * DOWN)
        vals = Text("0.6652   0.2447   0.0900", font_size=SMALL_SIZE, color=COOL)
        vals.move_to(3.9 * LEFT + 2.3 * DOWN)
        self.play(FadeIn(bars), FadeIn(t_label), FadeIn(vals))
        self.wait(0.6)

        for t_str, values, val_str in [
            ("T = 0.5", SOFTMAX_T_HALF, "0.8668   0.1173   0.0159"),
            ("T = 2", SOFTMAX_T2, "0.5065   0.3072   0.1863"),
        ]:
            new_bars = _prob_bars(
                values, ["a", "b", "c"], bar_width=0.7, gap=0.55, unit=2.6, color=COOL
            ).move_to(3.9 * LEFT + 1.15 * DOWN, aligned_edge=DOWN)
            new_label = MathTex(t_str, font_size=34, color=COOL).move_to(3.9 * LEFT + 1.75 * DOWN)
            new_vals = Text(val_str, font_size=SMALL_SIZE, color=COOL)
            new_vals.move_to(3.9 * LEFT + 2.3 * DOWN)
            self.play(
                Transform(bars, new_bars),
                FadeOut(t_label),
                FadeOut(vals),
            )
            t_label, vals = new_label, new_vals
            self.play(FadeIn(t_label), FadeIn(vals))
            self.wait(0.4)

        winner = caption("sharpen or flatten — the winner never changes:")
        winner2 = caption("dividing by T and exponentiating are both monotone")
        on_frame(winner.move_to(2.55 * RIGHT + 1.0 * UP))
        on_frame(winner2.next_to(winner, DOWN, buff=0.15))
        limits = MathTex(
            r"T \to 0:\ (1, 0, 0) \qquad T \to \infty:\ (\tfrac13, \tfrac13, \tfrac13)",
            font_size=30,
        ).move_to(2.55 * RIGHT + 0.1 * UP)
        limit_note = caption("winner-take-all and uniform — limits, never values")
        on_frame(limit_note.move_to(2.55 * RIGHT + 0.5 * DOWN))
        self.play(FadeIn(winner), FadeIn(winner2))
        self.play(Write(limits))
        self.play(FadeIn(limit_note))
        self.wait(1.0)

        # Why e: every base is a temperature.
        self.play(FadeOut(opening))
        why_e = Text(
            "Why e? Change the base and watch what happens.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(why_e))
        base2 = MathTex(
            r"\text{base 2: } \frac{2^{z_i}}{\sum_j 2^{z_j}}"
            r" = \left(\tfrac47,\ \tfrac27,\ \tfrac17\right)",
            font_size=32,
        ).move_to(2.55 * RIGHT + 1.35 * DOWN)
        base_temp = MathTex(
            r"b^{z} = e^{z \ln b} \;\Rightarrow\;"
            r" \text{base } b \equiv T = \tfrac{1}{\ln b}\ \ (b > 1)",
            font_size=32,
        ).move_to(2.55 * RIGHT + 2.15 * DOWN)
        natural = caption("no base above 1 is forced — each is e at another T;")
        natural2 = caption("e is the convention because ln is the natural counter")
        on_frame(natural.move_to(2.55 * RIGHT + 2.85 * DOWN))
        on_frame(natural2.next_to(natural, DOWN, buff=0.15))
        self.play(Write(base2))
        self.play(Write(base_temp))
        self.play(FadeIn(natural), FadeIn(natural2))
        self.wait(1.2)

        # The caveat the dial proves.
        self.play(
            FadeOut(
                VGroup(
                    why_e,
                    dial,
                    bars,
                    t_label,
                    vals,
                    winner,
                    winner2,
                    limits,
                    limit_note,
                    base2,
                    base_temp,
                    natural,
                    natural2,
                )
            )
        )
        caveat = Text(
            "The dial is also a caveat about what the numbers mean.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(caveat))
        guo = caption("modern networks run overconfident; fitting one shared T")
        guo2 = caption("recalibrates them without changing a single prediction")
        guo3 = caption("(Guo, Pleiss, Sun & Weinberger, 2017)")
        asserted = Text(
            "Numbers you can rescale wholesale were asserted, not measured.",
            font_size=BODY_SIZE,
        )
        guo.move_to(0.9 * UP)
        guo2.next_to(guo, DOWN, buff=0.15)
        guo3.next_to(guo2, DOWN, buff=0.15)
        asserted.move_to(0.55 * DOWN)
        self.play(FadeIn(guo), FadeIn(guo2), FadeIn(guo3))
        self.play(FadeIn(asserted))
        self.wait(1.0)

        self.play(FadeOut(VGroup(caveat, guo, guo2, guo3, asserted)))
        takeaway = Text(
            "Softmax is a soft argmax — sharpness is a dial; the ranking is not",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheLossThatTrains(ConceptScene):
    """NLL as the LSE gap, and per-frame losses adding — the join with CTC."""

    def construct(self):
        self.play(FadeIn(self.title("The Loss That Trains"), shift=0.3 * DOWN))

        opening = Text(
            "Score the machine by the log-likelihood it assigns the truth.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))
        collapse = MathTex(
            r"-\sum_k y_k \ln p_k \;=\; -\ln p_{\text{correct}}",
            font_size=40,
        ).move_to(1.6 * UP)
        onehot = caption("one correct class per frame, so the sum collapses —")
        onehot2 = caption('the negative log-likelihood (its alias: "cross-entropy loss")')
        onehot.next_to(collapse, DOWN, buff=0.3)
        onehot2.next_to(onehot, DOWN, buff=0.15)
        self.play(Write(collapse))
        self.play(FadeIn(onehot), FadeIn(onehot2))
        self.wait(0.8)

        # The gap device: the loss is LSE(z) minus the correct score.
        self.play(FadeOut(VGroup(opening, collapse, onehot, onehot2)))
        gap_intro = Text(
            "For softmax scores, the loss is a visible gap.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(gap_intro))
        scores = _prob_bars(
            [2 / 3, 1 / 3, 0.02], ["a", "b", "c"], bar_width=0.6, gap=0.6, unit=2.7, color=COOL
        ).move_to(3.9 * LEFT + 1.5 * DOWN, aligned_edge=DOWN)
        # Tall bars carry their score inside the top — the LSE ruler runs
        # just above the tallest bar, and a label above it would sit on
        # the line; the sliver bar keeps its label above.
        score_vals = VGroup()
        for bar, v in zip(scores, ["2", "1", "0"], strict=True):
            label = Text(v, font_size=LABEL_SIZE, color=COOL)
            if bar[0].height > 0.6:
                label.move_to(bar[0].get_top() + 0.24 * DOWN)
            else:
                label.next_to(bar[0], UP, buff=0.12)
            score_vals.add(label)
        # The ruler's height is a claim: LSE(z) >= max(z), so it must sit
        # measurably above the tallest bar — derived from the bar itself,
        # in the bars' own units (2.7 scene units per 3 score units).
        lse_y = scores[0][0].get_bottom()[1] + 2.7 * (2.4076 / 3)
        ruler = DashedLine(
            [-6.2, lse_y, 0],
            [-1.6, lse_y, 0],
            color=ACCENT,
            stroke_width=2.5,
        )
        lse_tag = MathTex(r"\mathrm{LSE}(z) = 2.4076", font_size=28, color=ACCENT)
        lse_tag.next_to(ruler, UP, buff=0.12).align_to(ruler, RIGHT)
        smooth = caption("the smooth max —")
        smooth2 = caption("the log-sum-exp ruler, again")
        smooth.move_to(3.9 * LEFT + 2.4 * DOWN)
        smooth2.next_to(smooth, DOWN, buff=0.15)
        self.play(FadeIn(scores), FadeIn(score_vals))
        self.play(Create(ruler), FadeIn(lse_tag))
        self.play(FadeIn(smooth), FadeIn(smooth2))
        identity = MathTex(
            r"-\ln \mathrm{softmax}(z)_c = \mathrm{LSE}(z) - z_c",
            font_size=36,
            color=ACCENT,
        ).move_to(3.0 * RIGHT + 1.3 * UP)
        cases = MathTex(
            r"c = a\!: 0.4076 \quad c = b\!: 1.4076 \quad c = c\!: 2.4076",
            font_size=30,
        ).move_to(3.0 * RIGHT + 0.5 * UP)
        linearish = caption("the further the truth's score falls behind,")
        linearish2 = caption("the more the frame pays — confidently wrong is costly")
        on_frame(linearish.move_to(2.8 * RIGHT + 0.25 * DOWN))
        on_frame(linearish2.next_to(linearish, DOWN, buff=0.15))
        self.play(Write(identity))
        self.play(Write(cases))
        self.play(FadeIn(linearish), FadeIn(linearish2))
        self.wait(1.2)

        # The join: per-frame products under the conditional independence license.
        self.play(
            FadeOut(
                VGroup(
                    gap_intro,
                    scores,
                    score_vals,
                    ruler,
                    lse_tag,
                    smooth,
                    smooth2,
                    identity,
                    cases,
                    linearish,
                    linearish2,
                )
            )
        )
        join = Text(
            "Frames chain: the per-frame matrix, scored one column at a time.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(join))
        rows = ["A", "B", "ε"]
        cols = [["0.7", "0.2", "0.1"], ["0.6", "0.1", "0.3"], ["0.2", "0.1", "0.7"]]
        picked = [0, 0, 2]
        grid = VGroup()
        for t, col in enumerate(cols):
            for r, value in enumerate(col):
                color = GOOD if picked[t] == r else MUTED
                cell = chip(value, color, width=1.05, height=0.6)
                cell.move_to([-3.4 + t * 1.35, 1.3 - r * 0.75, 0])
                grid.add(cell)
        row_tags = VGroup(
            *[
                Text(r, font_size=LABEL_SIZE, color=MUTED).move_to([-4.55, 1.3 - i * 0.75, 0])
                for i, r in enumerate(rows)
            ]
        )
        col_sums = caption("each column is a softmax output — a pmf, summing to 1")
        col_sums.move_to(2.3 * LEFT + 0.95 * DOWN)
        self.play(FadeIn(row_tags), LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.05))
        self.play(FadeIn(col_sums))
        path = MathTex(
            r"P(\text{A, A, } \varepsilon) = 0.7 \times 0.6 \times 0.7 = 0.294",
            font_size=32,
        ).move_to(3.6 * RIGHT + 1.3 * UP)
        license_note = caption("multiplying is licensed: the frames are independent")
        license_note2 = caption("given the input — the conditioning series said when")
        license_note.move_to(0.3 * RIGHT + 1.6 * DOWN)
        license_note2.next_to(license_note, DOWN, buff=0.15)
        log_form = MathTex(
            r"\ln P = -0.3567 - 0.5108 - 0.3567 = -1.2242",
            font_size=32,
            color=GOOD,
        ).move_to(3.6 * RIGHT + 0.35 * UP)
        adds = caption("independent frames: losses add")
        adds.next_to(log_form, DOWN, buff=0.2)
        self.play(Write(path))
        self.play(FadeIn(license_note), FadeIn(license_note2))
        self.play(Write(log_form))
        self.play(FadeIn(adds))
        self.wait(1.2)

        # When useful: the CTC loss, and the gradient waiting behind it.
        self.play(
            FadeOut(
                VGroup(
                    join,
                    grid,
                    row_tags,
                    col_sums,
                    path,
                    license_note,
                    license_note2,
                    log_form,
                    adds,
                )
            )
        )
        ctc = caption("summed over every path that collapses to the transcript,")
        ctc2 = caption("the path products give P(transcript | input) — the trellis's sum;")
        ctc3 = caption("the CTC loss is its negative log — a 29-way softmax per frame")
        ctc4 = caption("in Deep Speech; a 50,257-way softmax per token in GPT-2")
        grad = caption("and its gradient — softmax output minus how often the truth")
        grad2 = caption("used each cell — is the next series")
        ctc.move_to(1.1 * UP)
        ctc2.next_to(ctc, DOWN, buff=0.15)
        ctc3.next_to(ctc2, DOWN, buff=0.15)
        ctc4.next_to(ctc3, DOWN, buff=0.15)
        grad.move_to(0.75 * DOWN)
        grad2.next_to(grad, DOWN, buff=0.15)
        self.play(FadeIn(ctc), FadeIn(ctc2), FadeIn(ctc3), FadeIn(ctc4))
        self.play(FadeIn(grad), FadeIn(grad2))
        self.wait(1.0)

        takeaway = Text(
            "The loss is −ln p(truth) — and over independent frames, losses add",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
