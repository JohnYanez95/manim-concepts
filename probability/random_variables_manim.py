"""Random variables — the die as a function, and the pmf as sorted area.

Six scenes closing the graph's oldest promise: `counting-rules` →
binomial, open since the repo's first topic. The stamped square makes
the random variable a fixed labeling; sorting its cells births the pmf
as conserved area; the balance point defines expectation without the
long run; linearity works on dependent pairs; the binomial columns
close the promise with C(4,k) as a visible cell count; and the closer
quantifies the swamping `WhenToUseIt` seeded.

    TheStampedSquare     the function is ink; only the dart is random
    SortTheSquare        the pmf born as conserved, rearranged area
    TheBalancePoint      E as fulcrum; 3.5 is not a face
    SameOutcomesAdd      linearity over the same outcomes; no independence
    TheBinomialColumns   C(4,k) cells x p^k q^(4-k) areas — the promise closes
    ProportionsConverge  proportions converge, counts spread — quantified

Every number on screen traces to plan 007's verified anchors (main
report + addendum); all probability arithmetic there ran in exact
fractions, and display forms like /16 and /256 are forced manually.

Render:
    uv run python probability/random_variables_manim.py
    uv run python probability/random_variables_manim.py -s SortTheSquare -q draft
"""

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
    render_cli,
)


def _axis_segments(p):
    """Two flips along one axis: boundaries and head counts, H before T.

    First flip cuts at p, second cuts each part at p again — segment
    widths p*p, p*q, q*p, q*q with head counts 2, 1, 1, 0.
    """
    q = 1 - p
    widths = [p * p, p * q, q * p, q * q]
    heads = [2, 1, 1, 0]
    bounds = [0.0]
    for w in widths:
        bounds.append(bounds[-1] + w)
    return bounds, heads


def _flip_square(p=0.5, side=3.2, stamp_size=LABEL_SIZE):
    """The four-flip square: 16 cells, each stamped with its head count.

    Flips 1-2 cut the x axis, flips 3-4 the y axis; a cell's area is
    p^k q^(4-k) for its head count k. Returns (cells, stamps, ks) with
    matching indices, centered on the origin. ``stamp_size=None`` skips
    the stamps — an unfair square's smallest cells are thinner than any
    readable glyph, and there the highlights carry the argument.
    """
    xb, xh = _axis_segments(p)
    yb, yh = _axis_segments(p)
    cells, stamps, ks = VGroup(), VGroup(), []
    for i in range(4):
        for j in range(4):
            w = (xb[i + 1] - xb[i]) * side
            h = (yb[j + 1] - yb[j]) * side
            cell = Rectangle(width=w, height=h, stroke_width=2, color=MUTED)
            cell.move_to(
                [
                    (xb[i] + xb[i + 1]) / 2 * side - side / 2,
                    (yb[j] + yb[j + 1]) / 2 * side - side / 2,
                    0,
                ]
            )
            k = xh[i] + yh[j]
            if stamp_size is not None:
                stamps.add(Text(str(k), font_size=stamp_size, color=COOL).move_to(cell))
            cells.add(cell)
            ks.append(k)
    return cells, stamps, ks


def _pmf_bars(weights, labels, x0=1.2, cell=0.5, gap=1.15, color=MUTED):
    """Columns of stacked unit cells over value tags — the sorted square.

    ``weights`` are integer cell counts per value; each column stacks
    that many squares of side ``cell`` above its value tag.
    """
    columns = VGroup()
    for k, (count, label) in enumerate(zip(weights, labels, strict=True)):
        x = x0 + k * gap
        stack = VGroup(
            *[
                Square(side_length=cell, stroke_width=2, color=color).move_to(
                    [x, -1.5 + (r + 0.5) * cell, 0]
                )
                for r in range(count)
            ]
        )
        tag = Text(label, font_size=SMALL_SIZE, color=COOL).move_to([x, -1.95, 0])
        columns.add(VGroup(stack, tag))
    return columns


