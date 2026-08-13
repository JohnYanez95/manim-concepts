"""Dynamic programming — the move the trellis performed without a name.

Six scenes. The repo's oldest promise: the alignment series ran a dynamic
program on screen and never said so; this series names the move — the
recursion tree folding into a small table — and re-reads two pictures the
viewer already owns as instances of it.

    TheQuestionAskedTwice   177 calls to settle 11 questions
    WriteTheAnswersDown     the tree folds; the move gets its name
    TheLatticeRecounted     shared prefixes, counted once — Pascal's sum
    TheTrellisWasAMemo      the forward trellis re-read as a stored answer
    WhatBreaksIt            DP pays exactly for how much past the future needs
    TheSignatureInTheWild   the two-part signature, mapped over the wild

Every number on screen traces to plan 013's verification pass (exact
integer arithmetic, two independent routes; the study guide's DP chapter
is the seed — ADR 008's pipeline running book-to-screen).

Render:
    uv run python algorithms/dynamic_programming_manim.py
    uv run python algorithms/dynamic_programming_manim.py -s WriteTheAnswersDown -q draft
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
    on_frame,
    palette,
    render_cli,
)

# The fib(5) call tree, plan 013 anchor A: 15 call nodes, 6 distinct
# subproblems. Nested tuples (label, children); drawn depth-by-depth with
# x assigned by leaf order — small enough to be honest (177 is a ticker,
# never a drawing; decision 6).
FIB5_TREE = (
    5,
    (
        (4, ((3, ((2, ((1, ()), (0, ()))), (1, ()))), (2, ((1, ()), (0, ()))))),
        (3, ((2, ((1, ()), (0, ()))), (1, ()))),
    ),
)

# Anchor A tables (n = 0..12), both routes verified in the plan.
FIB = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
CALLS = [1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177, 287, 465]

# The walker's lattice, anchor D: node (i, j) = C(i+j, j), rows bottom-up.
LATTICE = [[1, 1, 1, 1, 1], [1, 2, 3, 4, 5], [1, 3, 6, 10, 15]]

# The mini trellis (states ε, A, ε), anchor E: columns by recurrence AND
# enumeration; accepted 3 + 3 = 6 of 2^3 = 8 raw paths. No skip edges —
# the middle state's neighbours are both blanks (pitfall 9).
MINI_COLUMNS = [[1, 1, 0], [1, 2, 1], [1, 3, 3]]

# Anchor G: the exact 41-digit path count at T = 100, U = 50.
BIG_COUNT = "20{,}128{,}660{,}909{,}731{,}932{,}294{,}240{,}234{,}380{,}929{,}315{,}748{,}140"


def _tree_layout(tree, x0=-6.0, leaf_gap=1.28, y0=2.0, dy=0.95):
    """Positions for a nested-tuple call tree, x by leaf order, y by depth.

    Returns (nodes, edges): nodes as (label, depth, x, y, path) where path
    is the root-to-node index tuple (unique id), edges as (parent_path,
    child_path) pairs.
    """
    nodes, edges = [], []
    cursor = [0]

    def place(sub, depth, path):
        label, children = sub
        if not children:
            x = x0 + cursor[0] * leaf_gap
            cursor[0] += 1
        else:
            child_xs = []
            for i, ch in enumerate(children):
                place(ch, depth + 1, path + (i,))
                child_xs.append(next(n[2] for n in nodes if n[4] == path + (i,)))
                edges.append((path, path + (i,)))
            x = sum(child_xs) / len(child_xs)
        nodes.append((label, depth, x, y0 - depth * dy, path))

    place(tree, 0, ())
    return nodes, edges


def _tree_mobjects(background_color, radius=0.27, font_size=18):
    """The fib(5) tree as manim objects, keyed by path for targeting."""
    nodes, edges = _tree_layout(FIB5_TREE)
    lookup = {path: (label, x, y) for label, _, x, y, path in nodes}
    circles, labels = {}, {}
    edge_group = VGroup()
    for parent, child in edges:
        _, px, py = lookup[parent]
        _, cx, cy = lookup[child]
        edge_group.add(
            Line([px, py, 0], [cx, cy, 0], color=MUTED, stroke_width=1.6, stroke_opacity=0.6)
        )
    for path, (label, x, y) in lookup.items():
        circles[path] = (
            Circle(radius=radius, color=MUTED, stroke_width=1.8)
            .set_fill(background_color, opacity=1.0)
            .move_to([x, y, 0])
        )
        labels[path] = Text(f"F{label}", font_size=font_size).move_to([x, y, 0])
    return lookup, circles, labels, edge_group


class TheQuestionAskedTwice(ConceptScene):
    """Computed exactly as written, the recursion asks the same question over and over."""

    def construct(self):
        self.play(FadeIn(self.title("The Question Asked Twice"), shift=0.3 * DOWN))

        opening = Text(
            "F(n) = F(n−1) + F(n−2). Correct. Now watch it run.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        lookup, circles, labels, edges = _tree_mobjects(self.camera.background_color)
        tree = VGroup(edges, VGroup(*circles.values()), VGroup(*labels.values()))
        tree.shift(0.35 * DOWN)
        # The convention, pinned before any counting (decision 6).
        convention = caption("every call counts as one; F0 and F1 answer directly")
        convention.to_edge(DOWN, buff=0.4)
        self.play(Create(edges, lag_ratio=0.02, run_time=1.4), FadeIn(VGroup(*circles.values())))
        self.play(
            LaggedStart(*[FadeIn(la, scale=0.7) for la in labels.values()], lag_ratio=0.04),
            run_time=1.2,
        )
        self.play(FadeIn(convention))
        self.wait(0.6)

        # The repetition, made countable: same label, many parents.
        self.play(FadeOut(opening))
        note = Text(
            "the same question, asked under different parents",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(note))
        for value, color in ((3, palette(0)), (2, palette(1)), (1, palette(2))):
            dupes = [circles[p] for p, (la, _, _) in lookup.items() if la == value]
            count = len(dupes)
            flash = VGroup(
                *[SurroundingRectangle(c, color=color, buff=0.06, corner_radius=0.1) for c in dupes]
            )
            tag = Text(f"F{value} asked {count} times", font_size=SMALL_SIZE, color=color)
            tag.move_to([4.55, 1.4 - 0.55 * (3 - value), 0])
            on_frame(tag)
            self.play(Create(flash), FadeIn(tag), run_time=0.8)
            self.play(FadeOut(flash), run_time=0.4)
        self.wait(0.5)

        # The ticker to n = 10 — never drawn, only counted (decision 6).
        self.play(FadeOut(note))
        ticker_head = Text(
            "this tree is n = 5: fifteen calls for six questions. Push n up:",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(ticker_head))
        self.play(FadeOut(convention))
        ticker = MathTex(
            r"n = 6:\ 25 \text{ calls} \qquad n = 8:\ 67"
            r" \qquad n = 10:\ {\bf 177} \text{ calls for } 11 \text{ questions}",
            font_size=30,
            color=ACCENT,
        ).to_edge(DOWN, buff=0.75)
        self.play(Write(ticker))
        self.wait(0.8)
        compound = caption("the repeats compound at the sequence's own rate:")
        compound2 = caption("at n = 10, F8 is asked 2×, F7 3×, F6 5× …")
        self.play(FadeOut(ticker))
        compound.to_edge(DOWN, buff=0.6)
        compound2.next_to(compound, DOWN, buff=0.15)
        on_frame(compound2)
        self.play(FadeIn(compound), FadeIn(compound2))
        self.wait(1.0)
        rows = VGroup()

        # Formula last.
        self.play(FadeOut(VGroup(tree, ticker_head, rows, compound, compound2)))
        formula = MathTex(
            r"\text{calls}(n) \;=\; 2\,F(n{+}1) - 1",
            font_size=48,
            color=ACCENT,
        ).move_to(0.85 * UP)
        formula_note = caption("checked against an instrumented count at every n up to 12 —")
        formula_note2 = caption("the tree grows at the sequence's own golden rate")
        formula_note.move_to(0.05 * DOWN)
        formula_note2.next_to(formula_note, DOWN, buff=0.15)
        closing = Text(
            "the defect is never the answer — it is the asking",
            font_size=BODY_SIZE,
        ).move_to(1.35 * DOWN)
        self.play(Write(formula))
        self.play(FadeIn(formula_note), FadeIn(formula_note2))
        self.play(FadeIn(closing))
        self.wait(1.6)


class WriteTheAnswersDown(ConceptScene):
    """Store each answer once and the tree folds — the move gets its name."""

    def construct(self):
        self.play(FadeIn(self.title("Write the Answers Down"), shift=0.3 * DOWN))

        opening = Text(
            "Same tree. One new habit: write each answer down, once.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        lookup, circles, labels, edges = _tree_mobjects(self.camera.background_color)
        tree = VGroup(edges, VGroup(*circles.values()), VGroup(*labels.values()))
        tree.shift(0.15 * UP).scale(0.86, about_point=[0, 0.7, 0])
        self.play(FadeIn(tree))

        # The memo row: six boxes, one per distinct question.
        memo_boxes, memo_vals = VGroup(), VGroup()
        for i in range(6):
            box = Square(side_length=0.62, color=GOOD, stroke_width=2).move_to(
                [-3.1 + i * 1.24, -2.35, 0]
            )
            tag = Text(f"F{i}", font_size=15, color=MUTED).next_to(box, DOWN, buff=0.12)
            memo_boxes.add(VGroup(box, tag))
        memo_label = caption("the memo — six boxes for six questions")
        memo_label.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(memo_boxes), FadeIn(memo_label))

        # First computation of each label writes down (GOOD); every later
        # copy greys out WARM and reads up — the Erickson fold.
        first_seen: dict[int, tuple] = {}
        # Call order is depth-first, left child first: sort paths lexically.
        for path in sorted(lookup, key=lambda p: (p, len(p))):
            label = lookup[path][0]
            if label not in first_seen:
                first_seen[label] = path
        writes, grey_targets = [], []
        for path, (label, _, _) in lookup.items():
            if first_seen[label] == path:
                writes.append((label, path))
            else:
                grey_targets.append(path)
        write_anims = []
        for label, _path in sorted(writes):
            value = Text(str(FIB[label]), font_size=20, color=GOOD).move_to(memo_boxes[label][0])
            memo_vals.add(value)
            write_anims.append(FadeIn(value, shift=0.2 * DOWN))
        self.play(
            LaggedStart(*write_anims, lag_ratio=0.15),
            *[circles[p].animate.set_stroke(GOOD) for _, p in writes],
            run_time=1.4,
        )
        grey = caption("every later copy is a lookup, not a computation")
        self.play(FadeOut(memo_label))
        grey.to_edge(DOWN, buff=0.35)
        self.play(
            FadeIn(grey),
            *[circles[p].animate.set_stroke(WARM, opacity=0.45) for p in grey_targets],
            *[labels[p].animate.set_opacity(0.35) for p in grey_targets],
            run_time=1.0,
        )
        count_drop = MathTex(
            r"15 \text{ calls} \;\to\; 6 \text{ computations}",
            font_size=32,
            color=ACCENT,
        ).move_to([4.5, 1.6, 0])
        on_frame(count_drop)
        count_drop2 = MathTex(
            r"177 \;\to\; 11 \ \text{ at } n = 10",
            font_size=30,
            color=ACCENT,
        ).next_to(count_drop, DOWN, buff=0.25)
        self.play(Write(count_drop))
        self.play(Write(count_drop2))
        self.wait(1.0)

        # The naming beat.
        self.play(
            FadeOut(VGroup(tree, memo_boxes, memo_vals, grey, opening, count_drop, count_drop2))
        )
        name = Text(
            "Dynamic programming: solve every small version once,",
            font_size=BODY_SIZE,
        ).move_to(1.55 * UP)
        name2 = Text(
            "store it, and let the big version assemble itself.",
            font_size=BODY_SIZE,
        ).move_to(1.05 * UP)
        conditions = MathTex(
            r"\text{it works when:}\quad \text{the questions repeat}\ \ \wedge\ \ "
            r"\text{the stored number is all the future needs}",
            font_size=28,
        ).move_to(0.1 * UP)
        history = caption('"memo functions" — Michie, Nature, 1968; the name "dynamic')
        history2 = caption("programming\" is Bellman's, and the story he told about choosing it")
        history3 = caption(
            "— a word no Congressman could object to — is his retelling, not history"
        )
        history.move_to(0.85 * DOWN)
        history2.next_to(history, DOWN, buff=0.15)
        history3.next_to(history2, DOWN, buff=0.15)
        self.play(FadeIn(name), FadeIn(name2))
        self.play(Write(conditions))
        self.play(FadeIn(history), FadeIn(history2), FadeIn(history3))
        self.wait(1.8)


class TheLatticeRecounted(ConceptScene):
    """Shared prefixes, counted once — the walker's 15 routes by Pascal's sum."""

    def construct(self):
        self.play(FadeIn(self.title("The Lattice, Recounted"), shift=0.3 * DOWN))

        opening = Text(
            "The counting series chose 2 of 6 steps: 15 routes. Recount them —",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        opening2 = caption("this time, without ever listing one")
        opening2.next_to(opening, DOWN, buff=0.18)
        self.play(FadeIn(opening), FadeIn(opening2))

        # The 5×3 node grid; node (i, j) counts routes from the origin.
        xs = [-3.6 + 1.5 * i for i in range(5)]
        ys = [-2.1 + 1.15 * j for j in range(3)]
        nodes = {}
        grid = VGroup()
        for j, y in enumerate(ys):
            for i, x in enumerate(xs):
                c = Circle(radius=0.3, color=MUTED, stroke_width=1.8).set_fill(
                    self.camera.background_color, opacity=1.0
                )
                c.move_to([x, y, 0])
                nodes[(i, j)] = c
                grid.add(c)
        lines = VGroup()
        for j in range(3):
            for i in range(5):
                if i < 4:
                    lines.add(
                        Line(
                            nodes[(i, j)].get_center(),
                            nodes[(i + 1, j)].get_center(),
                            color=MUTED,
                            stroke_width=1.6,
                            stroke_opacity=0.55,
                        )
                    )
                if j < 2:
                    lines.add(
                        Line(
                            nodes[(i, j)].get_center(),
                            nodes[(i, j + 1)].get_center(),
                            color=MUTED,
                            stroke_width=1.6,
                            stroke_opacity=0.55,
                        )
                    )
        self.play(Create(lines, lag_ratio=0.02, run_time=1.2), FadeIn(grid))

        # Fill by Pascal addition, bottom row first — arrows match the fill
        # order (pitfall 7): each count arrives from the left and from below.
        figures = {}
        fills = []
        for j in range(3):
            for i in range(5):
                value = LATTICE[j][i]
                fig = Text(str(value), font_size=19).move_to(nodes[(i, j)])
                figures[(i, j)] = fig
                fills.append(FadeIn(fig, scale=0.7))
        rule = caption("each node: routes from the left + routes from below")
        self.play(FadeOut(opening2))
        rule.to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*fills, lag_ratio=0.06), FadeIn(rule), run_time=2.2)

        # The convergence bundle: two routes end at one node, leave as one
        # number — the overlap condition, drawn.
        target = nodes[(2, 1)]
        left_arrow = Arrow(
            nodes[(1, 1)].get_center(),
            target.get_center(),
            color=COOL,
            stroke_width=5,
            buff=0.3,
            max_tip_length_to_length_ratio=0.2,
        )
        below_arrow = Arrow(
            nodes[(2, 0)].get_center(),
            target.get_center(),
            color=COOL,
            stroke_width=5,
            buff=0.3,
            max_tip_length_to_length_ratio=0.2,
        )
        ring = SurroundingRectangle(target, color=ACCENT, buff=0.08, corner_radius=0.12)
        sum_read = MathTex(r"2 + 1 = 3", font_size=30, color=ACCENT)
        sum_read.next_to(target, UP + RIGHT, buff=0.15).shift(0.2 * RIGHT)
        converge = caption("two routes converge — stored once, every continuation counted once")
        self.play(Create(left_arrow), Create(below_arrow), Create(ring))
        self.play(FadeOut(rule), FadeOut(opening))
        converge.to_edge(DOWN, buff=0.4)
        self.play(Write(sum_read), FadeIn(converge))
        self.wait(1.0)

        # The corner lands on the counting series' own number.
        corner_ring = SurroundingRectangle(nodes[(4, 2)], color=GOOD, buff=0.08, corner_radius=0.12)
        check = MathTex(
            r"15 \;=\; \binom{6}{2}",
            font_size=36,
            color=GOOD,
        ).move_to([4.9, 2.15, 0])
        on_frame(check)
        check_note = caption("the counting series' answer,\nreached by additions alone")
        check_note.next_to(check, DOWN, buff=0.28)
        on_frame(check_note)
        self.play(Create(corner_ring), Write(check), FadeIn(check_note))
        self.wait(1.0)

        # Formula last.
        self.play(
            FadeOut(
                VGroup(
                    grid,
                    lines,
                    VGroup(*figures.values()),
                    left_arrow,
                    below_arrow,
                    ring,
                    sum_read,
                    converge,
                    corner_ring,
                    check,
                    check_note,
                )
            )
        )
        formula = MathTex(
            r"R(i, j) \;=\; R(i{-}1, j) + R(i, j{-}1)",
            font_size=46,
            color=ACCENT,
        ).move_to(0.85 * UP)
        closing = caption("recounted, never listed — an exponential list of routes")
        closing2 = caption("reorganised into fifteen small sums")
        closing.move_to(0.1 * DOWN)
        closing2.next_to(closing, DOWN, buff=0.15)
        self.play(Write(formula))
        self.play(FadeIn(closing), FadeIn(closing2))
        self.wait(1.6)


class TheTrellisWasAMemo(ConceptScene):
    """The forward trellis was dynamic programming all along — α is a stored answer."""

    def construct(self):
        self.play(FadeIn(self.title("The Trellis Was a Memo"), shift=0.3 * DOWN))

        opening = Text(
            "You have watched this move before — without its name.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The mini trellis: transcript A, states (ε, A, ε), T = 3. No skip
        # edges — both of A's neighbours are blanks (pitfall 9).
        state_labels = ["ε", "A", "ε"]
        state_colors = [MUTED, palette(0), MUTED]
        xs = [-2.2 + 1.7 * t for t in range(3)]
        ys = [1.15 - 1.0 * s for s in range(3)]
        nodes = {}
        grid = VGroup()
        for t, x in enumerate(xs):
            for s, y in enumerate(ys):
                c = Circle(radius=0.3, color=MUTED, stroke_width=1.8).set_fill(
                    self.camera.background_color, opacity=1.0
                )
                c.move_to([x, y, 0])
                nodes[(t, s)] = c
                grid.add(c)
        row_tags = VGroup(
            *[
                Text(state_labels[s], font_size=SMALL_SIZE, color=state_colors[s]).move_to(
                    [-3.3, ys[s], 0]
                )
                for s in range(3)
            ]
        )
        col_tags = VGroup(
            *[
                Text(f"t={t + 1}", font_size=SMALL_SIZE, color=COOL).move_to(
                    [xs[t], ys[0] + 0.62, 0]
                )
                for t in range(3)
            ]
        )
        edges = VGroup()
        for t in range(2):
            for s in range(3):
                for s2 in (s, s + 1):
                    if s2 <= 2:
                        edges.add(
                            Line(
                                nodes[(t, s)].get_center(),
                                nodes[(t + 1, s2)].get_center(),
                                color=MUTED,
                                stroke_width=1.6,
                                stroke_opacity=0.55,
                            )
                        )
        self.play(FadeIn(row_tags), FadeIn(col_tags), Create(edges, run_time=1.0), FadeIn(grid))

        figures = []
        for t in range(3):
            entering = VGroup()
            for s in range(3):
                v = MINI_COLUMNS[t][s]
                if v == 0:
                    continue
                fig = Text(str(v), font_size=19).move_to(nodes[(t, s)])
                figures.append(fig)
                entering.add(fig)
            self.play(
                LaggedStart(*[FadeIn(f, scale=0.7) for f in entering], lag_ratio=0.1),
                run_time=0.6,
            )
        # The waist: two prefixes end in one cell; store once, reuse after.
        waist = SurroundingRectangle(nodes[(1, 1)], color=ACCENT, buff=0.08, corner_radius=0.12)
        waist_note = caption("two prefixes end here — εA and AA — stored once, reused after")
        waist_note.to_edge(DOWN, buff=0.4)
        self.play(Create(waist), FadeIn(waist_note))
        accepted = MathTex(r"3 + 3 = 6", font_size=34, color=ACCENT).move_to([4.3, 0.6, 0])
        acc_note = caption("of the 8 raw paths — the memo,\nfilled column by column")
        acc_note.next_to(accepted, DOWN, buff=0.28)
        on_frame(acc_note)
        self.play(Write(accepted), FadeIn(acc_note))
        self.wait(1.0)

        # The flagship re-read + the scale card.
        self.play(
            FadeOut(
                VGroup(
                    grid,
                    edges,
                    row_tags,
                    col_tags,
                    VGroup(*figures),
                    waist,
                    waist_note,
                    accepted,
                    acc_note,
                    opening,
                )
            )
        )
        reread = Text(
            "The alignment series' grid: 81 raw paths, 15 accepted, 20 circles.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        alpha_read = MathTex(
            r"\alpha_t(s) \text{ was a stored answer all along}",
            font_size=36,
            color=ACCENT,
        ).move_to(1.5 * UP)
        self.play(FadeIn(reread), Write(alpha_read))
        scale_head = Text("At a real utterance's scale, T = 100, U = 50:", font_size=SMALL_SIZE)
        scale_head.move_to(0.7 * UP)
        cells = MathTex(
            r"\text{the table: } 100 \times 101 = 10{,}100 \text{ cells}",
            font_size=32,
            color=COOL,
        ).move_to(0.1 * UP)
        paths = MathTex(BIG_COUNT, font_size=17, color=WARM).move_to(0.55 * DOWN)
        paths_note = caption("the list it replaces — 41 digits, about 2.013 × 10⁴⁰ paths;")
        paths_note2 = caption("thirty-six orders of magnitude between the table and the list")
        paths_note.move_to(1.15 * DOWN)
        paths_note2.next_to(paths_note, DOWN, buff=0.15)
        self.play(FadeIn(scale_head))
        self.play(Write(cells))
        self.play(Write(paths))
        self.play(FadeIn(paths_note), FadeIn(paths_note2))
        self.wait(1.2)

        # The reconciliation + the two-stories bridge (decisions 2 and 5).
        self.play(
            FadeOut(VGroup(reread, alpha_read, scale_head, cells, paths, paths_note, paths_note2))
        )
        recon = Text(
            "Memoized or tabulated, it is one table in two orders:",
            font_size=BODY_SIZE,
        ).move_to(1.5 * UP)
        recon2 = caption("asked-when-needed, or filled deliberately in the order the")
        recon3 = caption("questions depend on each other — the column sweep is the second")
        recon2.move_to(0.8 * UP)
        recon3.next_to(recon2, DOWN, buff=0.15)
        bridge = Text("And two stories, one move:", font_size=BODY_SIZE).move_to(0.35 * DOWN)
        bridge2 = caption("Fibonacci stops recomputing; the trellis never computed a path at all —")
        bridge3 = caption("a sum reorganised, distributivity doing the factoring. In both:")
        bridge4 = Text(
            "one stored answer serves many parents",
            font_size=BODY_SIZE,
        ).move_to(2.35 * DOWN)
        bridge2.move_to(1.0 * DOWN)
        bridge3.next_to(bridge2, DOWN, buff=0.15)
        self.play(FadeIn(recon), FadeIn(recon2), FadeIn(recon3))
        self.play(FadeIn(bridge), FadeIn(bridge2), FadeIn(bridge3))
        self.play(FadeIn(bridge4, shift=0.2 * UP), Create(boxed(bridge4, buff=0.22)))
        self.wait(1.8)


class WhatBreaksIt(ConceptScene):
    """Dynamic programming pays exactly for how much past the future needs."""

    def construct(self):
        self.play(FadeIn(self.title("What Breaks It"), shift=0.3 * DOWN))

        opening = Text(
            "Two ways to lose the bargain.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # (a) No overlap: disjoint halves — a memo nobody reads twice.
        no_overlap = Text("1. Nothing repeats.", font_size=BODY_SIZE, color=COOL)
        no_overlap.move_to([-3.6, 1.5, 0])
        labels_txt = [
            ("sort 8", 0, 0),
            ("sort a–d", -1.5, -1),
            ("sort e–h", 1.5, -1),
            ("sort a–b", -2.25, -2),
            ("sort c–d", -0.75, -2),
            ("sort e–f", 0.75, -2),
            ("sort g–h", 2.25, -2),
        ]
        dc_nodes = VGroup()
        for text, dx, dy in labels_txt:
            chip = Text(text, font_size=14, color=MUTED).move_to(
                [-3.4 + dx * 0.85, 0.6 + dy * 0.75, 0]
            )
            dc_nodes.add(chip)
        dc_edges = VGroup(
            *[
                Line(
                    dc_nodes[a].get_bottom() + 0.16 * DOWN,
                    dc_nodes[b].get_top() + 0.16 * UP,
                    color=MUTED,
                    stroke_width=1.4,
                    stroke_opacity=0.5,
                )
                for a, b in ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6))
            ]
        )
        dc_note = caption("every label distinct: a memo written once and read never —")
        dc_note2 = caption("filing, not speedup; divide and conquer is the tree-shaped sibling")
        dc_note.move_to([-3.4, -1.35, 0])
        dc_note2.next_to(dc_note, DOWN, buff=0.15)
        on_frame(dc_note)
        on_frame(dc_note2)
        self.play(FadeIn(no_overlap), FadeIn(dc_nodes), Create(dc_edges))
        self.play(FadeIn(dc_note), FadeIn(dc_note2))

        # The shape table: the verdict in one glance.
        shapes = VGroup()
        for i, (shape, verdict) in enumerate(
            (
                ("chain", "decrease & conquer"),
                ("tree", "divide & conquer — no reuse"),
                ("DAG", "dynamic programming — reuse"),
            )
        ):
            row = Text(f"{shape}:  {verdict}", font_size=15, color=MUTED if i < 2 else GOOD)
            row.move_to([3.9, 1.15 - 0.5 * i, 0])
            on_frame(row)
            shapes.add(row)
        shape_head = Text(
            "the subproblem graph's shape is the verdict",
            font_size=SMALL_SIZE,
            color=COOL,
        ).move_to([3.9, 1.75, 0])
        on_frame(shape_head)
        self.play(FadeIn(shape_head), FadeIn(shapes))
        self.wait(1.2)

        # (b) No small state: the cells fatten.
        self.play(
            FadeOut(
                VGroup(
                    no_overlap, dc_nodes, dc_edges, dc_note, dc_note2, shapes, shape_head, opening
                )
            )
        )
        fat_head = Text(
            "2. The future needs more of the past.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(fat_head))
        step1 = MathTex(
            r"\text{legality reads one state back:}\quad 101 \text{ states per column}",
            font_size=32,
        ).move_to(1.2 * UP)
        step2 = MathTex(
            r"\text{legality reads two back:}\quad 101^2 = 10{,}201"
            r"\quad\Rightarrow\quad 1{,}020{,}100 \text{ cells}",
            font_size=32,
            color=COOL,
        ).move_to(0.45 * UP)
        step2_note = caption("fatter, and still polynomial — the price is paid, not fatal")
        step2_note.move_to(0.25 * DOWN)
        step3 = MathTex(
            r"\text{legality reads \emph{everything}:}\quad"
            r" \text{the state IS the path}",
            font_size=32,
            color=WARM,
        ).move_to(1.0 * DOWN)
        step3_note = caption("the table becomes the exponential list it was meant to replace —")
        step3_note2 = caption("no small state summarises the past, and the bargain is off")
        step3_note.move_to(1.7 * DOWN)
        step3_note2.next_to(step3_note, DOWN, buff=0.15)
        self.play(Write(step1))
        self.play(Write(step2), FadeIn(step2_note))
        self.play(Write(step3))
        self.play(FadeIn(step3_note), FadeIn(step3_note2))
        self.wait(1.2)

        # The principle, priced.
        self.play(
            FadeOut(VGroup(fat_head, step1, step2, step2_note, step3, step3_note, step3_note2))
        )
        takeaway = Text(
            "DP pays exactly for how much past the future needs",
            font_size=24,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class TheSignatureInTheWild(ConceptScene):
    """The two-part signature — an exponential sum and a small state — mapped over the wild."""

    def construct(self):
        self.play(FadeIn(self.title("The Signature in the Wild"), shift=0.3 * DOWN))

        opening = Text(
            "Two marks, both required: an exponential family of arrangements,",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        opening2 = caption("and a small state whose holders share every legal future")
        opening2.next_to(opening, DOWN, buff=0.18)
        self.play(FadeIn(opening), FadeIn(opening2))

        pairs = [
            ("edit distance", "state: a prefix pair — the Wagner–Fischer table"),
            ("routes on grids", "state: the junction you stand at"),
            ("hidden-state models", 'state: the state at frame t — "a dynamic'),
            ("", 'programming algorithm" (Graves, citing Rabiner)'),
            ("Pascal's rule", "state: the cell — queued back home in counting"),
        ]
        table = VGroup()
        y = 1.15
        for left, right in pairs:
            if left:
                left_m = Text(left, font_size=SMALL_SIZE, color=COOL).move_to([-3.8, y, 0])
                arrow = Arrow(
                    [-2.0, y, 0],
                    [-1.2, y, 0],
                    color=MUTED,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.25,
                )
                table.add(left_m, arrow)
            right_m = Text(right, font_size=SMALL_SIZE, color=GOOD).move_to([2.2, y, 0])
            on_frame(right_m)
            table.add(right_m)
            y -= 0.62
        for m in table:
            self.play(FadeIn(m), run_time=0.25)
        self.wait(0.8)

        # Horizon, use-case framing only — the wiki row's recorded anchors.
        self.play(FadeOut(VGroup(opening, opening2, table)))
        horizon = Text("And on this road specifically:", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        h1 = caption("the same grid, swept backward, is a second dynamic program —")
        h2 = caption("over suffixes; the recurrence's additions inherit log-space from")
        h3 = caption("the underflow cliff; and the trellis's constant column is the law")
        h4 = caption("of total probability, read over the frame's states")
        h1.move_to(1.2 * UP)
        h2.next_to(h1, DOWN, buff=0.15)
        h3.next_to(h2, DOWN, buff=0.15)
        h4.next_to(h3, DOWN, buff=0.15)
        self.play(FadeIn(horizon))
        self.play(FadeIn(h1), FadeIn(h2), FadeIn(h3), FadeIn(h4))
        takeaway = Text(
            "an exponential sum, a small state — solve each question once",
            font_size=24,
        ).move_to(1.5 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
