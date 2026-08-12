"""The derivative toolkit — naming what the zoom built, and just enough rules.

The series the CTC gradient waits on: the slope as a function (d/dx
names the settling ratio `ZoomUntilStraight` built), nudge geometry
for x², the sum and chain rules, e^x and ln in notation, the score
function deriving the likelihood peak the probability series read off
its plotted curve, and the closer — the smooth max's sensitivities ARE the softmax
shares, leaving p − one-hot one subtraction away.

    TheSlopeIsAFunction     the slope at every point is a second curve
    NudgeInNudgeOut         the x² square: strips live, the corner dies
    NudgesAddNudgesCompose  the two load-bearing rules
    TheCurveThatIsItsOwnSlope   e^x and ln, in d/dx notation
    ZeroSlopeFindsThePeak   the score finds the MLE peak by hand
    TheSmoothMaxsShares     dLSE = softmax; the loss gradient lands

Every number on screen traces to plan 009's verified anchors; tables
use forward quotients (the symmetric quotient of a quadratic is exact
and would kill the settling narrative), and dt stays a real number
throughout.

Render:
    uv run python calculus/derivatives_manim.py
    uv run python calculus/derivatives_manim.py -s TheSlopeIsAFunction -q draft
"""

from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    GOOD,
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


def _quotient_table(rows, settle, x=0.0, y=0.0, row_size=34):
    """A settling forward-quotient table with an ACCENT limit readout."""
    lines = VGroup(*[MathTex(r, font_size=row_size) for r in rows])
    lines.arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to([x, y, 0])
    limit = MathTex(settle, font_size=40, color=ACCENT)
    limit.next_to(lines, RIGHT, buff=0.7)
    return lines, limit


