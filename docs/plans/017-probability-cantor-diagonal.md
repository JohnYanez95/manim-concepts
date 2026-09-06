# Plan 017: `probability/` — Cantor's diagonal, the interval is not a sequence

The maintainer's ask (2026-09-06): a series on Cantor's diagonalization
argument, in the language of Bertsekas & Tsitsiklis, *Introduction to
Probability*, 2nd ed., Chapter 1, Problem 4* (pp. 53–54): "Show that the
unit interval [0, 1] is uncountable, i.e., its elements cannot be arranged
in a sequence." Home: `probability/`, module `cantor_diagonal_manim.py`,
seven scenes — the topic's seventh series. It is the first series here
whose result is a *negative* claim, and its level 3 is a claim about the
repo's own grammar: "probability is area" was never a sum over points, and
this argument is why. Branch `feat/probability-cantor-diagonal`, cut from
`main` at ce317e5 (PR #18 merged, clean, level with origin).

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier + verifier addendum); design | Scene design written into the plan |
| 1 | Module stub in `probability/`, README seventh-series Scope clause + subsection + row 1 | `make check` |
| 2 | Seven scenes at draft; layout linter clean; frames verified by eye (inside transition windows too — the digit grid replaces rows in place) | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, Scope exclusions reworded, wiki graph + log (new node, edges, promises opened); ADR-008 step: `primitives/cantor-diagonal.tex`, `answers/cantor_diagonal.py`, `017.*` anchors, INDEX row, solve gate; welcome.gif at sixteen series (the three-rows-of-five layout needs a fourth row) | `make test` |
| 4 | Local CodeRabbit + connection-auditor, findings addressed; root README row | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p60 render |

## Checklist

- [x] Phase 0: pedagogy report + verifier report (anchors A–K) pinned
  below as digests; verifier addendum (anchors L–T, the exact on-screen
  objects) pinned — design finalized (seven scenes; decisions D1–D10);
  design approved by the maintainer 2026-09-06
- [x] Phase 1: module stub (`ArrangedInASequence` built in full — the
  simplest scene; module docstring listing all seven) + README
  seventh-series Scope clause, subsection and row 1; `make check` green
- [x] Phase 2: seven scenes at draft (7 files, distinct names; 36, 41,
  34, 47, 49, 39, 54 s). `_DigitTable` shared by scenes 4 and 5 (the
  diagonal boxed cell by cell, never a line). Linter: 63 findings on the
  first pass — the zigzag's "q = n" column heads wider than their cells
  (bare digits plus one axis letter now), the walk's polyline through
  every stamp (dropped: the stamps appearing in order are the walk), the
  {1, 2} rule on the first caption of scene 5, scene 6's heading on a
  column head, the cover rectangles grazing the point names in the
  closer — all fixed, linter clean on all seven. Width discipline: every
  caption trimmed to ≤ 76 characters and side-column captions to ≤ 30,
  by the CLAUDE.md budget, before the first render. Frames verified on
  12-frame contact sheets for all seven, plus scene 4's
  caption-replacement window (27–39 s: one caption, one boxed row at a
  time) and the closer's cover beat (names staggered so x₃, x₅, x₄
  read apart). Bug caught by the linter's dry run: the y′ row indexed
  the table's first row for column positions and that row is a digit
  shorter — columns now come from the table geometry
- [x] Phase 3: README complete (seven rows, all three levels; Scope's
  two exclusions reworded — the Cantor series says why the continuous
  road cannot be a point-sum, countable additivity stated once as
  Axiom 2; 44 plan-017 references unchecked for the maintainer's pass,
  titles kept under the 80-column rule with full author names in the
  descriptions); queue entries for the two promises opened
  (probability/ Ideas: length as a probability law — existence;
  algorithms/ Ideas: undecidability by the diagonal); wiki —
  `cantor-diagonal` node, four delivered edges (`counting-rules`,
  `independence`, `inclusion-exclusion`, `e-and-ln`), two promised
  rows, the outer-product grid's plan-017 stop, log entry with the
  branch note; **ADR-008 step**: `primitives/cantor-diagonal.tex`
  (seven sections retold from the scenes, nine problems),
  `answers/cantor_diagonal.py` (every answer by exact Fractions and
  integer long division, every rule asserted), seventeen `017.*`
  anchors (121 total), study INDEX row (no guide retrieves it — with
  inclusion–exclusion it seeds the counting-and-chance objective);
  **the independent solve gate passed 9/9** (a fresh-context solver
  given statements only reproduced every answer, including the
  re-run's y′ = 0.212111… and the zigzag's stamp 20 = 5/2); compiled
  standalone in guide and solutions modes (8 + 3 pages, every anchor
  spliced, every citation resolved); `sync_references` (252 entries,
  208 verified) and `build_anchors` committed in sync, both
  ctc-algorithm PDFs rebuilt; welcome re-rendered at sixteen series in
  four rows of four (434 KB, frame verified). `make test` green (285),
  `make check` green, `make study` green
