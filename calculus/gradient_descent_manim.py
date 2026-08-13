"""Gradient descent — the walk downhill, one line applied over and over.

The derivative toolkit's payoff: the slope becomes an update
(w <- w - eta L'(w)), the learning rate's four fates fall out of one
per-step factor, the nudge square prices the cliff, the sign-change
habit stamps every stopping place, the walk is not a ball, and the
road's own 12-knob loss walks 0.7181 -> 0.0003 read entirely off the
loss-vs-step chart the bowl taught.

    TheSlopeBecomesAStep    the update derived, the bowl walked
    TheLearningRateIsABet   one dial, four fates, one per-step factor
    TheCornerChargesTheFee  the nudge square prices the cliff
    WhereTheWalkStops       valleys, hilltops, shelves — sign-change stamps
    TheWalkIsNotABall       the basin hop no ball could make
    TheRoadsOwnWalk         the 12-knob loss, read off one chart

Every number on screen traces to plan 014's verified anchors; bowl
and factor-table values are exact dyadic rationals, double-well and
road-walk values are float64 shown at 4 decimal places.

Render:
    uv run python calculus/gradient_descent_manim.py
    uv run python calculus/gradient_descent_manim.py -s TheSlopeBecomesAStep -q draft
"""

import math

from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    GOOD,
    MUTED,
    WARM,
    ConceptScene,
    boxed,
    caption,
    chip,
    on_frame,
    palette,
    render_cli,
)


def _axes(x_range, y_range, x_length, y_length):
    """Muted axes in the house style, no tips."""
    return Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": True},
    )


def _walk(w0, eta, lprime, steps):
    """Iterate w <- w - eta * L'(w); float64 is the verified route (4 dp on screen)."""
    ws = [w0]
    for _ in range(steps):
        ws.append(ws[-1] - eta * lprime(ws[-1]))
    return ws


