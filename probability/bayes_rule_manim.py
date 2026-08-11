"""Bayes' rule — walking through the door the last series left open.

Six scenes: the one-line division and its renaming, counting the answer
out in whole people, the waterfall and the odds form, the prevalence pair
completed as a factorization, iterated updating, and Monty Hall at last —
with the host's protocol as the likelihood.

    ThroughTheFrontDoor   divide the standing identity; rename the parts
    CountingItOut         Diseasitis in whole students: 18/42 = 3/7
    TheOddsForm           the waterfall; prior odds x LR = posterior odds
    OneTestTwoPatients    LR = 9, two priors, two posteriors: 1/2 vs 1/12
    YesterdaysPosterior   odds multiply; a head and a tail cancel exactly
    TheHostsProtocol      Monty, Fall, Crawl — the likelihood is behavior

Every number on screen is exact and machine-verified in plan 004,
including the Monty Small 1/(1+p) dial (enumerated at five values of p).

Render:
    uv run python probability/bayes_rule_manim.py
    uv run python probability/bayes_rule_manim.py -s TheHostsProtocol -q draft
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
    SMALL_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    chip,
    palette,
    render_cli,
)

# Same assignment as the sibling probability modules: hypotheses stay teal,
# evidence stays pink, across the whole topic.
HYP_COLOR = palette(0)
EV_COLOR = palette(1)


class ThroughTheFrontDoor(ConceptScene):
    """One line past the door: P(A|B) = P(B|A) P(A) / P(B), then rename it."""

    def construct(self):
        self.play(FadeIn(self.title("Through the Front Door"), shift=0.3 * DOWN))

        recall = Text("Where the last series stopped:", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        door = MathTex(
            r"P(A)\,P(B \mid A) = P(B)\,P(A \mid B)", font_size=44, color=ACCENT
        ).move_to(1.5 * UP)
        self.play(FadeIn(recall))
        self.play(Write(door))
        self.wait(0.5)

        # --- the one-line division ---------------------------------------------
        divide = caption("divide by P(B) — positivity inherited from the definition")
        divide.next_to(door, DOWN, buff=0.35)
        self.play(FadeIn(divide))
        bayes = MathTex(
            r"P(A \mid B)",
            r"=",
            r"\frac{P(B \mid A)\,P(A)}{P(B)}",
            font_size=FORMULA_SIZE,
        ).move_to(0.15 * DOWN)
        bayes[0].set_color(ACCENT)
        self.play(Write(bayes))
        self.wait(0.6)

        # --- the renaming -------------------------------------------------------
        # The old identity leaves and the fraction takes the stage alone: the
        # name labels land where the door equation was, and labels pointing at
        # one formula while another sits behind them is exactly the overlap
        # motion discipline exists to prevent.
        self.play(FadeOut(recall), FadeOut(door), FadeOut(divide), run_time=0.4)
        self.play(bayes.animate.move_to(0.9 * UP))
        names = VGroup(
            Text("posterior", font_size=LABEL_SIZE, color=ACCENT),
            Text("likelihood", font_size=LABEL_SIZE, color=EV_COLOR),
            Text("prior", font_size=LABEL_SIZE, color=HYP_COLOR),
            Text("total probability over the hypotheses", font_size=SMALL_SIZE, color=MUTED),
        )
        names[0].next_to(bayes[0], DOWN, buff=0.6)
        names[1].next_to(bayes[2], UP, buff=0.5).shift(0.8 * LEFT)
        names[2].next_to(bayes[2], UP, buff=0.5).shift(1.3 * RIGHT)
        names[3].next_to(bayes[2], DOWN, buff=0.55)
        arrows = VGroup(
            Arrow(
                names[0].get_top(),
                bayes[0].get_bottom(),
                buff=0.08,
                color=MUTED,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.2,
            ),
            Arrow(
                names[1].get_bottom(),
                bayes[2].get_top() + 0.7 * LEFT,
                buff=0.08,
                color=MUTED,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.2,
            ),
            Arrow(
                names[2].get_bottom(),
                bayes[2].get_top() + 0.9 * RIGHT,
                buff=0.08,
                color=MUTED,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.2,
            ),
        )
        self.play(
            LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.2),
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
        )
        lotp_note = caption("the denominator is the column sum you already know")
        lotp_note.next_to(names[3], DOWN, buff=0.25)
        self.play(FadeIn(lotp_note))
        self.wait(1.0)

        # --- the reading ---------------------------------------------------------
        self.play(FadeOut(VGroup(bayes, names, arrows, lotp_note)))
        claim = Text(
            "Evidence doesn't determine beliefs — it updates them",
            font_size=28,
        ).move_to(0.5 * UP)
        law = MathTex(
            r"\text{posterior} \propto \text{prior} \times \text{likelihood}",
            font_size=44,
            color=ACCENT,
        ).next_to(claim, DOWN, buff=0.5)
        last = caption("normalize last — the denominator can wait").next_to(law, DOWN, buff=0.4)
        self.play(FadeIn(claim, shift=0.2 * UP), Create(boxed(claim, buff=0.28)))
        self.play(Write(law))
        self.play(FadeIn(last))
        self.wait(2)


class CountingItOut(ConceptScene):
    """The first Bayes computation in whole people — no formula required."""

    def construct(self):
        self.play(FadeIn(self.title("Counting It Out"), shift=0.3 * DOWN))

        setup = Text(
            "Diseasitis: 20% of students have it. The tongue depressor\n"
            "turns black for 90% of the sick — and 30% of the healthy.",
            font_size=BODY_SIZE,
            line_spacing=1.1,
        ).next_to(self.head, DOWN, buff=0.35)
        self.play(FadeIn(setup))

        # --- whole students, no formula ----------------------------------------
        hundred = Text("100 students", font_size=LABEL_SIZE).move_to(1.0 * UP)
        row1 = (
            VGroup(
                chip("20 sick", HYP_COLOR, width=2.0),
                chip("80 healthy", MUTED, width=2.4),
            )
            .arrange(RIGHT, buff=0.6)
            .next_to(hundred, DOWN, buff=0.4)
        )
        row2 = (
            VGroup(
                chip("18 black", GOOD, width=1.9),
                chip("24 black", WARM, width=1.9),
            )
            .arrange(RIGHT, buff=0.9)
            .next_to(row1, DOWN, buff=0.45)
        )
        for upper, lower in zip(row1, row2, strict=True):
            lower.match_x(upper)
        self.play(FadeIn(hundred))
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in row1], lag_ratio=0.2))
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in row2], lag_ratio=0.2))
        self.wait(0.5)

        answer = MathTex(
            r"P(\text{sick} \mid \text{black}) = \frac{18}{18 + 24} = \frac{18}{42}"
            r" = \frac{3}{7}",
            font_size=RESULT_SIZE,
            color=ACCENT,
        ).next_to(row2, DOWN, buff=0.55)
        self.play(Write(answer))
        inside = caption("the prior rode inside the counts — you never wrote the formula")
        inside.next_to(answer, DOWN, buff=0.3)
        self.play(FadeIn(inside))
        self.wait(1.0)

        # --- why this format matters --------------------------------------------
        self.play(FadeOut(VGroup(setup, hundred, row1, row2, answer, inside)))
        evidence = VGroup(
            Text("The format is not cosmetic:", font_size=BODY_SIZE),
            Text(
                "probabilities: 4% of people compute the posterior correctly",
                font_size=BODY_SIZE,
                color=WARM,
            ),
            Text(
                "whole-people counts: 24% — and physicians go from 21% to 87%",
                font_size=BODY_SIZE,
                color=GOOD,
            ),
        ).arrange(DOWN, buff=0.35)
        evidence.move_to(0.5 * UP)
        self.play(LaggedStart(*[FadeIn(e) for e in evidence], lag_ratio=0.3))
        self.wait(1.0)

        self.play(FadeOut(evidence))
        takeaway = Text("Count whole people first — formula second", font_size=28)
        takeaway.move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class TheOddsForm(ConceptScene):
    """The waterfall: prior odds times the likelihood ratio, nothing else."""

    def construct(self):
        self.play(FadeIn(self.title("The Odds Form"), shift=0.3 * DOWN))

        setup = Text("The same Diseasitis — drawn as two streams", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        self.play(FadeIn(setup))

        # --- the waterfall -------------------------------------------------------
        # Stream widths are the prior odds (1:4); pass-through fractions are
        # the likelihoods (90%, 30%); the pool holds the posterior odds 3:4.
        top_y, pool_y = 1.7, -1.1
        sick_top = Rectangle(
            width=0.7, height=0.5, stroke_width=0, fill_color=HYP_COLOR, fill_opacity=0.7
        ).move_to(np.array([-2.6, top_y, 0]))
        healthy_top = Rectangle(
            width=2.8, height=0.5, stroke_width=0, fill_color=MUTED, fill_opacity=0.55
        ).move_to(np.array([0.8, top_y, 0]))
        top_tags = VGroup(
            Text("sick 20", font_size=SMALL_SIZE, color=HYP_COLOR).next_to(sick_top, UP, 0.15),
            Text("healthy 80", font_size=SMALL_SIZE, color=MUTED).next_to(healthy_top, UP, 0.15),
        )
        sick_pool = Rectangle(
            width=0.63, height=0.5, stroke_width=0, fill_color=GOOD, fill_opacity=0.75
        ).move_to(np.array([-2.6, pool_y, 0]))
        healthy_pool = Rectangle(
            width=0.84, height=0.5, stroke_width=0, fill_color=WARM, fill_opacity=0.7
        ).move_to(np.array([0.8, pool_y, 0]))
        falls = VGroup(
            Arrow(
                sick_top.get_bottom(),
                sick_pool.get_top(),
                buff=0.1,
                color=HYP_COLOR,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            ),
            Arrow(
                healthy_top.get_bottom(),
                healthy_pool.get_top(),
                buff=0.1,
                color=MUTED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            ),
        )
        pass_tags = VGroup(
            Text("90% pass", font_size=SMALL_SIZE, color=GOOD).next_to(falls[0], LEFT, 0.2),
            Text("30% pass", font_size=SMALL_SIZE, color=WARM).next_to(falls[1], RIGHT, 0.2),
        )
        pool_tags = VGroup(
            Text("18", font_size=LABEL_SIZE, color=GOOD).next_to(sick_pool, DOWN, 0.15),
            Text("24", font_size=LABEL_SIZE, color=WARM).next_to(healthy_pool, DOWN, 0.15),
        )
        self.play(FadeIn(sick_top), FadeIn(healthy_top), FadeIn(top_tags))
        self.play(GrowArrow(falls[0]), GrowArrow(falls[1]), FadeIn(pass_tags))
        self.play(FadeIn(sick_pool), FadeIn(healthy_pool), FadeIn(pool_tags))
        self.wait(0.5)

        arithmetic = MathTex(r"(1{:}4) \times (3{:}1) = 3{:}4", font_size=40, color=ACCENT).next_to(
            pool_tags, DOWN, buff=0.5
        )
        guard = caption("odds, not a fraction: 3:4 is the probability 3/7")
        guard.next_to(arithmetic, DOWN, buff=0.28)
        self.play(Write(arithmetic))
        self.play(FadeIn(guard))
        self.wait(0.9)

        # --- invariance: only ratios survive ------------------------------------
        halved = Text(
            "halve both pass-through rates (45%, 15%) — the pool ratio never moves",
            font_size=SMALL_SIZE,
        ).move_to(np.array([0, pool_y - 1.55, 0]))
        self.play(FadeOut(arithmetic), FadeOut(guard), run_time=0.3)
        # The pool labels must move with the picture: halved pass-through
        # means 9 and 24 -> 12 in the pool, and a shrunken pool still
        # labelled 18/24 would be the picture contradicting the math.
        new_tags = VGroup(
            Text("9", font_size=LABEL_SIZE, color=GOOD),
            Text("12", font_size=LABEL_SIZE, color=WARM),
        )
        # The rate labels are part of the same claim: 90%/30% on screen
        # under a caption saying 45%/15% would be the picture contradicting
        # the math again.
        halved_tags = VGroup(
            Text("45% pass", font_size=SMALL_SIZE, color=GOOD).next_to(falls[0], LEFT, 0.2),
            Text("15% pass", font_size=SMALL_SIZE, color=WARM).next_to(falls[1], RIGHT, 0.2),
        )
        # Sequenced per motion discipline: the old rate labels leave fully
        # before the halved ones occupy the same spots.
        self.play(FadeOut(pass_tags), run_time=0.4)
        self.play(
            sick_pool.animate.stretch(0.5, 0),
            healthy_pool.animate.stretch(0.5, 0),
            FadeOut(pool_tags),
            FadeIn(halved),
        )
        new_tags[0].next_to(sick_pool, DOWN, buff=0.15)
        new_tags[1].next_to(healthy_pool, DOWN, buff=0.15)
        self.play(FadeIn(new_tags), FadeIn(halved_tags), run_time=0.4)
        still = MathTex(r"9{:}12 = 3{:}4", font_size=34, color=ACCENT)
        still.next_to(halved, DOWN, buff=0.25)
        self.play(Write(still))
        self.wait(0.9)

        # --- the law, and the reveal ---------------------------------------------
        waterfall = VGroup(
            sick_top,
            healthy_top,
            top_tags,
            falls,
            pass_tags,
            sick_pool,
            healthy_pool,
            new_tags,
            halved_tags,
            halved,
            still,
            setup,
        )
        self.play(FadeOut(waterfall))
        law = MathTex(
            r"\text{posterior odds} = \text{prior odds} \times \text{likelihood ratio}",
            font_size=44,
            color=ACCENT,
        ).move_to(0.75 * UP)
        reveal = VGroup(
            caption("and the waterfall is not a new picture:"),
            caption("it is the tree from the conditional series with the division deferred —"),
            caption("the chips, the tree, and the two slices were one object all along"),
        ).arrange(DOWN, buff=0.2)
        reveal.next_to(law, DOWN, buff=0.5)
        self.play(Write(law), Create(boxed(law, buff=0.32)))
        self.play(LaggedStart(*[FadeIn(r) for r in reveal], lag_ratio=0.3))
        self.wait(2)


class OneTestTwoPatients(ConceptScene):
    """One test, one likelihood ratio — and two very different posteriors."""

    def construct(self):
        self.play(FadeIn(self.title("One Test, Two Patients"), shift=0.3 * DOWN))

        card = MathTex(
            r"\text{sensitivity } \tfrac{9}{10},\quad \text{false alarms } \tfrac{1}{10}"
            r"\quad\Longrightarrow\quad LR = 9",
            font_size=38,
        ).next_to(self.head, DOWN, buff=0.4)
        card[0][-1].set_color(ACCENT)
        one_number = caption("the test's one number — it belongs to the test, not the patient")
        one_number.next_to(card, DOWN, buff=0.3)
        self.play(Write(card))
        self.play(FadeIn(one_number))
        self.wait(0.6)

        # --- two patients, one factor -------------------------------------------
        left = VGroup(
            Text("prevalence 10%", font_size=LABEL_SIZE, color=HYP_COLOR),
            MathTex(r"1{:}9 \xrightarrow{\;\times 9\;} 9{:}9 = 1{:}1", font_size=34),
            MathTex(r"P(\text{sick} \mid +) = \tfrac{1}{2}", font_size=38, color=ACCENT),
            caption("the 9/18 you counted"),
        ).arrange(DOWN, buff=0.32)
        right = VGroup(
            Text("prevalence 1%", font_size=LABEL_SIZE, color=HYP_COLOR),
            MathTex(r"1{:}99 \xrightarrow{\;\times 9\;} 9{:}99 = 1{:}11", font_size=34),
            MathTex(r"P(\text{sick} \mid +) = \tfrac{1}{12}", font_size=38, color=ACCENT),
            caption("the 9/108 you counted"),
        ).arrange(DOWN, buff=0.32)
        left.move_to(np.array([-3.2, -0.6, 0]))
        right.move_to(np.array([3.2, -0.6, 0]))
        self.play(LaggedStart(*[FadeIn(x, shift=0.2 * UP) for x in left], lag_ratio=0.2))
        self.play(LaggedStart(*[FadeIn(x, shift=0.2 * UP) for x in right], lag_ratio=0.2))
        self.wait(0.9)

        factored = Text(
            "the pair the last series counted — now factored: fixed LR, moving prior",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(factored))
        self.wait(0.9)

        # --- the accuracy collapse ----------------------------------------------
        self.play(FadeOut(VGroup(card, one_number, left, right, factored)))
        collapse = VGroup(
            Text('"the test is 90% accurate"', font_size=30, color=WARM),
            Text("is one word hiding two numbers —", font_size=BODY_SIZE),
            Text("and neither of them is the posterior", font_size=BODY_SIZE),
        ).arrange(DOWN, buff=0.3)
        collapse.move_to(0.8 * UP)
        negative = caption(
            "the negative result has a number too: LR 1/9 — 1:9 becomes 1:81, P = 1/82"
        )
        negative.next_to(collapse, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(c) for c in collapse], lag_ratio=0.25))
        self.play(FadeIn(negative))
        self.wait(1.0)

        self.play(FadeOut(collapse), FadeOut(negative))
        takeaway = Text("A posterior cannot be stated without its prior", font_size=28).move_to(
            0.2 * DOWN
        )
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class YesterdaysPosterior(ConceptScene):
    """Yesterday's posterior is today's prior — and evidence can cancel exactly."""

    def construct(self):
        self.play(FadeIn(self.title("Yesterday's Posterior"), shift=0.3 * DOWN))

        recall = Text(
            "Your two coins again: 9/10 heads vs 1/10 heads — LR per head: 9",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        echo = caption("the same factor as the test — one number, two stories")
        echo.next_to(recall, DOWN, buff=0.25)
        self.play(FadeIn(recall))
        self.play(FadeIn(echo))
        self.wait(0.5)

        # --- the chain ------------------------------------------------------------
        chain = MathTex(
            r"1{:}1",
            r"\xrightarrow{\ \text{H}\ (\times 9)\ }",
            r"9{:}1",
            r"\xrightarrow{\ \text{H}\ (\times 9)\ }",
            r"81{:}1",
            font_size=44,
        ).move_to(0.7 * UP)
        chain[0].set_color(MUTED)
        chain[2].set_color(HYP_COLOR)
        chain[4].set_color(ACCENT)
        probs = VGroup(
            MathTex(r"\tfrac{1}{2}", font_size=28, color=MUTED),
            MathTex(r"\tfrac{9}{10}", font_size=28, color=HYP_COLOR),
            MathTex(r"\tfrac{81}{82}", font_size=28, color=ACCENT),
        )
        for tex, part in zip(probs, [chain[0], chain[2], chain[4]], strict=True):
            tex.next_to(part, DOWN, buff=0.3)
        self.play(Write(chain[0]), FadeIn(probs[0]))
        self.play(Write(chain[1]), Write(chain[2]), FadeIn(probs[1]))
        license_note = Text(
            "the second multiplication is licensed by conditional independence\n"
            "given the coin — the third kind of independence you already met",
            font_size=SMALL_SIZE,
            color=ACCENT,
            line_spacing=1.1,
        ).next_to(probs[1], DOWN, buff=0.5)
        self.play(FadeIn(license_note))
        self.play(Write(chain[3]), Write(chain[4]), FadeIn(probs[2]))
        self.wait(0.9)

        # --- cancellation ----------------------------------------------------------
        self.play(FadeOut(license_note))
        cancel = MathTex(
            r"9{:}1 \xrightarrow{\ \text{T}\ (\times \tfrac{1}{9})\ } 1{:}1",
            font_size=40,
        ).move_to(1.35 * DOWN)
        cancel[0][-3:].set_color(GOOD)
        exact = Text(
            "a head and a tail cancel exactly — impossible if evidence replaced belief,\n"
            "automatic when it reweights",
            font_size=SMALL_SIZE,
            line_spacing=1.1,
        ).next_to(cancel, DOWN, buff=0.35)
        self.play(Write(cancel))
        self.play(FadeIn(exact))
        self.wait(1.0)

        zero = caption("and a prior of zero stays zero — multiplication cannot resurrect")
        zero.next_to(exact, DOWN, buff=0.3)
        self.play(FadeIn(zero))
        self.wait(0.7)

        self.play(FadeOut(VGroup(recall, echo, chain, probs, cancel, exact, zero)))
        takeaway = Text("Yesterday's posterior is today's prior", font_size=28)
        takeaway.move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class TheHostsProtocol(ConceptScene):
    """Monty Hall as ordinary Bayes: the likelihood is the host's behavior."""

    def construct(self):
        self.play(FadeIn(self.title("The Host's Protocol"), shift=0.3 * DOWN))

        setup = Text(
            "You pick door 1. The host opens door 3 — a goat. Switch?",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(setup))

        doors = (
            VGroup(
                chip("door 1", HYP_COLOR, width=1.5),
                chip("door 2", HYP_COLOR, width=1.5),
                chip("goat", WARM, width=1.5),
            )
            .arrange(RIGHT, buff=0.5)
            .move_to(2.0 * UP)
        )
        self.play(LaggedStart(*[FadeIn(d, scale=0.8) for d in doors], lag_ratio=0.15))
        self.wait(0.4)

        # --- the proportionality table: prior x likelihood of the host's ACTION --
        def protocol_row(name, likes, posts, verdict, color):
            cells = VGroup(
                Text(name, font_size=LABEL_SIZE),
                MathTex(likes, font_size=30, color=EV_COLOR),
                MathTex(posts, font_size=30),
                Text(verdict, font_size=LABEL_SIZE, weight=BOLD, color=color),
            )
            cells.arrange(RIGHT, buff=0.7)
            return cells

        rows = VGroup(
            protocol_row("standard", r"\tfrac{1}{2},\ 1,\ 0", r"1{:}2{:}0", "wins 2/3", ACCENT),
            protocol_row(
                "Monty Fall", r"\tfrac{1}{2},\ \tfrac{1}{2},\ 0", r"1{:}1{:}0", "wins 1/2", WARM
            ),
            protocol_row("Monty Crawl", r"0,\ 1,\ 0", r"0{:}1{:}0", "wins — certainly", GOOD),
        )
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(0.45 * DOWN + 0.3 * LEFT)
        header = caption(
            "each row: the likelihood of the host's action under car @ 1, 2, 3 —\n"
            "then the posterior, and the switch verdict"
        )
        header.next_to(rows, UP, buff=0.4)
        self.play(FadeIn(header))
        for row in rows:
            self.play(FadeIn(row, shift=0.2 * RIGHT), run_time=0.7)
            self.wait(0.3)
        self.wait(0.5)

        point = Text(
            "same opened door, three answers — the likelihood is the host's behavior,\n"
            "not the revealed fact",
            font_size=BODY_SIZE,
            color=ACCENT,
            line_spacing=1.1,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(point))
        self.wait(1.0)

        # --- the dial, and the principle -----------------------------------------
        self.play(FadeOut(VGroup(doors, header, rows, point, setup)))
        dial = MathTex(
            r"\text{opens the high door with probability } p:\quad "
            r"P(\text{switch wins}) = \frac{1}{1+p}",
            font_size=36,
        ).move_to(1.3 * UP)
        dial_note = caption("p = 1/2 is the classic 2/3; p = 0 is Crawl's certainty — verified")
        dial_note.next_to(dial, DOWN, buff=0.3)
        principle = Text(
            "Rosenthal's proportionality principle — posteriors proportional to\n"
            "prior × likelihood of what you observed — is just Bayes with a uniform prior",
            font_size=SMALL_SIZE,
            line_spacing=1.1,
        ).next_to(dial_note, DOWN, buff=0.5)
        self.play(Write(dial))
        self.play(FadeIn(dial_note))
        self.play(FadeIn(principle))
        self.wait(0.9)

        uses = VGroup(
            caption("diagnosis: the prior is the prevalence"),
            caption("spam: the prior is the base rate"),
            caption("court: forgetting the prior is the prosecutor's fallacy"),
        ).arrange(DOWN, buff=0.22)
        uses.next_to(principle, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(u) for u in uses], lag_ratio=0.25))
        self.wait(0.9)

        self.play(FadeOut(VGroup(dial, dial_note, principle, uses)))
        takeaway = Text(
            "Condition on what happened, the way it happened — then multiply",
            font_size=26,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