- [ ] Phase 4
- [ ] Phase 5

## Phase 0 — research digests (ADR 007: digests, not transcripts)

### Source text (verifier anchor A, read verbatim)

The problem is in both editions with the same number and title, and its
solution is printed in the book (starred problems are "solved in the
text"; both posted solution manuals skip 1.3 and 1.4). 1st ed. (2002,
ISBN 1-886529-40-X): pp. 52–53, publisher's posted Chapter 1. 2nd ed.
(2008, ISBN 978-1-886529-23-6): pp. 53–54 — the running header "54 Sample
Space and Probability Chap. 1" in the maintainer's scan is the 2nd
edition. B&T's digit notation is $x_n = 0.a_n^1 a_n^2 a_n^3\cdots$ —
**subscript = which number, superscript = position** (the scenes keep
this). Their rule is only "1 or 2, chosen so that it is different from the
nth digit of $x_n$"; the instantiation used on screen — $d_n = 1$ unless
$a_n^n = 1$, then $d_n = 2$ — is ours (verifier flag 5).

### Pedagogy digest

- **Consensus ladder**: what "arranged in a sequence" means (Velleman's
  "listability": every element gets a finite position number; repeats
  allowed) → surprisingly large sets ARE listable (integers; pairs by
  anti-diagonals; fractions with duplicates skipped) → every point has a
  decimal expansion, the 0.5000…/0.4999… exception named, uniqueness
  asserted not proved (B&T's own "it can be shown") → the grid, the
  diagonal, the rule → y is on no row → the closing form.
- **Two camps on the object**: Cantor 1891, Velleman, Halmos, Abbott 1.6.4
  diagonalise two-symbol *sequences* (no representation issue) and reach
  the reals afterwards; B&T, Abbott 1.6.1, Martin, most intro courses
  diagonalise decimal rows with a digit rule avoiding 0 and 9. **The series
  follows B&T** (the maintainer's ask); the sequence form returns as the
  level-3 "same diagonal on subsets".
- **Closing form**: build y for an *arbitrary* list (direct — Velleman's
  positive restatement ∃y ∀n y ≠ xₙ; Bauer's proof-of-negation; Hodges'
  1998 catalogue of reductio taught badly), *then* read B&T's contradiction
  sentence as the caption. Both languages on screen, agreeing.
- **Devices that work**: Filippou's *diagonal-first* reveal (show the
  diagonal digits alone, build y, then reveal the rows and slide each up
  beside y with digit n glowing); Martin's off-diagonal selection ("one
  cell per row, at most one per column — any such selection works": the
  diagonal is bookkeeping, not geometry); the *re-run* (prepend y, run the
  rule again, y′ appears) as the counter to "just add it to the list";
  stacked lists with pairing arrows, never side-by-side sets (Tsamir &
  Tirosh 1999: side-by-side elicits part–whole, stacked elicits
  one-to-one); the ε/2ⁿ cover (the halving the `ChainsOfTrials` square
  already draws) making "a listed set has area 0" visible; the
  Kronecker/Cantor query game (Alon et al. 2023: digit n costs one look-up)
  against "the process never finishes".