class TheSlopeBecomesAStep(ConceptScene):
    """A slope is a reason to move — one line turns it into motion."""

    def construct(self):
        self.play(FadeIn(self.title("The Slope Becomes a Step"), shift=0.3 * DOWN))
        opening = Text(
            "The toolkit reads which way is downhill. Now take the step.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        ax = _axes([-4.6, 4.6, 2], [0, 17, 8], 6.4, 4.0).move_to(3.2 * LEFT + 0.9 * DOWN)
        bowl = ax.plot(lambda w: w * w, x_range=[-4.1, 4.1], color=MUTED)
        tag = MathTex(r"L(w) = w^2", font_size=32, color=MUTED)
        tag.move_to(ax.c2p(-2.2, 15.5))
        self.play(Create(ax), Create(bowl), FadeIn(tag))

        # The sign of the slope is already a compass.
        left_arrow = Arrow(ax.c2p(-3.4, 0), ax.c2p(-2.2, 0), color=ACCENT, buff=0)
        right_arrow = Arrow(ax.c2p(3.4, 0), ax.c2p(2.2, 0), color=ACCENT, buff=0)
        compass = caption("slope < 0: right · slope > 0: left")
        compass.next_to(ax, DOWN, buff=0.3)
        bottom = Dot(ax.c2p(0, 0), color=GOOD, radius=0.07)
        bottom_tag = caption("L' = 0 — nowhere to go", color=GOOD)
        bottom_tag.next_to(compass, DOWN, buff=0.12)
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.play(FadeIn(compass))
        self.play(FadeIn(bottom, scale=0.5), FadeIn(bottom_tag))
        self.wait(0.5)

        # The rule's shape is forced, not posited: the toolkit's own nudge algebra.
        derive = VGroup(
            MathTex(r"\Delta L \approx L'(w)\,\Delta w", font_size=34),
            MathTex(r"\text{choose } \Delta w = -\eta\,L'(w)", font_size=34),
            MathTex(r"\Delta L \approx -\eta\,L'(w)^2 \le 0", font_size=34, color=ACCENT),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        derive.move_to(3.6 * RIGHT + 1.2 * UP)
        on_frame(derive)
        forced = caption("for a small step, the change is downhill")
        forced.next_to(derive, DOWN, buff=0.3)
        on_frame(forced)
        for line in derive:
            self.play(FadeIn(line, shift=0.2 * LEFT), run_time=0.7)
        self.play(FadeIn(forced))
        self.wait(0.7)

        # Run it: eta = 1/4 on the bowl from w0 = 4 — the walk halves forever.
        walk = [4.0, 2.0, 1.0, 0.5, 0.25]
        dots = VGroup(*[Dot(ax.c2p(w, w * w), color=ACCENT, radius=0.06) for w in walk])
        chords = VGroup(
            *[
                Arrow(
                    ax.c2p(a, a * a),
                    ax.c2p(b, b * b),
                    color=COOL,
                    buff=0.05,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.12,
                )
                for a, b in zip(walk[:-1], walk[1:], strict=True)
            ]
        )
        ticks = VGroup(*[Dot(ax.c2p(w, 0), color=COOL, radius=0.045) for w in walk])
        eta_chip = chip("η = 1/4,  w₀ = 4", COOL, width=3.2)
        eta_chip.next_to(ax, UP, buff=0.15).shift(1.2 * RIGHT)
        self.play(FadeOut(left_arrow), FadeOut(right_arrow), FadeOut(compass))
        self.play(FadeIn(eta_chip), FadeIn(dots[0], scale=0.5), FadeIn(ticks[0], scale=0.5))
        for k in range(4):
            self.play(GrowArrow(chords[k]), run_time=0.6)
            self.play(FadeIn(dots[k + 1], scale=0.5), FadeIn(ticks[k + 1], scale=0.5), run_time=0.4)
        brake = caption("the steps shrink on their own —")
        brake2 = caption("the landscape brakes, not a schedule")
        brake.move_to(3.6 * RIGHT + 1.1 * DOWN)
        brake2.next_to(brake, DOWN, buff=0.15)
        on_frame(brake)
        on_frame(brake2)
        self.play(FadeIn(brake), FadeIn(brake2))
        ticker = caption("step 9:  w = 4/512 = 0.0078125 < 0.01", color=COOL)
        ticker.next_to(brake2, DOWN, buff=0.35)
        on_frame(ticker)
        self.play(FadeIn(ticker))
        self.wait(1.0)

        # Formula last.
        rule = MathTex(r"w \;\leftarrow\; w - \eta\,L'(w)", font_size=44)
        rule.move_to(3.6 * RIGHT + 3.2 * DOWN)
        on_frame(rule)
        self.play(FadeOut(opening))
        self.play(Write(rule))
        self.play(Create(boxed(rule)))
        self.wait(1.5)


class TheLearningRateIsABet(ConceptScene):
    """One dial, four fates: the per-step factor 1 − 2η decides everything."""

    def construct(self):
        self.play(FadeIn(self.title("The Learning Rate Is a Bet"), shift=0.3 * DOWN))
        collapse = MathTex(
            r"w \leftarrow w - \eta \cdot 2w = (1 - 2\eta)\,w",
            font_size=38,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(collapse))
        scaling = caption("on this bowl the walk is repeated scaling — one factor per bet")
        scaling.next_to(collapse, DOWN, buff=0.2)
        self.play(FadeIn(scaling))

        # Four number-line rows, one bet each; the same w0 = 4 everywhere.
        rows = [
            (r"\eta = \tfrac14", r"\times\ \tfrac12", [4.0, 2.0, 1.0, 0.5], COOL, "glides in"),
            (
                r"\eta = \tfrac34",
                r"\times\ (-\tfrac12)",
                [4.0, -2.0, 1.0, -0.5],
                COOL,
                "overshoots, converges",
            ),
            (r"\eta = 1", r"\times\ (-1)", [4.0, -4.0, 4.0, -4.0], ACCENT, "ping-pongs forever"),
            (r"\eta = \tfrac54", r"\times\ (-\tfrac32)", [4.0, -6.0, 9.0], WARM, "diverges"),
        ]
        unit = 0.36  # scene units per w-unit on the rows
        row_mobs = VGroup()
        for i, (eta_tex, factor_tex, ws, color, fate) in enumerate(rows):
            y = 1.35 - 1.15 * i
            line = Line([-6.7 * unit, y, 0], [9.7 * unit, y, 0], color=MUTED, stroke_width=2)
            zero = Line([0, y - 0.09, 0], [0, y + 0.09, 0], color=MUTED, stroke_width=2)
            label = MathTex(eta_tex, font_size=30).move_to([-4.9, y + 0.28, 0])
            factor = MathTex(factor_tex, font_size=28, color=color)
            factor.move_to([-4.9, y - 0.24, 0])
            dots = VGroup(*[Dot([w * unit, y, 0], color=color, radius=0.055) for w in ws])
            hops = VGroup(
                *[
                    ArcBetweenPoints(
                        [a * unit, y, 0],
                        [b * unit, y, 0],
                        angle=-0.9,
                        color=color,
                        stroke_width=3,
                    )
                    for a, b in zip(ws[:-1], ws[1:], strict=True)
                ]
            )
            fate_cap = caption(fate, color=color).move_to([5.4, y, 0])
            on_frame(fate_cap)
            row = VGroup(line, zero, label, factor, dots, hops, fate_cap)
            row_mobs.add(row)
        row_mobs.shift(0.35 * DOWN)

        for row in row_mobs:
            line, zero, label, factor, dots, hops, fate_cap = row
            self.play(Create(line), Create(zero), FadeIn(label), FadeIn(factor), run_time=0.5)
            self.play(FadeIn(dots[0], scale=0.5), run_time=0.3)
            for k in range(len(hops)):
                self.play(Create(hops[k]), FadeIn(dots[k + 1], scale=0.5), run_time=0.35)
            self.play(FadeIn(fate_cap), run_time=0.4)
        self.wait(0.8)

        # The loss inset cannot tell the first two rows apart.
        self.play(FadeOut(scaling))
        same = caption("η = ¾ crosses the bottom every step — and its losses", color=COOL)
        same2 = caption("are 16, 4, 1, ¼: identical to the glide's, step for step", color=COOL)
        same.move_to(0.0 * RIGHT + 3.25 * DOWN)
        same2.next_to(same, DOWN, buff=0.15)
        on_frame(same)
        on_frame(same2)
        self.play(FadeIn(same), FadeIn(same2))
        self.wait(1.0)
        self.play(FadeOut(same), FadeOut(same2))

        # Convergence is |factor| < 1 — and too small merely bills you.
        bill = caption("η = 1/40 also arrives — in 117 steps against 9:")
        bill2 = caption("too small never lies; it bills you")
        bill.move_to(0.0 * RIGHT + 3.25 * DOWN)
        bill2.next_to(bill, DOWN, buff=0.15)
        self.play(FadeIn(bill), FadeIn(bill2))
        self.wait(1.0)
        self.play(FadeOut(bill), FadeOut(bill2))

        verdict = MathTex(
            r"|1 - 2\eta| < 1 \;\iff\; 0 < \eta < 1",
            font_size=40,
        ).move_to(0.7 * LEFT + 3.5 * DOWN)
        pinned = caption("— for this bowl", color=ACCENT)
        pinned.next_to(verdict, RIGHT, buff=0.75)
        on_frame(pinned)
        self.play(Write(verdict))
        self.play(Create(boxed(verdict)), FadeIn(pinned))
        self.wait(1.5)


class TheCornerChargesTheFee(ConceptScene):
    """Why the cliff sits at η = 1: the nudge square with a finite step."""

    def construct(self):
        self.play(FadeIn(self.title("The Corner Charges the Fee"), shift=0.3 * DOWN))
        opening = Text(
            "The toolkit's square again — but the step is no longer tiny.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The square: two strips pay, the corner charges.
        side = 2.0
        dw = 0.7
        origin = [-5.4, -2.4, 0]
        base = Square(side_length=side, color=COOL, fill_color=COOL, fill_opacity=0.12)
        base.move_to([origin[0] + side / 2, origin[1] + side / 2, 0])
        strip_r = Rectangle(width=dw, height=side, color=COOL, fill_color=COOL, fill_opacity=0.35)
        strip_r.move_to([origin[0] + side + dw / 2, origin[1] + side / 2, 0])
        strip_t = Rectangle(width=side, height=dw, color=COOL, fill_color=COOL, fill_opacity=0.35)
        strip_t.move_to([origin[0] + side / 2, origin[1] + side + dw / 2, 0])
        corner = Square(side_length=dw, color=WARM, fill_color=WARM, fill_opacity=0.45)
        corner.move_to([origin[0] + side + dw / 2, origin[1] + side + dw / 2, 0])
        w_tag = MathTex(r"w", font_size=32).next_to(base, DOWN, buff=0.15)
        dw_tag = MathTex(r"\Delta w", font_size=30, color=COOL).next_to(strip_r, DOWN, buff=0.15)
        strips_tag = MathTex(r"2w\,\Delta w", font_size=32, color=COOL)
        strips_tag.next_to(strip_t, UP, buff=0.18)
        corner_tag = MathTex(r"\Delta w^2", font_size=30, color=WARM)
        corner_tag.next_to(corner, RIGHT, buff=0.18)
        on_frame(corner_tag)
        self.play(Create(base), FadeIn(w_tag))
        self.play(FadeIn(strip_r), FadeIn(strip_t), FadeIn(dw_tag), FadeIn(strips_tag))
        self.play(FadeIn(corner), FadeIn(corner_tag))
        pay = caption("the strips pay; the corner charges back")
        pay.next_to(strips_tag, UP, buff=0.3)
        on_frame(pay)
        self.play(FadeIn(pay))
        self.wait(0.5)

        # The ledger, exactly.
        ledger = VGroup(
            MathTex(r"\Delta L = 2w\,\Delta w + \Delta w^2", font_size=34),
            MathTex(r"\Delta w = -2\eta w", font_size=34),
            MathTex(
                r"\Delta L = -4\eta w^2 + 4\eta^2 w^2 = 4\eta w^2(\eta - 1)",
                font_size=34,
                color=ACCENT,
            ),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ledger.move_to(2.6 * RIGHT + 1.35 * UP)
        on_frame(ledger)
        for line in ledger:
            self.play(FadeIn(line, shift=0.2 * LEFT), run_time=0.7)

        at4 = caption("checked at w = 4:")
        checks = VGroup(
            chip("η = ¼:  ΔL = −12   (16 → 4)", GOOD, width=5.0),
            chip("η = 1:  ΔL = 0   (16 → 16)", ACCENT, width=5.0),
            chip("η = 5/4:  ΔL = +20   (16 → 36)", WARM, width=5.6),
        ).arrange(DOWN, buff=0.22)
        checks.move_to(2.6 * RIGHT + 1.1 * DOWN)
        on_frame(checks)
        at4.next_to(checks, UP, buff=0.15).align_to(checks, LEFT)
        self.play(FadeIn(at4))
        for c in checks:
            self.play(FadeIn(c, shift=0.15 * UP), run_time=0.5)
        tie = caption("strips grow like η, the corner like η² —", color=ACCENT)
        tie2 = caption("they tie exactly at η = 1", color=ACCENT)
        tie.next_to(checks, DOWN, buff=0.3)
        tie2.next_to(tie, DOWN, buff=0.15)
        on_frame(tie)
        on_frame(tie2)
        self.play(FadeIn(tie), FadeIn(tie2))
        self.wait(1.0)

        # The bet's other side: the same eta, a sharper bowl.
        self.play(
            FadeOut(pay),
            FadeOut(at4),
            FadeOut(checks),
            FadeOut(strips_tag),
            FadeOut(corner_tag),
            FadeOut(dw_tag),
            FadeOut(w_tag),
            FadeOut(base),
            FadeOut(strip_r),
            FadeOut(strip_t),
            FadeOut(corner),
        )
        ax = _axes([-4.6, 4.6, 2], [0, 17, 8], 5.2, 3.2).move_to(3.9 * LEFT + 1.1 * DOWN)
        ghost = ax.plot(lambda w: w * w, x_range=[-4.1, 4.1], color=MUTED)
        slim = ax.plot(lambda w: 4 * w * w, x_range=[-2.05, 2.05], color=WARM)
        slim_tag = MathTex(r"L = 4w^2", font_size=30, color=WARM)
        slim_tag.next_to(ax, UP, buff=0.12).align_to(ax, LEFT).shift(0.3 * RIGHT)
        ghost_tag = MathTex(r"w^2", font_size=28, color=MUTED)
        ghost_tag.next_to(ax, UP, buff=0.12).align_to(ax, RIGHT).shift(0.3 * LEFT)
        self.play(Create(ax), Create(ghost), FadeIn(ghost_tag))
        self.play(Create(slim), FadeIn(slim_tag))
        pp = VGroup(
            Dot(ax.c2p(2, 16), color=WARM, radius=0.06),
            Dot(ax.c2p(-2, 16), color=WARM, radius=0.06),
        )
        pp_arrow = ArcBetweenPoints(
            ax.c2p(2, 16), ax.c2p(-2, 16), angle=0.5, color=WARM, stroke_width=3
        )
        same_bet = caption("the same η = ¼ that glided on w²…", color=WARM)
        same_bet2 = caption("…ping-pongs here: factor 1 − 8η = −1", color=WARM)
        same_bet.next_to(ax, DOWN, buff=0.3)
        same_bet2.next_to(same_bet, DOWN, buff=0.15)
        on_frame(same_bet)
        on_frame(same_bet2)
        self.play(FadeIn(pp), Create(pp_arrow))
        self.play(FadeIn(same_bet), FadeIn(same_bet2))
        thresholds = caption("safe rates:  w²: η < 1   ·   4w²: η < ¼")
        thresholds.move_to(2.6 * RIGHT + 1.35 * DOWN)
        on_frame(thresholds)
        self.play(FadeIn(thresholds))
        self.wait(0.8)

        # Formula last: the fee, priced.
        self.play(FadeOut(opening))
        fee = caption("a bet about curvature — and the corner is its fee")
        fee.move_to(3.0 * RIGHT + 3.45 * DOWN)
        on_frame(fee)
        self.play(Create(boxed(ledger[2], buff=0.12)), FadeIn(fee))
        self.wait(1.5)


class WhereTheWalkStops(ConceptScene):
    """The update is zero wherever L' is — and the rule cannot tell which flat ground."""

    def construct(self):
        self.play(FadeIn(self.title("Where the Walk Stops"), shift=0.3 * DOWN))
        opening = Text(
            "Descent stops at flat ground. Flat ground comes in three kinds.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        ax = _axes([-1.7, 1.7, 1], [-0.4, 0.55, 0.25], 6.8, 3.4).move_to(3.0 * LEFT + 1.1 * DOWN)
        well = ax.plot(lambda w: w**4 / 4 - w**2 / 2, x_range=[-1.62, 1.62], color=MUTED)
        tag = MathTex(r"L(w) = \tfrac{w^4}{4} - \tfrac{w^2}{2}", font_size=30, color=MUTED)
        tag.next_to(ax, UP, buff=0.1)
        lp = MathTex(r"L'(w) = w^3 - w = 0 \ \text{at}\ -1,\ 0,\ 1", font_size=32)
        lp.move_to(3.8 * RIGHT + 1.6 * UP)
        on_frame(lp)
        self.play(Create(ax), Create(well), FadeIn(tag))
        self.play(FadeIn(lp))

        # Sign-change stamps: the derivative series' habit, doing its job.
        flats = VGroup(
            Dot(ax.c2p(-1, -0.25), color=GOOD, radius=0.06),
            Dot(ax.c2p(0, 0), color=WARM, radius=0.06),
            Dot(ax.c2p(1, -0.25), color=GOOD, radius=0.06),
        )
        stamp_l = caption("− to +: valley", color=GOOD).next_to(ax.c2p(-1, -0.25), DOWN, buff=0.25)
        stamp_m = caption("+ to −: hilltop", color=WARM).next_to(ax.c2p(0, 0), UP, buff=0.3)
        stamp_r = caption("− to +: valley", color=GOOD).next_to(ax.c2p(1, -0.25), DOWN, buff=0.25)
        on_frame(stamp_l)
        on_frame(stamp_r)
        self.play(FadeIn(flats, lag_ratio=0.3))
        self.play(FadeIn(stamp_l), FadeIn(stamp_m), FadeIn(stamp_r))
        self.wait(0.6)

        # Walk one: from 0.5, into the valley at 1 — monotone, no overshoot.
        walk1 = _walk(0.5, 0.1, lambda w: w**3 - w, 24)
        shown1 = walk1[::4] + [walk1[-1]]
        dots1 = VGroup(
            *[Dot(ax.c2p(w, w**4 / 4 - w**2 / 2), color=COOL, radius=0.05) for w in shown1]
        )
        w1_chip = chip("η = 0.1,  w₀ = 0.5", COOL, width=3.4)
        w1_chip.move_to(3.8 * RIGHT + 0.6 * UP)
        on_frame(w1_chip)
        self.play(FadeIn(w1_chip))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots1], lag_ratio=0.18))
        arrive1 = caption("climbs monotonically to the valley;")
        arrive1b = caption("within 0.01 of w = 1 by step 24")
        arrive1.move_to(3.8 * RIGHT + 0.0 * UP)
        arrive1b.next_to(arrive1, DOWN, buff=0.15)
        on_frame(arrive1)
        on_frame(arrive1b)
        self.play(FadeIn(arrive1), FadeIn(arrive1b))
        self.wait(0.6)

        # Walk two: started exactly on the hilltop, the rule sits forever.
        sit = Dot(ax.c2p(0, 0), color=WARM, radius=0.08)
        self.play(FadeIn(sit, scale=0.4))
        self.play(Indicate(sit, color=WARM, scale_factor=1.6))
        sits = caption("from w₀ = 0 the update is exactly zero;", color=WARM)
        sits2 = caption("the walk sits on the hilltop,", color=WARM)
        sits3 = caption("certifying nothing", color=WARM)
        sits.move_to(3.8 * RIGHT + 0.9 * DOWN)
        sits2.next_to(sits, DOWN, buff=0.15)
        sits3.next_to(sits2, DOWN, buff=0.15)
        on_frame(sits)
        on_frame(sits2)
        self.play(FadeIn(sits), FadeIn(sits2), FadeIn(sits3))
        nudge = caption("nudged to 0.1, it falls in (step 42)")
        nudge.next_to(sits3, DOWN, buff=0.3)
        on_frame(nudge)
        walk2 = _walk(0.1, 0.1, lambda w: w**3 - w, 42)
        shown2 = walk2[::7] + [walk2[-1]]
        dots2 = VGroup(
            *[Dot(ax.c2p(w, w**4 / 4 - w**2 / 2), color=ACCENT, radius=0.045) for w in shown2]
        )
        self.play(FadeIn(nudge))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots2], lag_ratio=0.15))
        self.wait(0.8)

        # The third kind of flat: a shelf, crawled into and never certified.
        self.play(
            FadeOut(sits),
            FadeOut(sits2),
            FadeOut(sits3),
            FadeOut(nudge),
            FadeOut(arrive1),
            FadeOut(arrive1b),
            FadeOut(w1_chip),
        )
        shelf_ax = _axes([0, 1.3, 1], [0, 0.4, 0.2], 2.9, 1.7).move_to(4.3 * RIGHT + 1.05 * DOWN)
        on_frame(shelf_ax)
        shelf = shelf_ax.plot(lambda w: w**3 / 3, x_range=[0, 1.06], color=MUTED)
        shelf_tag = MathTex(r"L = \tfrac{w^3}{3}", font_size=26, color=MUTED)
        shelf_tag.next_to(shelf_ax, UP, buff=0.1)
        crawl = _walk(1.0, 0.1, lambda w: w * w, 8)
        crawl_dots = VGroup(
            *[Dot(shelf_ax.c2p(w, w**3 / 3), color=COOL, radius=0.04) for w in crawl]
        )
        self.play(Create(shelf_ax), Create(shelf), FadeIn(shelf_tag))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in crawl_dots], lag_ratio=0.12))
        shelf_cap = caption("a shelf: no sign change, no minimum —")
        shelf_cap2 = caption("the crawl slows without arriving")
        shelf_cap.next_to(shelf_ax, DOWN, buff=0.25)
        shelf_cap2.next_to(shelf_cap, DOWN, buff=0.15)
        on_frame(shelf_cap)
        on_frame(shelf_cap2)
        self.play(FadeIn(shelf_cap), FadeIn(shelf_cap2))
        self.wait(0.8)

        # Formula last: the stop condition, and the stamp that reads it.
        self.play(FadeOut(opening))
        stop = MathTex(
            r"L'(w) = 0 \ \text{ends the walk; the sign change says what was found}",
            font_size=32,
        ).move_to(0.2 * RIGHT + 3.5 * DOWN)
        on_frame(stop)
        self.play(Write(stop))
        self.play(Create(boxed(stop, buff=0.18)))
        self.wait(1.5)