class TheStampedSquare(ConceptScene):
    """The die as a function, not a set: the label is ink, the dart is random."""

    def construct(self):
        self.play(FadeIn(self.title("The Stamped Square"), shift=0.3 * DOWN))

        opening = Text(
            "Events were subsets. A random variable labels every outcome.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The die first: six faces, each stamped with the number it shows.
        faces = VGroup(
            *[
                VGroup(
                    Square(side_length=0.8, stroke_width=2, color=MUTED),
                    Text(f"face {i}", font_size=SMALL_SIZE, color=MUTED),
                ).arrange(DOWN, buff=0.15)
                for i in range(1, 7)
            ]
        ).arrange(RIGHT, buff=0.55)
        faces.move_to(1.05 * UP)
        stamps = VGroup(
            *[
                Text(str(i + 1), font_size=LABEL_SIZE, color=COOL).move_to(faces[i][0])
                for i in range(6)
            ]
        )
        rule = MathTex(r"X(\text{face}) = \text{the number shown}", font_size=40)
        rule.move_to(0.75 * DOWN)
        ink = caption("the die as a function, not a set — the ink is fixed")
        ink2 = caption("before anything is ever rolled")
        ink.next_to(rule, DOWN, buff=0.3)
        ink2.next_to(ink, DOWN, buff=0.15)
        self.play(LaggedStart(*[FadeIn(f) for f in faces], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in stamps], lag_ratio=0.1))
        self.play(Write(rule))
        self.play(FadeIn(ink), FadeIn(ink2))
        self.wait(1.0)

        # The owned square, stamped: head counts as ink on 16 cells.
        self.play(FadeOut(VGroup(opening, faces, stamps, rule, ink, ink2)))
        cells, cell_stamps, ks = _flip_square()
        VGroup(cells, cell_stamps).move_to(3.2 * LEFT + 0.35 * DOWN)
        recall = Text(
            "Four flips — the square you have quartered twice before.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))
        self.play(FadeIn(cells))
        stamp_note = caption("stamp every cell with its head count:")
        stamp_note.move_to(2.4 * RIGHT + 1.3 * UP)
        self.play(FadeIn(stamp_note))
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in cell_stamps], lag_ratio=0.04))
        self.wait(0.6)

        # A dart lands; the label is looked up, never generated.
        target = cells[6]
        dart = Dot(color=ACCENT).move_to(target.get_center() + 0.18 * RIGHT + 0.12 * UP)
        readout = MathTex(r"X = 2", font_size=44, color=ACCENT)
        readout.move_to(2.4 * RIGHT + 0.15 * UP)
        looked_up = caption("the dart is the only random object on screen —")
        looked_up2 = caption("the label was waiting; it is looked up, never generated")
        looked_up.next_to(readout, DOWN, buff=0.35)
        looked_up2.next_to(looked_up, DOWN, buff=0.15)
        self.play(FadeIn(dart, scale=0.4))
        self.play(Write(readout))
        self.play(FadeIn(looked_up), FadeIn(looked_up2))
        self.wait(1.0)

        self.play(FadeOut(VGroup(recall, stamp_note, readout, looked_up, looked_up2, dart)))
        takeaway = Text(
            "A random variable is a fixed rule reading a random outcome",
            font_size=26,
        ).move_to(2.95 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class SortTheSquare(ConceptScene):
    """The pmf born as rearranged area: five values fed by sixteen equal cells."""

    def construct(self):
        self.play(FadeIn(self.title("Sort the Square"), shift=0.3 * DOWN))

        prompt = Text(
            "Slide every stamped cell into the column of its value.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        cells, stamps, ks = _flip_square()
        square = VGroup(cells, stamps).move_to(4.3 * LEFT + 0.55 * DOWN)
        self.play(FadeIn(square))

        # The sort: cell copies fly into stacks grouped by value.
        counts = [1, 4, 6, 4, 1]
        columns = _pmf_bars(counts, ["0", "1", "2", "3", "4"], x0=0.4, cell=0.47, gap=1.25)
        filled = [0] * 5
        movers = VGroup()
        for cell, k in zip(cells, ks, strict=True):
            dest = columns[k][0][filled[k]]
            copy = cell.copy().set_stroke(color=MUTED)
            movers.add(copy)
            copy.generate_target()
            copy.target.become(dest)
            filled[k] += 1
        value_tags = VGroup(*[columns[k][1] for k in range(5)])
        self.play(FadeIn(value_tags))
        self.play(LaggedStart(*[MoveToTarget(m) for m in movers], lag_ratio=0.05), run_time=3.2)
        weights = VGroup(
            *[
                Text(f"{c}/16", font_size=SMALL_SIZE, color=ACCENT).next_to(
                    columns[k][0][-1], UP, buff=0.15
                )
                for k, c in enumerate(counts)
            ]
        )
        self.play(LaggedStart(*[FadeIn(w) for w in weights], lag_ratio=0.15))
        born = caption("five values, sixteen equally likely cells — unequal bars")
        born2 = caption("from equal cells; the area only moved, it never changed")
        born.move_to(2.45 * DOWN)
        born2.next_to(born, DOWN, buff=0.15)
        total = MathTex(
            r"\tfrac{1}{16}+\tfrac{4}{16}+\tfrac{6}{16}+\tfrac{4}{16}+\tfrac{1}{16} = 1",
            font_size=30,
        ).move_to(3.3 * DOWN)
        self.play(FadeIn(born), FadeIn(born2))
        self.play(Write(total))
        self.wait(1.2)

        # Same blueprint, different houses: Y = tails sorts identically.
        self.play(FadeOut(VGroup(born, born2, total, prompt)))
        y_prompt = Text(
            "Now stamp the SAME square with Y = number of tails.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        y_stamps = VGroup(
            *[
                Text(str(4 - k), font_size=LABEL_SIZE, color=GOOD).move_to(cell)
                for cell, k in zip(cells, ks, strict=True)
            ]
        )
        self.play(FadeIn(y_prompt))
        # Old ink leaves before new ink arrives — never a simultaneous swap.
        self.play(LaggedStart(*[FadeOut(s) for s in stamps], lag_ratio=0.04))
        self.play(LaggedStart(*[FadeIn(y, scale=0.6) for y in y_stamps], lag_ratio=0.04))
        same = MathTex(r"X + Y = 4\ \text{in every cell}", font_size=38)
        same.move_to(2.35 * DOWN + 3.9 * LEFT)
        twin = caption("Y sorts into the SAME columns — one blueprint, two houses:")
        twin2 = caption("the distribution forgets which cell was which; the variable remembers")
        twin.move_to(2.45 * DOWN + 1.2 * RIGHT)
        twin2.next_to(twin, DOWN, buff=0.15)
        self.play(Write(same))
        self.play(FadeIn(twin), FadeIn(twin2))
        self.wait(1.2)

        self.play(FadeOut(VGroup(y_prompt, same, twin, twin2)))
        takeaway = Text(
            "The pmf is the square's own area, sorted by value",
            font_size=26,
        ).move_to(2.7 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheBalancePoint(ConceptScene):
    """Expectation defined, not simulated: the fulcrum under the bars."""

    def construct(self):
        self.play(FadeIn(self.title("The Balance Point"), shift=0.3 * DOWN))

        definition = MathTex(r"E[X] = \sum_x x \cdot P(X = x)", font_size=44, color=ACCENT).next_to(
            self.head, DOWN, buff=0.4
        )
        definition_box = boxed(definition, buff=0.28)
        weighted = caption("a weighted average — weights from the measure, nothing else")
        weighted.next_to(definition, DOWN, buff=0.45)
        self.play(Write(definition), Create(definition_box))
        self.play(FadeIn(weighted))

        # The fair die: six equal bars, fulcrum at 3.5 — not a face.
        axis = Line([-4.3, -0.55, 0], [1.4, -0.55, 0], color=MUTED, stroke_width=2)

        def bar_at(x_val, height, color=MUTED):
            x = -3.9 + (x_val - 1) * 0.96 + 2.4
            bar = Rectangle(width=0.55, height=height, stroke_width=2, color=color).move_to(
                [x - 2.4, -0.55 + height / 2 + 0.02, 0]
            )
            return bar

        bars = VGroup(*[bar_at(v, 0.75) for v in range(1, 7)])
        face_tags = VGroup(
            *[
                Text(str(v), font_size=SMALL_SIZE, color=COOL).next_to(bars[v - 1], DOWN, buff=0.42)
                for v in range(1, 7)
            ]
        )
        fulcrum = Triangle(color=ACCENT, fill_color=ACCENT, fill_opacity=1).scale(0.16)
        fulcrum.move_to([-1.5, -1.35, 0])
        balance = MathTex(r"E = 3.5", font_size=40, color=ACCENT)
        balance.next_to(fulcrum, DOWN, buff=0.2)
        self.play(Create(axis), FadeIn(bars), FadeIn(face_tags))
        self.play(FadeIn(fulcrum, shift=0.2 * UP), Write(balance))
        not_face = caption("3.5 is not a face — the fulcrum")
        not_face2 = caption("need not sit under a mass")
        not_face.move_to(3.4 * RIGHT + 0.15 * UP)
        not_face2.next_to(not_face, DOWN, buff=0.15)
        self.play(FadeIn(not_face), FadeIn(not_face2))
        self.wait(1.0)

        # The two sums are one: grouping was all the sort did.
        two_sums = MathTex(
            r"\underbrace{\textstyle\sum_\omega X(\omega)\cdot\tfrac{1}{16}}_{32/16}"
            r" \;=\; \underbrace{\textstyle\sum_k k \cdot P(X{=}k)}_{2}",
            font_size=34,
        ).move_to(2.55 * DOWN + 2.2 * LEFT)
        grouping = caption("stamps over cells = values times weights;")
        grouping2 = caption("the sort was a regrouping — one sum")
        grouping.move_to(2.3 * DOWN + 3.2 * RIGHT)
        grouping2.next_to(grouping, DOWN, buff=0.15)
        self.play(Write(two_sums))
        self.play(FadeIn(grouping), FadeIn(grouping2))
        self.wait(1.2)

        # The measure moves the balance point: the owned biased die.
        self.play(FadeOut(VGroup(two_sums, grouping, grouping2, not_face, not_face2, weighted)))
        biased_bars = VGroup(*[bar_at(v, 0.75) for v in range(1, 6)], bar_at(6, 1.5, WARM))
        shift_note = Text(
            "Double the weight on 6 — the die from the independence series:",
            font_size=BODY_SIZE,
        ).move_to(2.2 * DOWN)
        new_balance = MathTex(r"E = \tfrac{27}{7} \approx 3.8571", font_size=40, color=ACCENT)
        new_balance.move_to(3.4 * RIGHT + 0.15 * UP)
        moved = caption("the balance point belongs to the measure —")
        moved2 = caption("the same faces, reweighted, balance anew")
        moved.move_to(2.9 * RIGHT + 1.35 * DOWN)
        moved2.next_to(moved, DOWN, buff=0.15)
        self.play(FadeIn(shift_note))
        self.play(Transform(bars, biased_bars))
        self.play(fulcrum.animate.shift(0.357 * 0.96 * RIGHT), Write(new_balance))
        self.play(FadeIn(moved), FadeIn(moved2))
        self.wait(1.0)

        price = caption("Huygens, 1657: E is the fair price of the ticket —")
        price2 = caption("the number you can act on, defined with no long run in sight")
        price.move_to(2.75 * DOWN)
        price2.next_to(price, DOWN, buff=0.15)
        self.play(FadeIn(price), FadeIn(price2))
        self.wait(2)


class SameOutcomesAdd(ConceptScene):
    """Linearity over the same outcomes — dependence is welcome."""

    def construct(self):
        self.play(FadeIn(self.title("Same Outcomes Add"), shift=0.3 * DOWN))

        claim = MathTex(r"E[X + Y] = E[X] + E[Y]", font_size=48, color=ACCENT).next_to(
            self.head, DOWN, buff=0.4
        )
        claim_box = boxed(claim, buff=0.3)
        self.play(Write(claim), Create(claim_box))

        table_proof = MathTex(
            r"\sum_\omega \big(X(\omega) + Y(\omega)\big)\,P(\omega)"
            r" = \sum_\omega X(\omega)P(\omega) + \sum_\omega Y(\omega)P(\omega)",
            font_size=36,
        ).move_to(0.8 * UP)
        distributes = caption("one sum over the SAME outcomes — addition distributes,")
        distributes2 = caption("and independence never enters the argument")
        distributes.next_to(table_proof, DOWN, buff=0.3)
        distributes2.next_to(distributes, DOWN, buff=0.15)
        self.play(Write(table_proof))
        self.play(FadeIn(distributes), FadeIn(distributes2))
        self.wait(0.8)

        # A maximally dependent pair passes.
        dependent = MathTex(
            r"Y = 4 - X:\quad E[X] + E[Y] = 2 + 2 = 4\ \text{always}",
            font_size=38,
            color=GOOD,
        ).move_to(0.85 * DOWN)
        dep_note = caption("heads and tails are as dependent as two variables can be —")
        dep_note2 = caption("linearity does not care; that is what makes it a workhorse")
        dep_note.next_to(dependent, DOWN, buff=0.3)
        dep_note2.next_to(dep_note, DOWN, buff=0.15)
        self.play(Write(dependent))
        self.play(FadeIn(dep_note), FadeIn(dep_note2))
        self.wait(1.0)

        # The owned 6x6 grid: two dice, diagonals, E = 7 twice.
        self.play(
            FadeOut(VGroup(table_proof, distributes, distributes2, dependent, dep_note, dep_note2))
        )
        grid = VGroup()
        for a in range(6):
            for b in range(6):
                cell = Square(side_length=0.42, stroke_width=1.5, color=MUTED)
                cell.move_to([-4.4 + a * 0.42, 1.35 - b * 0.42, 0])
                if a + b == 5:
                    cell.set_fill(GOOD, opacity=0.35)
                grid.add(cell)
        grid_tag = caption("the two-dice grid you already own —")
        grid_tag2 = caption("the sum paints diagonals")
        grid_tag.move_to(3.0 * LEFT + 1.75 * DOWN)
        grid_tag2.next_to(grid_tag, DOWN, buff=0.15)
        seven = MathTex(
            r"E[\text{sum}] = \sum_s s \cdot \tfrac{\#\,\text{diagonal}}{36} = 7",
            font_size=36,
        ).move_to(2.9 * RIGHT + 1.0 * UP)
        twice = MathTex(
            r"= E[\text{die}_1] + E[\text{die}_2] = 3.5 + 3.5",
            font_size=36,
            color=GOOD,
        ).next_to(seven, DOWN, buff=0.35)
        diag_note = caption("counts (1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1)/36 —")
        diag_note2 = caption("the green diagonal is the six ways to seven;")
        diag_note3 = caption("both routes land on 7")
        diag_note.move_to(2.8 * RIGHT + 0.55 * DOWN)
        diag_note2.next_to(diag_note, DOWN, buff=0.15)
        diag_note3.next_to(diag_note2, DOWN, buff=0.15)
        self.play(FadeIn(grid), FadeIn(grid_tag), FadeIn(grid_tag2))
        self.play(Write(seven))
        self.play(Write(twice))
        self.play(FadeIn(diag_note), FadeIn(diag_note2), FadeIn(diag_note3))
        self.wait(1.2)

        self.play(
            FadeOut(
                VGroup(grid, grid_tag, grid_tag2, seven, twice, diag_note, diag_note2, diag_note3)
            )
        )
        takeaway = Text(
            "Expectations add — even when the variables don't ignore each other",
            font_size=26,
        ).move_to(0.6 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


class TheBinomialColumns(ConceptScene):
    """The oldest promise closes: C(4,k) cells, each of area p^k q^(4-k)."""

    def construct(self):
        self.play(FadeIn(self.title("The Binomial Columns"), shift=0.3 * DOWN))

        recall = Text(
            "Count the cells in each sorted column: 1, 4, 6, 4, 1.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))

        counts_row = MathTex(
            r"1,\ 4,\ 6,\ 4,\ 1 \;=\; \binom{4}{0},\ \binom{4}{1},"
            r"\ \binom{4}{2},\ \binom{4}{3},\ \binom{4}{4}",
            font_size=40,
        ).move_to(1.35 * UP)
        counted = caption("cells with k heads are 4-letter H/T words with k H's —")
        counted2 = caption("counted exactly the way the combinations series counts them")
        counted.next_to(counts_row, DOWN, buff=0.3)
        counted2.next_to(counted, DOWN, buff=0.15)
        self.play(Write(counts_row))
        self.play(FadeIn(counted), FadeIn(counted2))
        self.wait(1.0)

        # The unfair square: straight cuts at p — unequal cells, equal columns.
        self.play(FadeOut(VGroup(recall, counts_row, counted, counted2)))
        cells, stamps, ks = _flip_square(p=0.25, side=3.4, stamp_size=None)
        square = cells.move_to(4.0 * LEFT + 0.3 * DOWN)
        unfair = Text(
            "Re-cut the square with the coin's bias: p = 1/4.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(unfair))
        self.play(FadeIn(square))
        straight = caption("the cuts moved but stayed straight — the trials are still")
        straight2 = caption("independent; only the coin changed")
        straight.move_to(2.7 * RIGHT + 1.55 * UP)
        straight2.next_to(straight, DOWN, buff=0.15)
        self.play(FadeIn(straight), FadeIn(straight2))
        self.wait(0.8)

        one_head = VGroup(
            *[
                cell.copy().set_stroke(color=GOOD, width=4)
                for cell, k in zip(cells, ks, strict=True)
                if k == 1
            ]
        )
        area = MathTex(
            r"\text{every 1-head cell: } \tfrac{1}{4}\left(\tfrac{3}{4}\right)^{3}"
            r" = \tfrac{27}{256}",
            font_size=36,
            color=GOOD,
        ).move_to(2.9 * RIGHT + 0.35 * UP)
        order = caption("four different shapes, one area — a product does not care")
        order2 = caption("about the order of its factors; same count, same area")
        order.next_to(area, DOWN, buff=0.3)
        order2.next_to(order, DOWN, buff=0.15)
        self.play(LaggedStart(*[Create(c) for c in one_head], lag_ratio=0.15))
        self.play(Write(area))
        self.play(FadeIn(order), FadeIn(order2))
        self.wait(1.0)

        # Assembly: coefficient counts the cells, the power weighs one cell.
        self.play(
            FadeOut(VGroup(unfair, square, one_head, area, order, order2, straight, straight2))
        )
        pmf = MathTex(
            r"P(X = k) = \binom{n}{k}\, p^{k} (1-p)^{n-k}",
            font_size=48,
            color=ACCENT,
        ).move_to(1.35 * UP)
        pmf_box = boxed(pmf, buff=0.3)
        assembled = caption("the coefficient counts the column's cells; the power weighs")
        assembled2 = caption("one cell — nothing in the formula is a mystery factor")
        assembled.next_to(pmf, DOWN, buff=0.4)
        assembled2.next_to(assembled, DOWN, buff=0.15)
        self.play(Write(pmf), Create(pmf_box))
        self.play(FadeIn(assembled), FadeIn(assembled2))
        example = MathTex(
            r"n{=}4,\ p{=}\tfrac14:\ \ \tfrac{81}{256},\ \tfrac{108}{256},"
            r"\ \tfrac{54}{256},\ \tfrac{12}{256},\ \tfrac{1}{256}"
            r"\qquad E = np = 1",
            font_size=34,
        ).move_to(0.85 * DOWN)
        indicators = caption("E = np by the indicator stamps and linearity — no combinatorics;")
        indicators2 = caption("conditions: fixed n, two outcomes, constant p, independent trials")
        boundary = caption("(no replacement → no binomial: the aces already taught the boundary)")
        indicators.next_to(example, DOWN, buff=0.35)
        indicators2.next_to(indicators, DOWN, buff=0.15)
        boundary.next_to(indicators2, DOWN, buff=0.15)
        self.play(Write(example))
        self.play(FadeIn(indicators), FadeIn(indicators2))
        self.play(FadeIn(boundary))
        touches_e = caption("and the binomial touches e: zero successes in n trials of")
        touches_e2 = caption("chance 1/n is (1−1/n)ⁿ → 1/e ≈ 0.3679 — the split year, mirrored")
        touches_e.next_to(boundary, DOWN, buff=0.3)
        touches_e2.next_to(touches_e, DOWN, buff=0.15)
        self.play(FadeIn(touches_e), FadeIn(touches_e2))
        self.wait(2)


class ProportionsConverge(ConceptScene):
    """Swamping quantified: proportions converge while counts spread."""

    def construct(self):
        self.play(FadeIn(self.title("Proportions Converge"), shift=0.3 * DOWN))

        prompt = Text("Flip more. Watch two bands around one half.", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        self.play(FadeIn(prompt))

        left_head = Text("within ±5% of half", font_size=LABEL_SIZE, color=GOOD)
        left_head.move_to(3.3 * LEFT + 1.5 * UP)
        left_rows = VGroup(
            MathTex(r"n = 20:\quad 0.4966", font_size=36),
            MathTex(r"n = 100:\quad 0.7287", font_size=36),
            MathTex(r"n = 1000:\quad 0.9986", font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        left_rows.move_to(3.3 * LEFT + 0.25 * UP)
        right_head = Text("within ±5 heads", font_size=LABEL_SIZE, color=WARM)
        right_head.move_to(3.1 * RIGHT + 1.5 * UP)
        right_rows = VGroup(
            MathTex(r"n = 100:\quad 0.7287", font_size=36),
            MathTex(r"n = 1000:\quad 0.2720", font_size=36),
            MathTex(r"n = 10000:\quad 0.0876", font_size=36, color=WARM),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        right_rows.move_to(3.1 * RIGHT + 0.25 * UP)
        self.play(FadeIn(left_head), FadeIn(right_head))
        self.play(
            LaggedStart(*[Write(r) for r in [*left_rows, *right_rows]], lag_ratio=0.25),
            run_time=3.2,
        )
        shared = caption("the two n = 100 rows are the same band (45..55 heads) —")
        shared2 = caption("one number, two stories: rising on the left, falling on the right")
        shared.move_to(1.05 * DOWN)
        shared2.next_to(shared, DOWN, buff=0.15)
        self.play(FadeIn(shared), FadeIn(shared2))
        verdict = Text("Proportions converge; counts spread.", font_size=25)
        verdict2 = Text("Averages swamp — they never compensate.", font_size=25)
        verdict.move_to(2.05 * DOWN)
        verdict2.next_to(verdict, DOWN, buff=0.18)
        self.play(FadeIn(verdict), FadeIn(verdict2))
        self.wait(1.2)

        # The promises, named — the series' only forward pointers.
        self.play(
            FadeOut(VGroup(prompt, shared, shared2, left_head, left_rows, right_head, right_rows))
        )
        lln = MathTex(
            r"P\!\left(\left|\tfrac{S_n}{n} - \mu\right| \ge \varepsilon\right)"
            r" \to 0",
            font_size=40,
        ).move_to(0.9 * UP)
        named = caption("the weak law of large numbers — Bernoulli, proved by ~1689,")
        named2 = caption("printed 1713; this table computes instances of it — the theorem,")
        named3 = caption("and variance, arrive in a later series. And one caption for free:")
        named4 = caption("average surprisal over the 16 equal cells is exactly 4 bits")
        named.move_to(0.15 * DOWN)
        named2.next_to(named, DOWN, buff=0.15)
        named3.next_to(named2, DOWN, buff=0.15)
        named4.next_to(named3, DOWN, buff=0.15)
        self.play(Write(lln))
        self.play(FadeIn(named), FadeIn(named2))
        self.play(FadeIn(named3), FadeIn(named4))
        self.wait(1.4)

        self.play(FadeOut(VGroup(lln, named, named2, named3, named4)))
        takeaway = Text(
            "Per-frame distributions are pmfs like these — likelihood is next",
            font_size=26,
        ).move_to(3.25 * DOWN)
        final = VGroup(verdict, verdict2, takeaway)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(final, buff=0.26)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