- **Misconceptions and counters**: "add y to the list" → re-run; "never
  finishes" → y is defined by a rule, 1/3 = 0.333… is B&T's own unfinished
  example; "0.4999… = 0.5 breaks it" → two worries: duplicates on the list
  are harmless (put 1/2 on twice), and y equalling some xₙ under its
  *other* expansion is real — rules that can output 0 or 9 fail exactly so,
  the 1-or-2 rule makes y's expansion unique; "circular" → completeness is
  never used to build y; "the diagonal is a line" → off-diagonal selection;
  "finite tables: the new number is further down" → 10ᵏ rows vs k digits,
  infinitely row n and digit n pair off; "then ℚ is uncountable too" → y is
  off the list and nothing forces y rational (never say "infinitely many
  digits ⇒ irrational" — a popular solutions manual does, wrongly); never
  say "bigger infinity" — B&T's claim is "cannot be arranged in a
  sequence" and the repo has no cardinality to fake.
- **Pitfalls in good treatments**: "add 1 to each digit" (Martin; a
  published teaching animation's rule admits 0) fails on (0.0999…, 0.999…,
  …); binary flip fails on numbers (every row 0.0111…₂ = 1/2); Cantor's
  first proof (1874) is nested intervals, the diagonal is 1891 on m/w
  sequences; "halting problem" is not Turing's phrase; uncountable
  additivity is *undefined*, not false; the closer proves the uniform law
  *needs* uncountability, not that it exists (B&T's footnote is the
  boundary); the Cantor set is uncountable with area 0, so never let
  "uncountable ⇒ positive probability" be heard.
- **Level 3 ranked for this repo**: (a) probability needs area, not
  point-sums — the closer, a scene (P(point) = 0 from B&T Ex. 1.4's
  overflow, Axiom 2's countable clause verbatim with the word *sequence*
  boxed, the halving cover, "if [0,1] were a sequence its probability
  would be 0, not 1"); (b) Cantor's theorem as the same diagonal on a
  yes/no table — a scene; (c) Turing's diagonal — a caption, promised to
  `algorithms/`; (d) unnameable reals — a caption (Velleman ex. 7.2.11);
  (e) Russell — omitted.
- **Home**: `probability/`. The source is the probability text's chapter 1
  and its Example 1.5 *is* the repo's unit square; every scene grounds in
  furniture the viewer owns (the counting grid, the segment, the halving
  square); the Scope exclusions on densities and measure theory are
  respected, not breached — reworded to say why the road cannot be a
  point-sum. A `foundations/` topic would be honest taxonomy but a
  one-series shelf whose level-3 column still points at `probability/`;
  the precedent is `calculus/` housing e-and-ln by its payoff.
- **Key takeaway**: B&T's Axiom 2 is stated for a *sequence* of disjoint
  events, and Problem 4 says [0,1] cannot be arranged in a *sequence* —
  the same word. The closer boxes it.

### Verifier digest (anchors A–K; every on-screen number traces here or to the addendum)

- **A** Citation — above. Verbatim problem and solution captured.
- **B** Uniqueness: x ∈ [0,1] has two expansions iff x = k/10ᵐ, 0 < k < 10ᵐ
  (terminating): 0.d₁…dₘ000… and 0.d₁…(dₘ−1)999…. 0 has one expansion;
  **1 has one "0.digits" expansion, 0.999…** — writing "1.000…" would
  manufacture the second. The doubles are countable (a subset of ℚ; first
  twelve 1/10, 1/5, 3/10, 2/5, 1/2, 3/5, 7/10, 4/5, 9/10, 1/100, 1/50,
  3/100). Two-line proof: expansions agreeing before n, differing there by
  aₙ − bₙ ≥ 1, force aₙ − bₙ = 1, the a-tail all 0s, the b-tail all 9s
  (exhaustive check over all short prefixes and tails). B&T assert this
  ("it can be shown") without proof.
- **C** Digits in {1,2}: 0.111… = 1/9, 0.222… = 2/9 exactly; any such y
  has 1/9 ≤ y ≤ 2/9, strictly inside [0,1]. Rule: dₙ = 1 if aₙⁿ ≠ 1, else 2.
- **D** y ≠ xₙ as numbers even if xₙ has two expansions: if y = xₙ, the
  listed expansion of xₙ is an expansion of y; y has only one; so they
  agree at digit n; but dₙ ≠ aₙⁿ. The argument needs y's uniqueness only,
  never xₙ's — exactly why B&T's "Note that y has a unique decimal
  expansion" precedes "The number y differs from each xₙ".
- **E** Binary flip fails on numbers: x₁ = 0.1000…₂ = 1/2, xₙ = 0 for n ≥ 2;
  diagonal 1, 0, 0, …; flipped y = 0.0111…₂ = 1/2 = x₁. Fixes: B&T's two
  interior digits (Sipser p. 205: "never selecting the digits 0 or 9"), or
  Cantor's own setting — sequences, not numbers.
- **F** Expansions, truncated, two independent routes agreeing to 12
  digits: π−3 = 0.141592653589, 1/2 = 0.500000000000, 1/3 =
  0.333333333333, √2−1 = 0.414213562373, 1/e = 0.367879441171, e−2 =
  0.718281828459, ln 2 = 0.693147180559, φ−1 = 0.618033988749, 1/7 =
  0.142857142857. Six-row list (π−3, 1/2, 1/3, √2−1, 1/e, e−2): diagonal
  1, 0, 3, 2, 7, 1 → y = 0.211112… (both branches fire, at 1 and 6). Flag
  7: a finite list determines only the first digits of y; the "…" must be
  explained, not filled.
- **G** Countable precedents: ℤ from n ≥ 1 by n/2 (even), −(n−1)/2 (odd)
  → 0, 1, −1, 2, −2, …; Cantor pairing on ℕ₀ bijective, walk (0,0), (1,0),
  (0,1), (2,0), (1,1), (0,2), (3,0), …; ℚ∩(0,1) by denominator: 1/2, 1/3,
  2/3, 1/4, 3/4, 1/5, …; Calkin–Wilf 1, 1/2, 2, 1/3, 3/2, 2/3, 3, … (≠
  Stern–Brocot order).
- **H** History: 1874, "Ueber eine Eigenschaft des Inbegriffs aller
  reellen algebraischen Zahlen", Crelle 77, 258–262 — nested intervals
  (method per Wikipedia/MacTutor, paper not read); 1891, "Ueber eine
  elementare Frage der Mannigfaltigkeitslehre", Jahresbericht der DMV 1,
  pp. 75–78 (EuDML says 72–78 — keep pages off screen) — sequences of two
  symbols m and w, "b_ν … von a_{ν,ν} verschieden", "does not depend on
  considering the irrational numbers". Who first cast it in decimals: not
  verified — do not attribute.
- **I** The probability closer is in B&T themselves: p. 13 footnote (1st
  ed.), verbatim — "the legitimacy of using length as a probability law
  hinges on the fact that the unit interval has an uncountably infinite
  number of elements. Indeed, if the unit interval had a countable number
  of elements, with each element having zero probability, the additivity
  axiom would imply that the whole interval has zero probability, which
  would contradict the normalization axiom." Example 1.4 gives P(point) =
  0 ("events with a sufficiently large number of elements would have
  probability larger than 1"). **Axioms (p. 9 box): 1 Nonnegativity; 2
  Additivity, whose second clause is the countable form for "a sequence of
  disjoint events"; 3 Normalization.** (My brief had said Axiom 3 —
  wrong.)
- **J** Cantor's theorem: D = {s : s ∉ f(s)}; D = f(t) gives t ∈ D ⇔ t ∉ D.
  The 1891 paper's second half is this in indicator form, g(x) = 1 −
  φ(x,x). Turing 1936/37 (Proc. LMS (2) 42, 230–265), §8 "Application of
  the diagonal process" — "halting problem" is a later name; cite Sipser
  3rd ed. Thm 4.11 (A_TM undecidable — "D rejects ⟨D⟩ exactly when D
  accepts ⟨D⟩"), Thm 4.17 (ℝ uncountable, the 0/9 caveat), Thm 5.1
  (HALT_TM).
- **K** Re-run on the six-row list: prepend y → diagonal 2, 4, 0, 3, 1, 9,
  8 → y′ = 0.1111211… ≠ y (d′₁ = 3 − d₁ always), off the new list too.
- **Flags kept live**: 1 (digit index orientation), 3 (never write
  1.000…), 5 (the rule is ours), 6 (binary flip only on sequences), 7 (a
  finite list fixes finitely many digits of y), 13 (Axiom 2 is
  additivity), 15 (halting is Sipser's name, not Turing's), 16 (no first
  author for the decimal form).

### Verifier addendum (anchors L–T; no discrepancies against the design)

- **L** The seven-row list, digits truncated (8 shown; 12 held): π−3
  0.14159265, 1/2 0.50000000, 1/3 0.33333333, √2−1 0.41421356, 1/e
  0.36787944, e−2 0.71828182, 1/2 as 0.49999999 (value checked: 4/10 +
  (9/100)/(1 − 1/10) = 1/2). Diagonal aₙⁿ = **1, 0, 3, 2, 7, 1, 9**; y
  digits **2, 1, 1, 1, 1, 2, 1** (y = 0.2111121…); the "= 1 → 2" branch
  fires at positions 1 and 6, the other at 2, 3, 4, 5, 7; y differs from
  row n at digit n for all seven; all digits in {1,2} so 1/9 ≤ y ≤ 2/9 —
  and rows 2 and 7 are both 1/2 ∉ [1/9, 2/9], so the 0.5000…/0.4999… trap
  visibly does not bite.
- **M** The re-run: y prepended (only d₁…d₇ known — the row ends in "…"),
  rows shifted to 2–8. New diagonal **2, 4, 0, 3, 1, 9, 8, 9** → y′ =
  **1, 1, 1, 1, 2, 1, 1, 1**; d′₁ = 3 − d₁ always, so y′ ≠ y at digit 1
  unconditionally; y′ off every shifted row at its own position; y's
  unknown tail is never consulted (all eight digits of y′ determined).
- **N** "+1 mod 10" failure: x₁ = 0.0999… = 1/10, xₙ = 0.999… = 1 (n ≥ 2);
  diagonal 0, 9, 9, … → y = 0.1000… = 1/10 = x₁ exactly. 1 ∈ [0,1] is
  written 0.999… under the "0.digits" convention.
- **O** Zigzag stamps, anti-diagonal order starting at the top row:
  stamp(p,q) = (s−2)(s−1)/2 + p with s = p+q. 5×5: row 1 = 1 2 4 7 11;
  row 2 = 3 5 8 12 17; row 3 = 6 9 13 18 24; row 4 = 10 14 19 25 32;
  row 5 = 15 20 26 33 41. Cells with p+q ≤ 6: 15. Fractions p/q in walk
  order, first 15 stamps: kept 1/1[1], 1/2[2], 2/1[3], 1/3[4], 3/1[6],
  1/4[7], 2/3[8], 3/2[9], 4/1[10], 1/5[11], 5/1[15] (eleven); skipped
  2/2[5], 2/4[12], 3/3[13], 4/2[14] (four). Every positive rational
  appears exactly once in the kept walk (one lowest-terms cell each).
  Flag 1: the 12th kept fraction 1/6 has stamp 16 = cell (1,6), outside a
  5×5 window — **scene 2 stamps the 15 cells with p+q ≤ 6 and stops at
  eleven kept**.
- **P** Integers under the naturals: g(n) = n/2 (even), −(n−1)/2 (odd);
  (1,0), (2,1), (3,−1), (4,2), (5,−2), (6,3), (7,−3), (8,4), (9,−4),
  (10,5); bijective onto a range, inverse z > 0 → 2z, z ≤ 0 → 1 − 2z.
- **Q** Martin's example verbatim (p. 3): S = {1,2,3,4}, f(1) = {1,3},
  f(2) = {1,3,4}, f(3) = {}, f(4) = {2,4}, and his set is named **X** =
  {2,3}. Table (m rows, n columns, yes iff n ∈ f(m)): yes no yes no /
  yes no yes yes / no no no no / no yes no yes; diagonal yes, no, no,
  yes; X = {2,3} on no row, witnessed at the diagonal cell each time;
  |𝒫(S)| = 16 vs 4, at most 4 subsets hit. Martin says "1895" — the
  date never comes from this handout.
- **R** Point-mass overflow: p = 3/20, 1/p = 20/3, N = 7 is the least N
  with Np > 1: 21/20 = 1.05. Halving cover partial sums ε(1 − 2⁻ᵏ): for
  ε = 1/10 → 1/20, 3/40, 7/80, 3/32, 31/320, 63/640 (0.05, 0.075, 0.0875,
  0.09375, 0.096875, 0.0984375), limit 1/10.
- **S** B&T 1st ed. Ch1.pdf, printed page = PDF page − 10, read from the
  rendered pages. Axioms box (p. 9) verbatim, Axiom 2's second clause:
  "More generally, if the sample space has an infinite number of elements
  and A₁, A₂, … is a sequence of disjoint events, then the probability of
  their union satisfies P(A₁ ∪ A₂ ∪ ···) = P(A₁) + P(A₂) + ···." Example
  1.4 (pp. 12–13) verbatim: "…what is the probability of the event
  consisting of a single element? It cannot be positive, because then,
  using the additivity axiom, it would follow that events with a
  sufficiently large number of elements would have probability larger
  than 1. Therefore, the probability of any event that consists of a
  single element must be 0. In this example, it makes sense to assign
  probability b − a to any subinterval [a, b] of [0, 1]…". Footnote †
  (p. 13) verbatim — the closer's sentence, already under I; its first
  half: "The 'length' of a subset S of [0, 1] is the integral ∫_S dt …
  For unusual sets, this integral may not be well defined mathematically,
  but such issues belong to a more advanced treatment of the subject."
  Not checked word-for-word against the 2nd edition (flag 7).
- **Flags kept live**: 1 (5×5 window — applied above), 2 (the prepended
  row ends in "…"), 3 (no dates from Martin), 4 (ℕ⁺ in scenes 1–2, one
  convention per scene), 6 (Martin's X, our D — say so if quoted), 7
  (1st-edition quotes; the 2nd edition's wording assumed identical, the
  README cites both).

## Scene design (seven scenes, `probability/cantor_diagonal_manim.py`)

Each scene carries its own title, as every series here does. Levels marked.
Every number below is an anchor reference (A–K in the verifier digest, L–T in
the addendum).

1. **`ArrangedInASequence`** (L1, ~40 s). Six `token`s numbered 1..6 (the
   combinatorics counting furniture) become a row that does not end; the
   claim chip: "arranged in a sequence = every element gets a finite
   position number" (repeats allowed — said). Under the naturals, the
   integers stacked with pairing arrows 1↔0, 2↔1, 3↔−1, 4↔2, 5↔−2 (P),
   one caption: "a list can always take one more" (Hilbert's n → n+1) —
   so the argument to come is not about running out of room. Points
   backward: `MultiplicativeRule`'s counting.
2. **`TheZigzag`** (L1, ~50 s). The counting grid (rows p, columns q)
   grown open at the right and bottom; the 15 cells with p+q ≤ 6 stamped
   1, 2, 3, … 15 along anti-diagonals (O); then each cell relabelled p/q,
   the four non-reduced ones (2/2, 2/4, 3/3, 4/2) tinted `MUTED` and
   skipped, eleven kept — "skipping never breaks a list". Beat: pairs and
   fractions are sequences. The surprise of scene 4 is earned here, before
   it is broken.
3. **`EveryPointHasDigits`** (L1, ~40 s). The unit segment cut into tenths,
   a landing point (probability furniture), its tenth read as a digit,
   then hundredths inside that tenth — the digits are the address. B&T's
   1/3 = 0.333…. The exception, drawn: 3 × 0.333… = 0.999… and 3 × 1/3 =
   1 (B: 0.999… = 1), so 0.5000… and 0.4999… are two rows for one point;
   caption in B&T's words — "this is the only kind of exception". Beat:
   every point is a row of digits; a few points own two rows.
4. **`TheDiagonalRule`** (L2, ~60 s, the centre). The grid of seven rows
   (L): π−3, 1/2 as 0.5000…, 1/3, √2−1, 1/e, e−2, 1/2 as 0.4999… — eight
   digit columns, "…" on both axes, digits at ≥ SMALL_SIZE, the diagonal
   cell of each row boxed `ACCENT`, never a drawn line. **Diagonal-first**:
   the seven diagonal digits alone, the rule stated as `MathTex`
   ($d_n = 1$ unless $a_n^n = 1$, then $2$), y assembled beneath; then the
   rows revealed and each slid up beside y with digit n glowing `WARM` —
   seven times. Closing beat: Martin's off-diagonal selection for one
   hold (one cell per row, at most one per column, "any such selection
   works — the diagonal is bookkeeping"). Beat: y differs from row n at
   digit n, for every n, by the rule; the rows beyond the screen follow
   the same rule (flag 7 said on screen).
5. **`WhyOneOrTwo`** (L2, ~60 s, the objections). Three beats, each a
   short list. (i) The "+1" rule on (0.0999…, 0.999…, 0.999…, …) yields
   0.1000… = x₁ (N, `WARM`): different digits, same number — a rule that
   can write 0 or 9 fails; the binary flip on (0.0111…₂, …) lands on the
   row (E). (ii) The 1-or-2 rule: no 0, no 9, so y owns one row (B, D) —
   "different digit ⇒ different number" (`GOOD`); and the duplicate 1/2 on
   scene 4's list was harmless. (iii) The re-run (M): y prepended, the
   rule run again, y′ ≠ y at digit 1 and off the new list — "the claim was
   never *this* list misses y; it is *every* list misses something".
   Close: the direct caption ("for any sequence, the rule finds a point not
   on it") over B&T's own sentence ("the sequence does not exhaust the
   elements of [0, 1], contrary to what was assumed").
6. **`TheSameDiagonalTwice`** (L3, ~40 s). Cantor's 1891 rows as a still:
   three sequences of m and w, b_ν ≠ a_{ν,ν} — two symbols, no numbers
   (H). Then the yes/no table for S = {1,2,3,4} and Martin's f (Q): entry
   (m, n) = "is n in f(m)?", the diagonal boxed, the bottom row D its
   flip, D = {2,3} on no row; 4 of 16 subsets hit at most. Beat: the same
   picture with different objects — no list of subsets of a set is
   complete; captions: Turing's diagonal on the computable sequences
   (promised to `algorithms/`), the unnameable reals (phrases are a
   sequence, points are not).
7. **`AreaNotSums`** (L3, ~60 s, the closer). `ProbabilityAsArea`'s unit
   segment. A single point given probability p = 0.15: seven equal bars
   stack past 1 (R, `WARM`) — so P(point) = 0 (B&T Ex. 1.4, S). Axiom 2's
   second clause on screen verbatim with the word **sequence** boxed
   `ACCENT`. The halving cover: intervals ε/2, ε/4, ε/8, … over listed
   points, total ε (R; the `ChainsOfTrials` halving) — a listed set has
   area 0. Then: "if [0, 1] were a sequence, its probability would be
   0 + 0 + ··· = 0, not 1" — B&T's footnote as the caption (I). Beat: the
   additivity axiom is stated for sequences; [0, 1] is not one; that is
   why "probability is area" was never a sum over points, and why the
   picture survives on the interval. Guards said on screen: this is
   consistency, not existence (Lebesgue is the "more advanced treatment");
   uncountable does not mean positive area (the Cantor set).

## Decisions (made at design time)

1. **Home `probability/`, seventh series** — see the pedagogy digest. The
   Scope exclusions are reworded, not removed: "Continuous distributions
   and densities — the road not taken until integration exists; the Cantor
   series says why that road cannot be a sum over points", and
   "Measure-theoretic formality … countable additivity is *stated* as
   B&T's axiom, which the earlier series used silently".
2. **B&T's language throughout**: "arranged in a sequence" is the whole of
   level 1; "uncountable" is B&T's gloss for it; "bigger infinity",
   cardinals and bijection-as-concept never appear (no cardinality is
   built here, so none is faked).
3. **Decimal rows, the 1-or-2 rule, our instantiation** (dₙ = 1 unless
   aₙⁿ = 1). B&T's digit notation kept (subscript = which number).
4. **Direct then contradiction**: y is built for an arbitrary list; B&T's
   contradiction sentence closes scene 5 as the caption. Both on screen.
5. **The list carries its own objection**: 1/2 appears twice, as 0.5000…
   and 0.4999…, so "duplicates" and "the other expansion" are met on the
   grid, not in prose. The rows are constants the repo has already shown
   (1/e and e−2 from the e-and-ln and matching series) plus π−3 and √2−1.
6. **Diagonal cells are boxed, never a line**, and the off-diagonal
   selection is shown once — the picture is a claim, and the claim is
   "one cell per row", not "a diagonal".
7. **Level 3 is two scenes**: Cantor's theorem (the same diagonal, honest
   and drawable) and the probability closer (the repo's own grammar). The
   closer is last because it lands in this topic.
8. **Turing is a promise, not a beat**: one caption in scene 6, a
   promised wiki edge to `algorithms/` ("the diagonal on computable
   sequences"); "halting problem" named only with Sipser as the source.
9. **History off screen except the 1891 still**: dates are captions
   ("Cantor, 1891 — two symbols, no decimals"); the 1874 nested-interval
   proof is a README note; no first-decimal-author is claimed.
10. **Welcome at sixteen**: four rows of four (the three-rows-of-five
    layout was already at the frame edge at fifteen). Name: "Cantor".

## What the series opens (to record in the wiki at phase 3)

- Promised: `algorithms/` — Turing's diagonal / undecidability (scene 6
  caption). Promised: the integration series — Lebesgue's uniform law as
  the "more advanced treatment" (scene 7 guard). Delivered edges:
  `counting-rules` (the grid zigzagged), `independence` (the unit
  segment/square as the sample space; the halving cover on
  `ChainsOfTrials`' square), `inclusion-exclusion` (finite additivity
  named as the finite case of Axiom 2), `e-and-ln` (1/e and e−2 as rows).
