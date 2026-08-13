# Algorithms

## Scope

The reorganisation moves that make impossible computations routine —
beginning with dynamic programming: the recursion tree that asks the
same question over and over, folded into a small table that asks each
question once. The series names the move the repo's trellis scenes
performed unnamed, grounds it in pictures the viewer already owns (the
counting series' lattice, the alignment series' trellis), and prices
its boundary instead of declaring it.

Deliberately **not** covered here:

- **The optimization-DP zoo.** No knapsack, rod cutting, longest
  increasing subsequence, or coin change; edit distance and
  routes on grids are *named* in the closer as signature instances,
  never worked. This series teaches counting/sum DP — the kind the
  repo's own road runs on — with Demaine's license that counting
  recurrences are "almost trivially correct".
- **"Optimal substructure" as vocabulary.** Replaced throughout by
  the honest counting condition: the stored answer is all the future
  needs (arrangements agreeing on the state have interchangeable
  futures). The optimization-specific machinery — greedy-vs-DP,
  exchange arguments — stays out.
- **Code and implementation.** Memoization vs tabulation appears
  only as one table in two orders (asked-when-needed vs filled
  deliberately); no pseudocode, no space-saving tricks, no
  asymptotics beyond cell counting.
- **The control-theory branch of the name.** Bellman equations,
  MDPs, policy and value iteration, reinforcement learning.
- **Beam search and approximate reorganisations** — queued in
  [`deep_learning/`](../deep_learning/README.md) Ideas, not here.

## Concepts

### dynamic_programming_manim.py