class TheSlopeIsAFunction(ConceptScene):
    """Every smooth curve carries a second curve: its slope at each point."""

    def construct(self):
        self.play(FadeIn(self.title("The Slope Is a Function"), shift=0.3 * DOWN))

        opening = Text(
            "The zoom read one slope, at one point. Now run it everywhere.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The dual graph: x² above, its slopes plotted beneath.
        top = _axes([-2, 2, 1], [0, 4, 2], 5.4, 2.4).move_to(3.4 * LEFT + 1.0 * UP)
        curve = top.plot(lambda x: x**2, x_range=[-2, 2], color=COOL)
        f_tag = MathTex(r"f(x) = x^2", font_size=30, color=COOL).next_to(top, RIGHT, buff=0.25)
        bottom = _axes([-2, 2, 1], [-4, 4, 2], 5.4, 2.4).move_to(3.4 * LEFT + 1.85 * DOWN)
        self.play(Create(top), Create(curve), FadeIn(f_tag))
        self.play(Create(bottom))

        # Tangent stubs at three points; each slope becomes a plotted dot.
        dots = VGroup()
        stubs = VGroup()
        for x0 in [-1.0, 0.5, 1.5]:
            slope = 2 * x0
            p = top.c2p(x0, x0**2)
            direction = np.array([1.0, 0.0, 0.0]) + np.array(
                [0.0, (top.c2p(0, 1)[1] - top.c2p(0, 0)[1]) * slope / 1.35, 0.0]
            )
            direction = direction / np.linalg.norm(direction)
            stub = Line(p - 0.55 * direction, p + 0.55 * direction, color=ACCENT, stroke_width=3)
            stubs.add(stub)
            dots.add(Dot(bottom.c2p(x0, slope), color=ACCENT, radius=0.06))
        read_off = caption("zoom, straighten, read the slope — at every x")
        read_off.move_to(3.4 * LEFT + 3.3 * DOWN)
        self.play(LaggedStart(*[Create(s) for s in stubs], lag_ratio=0.3))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3))
        self.play(FadeIn(read_off))
        slope_curve = bottom.plot(lambda x: 2 * x, x_range=[-2, 2], color=ACCENT)
        s_tag = MathTex(r"\frac{df}{dx} = 2x", font_size=32, color=ACCENT)
        s_tag.next_to(bottom, RIGHT, buff=0.25)
        self.play(Create(slope_curve), FadeIn(s_tag))
        two_numbers = caption("at x = 1 the height is 1, the slope is 2 —")
        two_numbers2 = caption("two different numbers, tracked on two curves")
        on_frame(two_numbers.move_to(3.8 * RIGHT + 2.0 * UP))
        on_frame(two_numbers2.next_to(two_numbers, DOWN, buff=0.15))
        self.play(FadeIn(two_numbers), FadeIn(two_numbers2))
        self.wait(1.0)

        # The settling table: the zoom made arithmetic.
        rows, limit = _quotient_table(
            [
                r"dt = 1:\quad \tfrac{(1+1)^2 - 1}{1} = 3",
                r"dt = 0.1:\quad 2.1",
                r"dt = 0.01:\quad 2.01",
                r"dt = 0.001:\quad 2.001",
            ],
            r"\rightarrow\ 2",
            x=3.3,
            y=0.3,
            row_size=30,
        )
        literally = caption("the entries are literally 2 + dt —")
        literally2 = caption("the settling is visible in the digits")
        on_frame(literally.move_to(3.8 * RIGHT + 1.5 * DOWN))
        on_frame(literally2.next_to(literally, DOWN, buff=0.15))
        self.play(FadeOut(VGroup(two_numbers, two_numbers2)))
        self.play(LaggedStart(*[Write(r) for r in rows], lag_ratio=0.3))
        self.play(Write(limit))
        self.play(FadeIn(literally), FadeIn(literally2))
        smooth_only = caption("(smooth curves only: |x| never straightens at 0)")
        on_frame(smooth_only.move_to(3.8 * RIGHT + 2.6 * DOWN))
        self.play(FadeIn(smooth_only))
        self.wait(1.0)

        # Notation: whose mark this repo writes.
        self.play(
            FadeOut(
                VGroup(
                    opening,
                    top,
                    curve,
                    f_tag,
                    bottom,
                    slope_curve,
                    s_tag,
                    stubs,
                    dots,
                    read_off,
                    rows,
                    limit,
                    literally,
                    literally2,
                    smooth_only,
                )
            )
        )
        leibniz = MathTex(r"\frac{df}{dx}", font_size=56, color=ACCENT).move_to(0.9 * UP)
        who = caption("Leibniz's mark — manuscript 1675, in print 1684;")
        who2 = caption("Newton wrote a dot. This repo writes Leibniz,")
        who3 = caption("because the chain rule will look like cancelling fractions")
        who.next_to(leibniz, DOWN, buff=0.4)
        who2.next_to(who, DOWN, buff=0.15)
        who3.next_to(who2, DOWN, buff=0.15)
        self.play(Write(leibniz))
        self.play(FadeIn(who), FadeIn(who2), FadeIn(who3))
        takeaway = Text(
            "The derivative is a function: the slope, at every point",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class NudgeInNudgeOut(ConceptScene):
    """The x² square: two strips carry the slope, the corner dies faster."""

    def construct(self):
        self.play(FadeIn(self.title("Nudge In, Nudge Out"), shift=0.3 * DOWN))

        opening = Text(
            "For x², the derivative is drawn, not computed.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The literal square, side x = 3 (drawn at 0.75 scale), nudged by dx.
        unit = 0.75
        x_len, dx_len = 3 * unit, 0.5 * unit
        base = Square(side_length=x_len, stroke_width=2, color=COOL)
        base.move_to(3.6 * LEFT + 0.55 * DOWN, aligned_edge=DOWN + LEFT)
        strip_r = Rectangle(
            width=dx_len,
            height=x_len,
            stroke_width=2,
            color=GOOD,
            fill_color=GOOD,
            fill_opacity=0.25,
        ).next_to(base, RIGHT, buff=0)
        strip_t = Rectangle(
            width=x_len,
            height=dx_len,
            stroke_width=2,
            color=GOOD,
            fill_color=GOOD,
            fill_opacity=0.25,
        ).next_to(base, UP, buff=0)
        corner = Square(
            side_length=dx_len,
            stroke_width=2,
            color=WARM,
            fill_color=WARM,
            fill_opacity=0.3,
        ).next_to(strip_t, RIGHT, buff=0)
        x_lab = MathTex("x", font_size=32, color=COOL).next_to(base, DOWN, buff=0.18)
        dx_lab = MathTex("dx", font_size=28, color=GOOD).next_to(strip_r, DOWN, buff=0.18)
        self.play(FadeIn(base), FadeIn(x_lab))
        self.play(FadeIn(strip_r), FadeIn(strip_t), FadeIn(dx_lab))
        self.play(FadeIn(corner, scale=0.6))
        strips_note = caption("grow the side by dx: two strips of area x·dx —")
        strips_note2 = caption("and one dx·dx corner")
        on_frame(strips_note.move_to(3.4 * RIGHT + 1.7 * UP))
        on_frame(strips_note2.next_to(strips_note, DOWN, buff=0.15))
        self.play(FadeIn(strips_note), FadeIn(strips_note2))
        expansion = MathTex(
            r"d(x^2) = 2x\,dx + dx^2",
            font_size=38,
        ).move_to(3.4 * RIGHT + 0.6 * UP)
        self.play(Write(expansion))
        self.wait(0.6)

        # Shrink dx: the corner dies faster than the strips.
        for scale in [0.5, 0.4]:
            new_dx = dx_len * scale
            new_r = Rectangle(
                width=new_dx,
                height=x_len,
                stroke_width=2,
                color=GOOD,
                fill_color=GOOD,
                fill_opacity=0.25,
            ).next_to(base, RIGHT, buff=0)
            new_t = Rectangle(
                width=x_len,
                height=new_dx,
                stroke_width=2,
                color=GOOD,
                fill_color=GOOD,
                fill_opacity=0.25,
            ).next_to(base, UP, buff=0)
            new_c = Square(
                side_length=new_dx,
                stroke_width=2,
                color=WARM,
                fill_color=WARM,
                fill_opacity=0.3,
            ).next_to(new_t, RIGHT, buff=0)
            self.play(
                Transform(strip_r, new_r),
                Transform(strip_t, new_t),
                Transform(corner, new_c),
                run_time=0.8,
            )
        dies = caption("halve dx: the strips halve, the corner quarters —")
        dies2 = caption("second-order small, discarded with a visible reason")
        on_frame(dies.move_to(3.4 * RIGHT + 0.35 * DOWN))
        on_frame(dies2.next_to(dies, DOWN, buff=0.15))
        self.play(FadeIn(dies), FadeIn(dies2))
        slope6 = MathTex(
            r"\text{at } x = 3:\ \ \frac{d(x^2)}{dx} = 2x = 6"
            r"\qquad \tfrac{3.01^2 - 9}{0.01} = 6.01",
            font_size=32,
        ).move_to(3.4 * RIGHT + 1.5 * DOWN)
        self.play(Write(slope6))
        self.wait(1.0)

        # Second view: the derivative as the local stretch factor.
        self.play(
            FadeOut(
                VGroup(
                    opening,
                    base,
                    strip_r,
                    strip_t,
                    corner,
                    x_lab,
                    dx_lab,
                    strips_note,
                    strips_note2,
                    expansion,
                    dies,
                    dies2,
                    slope6,
                )
            )
        )
        stretch_intro = Text(
            "Same fact, second picture: x² as a map between number lines.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(stretch_intro))
        line_in = NumberLine(x_range=[0, 4, 1], length=9.0, color=MUTED).move_to(0.7 * UP)
        line_out = NumberLine(x_range=[0, 10, 1], length=9.0, color=MUTED).move_to(1.1 * DOWN)
        in_tag = caption("x").next_to(line_in, LEFT, buff=0.3)
        out_tag = caption("x²").next_to(line_out, LEFT, buff=0.3)
        self.play(Create(line_in), Create(line_out), FadeIn(in_tag), FadeIn(out_tag))
        arrows = VGroup()
        for x0 in [0.9, 1.0, 1.1, 2.9, 3.0, 3.1]:
            arrows.add(
                Arrow(
                    line_in.n2p(x0),
                    line_out.n2p(x0**2),
                    stroke_width=2,
                    color=COOL,
                    buff=0.08,
                    max_tip_length_to_length_ratio=0.04,
                )
            )
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1))
        factors = caption("near x = 1 the spacing doubles; near x = 3 it lands ×6 —")
        factors2 = caption("the derivative is the local stretch factor (hold that thought)")
        factors.move_to(2.1 * DOWN)
        factors2.next_to(factors, DOWN, buff=0.15)
        self.play(FadeIn(factors), FadeIn(factors2))
        self.wait(1.0)

        self.play(
            FadeOut(
                VGroup(stretch_intro, line_in, line_out, in_tag, out_tag, arrows, factors, factors2)
            )
        )
        takeaway = Text(
            "Nudge in, response out — the derivative is the local multiplier",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class NudgesAddNudgesCompose(ConceptScene):
    """The toolkit's two load-bearing rules: changes add, rates multiply."""

    def construct(self):
        self.play(FadeIn(self.title("Nudges Add, Nudges Compose"), shift=0.3 * DOWN))

        opening = Text(
            "Two rules carry everything this repo will ever differentiate.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # Sum rule: one nudge, two independent height changes, stacked.
        sum_rule = MathTex(r"d(f + g) = df + dg", font_size=40).move_to(3.9 * LEFT + 1.1 * UP)
        stack_note = caption("heights stack, so their changes stack —")
        stack_note2 = caption("differentiate a sum term by term")
        stack_note.move_to(3.9 * LEFT + 0.3 * UP)
        stack_note2.next_to(stack_note, DOWN, buff=0.15)
        self.play(Write(sum_rule))
        self.play(FadeIn(stack_note), FadeIn(stack_note2))
        self.wait(0.8)
        self.play(FadeOut(VGroup(sum_rule, stack_note, stack_note2)))

        # Chain rule: a nudge propagating through three number lines.
        lines = VGroup()
        tags = ["x", "u = 2x", r"y = u^2"]
        ranges = [[0, 2, 1], [0, 4, 1], [0, 16, 4]]
        for i, (tag, rng) in enumerate(zip(tags, ranges, strict=True)):
            nl = NumberLine(x_range=rng, length=6.0, color=MUTED)
            nl.move_to(1.5 * RIGHT + (0.9 - 1.1 * i) * UP)
            label = MathTex(tag, font_size=28, color=MUTED).next_to(nl, LEFT, buff=0.35)
            lines.add(VGroup(nl, label))
        self.play(LaggedStart(*[FadeIn(line) for line in lines], lag_ratio=0.2))
        nudges = VGroup(
            Arrow(
                lines[0][0].n2p(1.0),
                lines[0][0].n2p(1.4),
                buff=0,
                color=ACCENT,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            ),
            Arrow(
                lines[1][0].n2p(2.0),
                lines[1][0].n2p(2.8),
                buff=0,
                color=ACCENT,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            ),
            Arrow(
                lines[2][0].n2p(4.0),
                lines[2][0].n2p(7.2),
                buff=0,
                color=ACCENT,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            ),
        )
        rate1 = chip("×2", GOOD, width=0.9).move_to(5.6 * RIGHT + 0.35 * UP)
        rate2 = chip("×4", GOOD, width=0.9).move_to(5.6 * RIGHT + 0.75 * DOWN)
        self.play(Create(nudges[0]))
        self.play(Create(nudges[1]), FadeIn(rate1, scale=0.7))
        self.play(Create(nudges[2]), FadeIn(rate2, scale=0.7))
        causes = caption("dx causes du causes dy — the middle change is real,")
        causes2 = caption("and the stretch factors compose: 2 × 4 = 8")
        causes.move_to(1.5 * RIGHT + 2.05 * DOWN)
        causes2.next_to(causes, DOWN, buff=0.15)
        self.play(FadeIn(causes), FadeIn(causes2))
        self.wait(1.0)

        # The table refutes the classic mistake on screen.
        self.play(
            FadeOut(
                VGroup(
                    opening,
                    lines,
                    nudges,
                    rate1,
                    rate2,
                    causes,
                    causes2,
                )
            )
        )
        check = Text(
            "Check it like the zoom would: nudge x = 1 and watch (2x)².",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(check))
        rows, limit = _quotient_table(
            [
                r"dx = 0.1:\quad \tfrac{(2.2)^2 - 4}{0.1} = 8.4",
                r"dx = 0.01:\quad 8.04",
                r"dx = 0.001:\quad 8.004",
            ],
            r"\rightarrow\ 8",
            x=-1.7,
            y=0.75,
            row_size=32,
        )
        self.play(LaggedStart(*[Write(r) for r in rows], lag_ratio=0.3))
        self.play(Write(limit))
        wrong = MathTex(
            r"\text{outer rate at } x = 1\text{?}\quad 2x \cdot 2 = 4\ \text{— no}",
            font_size=32,
            color=WARM,
        ).move_to(0.75 * DOWN)
        right = MathTex(
            r"\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}"
            r" = \underbrace{2u}_{\text{at } u = 2}\cdot\, 2 = 8",
            font_size=36,
            color=ACCENT,
        ).move_to(1.85 * DOWN)
        promise = caption("the du cancels because it is a real change that appears")
        promise2 = caption("twice — Leibniz's notation, keeping its promise")
        promise.move_to(3.05 * DOWN)
        promise2.next_to(promise, DOWN, buff=0.15)
        self.play(Write(wrong))
        self.play(Write(right))
        self.play(FadeIn(promise), FadeIn(promise2))
        self.wait(1.2)

        self.play(FadeOut(VGroup(check, rows, limit, wrong, right, promise, promise2)))
        takeaway = Text(
            "Rates multiply along a chain; changes add across a sum",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheCurveThatIsItsOwnSlope(ConceptScene):
    """The mystery constants become derivatives; ln pays e back as 1/x."""

    def construct(self):
        self.play(FadeIn(self.title("The Curve That Is Its Own Slope"), shift=0.3 * DOWN))

        recall = Text(
            "The mystery constants were derivatives all along.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))
        lineup = MathTex(
            r"\frac{d}{dx} b^x = (\ln b)\, b^x:"
            r"\quad 2^x\!: 0.6931 \quad 3^x\!: 1.0986 \quad 10^x\!: 2.3026",
            font_size=34,
        ).move_to(1.5 * UP)
        self.play(Write(lineup))
        rows, limit = _quotient_table(
            [
                r"\tfrac{e^{dt} - 1}{dt}:\quad dt = 1\!: 1.718282",
                r"dt = 0.1\!: 1.051709",
                r"dt = 0.01\!: 1.005017",
                r"dt = 0.001\!: 1.000500",
            ],
            r"\rightarrow\ 1",
            x=-1.9,
            y=0.0,
            row_size=30,
        )
        self.play(LaggedStart(*[Write(r) for r in rows], lag_ratio=0.25))
        self.play(Write(limit))
        own = MathTex(r"\frac{d}{dx} e^x = e^x", font_size=46, color=ACCENT).move_to(2.05 * DOWN)
        own_box = boxed(own, buff=0.28)
        measured = caption("by definition and measurement — e is the base whose")
        measured2 = caption("constant is 1; nothing here is being proved twice")
        measured.next_to(own, DOWN, buff=0.4)
        measured2.next_to(measured, DOWN, buff=0.15)
        self.play(Write(own), Create(own_box))
        self.play(FadeIn(measured), FadeIn(measured2))
        self.wait(1.0)

        # The undo trick: differentiate e^(ln x) = x.
        self.play(FadeOut(VGroup(recall, lineup, rows, limit, own, own_box, measured, measured2)))
        undo_intro = Text(
            "And ln? Differentiate the undo.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(undo_intro))
        undo = MathTex(r"e^{\ln x} = x", font_size=40).move_to(1.6 * UP)
        chain = MathTex(
            r"e^{\ln x} \cdot \frac{d(\ln x)}{dx} = 1"
            r"\qquad\Longrightarrow\qquad \frac{d(\ln x)}{dx} = \frac{1}{x}",
            font_size=38,
            color=ACCENT,
        ).move_to(0.6 * UP)
        chain_note = caption("the chain rule through the undo-never-cancel pair —")
        chain_note2 = caption("e^(ln x) is just x, so the whole left side is x · ln′(x)")
        chain_note.move_to(0.35 * DOWN)
        chain_note2.next_to(chain_note, DOWN, buff=0.15)
        self.play(Write(undo))
        self.play(Write(chain))
        self.play(FadeIn(chain_note), FadeIn(chain_note2))
        mirror = caption("the mirror check: at x = e, ln climbs at 1/e — the y = x")
        mirror2 = caption("reflection of e^x climbing at e; rise and run swap")
        mirror.move_to(1.45 * DOWN)
        mirror2.next_to(mirror, DOWN, buff=0.15)
        self.play(FadeIn(mirror), FadeIn(mirror2))
        euler = caption("Euler named e in 1748 (Introductio §122)")
        euler2 = caption("and wrote d(e^x) = e^x dx in 1755 (Institutiones §188)")
        euler.move_to(2.4 * DOWN)
        euler2.next_to(euler, DOWN, buff=0.15)
        self.play(FadeIn(euler), FadeIn(euler2))
        self.wait(1.2)

        self.play(
            FadeOut(
                VGroup(
                    undo_intro, undo, chain, chain_note, chain_note2, mirror, mirror2, euler, euler2
                )
            )
        )
        takeaway = Text(
            "e^x is its own slope; ln pays it back as 1/x",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class ZeroSlopeFindsThePeak(ConceptScene):
    """The score function derives the peak the softmax series read by eye."""

    def construct(self):
        self.play(FadeIn(self.title("Zero Slope Finds the Peak"), shift=0.3 * DOWN))

        opening = Text(
            "The softmax series read p̂ = 3/4 off the plotted curve.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The owned likelihood curve, now wearing a slope ribbon.
        ax = _axes([0, 1, 0.25], [0, 0.45, 0.15], 6.0, 2.9).move_to(3.0 * LEFT + 0.55 * DOWN)
        curve = ax.plot(lambda p: 4 * p**3 * (1 - p), x_range=[0, 1], color=COOL)
        formula = MathTex(r"L(p) = 4p^3(1-p)", font_size=34, color=COOL)
        formula.move_to(3.0 * LEFT + 1.55 * UP)
        peak = Dot(ax.c2p(0.75, 108 / 256), color=ACCENT, radius=0.07)
        drop = DashedLine(ax.c2p(0.75, 108 / 256), ax.c2p(0.75, 0), color=ACCENT, stroke_width=2)
        self.play(Create(ax), Write(formula))
        self.play(Create(curve))
        signs = VGroup(
            MathTex("+", font_size=34, color=GOOD).move_to(ax.c2p(0.4, 0) + 0.45 * DOWN),
            MathTex("0", font_size=34, color=ACCENT).move_to(ax.c2p(0.75, 0) + 0.45 * DOWN),
            MathTex("-", font_size=34, color=WARM).move_to(ax.c2p(0.92, 0) + 0.45 * DOWN),
        )
        ribbon = caption("slope + climbing, 0 at the top, − descending")
        ribbon.move_to(3.0 * LEFT + 3.05 * DOWN)
        self.play(FadeIn(peak, scale=0.6), Create(drop))
        self.play(LaggedStart(*[FadeIn(s) for s in signs], lag_ratio=0.2), FadeIn(ribbon))
        self.wait(0.6)

        # The score reader: the counting strip differentiated.
        score_def = MathTex(
            r"\frac{d \ln f}{dx} = \frac{f'}{f}",
            font_size=38,
            color=ACCENT,
        ).move_to(3.6 * RIGHT + 1.6 * UP)
        strip_note = caption("the counting strip differentiated:")
        strip_note2 = caption("under ln, products become sums")
        strip_note3 = caption("of relative rates (Euler, 1755)")
        on_frame(strip_note.move_to(3.6 * RIGHT + 0.95 * UP))
        on_frame(strip_note2.next_to(strip_note, DOWN, buff=0.13))
        on_frame(strip_note3.next_to(strip_note2, DOWN, buff=0.13))
        score = MathTex(
            r"\frac{d \ln L}{dp} = \frac{3}{p} - \frac{1}{1-p}",
            font_size=36,
        ).move_to(3.6 * RIGHT + 0.55 * DOWN)
        grid_vals = MathTex(
            r"+4 \;\big|\; +0.9524 \;\big|\; 0 \;\big|\; -1.25",
            font_size=30,
        ).move_to(3.6 * RIGHT + 1.35 * DOWN)
        at_ps = caption("at p = 1/2, 0.7, 3/4, 0.8 —")
        at_ps2 = caption("the sign flips at the peak")
        on_frame(at_ps.move_to(3.6 * RIGHT + 1.95 * DOWN))
        on_frame(at_ps2.next_to(at_ps, DOWN, buff=0.13))
        self.play(Write(score_def))
        self.play(FadeIn(strip_note), FadeIn(strip_note2), FadeIn(strip_note3))
        self.play(Write(score))
        self.play(Write(grid_vals), FadeIn(at_ps), FadeIn(at_ps2))
        solve = MathTex(
            r"\frac{3}{p} = \frac{1}{1-p} \;\Longrightarrow\; 3(1-p) = p"
            r" \;\Longrightarrow\; \hat{p} = \tfrac{3}{4}",
            font_size=34,
            color=ACCENT,
        ).move_to(3.6 * RIGHT + 3.0 * DOWN)
        self.play(Write(solve))
        self.wait(1.2)

        # The general line: the observed proportion, derived at last.
        self.play(
            FadeOut(
                VGroup(
                    score_def,
                    strip_note,
                    strip_note2,
                    strip_note3,
                    score,
                    grid_vals,
                    at_ps,
                    at_ps2,
                    solve,
                )
            )
        )
        general = MathTex(
            r"\frac{k}{p} - \frac{n-k}{1-p} = 0 \;\Longrightarrow\; \hat{p} = \frac{k}{n}",
            font_size=36,
            color=ACCENT,
        ).move_to(3.6 * RIGHT + 1.0 * UP)
        derived = caption("the observed proportion — the claim")
        derived2 = caption("ProportionsConverge made, now derived")
        on_frame(derived.move_to(3.6 * RIGHT + 0.15 * UP))
        on_frame(derived2.next_to(derived, DOWN, buff=0.13))
        self.play(Write(general))
        self.play(FadeIn(derived), FadeIn(derived2))
        self.wait(1.0)

        # Honesty: the converse error, and where the score lives.
        self.play(
            FadeOut(
                VGroup(
                    opening,
                    ax,
                    curve,
                    formula,
                    peak,
                    drop,
                    signs,
                    ribbon,
                    general,
                    derived,
                    derived2,
                )
            )
        )
        honesty = Text(
            "Two honest breaths before this tool goes in the kit.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(honesty))
        direct = MathTex(
            r"\frac{dL}{dp} = 4p^2(3 - 4p)\ \text{has a second root at } p = 0",
            font_size=34,
        ).move_to(1.1 * UP)
        valley = caption("a flat valley floor, not a peak — and x³'s slope touches")
        valley2 = caption("zero at 0 without any peak at all: zero slope is necessary,")
        valley3 = caption("not sufficient; check the sign change")
        valley.move_to(0.35 * UP)
        valley2.next_to(valley, DOWN, buff=0.15)
        valley3.next_to(valley2, DOWN, buff=0.15)
        positive = caption("and the score needs f > 0 — true for likelihoods,")
        positive2 = caption("undefined at the endpoints p = 0 and 1")
        positive.move_to(1.35 * DOWN)
        positive2.next_to(positive, DOWN, buff=0.15)
        self.play(Write(direct))
        self.play(FadeIn(valley), FadeIn(valley2), FadeIn(valley3))
        self.play(FadeIn(positive), FadeIn(positive2))
        self.wait(1.0)

        self.play(FadeOut(VGroup(honesty, direct, valley, valley2, valley3, positive, positive2)))
        takeaway = Text(
            "Set the score to zero: the best explanation is where the slope vanishes",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheSmoothMaxsShares(ConceptScene):
    """The sensitivities of LSE are the softmax; the loss gradient lands."""

    def construct(self):
        self.play(FadeIn(self.title("The Smooth Max's Shares"), shift=0.3 * DOWN))

        opening = Text(
            "Nudge one score and watch how much the smooth max cares.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        nudge = MathTex(
            r"z = (2, 1, 0):\quad \mathrm{LSE}(z) = 2.4076",
            font_size=36,
        ).move_to(1.7 * UP)
        moved = MathTex(
            r"z_1 \to 2.01:\quad \Delta \mathrm{LSE} = 0.00666 \approx 0.6652 \times 0.01",
            font_size=34,
        ).move_to(0.95 * UP)
        share_note = caption("the smooth max moves by e²'s share of the total —")
        share_note2 = caption("the first bar of a chart you already own")
        share_note.move_to(0.25 * UP)
        share_note2.next_to(share_note, DOWN, buff=0.15)
        self.play(Write(nudge))
        self.play(Write(moved))
        self.play(FadeIn(share_note), FadeIn(share_note2))
        derivation = MathTex(
            r"\frac{\partial}{\partial z_i} \ln\!\sum_j e^{z_j}"
            r" = \frac{e^{z_i}}{\sum_j e^{z_j}} = \mathrm{softmax}(z)_i",
            font_size=38,
            color=ACCENT,
        ).move_to(0.85 * DOWN)
        rules = caption("one chain rule (ln), one sum rule (the Σ) — the whole kit")
        rules.next_to(derivation, DOWN, buff=0.3)
        self.play(Write(derivation))
        self.play(FadeIn(rules))
        self.wait(1.0)

        # The bars reborn: same bars, same order, now a gradient read-out.
        self.play(
            FadeOut(VGroup(opening, nudge, moved, share_note, share_note2, derivation, rules))
        )
        reborn = Text(
            "The softmax bars, reborn as a gradient read-out.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(reborn))
        bars = VGroup()
        for i, (v, tag, val) in enumerate(
            zip(
                [0.6652, 0.2447, 0.0900],
                ["a", "b", "c"],
                ["0.6652", "0.2447", "0.0900"],
                strict=True,
            )
        ):
            bar = Rectangle(
                width=0.7,
                height=v * 2.6,
                stroke_width=2,
                color=COOL,
                fill_color=COOL,
                fill_opacity=0.35,
            ).move_to([-4.2 + i * 1.25, -1.1 + v * 1.3, 0])
            tag_m = Text(tag, font_size=SMALL_SIZE, color=MUTED).move_to([-4.2 + i * 1.25, -1.4, 0])
            val_m = Text(val, font_size=SMALL_SIZE, color=COOL).next_to(bar, UP, buff=0.12)
            bars.add(VGroup(bar, tag_m, val_m))
        grad_tag = MathTex(
            r"\nabla \mathrm{LSE}(z) = \mathrm{softmax}(z)",
            font_size=34,
            color=ACCENT,
        ).move_to(3.9 * LEFT + 1.5 * UP)
        shares_sum = caption("shares of the total, so they sum to 1")
        shares_sum.move_to(3.9 * LEFT + 2.3 * DOWN)
        self.play(FadeIn(bars), Write(grad_tag))
        self.play(FadeIn(shares_sum))

        # One subtraction later: the loss gradient, on pre-verified numbers.
        loss_grad = MathTex(
            r"\nabla\big(\mathrm{LSE}(z) - z_a\big)"
            r" = (0.6652 - 1,\ 0.2447,\ 0.0900)",
            font_size=32,
        ).move_to(2.9 * RIGHT + 1.3 * UP)
        landed = MathTex(
            r"= (-0.3348,\ 0.2447,\ 0.0900)",
            font_size=36,
            color=ACCENT,
        ).move_to(2.9 * RIGHT + 0.5 * UP)
        onehot = caption("softmax minus one-hot — the gradient of the NLL:")
        onehot2 = caption("descending this loss is climbing the likelihood")
        on_frame(onehot.move_to(2.9 * RIGHT + 0.25 * DOWN))
        on_frame(onehot2.next_to(onehot, DOWN, buff=0.15))
        self.play(Write(loss_grad))
        self.play(Write(landed))
        self.play(FadeIn(onehot), FadeIn(onehot2))
        saturate = MathTex(
            r"z_c \to 0, -2, -5, -10:",
            font_size=30,
        ).move_to(2.9 * RIGHT + 1.2 * DOWN)
        saturate2 = MathTex(
            r"\text{slope} \to -0.9100,\ -0.9868,\ -0.9993,\ \to -1",
            font_size=28,
        ).move_to(2.9 * RIGHT + 1.75 * DOWN)
        theorem = caption('"the gap grows roughly linearly" — now a theorem')
        on_frame(theorem.move_to(2.9 * RIGHT + 2.35 * DOWN))
        self.play(Write(saturate), Write(saturate2))
        self.play(FadeIn(theorem))
        self.wait(1.2)

        # When useful: the target changes, the picture stays.
        self.play(
            FadeOut(
                VGroup(
                    reborn,
                    bars,
                    grad_tag,
                    shares_sum,
                    loss_grad,
                    landed,
                    onehot,
                    onehot2,
                    saturate,
                    saturate2,
                    theorem,
                )
            )
        )
        closer = caption("every frame of CTC hands this exact picture a different")
        closer2 = caption("target — softmax minus where the truth actually was;")
        closer3 = caption("the gradient series is next")
        closer.move_to(0.9 * UP)
        closer2.next_to(closer, DOWN, buff=0.15)
        closer3.next_to(closer2, DOWN, buff=0.15)
        self.play(FadeIn(closer), FadeIn(closer2), FadeIn(closer3))
        takeaway = Text(
            "The smooth max's shares are the softmax — the gradient is p − one-hot",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