class TheWalkIsNotABall(ConceptScene):
    """The rule jumps; a ball rolls — the basin hop no ball could make."""

    def construct(self):
        self.play(FadeIn(self.title("The Walk Is Not a Ball"), shift=0.3 * DOWN))
        opening = Text(
            "Same double well, same rule — started from farther out.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        ax = _axes([-2.5, 2.5, 1], [-0.5, 2.3, 1], 6.6, 2.9).move_to(3.0 * LEFT + 0.5 * UP)
        well = ax.plot(lambda w: w**4 / 4 - w**2 / 2, x_range=[-2.0, 2.0], color=MUTED)
        self.play(Create(ax), Create(well))

        # From w0 = 2: tame — a ball would tell the same story.
        walk_tame = _walk(2.0, 0.1, lambda w: w**3 - w, 15)
        shown = walk_tame[:8]
        dots_tame = VGroup(
            *[Dot(ax.c2p(w, w**4 / 4 - w**2 / 2), color=COOL, radius=0.05) for w in shown]
        )
        tame_chip = chip("w₀ = 2,  η = 0.1", COOL, width=3.0)
        tame_chip.move_to(4.2 * RIGHT + 1.9 * UP)
        on_frame(tame_chip)
        self.play(FadeIn(tame_chip))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_tame], lag_ratio=0.15))
        tame_cap = caption("2.0000, 1.4000, 1.2656 — never below 1;")
        tame_cap2 = caption("a ball would agree with every step")
        tame_cap.move_to(3.95 * RIGHT + 1.15 * UP)
        tame_cap2.next_to(tame_cap, DOWN, buff=0.15)
        on_frame(tame_cap)
        on_frame(tame_cap2)
        self.play(FadeIn(tame_cap), FadeIn(tame_cap2))
        self.wait(0.6)

        # The walk's true home is the w-axis: from w0 = 4, one hop clears everything.
        line_y = -2.0
        unit = 1.25
        wline = Line([-5.2 * unit, line_y, 0], [5.2 * unit, line_y, 0], color=MUTED, stroke_width=2)
        ticks = VGroup()
        for w in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
            ticks.add(Line([w * unit, line_y - 0.08, 0], [w * unit, line_y + 0.08, 0], color=MUTED))
        wl_tag = caption("the w-axis — the walk's true home")
        wl_tag.next_to(wline, DOWN, buff=0.55)
        self.play(Create(wline), Create(ticks), FadeIn(wl_tag))
        slope_chip = chip("L′(4) = 60", WARM, width=1.9)
        slope_chip.move_to(4.2 * RIGHT + 0.1 * UP)
        on_frame(slope_chip)
        start4 = Dot([4 * unit, line_y, 0], color=WARM, radius=0.07)
        self.play(FadeIn(slope_chip), FadeIn(start4, scale=0.5))
        hop = CurvedArrow(
            [4 * unit, line_y, 0],
            [-2 * unit, line_y, 0],
            angle=0.75,
            color=WARM,
            stroke_width=4,
        )
        self.play(Create(hop))
        land = Dot([-2 * unit, line_y, 0], color=WARM, radius=0.07)
        hop_cap = caption("one hop: 4 → −2, over the hilltop and both walls", color=WARM)
        hop_cap.next_to(wl_tag, DOWN, buff=0.2)
        self.play(FadeIn(land, scale=0.5), FadeIn(hop_cap))
        walk_hop = _walk(-2.0, 0.1, lambda w: w**3 - w, 6)
        settle = VGroup(
            *[Dot([w * unit, line_y, 0], color=WARM, radius=0.045) for w in walk_hop[1:]]
        )
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in settle], lag_ratio=0.15))
        settle_cap = caption("…then −1.4, −1.27, settling in the LEFT valley", color=WARM)
        settle_cap.next_to(hop_cap, DOWN, buff=0.15)
        self.play(FadeIn(settle_cap))
        self.wait(0.8)

        # What a ball cannot do, in three stamps.
        self.play(FadeOut(tame_cap), FadeOut(tame_cap2), FadeOut(tame_chip), FadeOut(slope_chip))
        stamps = VGroup(
            caption("a ball coasts;"),
            caption("the rule has no memory"),
            caption("a ball rolls off the hilltop;"),
            caption("the rule sits"),
            caption("a ball never teleports;"),
            caption("the rule just did"),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        stamps.move_to(4.05 * RIGHT + 1.0 * UP)
        on_frame(stamps)
        for s in stamps:
            self.play(FadeIn(s, shift=0.15 * LEFT), run_time=0.4)
        self.wait(0.6)

        # The basin map: which valley a start lands in, colored on the line.
        self.play(FadeOut(hop_cap), FadeOut(settle_cap), FadeOut(wl_tag))
        basin_r = Line([0.05 * unit, line_y, 0], [3.31 * unit, line_y, 0], stroke_width=7)
        basin_r.set_color(palette(0))
        basin_far = Line([3.33 * unit, line_y, 0], [5.0 * unit, line_y, 0], stroke_width=7)
        basin_far.set_color(palette(1))
        boundary = MathTex(r"\sqrt{11} \approx 3.317", font_size=26)
        boundary.next_to([3.32 * unit, line_y, 0], UP, buff=0.22)
        on_frame(boundary)
        map_cap = caption("starts in (0, √11) land at +1; past it, they cross")
        map_cap.next_to(wline, DOWN, buff=0.55)
        mirror = caption("(mirrored on the left)")
        mirror.next_to(map_cap, DOWN, buff=0.15)
        self.play(Create(basin_r), Create(basin_far), FadeIn(boundary), FadeIn(map_cap))
        self.play(FadeIn(mirror))
        self.wait(0.8)

        # Close: the metaphor that survives.
        self.play(FadeOut(opening))
        keep = Text(
            "Keep the walker: it reads the ground underfoot, step by step.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(keep))
        self.wait(1.5)


class TheRoadsOwnWalk(ConceptScene):
    """Many knobs in one sentence — then the CTC road's real walk, read off one chart."""

    def construct(self):
        self.play(FadeIn(self.title("The Road's Own Walk"), shift=0.3 * DOWN))
        opening = Text(
            "Many knobs at once — and the generalisation costs one sentence.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The twelve knobs: the alignment table, trainable.
        grid = VGroup()
        for r in range(3):
            for c in range(4):
                cell = Square(side_length=0.5, color=MUTED, fill_color=MUTED, fill_opacity=0.15)
                cell.move_to([-4.6 + 0.6 * c, 1.3 - 0.6 * r, 0])
                grid.add(cell)
        grid_cap = caption("the alignment table — twelve knobs")
        grid_cap.next_to(grid, DOWN, buff=0.3)
        many = MathTex(
            r"\mathbf{w} \leftarrow \mathbf{w} - \eta\,\nabla L(\mathbf{w})", font_size=38
        )
        many.move_to(3.0 * RIGHT + 1.0 * UP)
        many_cap = caption("the gradient collects every knob's slope;")
        many_cap2 = caption("each reads its own, all move together")
        many_cap.next_to(many, DOWN, buff=0.25)
        many_cap2.next_to(many_cap, DOWN, buff=0.15)
        self.play(FadeIn(grid, lag_ratio=0.05), FadeIn(grid_cap))
        self.play(Write(many), FadeIn(many_cap), FadeIn(many_cap2))
        sentence = caption("that is all “plain gradient descent” ever meant", color=ACCENT)
        sentence.next_to(many_cap2, DOWN, buff=0.3)
        self.play(FadeIn(sentence))
        self.wait(0.8)

        # The walk itself, on the only readout there is.
        self.play(
            FadeOut(grid),
            FadeOut(grid_cap),
            FadeOut(many),
            FadeOut(many_cap),
            FadeOut(many_cap2),
            FadeOut(sentence),
            FadeOut(opening),
        )
        steps = [0, 10, 50, 200, 5000]
        losses = [0.7181, 0.1602, 0.0356, 0.0088, 0.0003]
        lin = _axes([0, 50, 10], [0, 0.75, 0.25], 5.4, 3.0).move_to(3.4 * LEFT + 0.55 * DOWN)
        lin_tag = caption("loss vs step — the first fifty")
        lin_tag.next_to(lin, UP, buff=0.12)
        lin_dots = VGroup(
            *[
                Dot(lin.c2p(s, v), color=COOL, radius=0.055)
                for s, v in zip(steps[:3], losses[:3], strict=True)
            ]
        )
        lin_guide = DashedLine(lin.c2p(0, 0.7181), lin.c2p(10, 0.1602), color=MUTED, stroke_width=2)
        self.play(Create(lin), FadeIn(lin_tag))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in lin_dots], lag_ratio=0.2))
        self.play(Create(lin_guide))
        sampled = caption("the cliff — most of the loss gone at once")
        sampled.next_to(lin, DOWN, buff=0.25)
        self.play(FadeIn(sampled))

        log = _axes([0, 5000, 1000], [-9, 0, 3], 5.4, 3.0).move_to(3.6 * RIGHT + 0.55 * DOWN)
        on_frame(log)
        log_tag = caption("all 5000 steps — log axis")
        log_tag.next_to(log, UP, buff=0.12)
        on_frame(log_tag)
        log_dots = VGroup(
            *[
                Dot(log.c2p(s, math.log(v)), color=COOL, radius=0.055)
                for s, v in zip(steps, losses, strict=True)
            ]
        )
        self.play(Create(log), FadeIn(log_tag))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in log_dots], lag_ratio=0.2))
        still = caption("five samples, η = 1 — the tail still falls", color=COOL)
        still.next_to(log, DOWN, buff=0.25)
        on_frame(still)
        self.play(FadeIn(still))
        ruler = caption("× per step: a straight march on the log ruler")
        ruler.next_to(still, DOWN, buff=0.15)
        on_frame(ruler)
        self.play(FadeIn(ruler))
        self.wait(0.8)

        # The physiology, priced: front-loaded early, the brake at scale late.
        self.play(FadeOut(sampled), FadeOut(still), FadeOut(ruler))
        factors = VGroup(
            chip("0 → 10:  × 0.86 per step", COOL, width=4.5),
            chip("200 → 5000:  × 0.9993 per step", MUTED, width=5.7),
        ).arrange(DOWN, buff=0.22)
        factors.move_to(3.6 * LEFT + 3.15 * DOWN)
        quarters = caption("over three-quarters gone in ten steps;")
        quarters2 = caption("the flat tail is scene 1's brake at scale")
        quarters.move_to(3.2 * RIGHT + 3.0 * DOWN)
        quarters2.next_to(quarters, DOWN, buff=0.15)
        on_frame(quarters)
        on_frame(quarters2)
        self.play(FadeIn(factors[0], shift=0.15 * UP), FadeIn(factors[1], shift=0.15 * UP))
        self.play(FadeIn(quarters), FadeIn(quarters2))
        self.wait(1.0)

        # Frame 3's gem, inherited from the gradient series.
        self.play(
            FadeOut(lin),
            FadeOut(lin_tag),
            FadeOut(lin_dots),
            FadeOut(lin_guide),
            FadeOut(log),
            FadeOut(log_tag),
            FadeOut(log_dots),
            FadeOut(factors),
            FadeOut(quarters),
            FadeOut(quarters2),
        )
        heights = [0.032, 0.218, 0.750]
        labels = ["A", "B", "ε"]
        bars = VGroup()
        for i, (h, lab) in enumerate(zip(heights, labels, strict=True)):
            bar = Rectangle(
                width=0.7,
                height=3.2 * h,
                color=palette(i),
                fill_color=palette(i),
                fill_opacity=0.5,
            )
            bar.move_to([-3.6 + 1.1 * i, -1.5 + 1.6 * h, 0])
            value = caption(f"{h:.3f}", color=palette(i)).next_to(bar, UP, buff=0.12)
            name = caption(lab).next_to(bar, DOWN, buff=0.12)
            bars.add(VGroup(bar, value, name))
        gem = caption("frame 3 settles mixed — gradient ≈ 10⁻⁴,")
        gem2 = caption("y matches γ out of indifference")
        gem.move_to(3.2 * RIGHT + 0.3 * UP)
        gem2.next_to(gem, DOWN, buff=0.15)
        on_frame(gem)
        on_frame(gem2)
        self.play(FadeIn(bars, lag_ratio=0.2))
        self.play(FadeIn(gem), FadeIn(gem2))
        self.wait(1.0)

        # When-useful close: the engine, and its age.
        closing = VGroup(
            caption("the engine under deep learning —"),
            caption("all real training adds is refinement;"),
            caption("and the rule is older than the field:"),
            caption("Cauchy, 1847, computing planetary"),
            caption("orbits (as quoted by Lemaréchal);"),
            caption("convergence theory a century later"),
            caption("(Curry, 1944)"),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        closing.move_to(3.2 * RIGHT + 1.9 * DOWN)
        on_frame(closing)
        for line in closing:
            self.play(FadeIn(line, shift=0.1 * LEFT), run_time=0.4)
        self.wait(1.8)


if __name__ == "__main__":
    render_cli()