Watch in order. The first two scenes build the move on neutral ground
(a recursion that repeats itself, then the fold that stops it); the
middle two recognize it in pictures the viewer already owns; the last
two price its boundary and map its signature. Every number traces to
[plan 013](../docs/plans/013-algorithms-dp.md)'s verification pass —
and the series itself was built from its own study-guide chapter, ADR
008's pipeline running book-to-screen.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `TheQuestionAskedTwice` | $\text{calls}(n) = 2F(n{+}1) - 1$ | Computed exactly as written, a correct recursion can ask the same question over and over — 177 calls to settle 11 distinct questions at $n = 10$. | The call tree drawn at $n = 5$ carries duplicate labels the eye can count (F3 under two parents, F2 under three); the repeats compound at the sequence's own rate — F8 asked 2×, F7 3×, F6 5× — and the closed form, checked against an instrumented count at every $n \le 12$, prices the whole tree. | The diagnosis step wherever a natural recursion is correct but slow: the defect is never the answer, it is the asking. |
| 2 | `WriteTheAnswersDown` | $F(n) = F(n{-}1) + F(n{-}2)$, each asked once | Store each answer at its first computation and the tree folds — 15 calls become 6 computations, 177 become 11. | First visits write into the memo row; every later copy greys into a lookup; and the move earns its name with its two conditions stated where the fold proves them — the questions repeat, and the stored number is all the future needs. | The naming: dynamic programming (Bellman's word, his naming story told as his story), memo functions (Michie, 1968) — the habit to reach for exactly when subproblems repeat and each stored answer carries everything the future needs. |
| 3 | `TheLatticeRecounted` | $R(i,j) = R(i{-}1,j) + R(i,j{-}1)$ | The counting series' 15 routes, recounted by additions alone — never listing one. | Each node sums routes from the left and from below (the arrows match the fill order); two routes converge on a node and leave as one number — the overlap condition drawn; the corner lands on $\binom{6}{2} = 15$, the counting series' own answer. | Pascal's rule as motion — the block-walking reading of every binomial coefficient, and the smallest complete instance of an exponential list reorganised into a table. |
| 4 | `TheTrellisWasAMemo` | $\alpha_t(s)$ — a stored answer | The forward trellis was dynamic programming all along. | The mini trellis (ε A ε) lands 3 + 3 = 6 of 8 raw paths with the waist cell stored once; the alignment series' 81/15/20 grid re-read; and the scale card — 10,100 cells against a 41-digit list (≈ 2.013 × 10⁴⁰, thirty-six orders of magnitude). Memoized or tabulated: one table, two orders. | The two-stories bridge: Fibonacci stops recomputing, the trellis never computed a path at all — in both, one stored answer serves many parents. |
| 5 | `WhatBreaksIt` | — | Dynamic programming pays exactly for how much past the future needs. | Nothing repeats → the subproblem graph is a tree and the memo is filing, not speedup (the shape is the verdict — the DAG's shared children are the reuse); the future needs more → cells fatten (101 → 10,201 states, ≈ 1.02 million cells, still polynomial) until "remember everything" makes the table the exponential list it was meant to replace. | Diagnosing whether the move applies — and pricing the state — before designing any table. |
| 6 | `TheSignatureInTheWild` | — | The two-part signature, both marks required: an exponential family of arrangements, and a small state whose holders share every legal future. | Mapped over the wild: edit distance (state: a prefix pair — the Wagner–Fischer table), routes on grids (the junction), hidden-state models ("a dynamic programming algorithm" — Graves, citing Rabiner), Pascal's rule (queued back home in counting). | The horizon, use-case framing only: the same grid swept backward is a second dynamic program; the recurrence's additions inherit log-space; the constant column is the law of total probability over the frame's states. |

Renders are numbered to match:
`01_TheQuestionAskedTwice.mp4` … `06_TheSignatureInTheWild.mp4`.

Render them:

```bash
uv run python algorithms/dynamic_programming_manim.py             # all six, 1080p60
uv run python algorithms/dynamic_programming_manim.py --list
uv run python algorithms/dynamic_programming_manim.py -s TheLatticeRecounted -q draft
```

See the [root README](../README.md) for the full flag list.

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below came out of the plan-013 research pass and started
unchecked; all seventeen were then verified by the maintainer, who
directed the ticks (2026-08-12) — including the two Secretary-of-Defense
biographies, kept deliberately: they are the date evidence behind scene
2's "his retelling, not history" hedge. Future entries start unchecked
until a human does the same.

- [x] [Jeff Erickson, *Algorithms*, ch. 3 "Dynamic Programming"](https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf)
      — the recursion-first sequence this series follows; the
      memo-trimmed tree figure; "not about filling in tables — smart
      recursion"; the 2F(n+1) − 1 call count derived independently.
- [x] [Erik Demaine, Jason Ku and Justin Solomon, MIT 6.006 S20 lecture 15](https://live.ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/9eb3e9a51a7b5b60b0f67c2277f8b0ee_MIT6_006S20_lec15.pdf)
      — SRTBOT; the star/chain/tree/DAG recursion-shape table; DP as
      in-degree > 1; counting recurrences "almost trivially correct".
- [x] [MIT OpenCourseWare, 6.006 lecture 15 video page](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-15-dynamic-programming-part-1-srtbot-fib-dags-bowling/)
      — the lecture the notes accompany.
- [x] [Stuart Dreyfus, "Richard Bellman on the Birth of Dynamic Programming" (2002)](https://pubsonline.informs.org/doi/10.1287/opre.50.1.48.17791)
      — Operations Research 50(1):48–51; Bellman's naming story
      verbatim from *Eye of the Hurricane* (1984), p. 159 — told on
      screen only as Bellman's story (see the plan's chronology).
- [x] [Richard Bellman, "On the Theory of Dynamic Programming" (PNAS, 1952)](https://www.pnas.org/doi/10.1073/pnas.38.8.716)
      — PNAS 38(8):716–719, communicated by J. von Neumann, June 5,
      1952: the term in print before Wilson's tenure — the primary
      chronology that keeps the naming story hedged.
- [x] [Richard Bellman, *The Theory of Dynamic Programming* (RAND P-550, 1954)](https://www.rand.org/content/dam/rand/pubs/papers/2008/P550.pdf)
      — the AMS Laramie address; the principle of optimality verbatim
      (p. 4, the plural wording this repo displays), and "a general
      prescription… in terms of the current state of the system".
- [x] [Historical Office, OSD — Charles E. Wilson](https://history.defense.gov/Multimedia/Biographies/Article-View/Article/571268/charles-e-wilson/)
      — Secretary of Defense Jan 28, 1953 – Oct 8, 1957: the date
      that contradicts the anecdote.
- [x] [Miller Center — George C. Marshall as Secretary of Defense](https://millercenter.org/president/truman/essays/marshall-1950-secretary-of-defense)
      — Fall 1950's actual Secretary of Defense.
- [x] [Donald Michie, "'Memo' Functions and Machine Learning" (Nature, 1968)](https://www.nature.com/articles/218019a0)
      — Nature 218:19–22; memo functions coined ("memoization" is
      not verbatim in the verified text and stays off screen).
- [x] [Robert A. Wagner and Michael J. Fischer (JACM, 1974)](https://dl.acm.org/doi/10.1145/321796.321811)
      — "The String-to-String Correction Problem": the standard
      edit-distance table the closer names (no "invented" claims; the
      metric is Levenshtein's).
- [x] [Michael Shindler et al., the DP-misconceptions replication (2022)](https://ics.uci.edu/~mikes/papers/Student_Misconceptions_Dynamic_Programming.pdf)
      — "Student Misconceptions of Dynamic Programming: A Replication
      Study": the M1–M12 codes this series designs against.
- [x] [Zehra, Ramanathan, Zhang and Zingaro (SIGCSE '18)](https://dl.acm.org/doi/abs/10.1145/3159450.3159528)
      — "Student Misconceptions of Dynamic Programming": the original
      study the replication confirms.
- [x] [Avik Das, "A Graphical Introduction to Dynamic Programming"](https://avikdas.com/2019/04/15/a-graphical-introduction-to-dynamic-programming.html)
      — the call-tree → DAG → table progression.
- [x] [VisuAlgo — Recursion Tree and DAG (DP)](https://visualgo.net/en/recursion)
      — interactive side-by-side of the naive tree and merged DAG.
- [x] [Reducible, "5 Simple Steps for Solving Dynamic Programming Problems"](https://www.youtube.com/watch?v=aPQY__2H3tE)
      — the strongest animated DP treatment surveyed (steps
      paraphrased in the research pass, not quoted).
- [x] [Oscar Levin, *Discrete Mathematics*, §3.1 Pascal's triangle](https://math.oscarlevin.com/discrete-book/sec_counting-pascal.html)
      — the left-plus-below addition rule taught as counting.
- [x] [Wikipedia — Block walking](https://en.wikipedia.org/wiki/Block_walking)
      — the lattice-route reading of Pascal's entries.

## Ideas not yet built

- Beam search as approximate reorganisation — lives in
  [`deep_learning/`](../deep_learning/README.md) Ideas; this topic
  hosts the exact-DP prerequisite it leans on.
- Divide and conquer as its own concept — the tree-shaped sibling
  scene 5 contrasts in one panel; a full treatment (merge sort's
  recurrence, the master theorem's pictures) would slot here.
- Edit distance worked in full — the closer names the Wagner–Fischer
  table; a dedicated scene would earn the KITTEN→SITTING grid the
  verifier has already pinned.
