"""Counting rules — why each formula is the shape it is.

Four rules, each built the same way: show the thing being counted, count it by
hand, then let the formula fall out of what was just seen rather than appearing
first and being justified afterwards. A fifth scene closes the loop by saying
when to reach for which.

    MultiplicativeRule   n_1 * n_2 * ... * n_k        a tree that becomes a grid
    PermutationRule      P(n,r) = n!/(n-r)!           slots filled from a shrinking pool
    CombinationRule      C(n,r) = n!/(r!(n-r)!)       r! orderings collapsing to one set
    PartitionRule        n!/(n_1! n_2! ... n_k!)      a row chopped into blocks
    WhenToUseIt          which rule a problem needs   four problem shapes, mapped

Render:
    uv run python combinatorics/counting_rules_manim.py
    uv run python combinatorics/counting_rules_manim.py --scene PermutationRule --quality high
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
    chip,
    palette,
    render_cli,
    token,
)


class MultiplicativeRule(ConceptScene):
    """Independent stages multiply: a tree of paths, re-cast as a grid."""

    def construct(self):
        self.play(FadeIn(self.title("The Multiplicative Rule"), shift=0.3 * DOWN))

        subtitle = Text("Stage 1: 3 shirts        Stage 2: 4 pants", font_size=BODY_SIZE).to_edge(
            DOWN, buff=0.45
        )
        self.play(FadeIn(subtitle))

        # --- build the tree ---------------------------------------------------
        # The root and its label are scaffolding — the tree has to start
        # somewhere, but the eye belongs on the coloured branches, not here.
        root = Dot(point=[-5.9, 0, 0], radius=0.09, color=MUTED)
        root_label = Text("start", font_size=SMALL_SIZE, color=MUTED).next_to(root, LEFT, buff=0.15)

        shirts = ["A", "B", "C"]
        pants = ["1", "2", "3", "4"]
        shirt_ys = [1.95, 0.0, -1.95]
        pant_offsets = [0.75, 0.25, -0.25, -0.75]

        edges1, nodes1, edges2, leaves = VGroup(), VGroup(), VGroup(), VGroup()
        for i, (shirt, y) in enumerate(zip(shirts, shirt_ys, strict=True)):
            color = palette(i)
            stage1 = np.array([-3.4, y, 0])
            edges1.add(
                Line(root.get_center(), stage1, stroke_width=3, color=color, stroke_opacity=0.8)
            )
            nodes1.add(token(shirt, color, radius=0.28).move_to(stage1))
            for pant, dy in zip(pants, pant_offsets, strict=True):
                stage2 = np.array([-0.4, y + dy, 0])
                edges2.add(Line(stage1, stage2, stroke_width=2, color=color, stroke_opacity=0.55))
                leaves.add(
                    Text(f"{shirt}{pant}", font_size=21, color=color).move_to(stage2 + 0.25 * RIGHT)
                )

        self.play(FadeIn(root), FadeIn(root_label))
        self.play(
            LaggedStart(*[Create(e) for e in edges1], lag_ratio=0.25),
            LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes1], lag_ratio=0.25),
            run_time=1.6,
        )
        self.play(LaggedStart(*[Create(e) for e in edges2], lag_ratio=0.05), run_time=1.8)
        self.play(
            LaggedStart(*[FadeIn(leaf, shift=0.15 * RIGHT) for leaf in leaves], lag_ratio=0.05),
            run_time=1.8,
        )

        brace = Brace(leaves, RIGHT, color=ACCENT)
        count = Text("12 outcomes", font_size=28, color=ACCENT).next_to(brace, RIGHT, buff=0.2)
        self.play(GrowFromCenter(brace), Write(count))
        self.wait(0.6)

        # --- collapse the tree into a grid ------------------------------------
        # The same 12 paths, re-drawn as a rectangle: the product is literally
        # an area, which is the intuition the formula is standing in for.
        tree = VGroup(root, root_label, edges1, nodes1, edges2, leaves, brace, count)
        self.play(FadeOut(tree), FadeOut(subtitle))

        cells, labels = VGroup(), VGroup()
        for i in range(3):
            for j in range(4):
                square = Square(
                    side_length=0.95,
                    stroke_width=2,
                    color=palette(i),
                    fill_color=palette(i),
                    fill_opacity=0.16,
                )
                square.move_to([(j - 1.5) * 1.0, (1 - i) * 1.0, 0])
                cells.add(square)
                labels.add(Text(f"{shirts[i]}{pants[j]}", font_size=SMALL_SIZE).move_to(square))
        grid = VGroup(cells, labels).move_to(0.2 * DOWN)

        row_labels = VGroup(
            *[
                token(shirt, palette(i), 0.26).next_to(cells[4 * i], LEFT, buff=0.3)
                for i, shirt in enumerate(shirts)
            ]
        )
        col_labels = VGroup(
            *[
                Text(pant, font_size=LABEL_SIZE).next_to(cells[j], UP, buff=0.25)
                for j, pant in enumerate(pants)
            ]
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(VGroup(cell, label), scale=0.7)
                    for cell, label in zip(cells, labels, strict=True)
                ],
                lag_ratio=0.05,
            ),
            FadeIn(row_labels),
            FadeIn(col_labels),
            run_time=2.0,
        )

        equation = MathTex(r"3", r"\times", r"4", r"=", r"12", font_size=54)
        equation.next_to(grid, DOWN, buff=0.55)
        # The two stage counts are unranked categories, not semantic roles —
        # neither shirts nor pants is "the primary quantity". Only the result
        # earns a named colour.
        equation[0].set_color(palette(0))
        equation[2].set_color(palette(1))
        equation[4].set_color(ACCENT)
        self.play(Write(equation))
        self.wait(0.8)

        # --- generalise --------------------------------------------------------
        self.play(
            FadeOut(grid),
            FadeOut(row_labels),
            FadeOut(col_labels),
            equation.animate.move_to(2.0 * UP).scale(0.72),
        )

        general = MathTex(
            r"N = n_1 \times n_2 \times \cdots \times n_k",
            font_size=FORMULA_SIZE,
            color=ACCENT,
        ).shift(0.4 * DOWN)
        note = Text(
            "k independent stages — multiply the choices at each one", font_size=BODY_SIZE
        ).next_to(general, DOWN, buff=0.5)
        self.play(Write(general))
        self.play(Create(boxed(general, buff=0.35)), FadeIn(note))
        self.wait(2)


class PermutationRule(ConceptScene):
    """Order matters: fill r slots from a pool that shrinks as you go."""

    def construct(self):
        self.play(FadeIn(self.title("The Permutation Rule"), shift=0.3 * DOWN))

        prompt = Text("Choose 3 of 5 objects — order matters", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        letters = ["A", "B", "C", "D", "E"]
        pool = VGroup(*[token(letter, palette(i)) for i, letter in enumerate(letters)])
        pool.arrange(RIGHT, buff=0.55).move_to(1.55 * UP)
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in pool], lag_ratio=0.12))

        slots = VGroup()
        for _ in range(3):
            slot = RoundedRectangle(
                width=1.15, height=1.15, corner_radius=0.14, stroke_width=3, color=MUTED
            )
            slot.set_stroke(opacity=0.7)
            slots.add(slot)
        slots.arrange(RIGHT, buff=0.75).move_to(1.1 * DOWN)
        order_labels = VGroup(
            *[
                Text(label, font_size=22, color=MUTED).next_to(slots[i], DOWN, 0.22)
                for i, label in enumerate(["1st", "2nd", "3rd"])
            ]
        )
        self.play(Create(slots), FadeIn(order_labels))

        picks = [0, 2, 4]  # A, C, E
        counts = [5, 4, 3]
        factors = VGroup()
        for k, (index, remaining) in enumerate(zip(picks, counts, strict=True)):
            available = VGroup(*[pool[i] for i in range(5) if i not in picks[:k]])
            halo = VGroup(
                *[Circle(radius=0.44, color=ACCENT, stroke_width=3).move_to(t) for t in available]
            )
            tag = Text(f"{remaining} available", font_size=LABEL_SIZE, color=ACCENT)
            tag.move_to([-4.85, 1.55, 0])
            self.play(
                LaggedStart(*[Create(h) for h in halo], lag_ratio=0.08),
                FadeIn(tag),
                run_time=0.9,
            )
            self.play(pool[index].animate.move_to(slots[k]), FadeOut(halo), run_time=0.7)
            factor = Text(str(remaining), font_size=34, color=ACCENT).next_to(
                slots[k], UP, buff=0.3
            )
            factors.add(factor)
            self.play(FadeOut(tag), FadeIn(factor, shift=0.2 * DOWN), run_time=0.5)

        product = MathTex(r"5 \times 4 \times 3 = 60", font_size=RESULT_SIZE, color=ACCENT)
        product.next_to(order_labels, DOWN, buff=0.45)
        self.play(Write(product))
        self.wait(0.7)

        # --- factorial form -----------------------------------------------------
        # 5x4x3 is only n! with the tail cancelled off. Showing the tail in WARM
        # is the whole argument for the (n-r)! in the denominator.
        stage = VGroup(pool, slots, order_labels, factors, prompt)
        self.play(FadeOut(stage), product.animate.move_to(2.05 * UP).scale(0.75))

        chain = MathTex(
            r"\underbrace{5 \times 4 \times 3}_{\text{keep } r=3}",
            r"\times",
            r"\underbrace{2 \times 1}_{\text{unwanted}}",
            r"=",
            r"5!",
            font_size=46,
        ).shift(0.55 * UP)
        chain[0].set_color(ACCENT)
        chain[2].set_color(WARM)
        self.play(Write(chain))
        self.wait(0.5)

        formula = MathTex(r"P^n_r=\frac{n!}{(n-r)!}", font_size=FORMULA_SIZE, color=ACCENT)
        formula.shift(1.35 * DOWN)
        check = MathTex(r"P^5_3=\frac{5!}{2!}=\frac{120}{2}=60", font_size=38)
        check.next_to(formula, DOWN, buff=0.45)
        self.play(Write(formula))
        self.play(FadeIn(check, shift=0.2 * UP))
        self.wait(2)


class CombinationRule(ConceptScene):
    """Order does not matter: every set was counted r! times, so divide."""

    def construct(self):
        self.play(FadeIn(self.title("The Combination Rule"), shift=0.3 * DOWN))

        prompt = Text("Choose 3 of 5 objects — order does NOT matter", font_size=BODY_SIZE)
        prompt.next_to(self.head, DOWN, buff=0.28)
        self.play(FadeIn(prompt))

        # 3! orderings of the same set collapse to one. These six ARE the
        # overcount — the same role the cancelled 2 x 1 tail plays in
        # PermutationRule — so they take WARM, not a neutral colour.
        words = ["ACE", "AEC", "CAE", "CEA", "EAC", "ECA"]
        column = VGroup(*[Text(word, font_size=30, color=WARM) for word in words])
        column.arrange(DOWN, buff=0.28).move_to(3.6 * LEFT + 0.4 * DOWN)
        self.play(
            LaggedStart(*[FadeIn(w, shift=0.2 * RIGHT) for w in column], lag_ratio=0.12),
            run_time=1.6,
        )

        brace = Brace(column, RIGHT, color=ACCENT)
        caption_tex = MathTex(r"3! = 6\ \text{orderings}", font_size=34, color=ACCENT)
        caption_tex.next_to(brace, RIGHT, buff=0.25)
        self.play(GrowFromCenter(brace), Write(caption_tex))

        arrow = Arrow(
            caption_tex.get_right() + 0.15 * RIGHT,
            caption_tex.get_right() + 2.1 * RIGHT,
            buff=0.1,
            color=MUTED,
        )
        one = MathTex(r"\{A, C, E\}", font_size=44, color=GOOD)
        one.next_to(arrow, RIGHT, buff=0.25)
        self.play(GrowArrow(arrow), FadeIn(one, scale=0.7))
        self.play(Indicate(one, color=GOOD))
        self.wait(0.6)

        idea = Text(
            "every combination was counted 3! times", font_size=BODY_SIZE, color=ACCENT
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(idea))
        self.wait(0.8)

        self.play(FadeOut(VGroup(column, brace, caption_tex, arrow, one, idea, prompt)))

        # --- divide out the overcount --------------------------------------------
        step = MathTex(
            r"\frac{P^5_3}{3!}", r"=", r"\frac{60}{6}", r"=", r"10", font_size=RESULT_SIZE
        ).shift(1.9 * UP)
        step[4].set_color(ACCENT)
        self.play(Write(step))

        combos = ["ABC", "ABD", "ABE", "ACD", "ACE", "ADE", "BCD", "BCE", "BDE", "CDE"]
        chips = VGroup(*[chip(combo, GOOD) for combo in combos])
        chips.arrange_in_grid(rows=2, cols=5, buff=0.28).shift(0.15 * DOWN)
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.08), run_time=1.8)

        formula = MathTex(
            r"C^n_r=\binom{n}{r}=\frac{n!}{r!\,(n-r)!}", font_size=FORMULA_SIZE, color=ACCENT
        )
        formula.to_edge(DOWN, buff=0.65)
        self.play(Write(formula))
        self.wait(2)


class PartitionRule(ConceptScene):
    """Split into labelled groups: divide out the order inside each block."""

    def construct(self):
        self.play(FadeIn(self.title("The Partition Rule"), shift=0.3 * DOWN))

        prompt = Text(
            "Split 6 distinct objects into groups of 3, 2 and 1", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.28)
        self.play(FadeIn(prompt))

        sizes = [3, 2, 1]
        # The three blocks are categories with no ranking between them, which is
        # exactly what PALETTE is for. They previously used COOL/WARM/GOOD, whose
        # meanings (primary quantity / cancelled / confirmed) none of them carry.
        # Pixel-identical either way — COOL, WARM and GOOD *are* PALETTE[0:3] —
        # so this only changes what the code claims.
        group_colors = [palette(i) for i in range(len(sizes))]
        objects = VGroup(*[token(str(i + 1), palette(i)) for i in range(6)])
        objects.arrange(RIGHT, buff=0.5).move_to(1.75 * UP)
        self.play(LaggedStart(*[FadeIn(o, scale=0.6) for o in objects], lag_ratio=0.1))

        line_up = MathTex(r"6! = 720\ \text{ orderings of the row}", font_size=36, color=ACCENT)
        line_up.move_to([0, 0.15, 0])
        self.play(Write(line_up))
        self.wait(0.5)

        # cut the row into blocks
        groups, boxes, tags = [], VGroup(), VGroup()
        start = 0
        for g, (size, color) in enumerate(zip(sizes, group_colors, strict=True)):
            group = VGroup(*objects[start : start + size])
            groups.append(group)
            box = SurroundingRectangle(group, color=color, buff=0.2, corner_radius=0.12)
            box.set_fill(color, opacity=0.08).set_stroke(width=3)
            boxes.add(box)
            tags.add(
                MathTex(rf"n_{{{g + 1}}} = {size}", font_size=34, color=color).next_to(
                    box, DOWN, buff=0.22
                )
            )
            start += size
        self.play(
            LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3),
            LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.3),
        )
        self.wait(0.4)

        inner = Text("inside a group, order is irrelevant", font_size=28, color=ACCENT)
        inner.next_to(line_up, DOWN, buff=0.35)
        self.play(FadeIn(inner))
        # Shuffle the first group to show the partition is unchanged by it —
        # that invariance is the n_1! in the denominator.
        first, second, third = groups[0][0], groups[0][1], groups[0][2]
        self.play(Swap(first, third), run_time=0.8)
        self.play(Swap(first, second), run_time=0.8)
        self.wait(0.4)

        self.play(FadeOut(VGroup(prompt, line_up, inner)))
        stage = VGroup(objects, boxes, tags)
        self.play(stage.animate.scale(0.82).move_to(1.55 * UP))

        calc = MathTex(
            r"\frac{6!}{3!\,\cdot\,2!\,\cdot\,1!}",
            r"=",
            r"\frac{720}{6 \cdot 2 \cdot 1}",
            r"=",
            r"60",
            font_size=RESULT_SIZE,
        ).shift(0.55 * DOWN)
        calc[4].set_color(ACCENT)
        self.play(Write(calc))
        self.wait(0.7)

        # Bespoke size: this formula carries a summation constraint alongside the
        # fraction, so it is wider than the one-line formulas FORMULA_SIZE is cut
        # for and has to come down to stay inside the frame.
        formula = MathTex(
            r"N=\frac{n!}{n_1!\,n_2!\cdots n_k!},\qquad \sum_{i=1}^{k} n_i = n",
            font_size=46,
            color=ACCENT,
        )
        formula.to_edge(DOWN, buff=0.7)
        self.play(Write(formula), Create(boxed(formula, buff=0.28)))
        self.wait(2)


class WhenToUseIt(ConceptScene):
    """Which rule a problem needs, and why all four are the same rule."""

    def construct(self):
        self.play(FadeIn(self.title("Which Rule, and When"), shift=0.3 * DOWN))

        # Level three of the narrative: the first four scenes establish what
        # each rule says and why it is true, and stop. Without this one the
        # module teaches four formulas instead of a way of deciding.
        cases = [
            ("k stages, each with its own menu", "Multiplicative"),
            ("Pick r of n — order is the answer", "Permutation"),
            ("Pick r of n — order irrelevant", "Combination"),
            ("Deal n into labelled groups", "Partition"),
        ]

        questions = VGroup(*[Text(q, font_size=21) for q, _ in cases])
        questions.arrange(DOWN, buff=0.66, aligned_edge=LEFT)
        questions.to_edge(LEFT, buff=0.7).shift(0.25 * DOWN)

        rules = VGroup(*[Text(r, font_size=23, weight=BOLD, color=ACCENT) for _, r in cases])
        rules.arrange(DOWN, buff=0.66, aligned_edge=LEFT)
        rules.to_edge(RIGHT, buff=1.5).shift(0.25 * DOWN)
        for question, rule in zip(questions, rules, strict=True):
            rule.match_y(question)

        # One x for every arrow, past the widest question, so the column reads
        # as a single mapping rather than four unrelated statements.
        start_x = questions.get_right()[0] + 0.3
        end_x = rules.get_left()[0] - 0.3
        arrows = VGroup(
            *[
                Arrow(
                    np.array([start_x, question.get_y(), 0]),
                    np.array([end_x, question.get_y(), 0]),
                    buff=0,
                    color=MUTED,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.18,
                )
                for question in questions
            ]
        )

        for question, arrow, rule in zip(questions, arrows, rules, strict=True):
            self.play(
                FadeIn(question, shift=0.2 * RIGHT),
                GrowArrow(arrow),
                FadeIn(rule, shift=0.2 * LEFT),
                run_time=0.65,
            )
        self.wait(0.8)

        # The transferable idea: the four are one rule with a correction, which
        # is what makes them worth remembering as a set.
        takeaway = Text(
            "All four are the product rule — minus the orderings you don't care about",
            font_size=22,
        )
        takeaway.to_edge(DOWN, buff=0.75)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.26)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
