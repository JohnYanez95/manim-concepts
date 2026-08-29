# Plan 016: `probability/` — inclusion–exclusion, two sets to n

The maintainer's ask (2026-08-29): a bridge on the inclusion–exclusion
property of probability, climbing 2 sets → 3 sets → 4 sets → n sets.
Home: `probability/`, module `inclusion_exclusion_manim.py`, seven
scenes — the topic's sixth series. It closes a standing promise: wiki
row 79's inclusion–exclusion strand (`counting-rules` → promised, via
`combinatorics/README.md` Ideas "two and three overlapping sets") is
delivered from the probability side — level 1 opens on countable cells
(the counting form) before the area form — and the seed audit's
recorded "Bernstein ↔ inclusion–exclusion device reuse" acts here.
Branch `feat/probability-inclusion-exclusion`, cut from `main` at
18d4cbb (clean, level with origin).

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier + addendum); design | Scene design written into the plan |
| 1 | Module stub in `probability/`, README sixth-series scope + subsection + row 1 | `make check` |
| 2 | Seven scenes at draft; layout linter clean; frames verified by eye (inside transition windows too) | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, combinatorics bullet re-homed, wiki graph + log; ADR-008 step: a NEW authored primitive (`inclusion-exclusion.tex`, answer script, `016.*` anchors, INDEX row, solve gate); welcome.gif at fifteen series | `make test` |
| 4 | Local CodeRabbit + connection-auditor, findings addressed; root README | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p60 render |

## Checklist

- [x] Phase 0: pedagogy report + verifier report (anchors A–K) +
  verifier addendum (anchors L–R) pinned below as digests; two
  repo-touchpoint maps consulted (file set, primitive shape, solve
  gate, wiki row shapes, welcome.gif recipe); design finalized
  (seven scenes; decisions D1–D10)
- [x] Phase 1: module stub (`TwoSetsOneOverlap` skeleton, module
  docstring listing all seven, `_die_strip`/`_tint` copied locally) +
  README sixth-series Scope clause, subsection and row 1; `make check`
  green (259 tests)
- [ ] Phase 2
- [ ] Phase 3
- [ ] Phase 4
- [ ] Phase 5

## Decisions (made at design time)

1. Home `probability/`, seven scenes; the counting promise re-homed:
   `combinatorics/README.md`'s Ideas bullet struck with a pointer
   ("delivered by `probability/`'s inclusion–exclusion series —
   counting form on the die strip first, then area"), and
   `probability/README.md` Scope's "Counting itself" exclusion gains
   the hand-over clause (cells are counted, the rule taught is area).
2. Level 2 is the **per-cell ledger**, not Venn bookkeeping. P = area
   in this repo, so Venn circles are not area-true (a 1/36 overlap
   drawn as a fat lens is a false claim under "the picture is a
   claim"). Every tally runs on grid cells stamped with a running
   count as terms arrive; circles appear exactly once (scene 3) as
   the schematic that breaks at four — counted to 14, retired with
   Venn's own 1881 sentence.
3. The n-set argument is "every point counted once" (Ross Prop. 4.4
   Remark 1) proved on screen by the **toggle pairing** S ↔ S △ {1}
   (White; Benjamin–Quinn): pairs cancel WARM, {1} survives GOOD. The
   binomial identity (1−1)^k = 0 is *not built* in this repo (the
   binomial theorem is queued in combinatorics), so it is a caption
   pointer, never "recalled".
4. Three-set example: the two-dice grid — A = first 6, B = second 6,
   C = sum ≥ 10 (union 12/36). Repo furniture, area-true, (6,6) in all
   three is the ledger's star cell (+3 −3 +1). Its empty A∩B-only
   region is shown honestly ("an empty region costs the formula
   nothing"). The verifier's every-region-non-empty candidate (1..30
   by 2, 3, 5: union 22/30, φ(30) = 8 survivors) is the closing
   scene's sieve pointer, not a scene.
5. Bernstein reuse uses the repo inset's numbers (two coins: A first
   H, B second H, C exactly one head — triple = 0, union 3/4), NOT the
   {1,2},{1,3},{1,4} form (triple 1/4, union 1). Two beats: the empty
   centre 3/2 − 3/4 + 0 = 3/4, and the license — the complement
   shortcut gives 7/8, error 1/8 = the product the true triple term
   is not.
6. Four sets = two examples sharing the coefficient row 4, 6, 4, 1:
   de Méré's four rolls (independent, every term a product, 671/1296)
   and four hats (dependent, 15/24 = 5/8, nine derangements listed).
   Showing only the independent one would teach the product form as
   the general one — both stay.
7. Numbers on screen: anchors A–R below, all by exact enumeration;
   the enumeration scripts become the committed answer script's
   assertions. Near-misses kept off screen as results: 1/3 is the
   OVERCOUNT in the two-dice two-set beat (11/36 true, scene 1) and
   the TRUE value in the three-set beat (12/36, scene 2) — each beat
   labels which, never a bare "1/3"; 0.37 / 0.368 are roundings (use
   0.3679 / 0.6321 or fractions); the toggle partial sums are shown in
   ONE convention (from j = 1: 4, −2, 2, 1 — never beside the j = 0
   form 1, −3, 3, −1, 0 under one label); "Bonferroni's inequality"
   also names P(EF) ≥ P(E)+P(F)−1 — not mixed in; Boole's bound on
   four hats is exactly 1 (honest, useless — said so); "1654" stays
   off screen (MathWorld names de Méré and Pascal, no year).
8. e is cited, not derived. The matching limit needs Σ(−1)^k/k! =
   e^{−1}, a series fact the repo has parked (Taylor). On-screen
   caption: e is `calculus/`'s compound-interest ceiling
   (`TheSplitYear`), 1/e already appeared as the binomial's
   zero-success limit (`TheBinomialColumns`), and the series is "a
   fact this repo has not built" — one promised wiki row (the
   exponential series) opens.
9. Attribution on screen: de Moivre 1718 (Problem XXV) for the
   matching problem, Montmort 1708/1713 for Treize. The general
   formula's "Da Silva 1854 / Sylvester 1883 / Poincaré 1896" lives
   in the README only — no single eponym on screen. Venn 1880/1881
   for the diagram and the four-ellipse fix; Grünbaum 1975 is FIVE
   ellipses and is not credited with four.
10. Study guide (ADR 008): a NEW authored primitive — the first since
    v1 (plans 013–015 graduated existing guide-first chapters), so the
    independent solve gate is owed and run (fresh-context solver,
    statements only, score recorded). No current guide retrieves it:
    `ctc-algorithm/manifest.tex` and its glue stay untouched (not on
    that road); a second guide objective is its own plan later.

Off-screen list: a four-circle "Venn" labelled with 16 regions; the
naive sums 1, 7/6, 12/36 presented as results; "Sylvester's formula"
/ "Poincaré's formula"; Grünbaum credited with four ellipses; the
{1,2},{1,3},{1,4} Bernstein numbers under the inset's name; any
claim that `calculus/` derived the exponential series; a Bonferroni
bound whose parity is mislabelled (one term upper, two lower, three
upper — Ross's phrasing); an "exact" rare-event value without the
independence assumption stated.

## Scene design

Colours: A = `palette(0)`, B = `palette(1)`, C = `palette(2)`, D =
`palette(3)` (categorical — N sets, no ranking); overcounted cells and
cancelled pairs WARM; the confirmed cell / survivor GOOD; the formula
being built ACCENT; scaffolding MUTED. Overlaps are translucent
overlays on top of a tint, never a second `set_fill` (the doubly
covered cell must visibly carry both colours — that is the point).
`_die_strip`/`_tint` copied module-locally (topic furniture, by the
conditional module's precedent); the 6×6 grid from
`independence_manim.py`'s `TheProductRule`; chips in a grid for
permutations (`CombinationRule`'s device); the question→arrow→verdict
layout for the close. Timings against manim defaults; the boxed
takeaway quartet closes every scene.

1. **`TwoSetsOneOverlap`** — L1: die strip, A = even {2,4,6}, B = at
   most 4 {1,2,3,4} (the `OneDieTwoEvents` pair); B's overlay shows
   {2,4} carrying both colours; |A∪B| = 3 + 4 − 2 = 5 — the counting
   form the combinatorics queue promised. L2: the naive 1/2 + 2/3 =
   7/6 > 1 alarm (WARM — a probability above 1 is an alarm the viewer
   cannot argue with); then the unit square: two bands, the overlap
   rectangle marked WARM once and removed; P(A∪B) = P(A) + P(B) −
   P(A∩B) = 5/6, boxed. L3: disjoint ⇒ the sum is exact ({1,2} vs
   {5,6}: 2/6 + 2/6 = 4/6; `NotMutualExclusivity` re-read — disjoint
   and independent are opposite ends of the overlap); independent ⇒
   the overlap is the product (P(A∩B) = 2/6 = (1/2)(2/3); shortcut
   1 − (1/2)(1/3) = 5/6; `TheProductRule` callback); "at least one"
   vs "exactly one" ({1,2,3,4,6} vs {1,3,6}: coefficient −1 vs −2 on
   the overlap, 5/6 vs 1/2). Closer on the two-dice grid: first 6 /
   second 6, 6/36 + 6/36 − 1/36 = 11/36; "12/36 is the overcount".
2. **`ThreeSetsOneLedger`** — L1: 6×6 grid, row 6 / column 6 / sum ≥
   10 tinted; count the union: 12 cells → 12/36. L2: the ledger —
   every cell stamped as terms arrive: +1 per set containing it (18
   stamps), −1 per pair (7), +1 for the triple (1); (6,6) reads 3 → 0
   → 1 ("after the subtractions it has vanished from a union it
   belongs to; the last term is the only one that knows about the
   centre" — say "add back", never "add"); every union cell ends at 1,
   every outside cell at 0; the empty A∩B-only region named as
   costing the formula nothing. Then Bernstein's 2×2 with the inset's
   events: 3/2 − 3/4 + 0 = 3/4, an empty centre a circle picture could
   not draw honestly. L3: the three-set formula boxed; the license
   beat — 1 − (1/2)³ = 7/8 ≠ 3/4, the error 1/8 is exactly the product
   the triple term is not: every pair term was a correct product, so
   "multiply the complements" is licensed by MUTUAL independence only
   (`ChainsOfTrials` quoted).
3. **`FourSetsNoPicture`** — L1: four circles, regions numbered to 14,
   "16 needed — two missing" (the two opposite-pairs-only regions,
   verified geometrically at build); Venn's sentence ("four circles
   cannot be so drawn as to intersect one another in the way
   required"); four ellipses as one still (16, Venn's own fix);
   circles retired — the grid stays, the ledger continues. L2: four
   hats — the 24 permutations as chips, the 9 derangements GOOD, 15
   with a match; terms 4·(1/4) − 6·(1/12) + 4·(1/24) − 1·(1/24) =
   15/24 = 5/8, each C(4,k)·(4−k)!/4!; de Méré's four rolls beside it:
   4·(1/6) − 6·(1/36) + 4·(1/216) − 1/1296 = 671/1296, every term a
   product; the shared coefficient row 4, 6, 4, 1 under the
   (1,4,6,4,1) columns the viewer met in `SortTheSquare`; any cell's
   ledger 4 − 6 + 4 − 1 = 1. L3: same coefficients, different p_k —
   the symmetric collapse Σ(−1)^{k+1} C(n,k) p_k is what makes n
   tractable; the complement 1 − (5/6)⁴ = 671/1296 gives de Méré in
   one line — independent events only.
4. **`EveryPointCountedOnce`** — L1: the n-set formula, Ross 4.4's
   compact form P(∪Aᵢ) = Σₖ (−1)^{k+1} Σ_{|S|=k} P(∩_{i∈S} Aᵢ); 2ⁿ − 1
   terms (1, 3, 7, 15). L2: a point in exactly k sets is counted
   C(k,1) − C(k,2) + C(k,3) − …; the nonempty subsets of {1..k} in two
   parity columns; the toggle pairing S ↔ S △ {1} greys each pair
   WARM, {1} survives GOOD — the alternating sum is 1 for every k
   (k = 3: three pairs; k = 4: seven pairs); the partial sums 4, −2,
   2, 1 shown as counts, not probabilities. L3: the symmetric form;
   captions: "(1−1)^k = 0 is the binomial theorem — queued in
   `combinatorics/`"; the indicator route 1 − ∏(1 − 1_A) with
   linearity (`SameOutcomesAdd`) as a one-line pointer.
5. **`TheMatchingLimit`** — L1: n hats returned at random,
   P(at least one match) = 1 − 1/2! + 1/3! − ⋯ ± 1/n!; the table
   n = 2..8 (1/2, 2/3, 5/8, 19/30, 91/144, 177/280, 3641/5760). L2:
   why the terms are 1/k!: C(n,k)(n−k)!/n! collapses; the partial
   sums oscillate and land — never monotone (above the limit at
   n = 3, below at n = 4; error bounded by the first omitted term).
   L3: 1 − 1/e ≈ 0.6321 with decision 8's caption; the two roads to
   1/e beside `TheBinomialColumns`' (1−1/n)ⁿ (0.3164 vs 0.375 at
   n = 4; 0.3436 vs 0.3679 at n = 8) — same limit, one road
   independent, one not; Montmort 1708 / de Moivre 1718 named; Ross's
   aside ("who would have guessed it doesn't go to 1?").
6. **`BracketsAndBounds`** — L1: stop the sum early — one term is an
   upper bound (Boole's inequality), two a lower, three an upper, and
   so on (Ross Remark 3's phrasing). L2: the two four-set ladders as
   bars bracketing the exact value (hats: 1, 1/2, 2/3, 5/8; rolls:
   2/3, 1/2, 14/27, 671/1296); why — a truncated ledger is a partial
   alternating row sum, ≥ 1 or ≤ 1 by parity (Benjamin–Quinn's
   partial-sum identity as a caption). L3: rare events — four at 0.01:
   bound 0.04 vs 0.0394 exact under independence (the union bound is
   nearly exact when events are rare); Boole's bound on four hats is
   exactly 1 (honest, useless); Bonferroni 1936 named.
7. **`WhenToUseIt`** — the mapping close: disjoint → add; independent
   → 1 − ∏(1 − pᵢ); dependent and symmetric → inclusion–exclusion
   with C(n,k); many rare events → the union bound; "exactly m of n" →
   Feller's sieve (pointer); 1..30 by 2, 3, 5 → 22 covered, 8
   survivors = φ(30) (pointer); Blitzstein & Hwang's "last resort"
   verdict as the closing caption.

## Pinned report: pedagogy researcher (digest — ADR 007)

Consensus climb in every standard text (Ross §2.4, Blitzstein & Hwang
1.6, Feller IV, Grinstead & Snell 3.1, Bóna ch. 7, MIT 18.05, Bristol
notes): two sets by cutting A∪B into disjoint pieces (B&H: the Venn
picture is "a useful intuition, but not a proof"); three sets by the
tally sentence ("added three times, subtracted three times, add it
back once"); n sets by one of four arguments — induction (Ross,
Bristol, Stanford 61DM: needs the distributive law at every step,
explains nothing about the signs), per-point counting (Ross Remark 1
"a noninductive argument", Feller, Haber, Wikipedia, Bóna — explains
the SHAPE, but every source imports Σ(−1)^k C(m,k) = 0 from the
binomial theorem), sign-reversing involution (White's Math 4707 notes,
Benjamin–Quinn's D.I.E.: toggle one element — no binomial theorem,
fully drawable as pairs cancelling), indicators 1 − ∏(1 − 1_A) with
expectation (B&H ch. 4; the binomial expansion in disguise). Repo
constraint (no binomial theorem built) forces per-point counting
proved by the toggle pairing; induction and indicators are captions.

The four-set hinge: Venn 1880 — "Beyond three terms circles fail us";
four circles give at most 14 regions (Euler: V = 12, E = 24, F = 14)
against 16 needed; Venn's own fix is four ellipses; Ruskey–Weston's
definition requires all 2ⁿ regions nonempty (fewer = an Euler
diagram); Cook: four curves is the practical legibility limit. The
sharper hinge for this repo: the picture does not FAIL at four
(ellipses work) — it was never area-true even at two; the grid stays
truthful at 2, 3, 4 and the ledger does the work from three on. The
best treatments show nothing visual at four: they go straight to
symmetric examples (matching; rolls) where every k-fold intersection
has the same probability and the formula collapses to
Σ(−1)^{k+1} C(n,k) p_k — the coefficients 4, 6, 4, 1 ARE the four-set
lesson.

Examples the texts use: Ross 5l (club, 43 members), 5m matching
(e^{−1} ≈ .3679), 5n couples (.6605); B&H 1.6.4 de Montmort with the
C(n,k) collapse and the closing advice ("try other tools before
turning to inclusion–exclusion as a last resort"); Grinstead & Snell
3.13 hat check with Table 3.7; Bóna derangements; combinatorics
courses use divisibility sieves. Recommendation adopted: die strip
(2 sets, counting first), two-dice grid (2 and 3 sets, area-true),
four hats + de Méré's rolls (4 sets, then n → 1/e); divisibility 1..30
as a pointer.

Level 3 on screen: Boole / the union bound as "stop after one term";
the Bonferroni ladder as alternating partial sums bracketing the
truth (Ross Remark 3 is the only text that states the whole ladder
before the examples); the complement shortcut for independent events
and its mutual-independence license (Bernstein); the matching limit.
Captions only: "exactly m of n" (Feller IV.3), Poisson approximation
of the match count, Euler's φ / sieves, the Bonferroni correction
(name), the "last resort" verdict.

Bernstein reuse, concretely: the inset's coins (A first H, B second H,
C exactly one head) give a three-set formula with an EMPTY centre
(3/2 − 3/4 + 0 = 3/4 — the region circles cannot honestly draw and a
grid can), and the license beat (1 − (1/2)³ = 7/8 ≠ 3/4; the error 1/8
is exactly the false product triple term while every pair term was a
correct product).

Visual devices: overlap counted twice on cells (overlay tint); the
per-cell ledger stamped term by term (no canonical figure exists —
descends from `SortTheSquare`'s stamps); the Pascal row as the
ledger's bill (2−1, 3−3+1, 4−6+4−1 under (1,2,1), (1,3,3,1),
(1,4,6,4,1)); the toggle pairing as two parity columns with pairs
greyed; four circles counted to 14 then four ellipses as one still;
the coefficient collapse under symmetry; the bracketing ladder as
bars; the two roads to 1/e side by side; the mapping close.

Misconceptions designed against: P(A or B) = P(A) + P(B) as default
(counter: make the sum exceed 1 before explaining); sign errors at
three sets (counter: the (6,6) ledger hits 0 — the cell has vanished
from a union it belongs to); mutually exclusive = independent (The
Mathematics Enthusiast 2009: 14/97 correct; counter: disjoint is when
the sum is EXACT, independent events always overlap by the product);
"at least one" heard as "exactly one" (counter: both regions drawn,
coefficient −1 vs −2); pairwise independence licensing the complement
product (Bernstein); the union bound "wrong" when it exceeds 1 (it is
a bound; on rare events within 1.5%); partial sums "converge"
monotonically (they overshoot, undershoot, land exactly); four
circles make a Venn diagram (count to 14); inclusion–exclusion as the
tool for every "at least one" (de Méré by complement in one line).

Technical pitfalls: Venn circles are not area-true; four-circle
diagrams labelled 16 are wrong; Bonferroni parity is routinely
mislabelled (a retrieved summary called the odd partial sum a lower
bound — use Ross's phrasing); empty Venn regions are legitimate and
the formula is unaffected; the per-point identity must be SHOWN or
pointed forward, never recalled; (1 − 1/n)ⁿ ≠ the derangement
probability at finite n — both → 1/e, do not conflate; a four-set
scene showing only independent rolls teaches the product form as
general; attribution — de Moivre 1718, Montmort 1708/1713, Boole,
Bonferroni 1936, Venn 1880 — never credit Venn with the identity or
its authors with the diagram; a listed set of derangements must be
verified (anchor P).

### Sources (for the topic README, `- [ ]`, authors as credited)

- John Venn, "On the Diagrammatic and Mechanical Representation of Propositions
  and Reasonings", Philosophical Magazine (5) 10(59), July 1880, 1–18,
  <https://www.tandfonline.com/doi/abs/10.1080/14786448008626877> — "Beyond
  three terms circles fail us"; the four-ellipse construction (paywalled;
  wording via Cook and Wikipedia).
- John D. Cook, "Limitations on Venn diagrams",
  <https://www.johndcook.com/blog/2024/09/28/limitations-on-venn-diagrams/> —
  quotes Venn 1880 on four circles; four curves as the practical legibility
  limit.
- Frank Ruskey and Mark Weston, "A Survey of Venn Diagrams: What is a Venn
  Diagram?" (EJC Dynamic Survey DS5),
  <https://www.combinatorics.org/files/Surveys/ds5/VennWhatEJC.html> — the
  formal definition (all 2ⁿ regions nonempty), Euler vs Venn diagrams, "4
  ellipses, originally found by Venn himself".
- Joseph K. Blitzstein and Jessica Hwang, Introduction to Probability, chs. 1–2
  excerpt,
  <https://law-and-algorithms.github.io/assets/files/Probability_Book_Excerpt_BlitzsteinHwang.pdf>
  — Thm 1.6.2(3) ("a useful intuition, but not a proof"), the three-circle tally
  sentence, Thm 1.6.3, Example 1.6.4 de Montmort with the C(n,k) collapse and 1
  − 1/e, the "last resort" advice.
- Charles M. Grinstead and J. Laurie Snell, Introduction to Probability, ch. 3
  source, <https://math.dartmouth.edu/~prob/prob/ch3.tex> — Theorem 3.10,
  Example 3.13 hat check, Table 3.7 (n = 3…10), Historical Remarks on de
  Montmort's Treize.
- Miklós Bóna, A Walk Through Combinatorics, ch. 7 "The Sieve" (Internet Archive
  text),
  <https://archive.org/stream/a-walk-through-combinatorics/a-walk-through-combinatorics_djvu.txt>
  — two- and three-set statements, the sieve formula with the (1−1)ⁿ proof, D(2)
  = 1, D(3) = 2, D(4) = 9.
- Stanford Math 61DM, "Handout: Inclusion-Exclusion Principle" (Fall 2016, no
  byline; hosted on Jacob Fox's course directory),
  <https://web.stanford.edu/~jacobfox/61DMfiles/inclusion-exclusion%20principle.pdf>
  — iteration to three sets, induction, then the per-element count Σ(−1)^{i+1}
  C(k,i) = 1; derangements to n!/e.
- Physics 116C (UC Santa Cruz, Fall 2012), "The Inclusion-Exclusion Principle"
  (no byline; hosted under Howard Haber's course page),
  <https://scipp-legacy.pbsci.ucsc.edu/~haber/ph116C/InclusionExclusion.pdf> —
  the cleanest written per-point proof (eq. 7) and the derangement count term by
  term.
- Dennis White, "Math 4707: Inclusion-Exclusion and Derangements",
  <https://www-users.cse.umn.edu/~reiner/Classes/Derangements.pdf> — PIE proved
  by a sign-reversing involution; D_n = Σ(−1)^k C(n,k)(n−k)!.
- Arthur T. Benjamin and Jennifer J. Quinn, "An Alternate Approach to
  Alternating Sums: A Method to DIE for",
  <https://math.hmc.edu/benjamin/wp-content/uploads/sites/5/2019/06/An-Alternate-Approach-to-Alternating-Sums.pdf>
  — the toggle-1 pairing with the n = 4 subset table; the partial-sum identity
  Σ_{k≤m}(−1)^k C(n,k) = (−1)^m C(n−1,m).
- Márton Balázs and Bálint Tóth, "Inclusion-exclusion principle" (University of
  Bristol, 2014), <https://people.maths.bris.ac.uk/~mb13434/incl_excl_n.pdf> —
  Prop. 1 two events by disjoint pieces; Thm 2 by induction ("add them back
  once. But then we run into trouble with four-intersections"); Corollary 3 the
  alternating bounds.
- Jeremy Orloff and Jonathan Bloom, MIT 18.05 class 2 reading "Probability:
  Terminology and Examples", <https://math.mit.edu/~dav/05.dir/class2-prep.pdf>
  — Rule 3 as "the inclusion-exclusion principle", "the overlap gets counted
  twice", "Rule 2 is a special case of Rule 3".
- David Guichard, An Introduction to Combinatorics and Graph Theory, §2.1 "The
  Inclusion-Exclusion Formula",
  <https://www.whitman.edu/mathematics/cgt_online/book/section02.01.html> — the
  complement form, the per-element count, worked sieve counts.
- cp-algorithms (primary contributor credited on-page: gabrielsimoes), "The
  Inclusion-Exclusion Principle",
  <https://cp-algorithms.com/combinatorics/inclusion-exclusion.html> — the
  per-element proof with (1−1)^k; coprime-counting and derangement applications.
- Art of Problem Solving wiki, "Principle of Inclusion-Exclusion",
  <https://artofproblemsolving.com/wiki/index.php/Principle_of_Inclusion-Exclusion>
  — the "counted three times, subtracted three times, counted once more"
  sentence in the form learners quote.
- Dan Ma, "A Blog on Probability and Statistics" — posts tagged
  inclusion-exclusion,
  <https://probabilityandstats.wordpress.com/tag/inclusion-exclusion-principle/>
  — the matching table n = 2…8 and P(exactly k matches) ≈ e^{−1}/k!.
- Gaston Sanchez, "De Mere's Games" (Introduction to Computing with Data),
  <https://www.gastonsanchez.com/intro2cwd/demere.html> — 1296 − 625 = 671
  outcomes with at least one six.
- Hossein Pishro-Nik, Introduction to Probability, Statistics, and Random
  Processes, §6.2.1 "Union Bound and Extension",
  <https://www.probabilitycourse.com/chapter6/6_2_1_union_bound_and_exten.php> —
  the union bound by induction, the alternating-terms bounds.
- Brilliant (credited contributors: Andy Hayes, Anuj Shikarkhane, Calvin Lin,
  Mahindra Jain, Suyeon Khim), "Probabilistic Principle of Inclusion and
  Exclusion",
  <https://brilliant.org/wiki/probabilistic-principle-of-inclusion-and-exclusion/>
  — the independent-events form beside the dependent form.
- The Mathematics Enthusiast, vol. 6 (2009), students' difficulties with
  independent and mutually exclusive events (author not retrieved — PDF returned
  403; credit before citing),
  <https://scholarworks.umt.edu/cgi/viewcontent.cgi?article=1133&context=tme> —
  the 97-student study; the "independence or mutually exclusive events are the
  same" misconception.

## Pinned report: source verifier (digest — ADR 007)

Every number computed in exact `Fraction`/integer arithmetic by
exhaustive enumeration under `uv run python`, with a second route
(closed form, recurrence, complement) wherever one exists; primary
texts read: Ross 10th ed. (PDF), Feller vol. 1 **1950 first edition**
(archive.org), Venn *Symbolic Logic* 1881 (archive.org), de Moivre
1718 (archive.org). The assertion scripts are reproduced in the
verifier transcript and become `answers/inclusion_exclusion.py` in
phase 3. [ENUM] = enumerated here; [SRC] = read in a source.

A. **One die, two sets** [ENUM]. A = even {2,4,6}, B = ≤ 3 {1,2,3}:
   |A∩B| = 1, |A∪B| = 5, P = 5/6 = 3/6 + 3/6 − 1/6; naive sum = 1 (a
   legal probability — flag 1). Disjoint pairs: {1,2} vs {5,6}:
   4/6 = 2/6 + 2/6. Source: Ross Prop. 4.3 (proved from Axiom 3 via
   E ∪ EᶜF); Feller IV (1.1) [SRC].
B. **Two dice, two sets** [ENUM]. First 6 / second 6: 6/36 + 6/36 −
   1/36 = 11/36; complement 1 − 25/36 = 11/36 (agree); 12/36 = 1/3 is
   the naive sum (flag 2).
C. **Three sets, 1..30 by 2, 3, 5** [ENUM]. Sizes 15, 10, 6; pairs 5,
   3, 2; triple 1; union 22; disjoint cells only-2/3/5 = 8/4/2,
   2∩3/2∩5/3∩5-only = 4/2/1, all three = 1 (30), none = 8 = φ(30) =
   {1,7,11,13,17,19,23,29}; 8/30 = 4/15 = (1−½)(1−⅓)(1−⅕) exactly.
   The only candidate with all seven regions non-empty (one die
   cannot: 7 cells > 6 outcomes; every two-dice triple tried has an
   empty region). Flag 3: "only-2" and "none" are both 8 — label.
D. **Bernstein** [ENUM]. {1,2},{1,3},{1,4} on four outcomes: singles
   1/2, pairs 1/4 (= products), triple 1/4 ≠ 1/8; union = Ω = 1 = 3/2
   − 3/4 + 1/4; pairwise-only cells all EMPTY. The repo inset
   (`independence_manim.py` ~602) is the OTHER Bernstein: two coins,
   A first H, B second H, C exactly one head — triple = 0, union 3/4
   = 3/2 − 3/4 + 0 (flag 4: name the one used). Both are Bernstein
   1946 per Bogomolny; Feller V.3 (e) credits "S. Bernstein" [SRC].
E. **Four hats / derangements** [ENUM, three routes: brute force,
   recurrence D(n) = (n−1)(D(n−1)+D(n−2)), series n!Σ(−1)^k/k!].
   n = 4: 24 permutations, 15 with ≥ 1 fixed point, D(4) = 9;
   P(≥ 1) = 15/24 = 5/8; census {0: 9, 1: 8, 2: 6, 3: 0, 4: 1} (flag 5:
   exactly three is impossible). Terms C(4,k)(4−k)!/4!: 1, 1/2, 1/6,
   1/24, i.e. 4·(1/4) − 6·(1/12) + 4·(1/24) − 1/24; partial sums 1,
   1/2, 2/3, 15/24. Table: n = 2..8 → D = 1, 2, 9, 44, 265, 1854,
   14833; P(no match) = 1/2, 1/3, 3/8, 11/30, 53/144, 103/280,
   2119/5760; P(≥ 1) = 1/2, 2/3, 5/8, 19/30, 91/144, 177/280,
   3641/5760. Source: Ross Ex. 5m (N hats: each level sums to 1/n!,
   "approximately .37"); Ross Problem 17 (the recurrence); Feller
   IV.4 table 0.333, 0.375, 0.367, 0.368, 0.36788, 0.367879 [SRC].
F. **Four circles** [derivation + SRC]. R(k) = R(k−1) + 2(k−1),
   R(1) = 2 → k² − k + 2: 2, 4, 8, 14, 22 vs 2ᵏ = 2, 4, 8, 16, 32;
   Euler at k = 4: V = 12, E = 24, F = 14. Venn, *Symbolic Logic*
   (1881) ch. V pp. 105–106, verbatim: "four circles cannot be so
   drawn as to intersect one another in the way required … the most
   simple and symmetrical diagram seems to me that produced by making
   four ellipses intersect one another … 16 partitions" [SRC]. The
   1880 paper (Phil. Mag. (5) 10(59), 1–18 — volume 10, not 9, flag
   18) quoted via Cook/Wikipedia (flag 7). Venn gives no "14" — that
   count is the modern gloss (flag 6: 14 is a maximum, needs every
   pair crossing twice). Grünbaum 1975 = FIVE ellipses (flag 8).
G. **Counted once** [ENUM]. Σ_{j=1}^{k} (−1)^{j+1} C(k,j) = 1 for k =
   1..6; running partial sums k = 3: 3, 0, 1; k = 4: 4, −2, 2, 1;
   k = 5: 5, −5, 5, 0, 1 — odd-length partial sums ≥ 1, even-length
   ≤ 1 (the Bonferroni pattern). Flag 9: partial sums hit 0 and −2 —
   counts, not probabilities. Source: Ross Prop. 4.4 Remark 1
   ("0 = (−1+1)^m") [SRC].
H. **The n-set formula** [SRC]. Ross Prop. 4.4 ("the inclusion–
   exclusion identity", provable by induction), Remark 2 compact form
   Σ_{r=1}^{n} (−1)^{r+1} Σ_{i₁<⋯<iᵣ} P(Eᵢ₁⋯Eᵢᵣ); Feller vol. 1 (1950)
   IV §1 Theorem (1.5) P₁ = S₁ − S₂ + S₃ − ⋯ ± S_N, S_r has C(N,r)
   terms (flag 10: 1950 edition read; 3rd-edition numbering
   unverified). Terms: 2ⁿ − 1 = 1, 3, 7, 15, 31 [ENUM].
I. **Union bound / Bonferroni** [ENUM + SRC]. Ross Remark 3: one term
   upper, two lower, three upper, "and so on"; (4.1) is "Boole's
   inequality"; Feller IV.6 problem (3): the truncation error has the
   sign of the first omitted term and is smaller in absolute value.
   Four hats: 1/2 ≤ 15/24 ≤ 2/3 ≤ 1 exactly. Flag 11: Boole's bound
   here is exactly 1 (vacuous). Flag 12: Ross Problem 11's
   "Bonferroni's inequality" P(EF) ≥ P(E)+P(F)−1 is a different
   statement. Bonferroni 1936 (Pubbl. R. Ist. Sup. Sci. Econ. Comm.
   Firenze 8, 1–62) via Wikipedia only.
J. **The limit** [ENUM, 30-digit Decimal]. 1/e = 0.367879441…, 1 − 1/e
   = 0.632120558…; D(n)/n! at n = 4..8: 0.375000, 0.366667, 0.368056,
   0.367857, 0.367882, error alternating and < 1/(n+1)!. Flag 13:
   0.37/0.368 are roundings. Flag 14: `calculus/` defines e as the
   compound-interest limit (`TheSplitYear`), Taylor series parked;
   `probability/README.md` already states (1−1/n)ⁿ → 1/e ≈ 0.3679
   (`TheBinomialColumns`) — cite the exponential series as unbuilt.
K. **Attribution** [SRC]. de Moivre, *Doctrine of Chances* (1718),
   Problem XXV — letters "taken promiscuously" (flag 15: it IS in
   1718; a "1738 only" claim is false). Montmort, *Essay d'analyse*
   1708 (Treize posed) / 1713 (solved, Nicolaus Bernoulli
   correspondence) — MacTutor. General formula: Da Silva 1854,
   Sylvester 1883, Poincaré 1896 (Prékopa: "frequently attributed to
   Poincaré but already known to de Moivre") — flag 16: no single
   eponym. Boole 1847 attribution unverified (flag 17: name, not
   year).
L. **One die, A = even, B = ≤ 4** [ENUM] (addendum). A∩B = {2,4},
   A∪B = {1,2,3,4,6}; 5/6 = 3/6 + 4/6 − 2/6; naive 1/2 + 2/3 = 7/6 > 1;
   complement 1 − 1/6; P(A∩B) = 1/3 = (1/2)(2/3) exactly, so the
   shortcut 1 − (1/2)(1/3) = 5/6 is legal for this pair; exactly one =
   {1,3,6} = 1/2 = P(A) + P(B) − 2P(A∩B).
M. **Two dice, three sets** [ENUM] (addendum). A = first 6, B =
   second 6, C = sum ≥ 10 = {(4,6),(5,5),(5,6),(6,4),(6,5),(6,6)}.
   S₁ = 18, S₂ = 1 + 3 + 3 = 7, S₃ = 1; union 12 = 18 − 7 + 1 →
   12/36 = 1/3 (TRUE here; the OVERCOUNT in B — the near-miss to
   label). Disjoint cells: A-only {(6,1),(6,2),(6,3)}, B-only
   {(1,6),(2,6),(3,6)}, C-only {(5,5)}, A∩B-only ∅, A∩C-only
   {(6,4),(6,5)}, B∩C-only {(4,6),(5,6)}, triple {(6,6)}, none 24.
   Ledger (6,6): +3 −3 +1 = 1. Exactly one = 7 = S₁ − 2S₂ + 3S₃.
   Partial sums 18/36, 11/36, 12/36: 11/36 ≤ 12/36 ≤ 18/36.
N. **Bernstein, the inset's form** [ENUM] (addendum). Union 3/4 =
   3/2 − 3/4 + 0; shortcut 1 − (1/2)³ = 7/8; error 7/8 − 3/4 = 1/8 =
   (1/2)³, the product the true triple term (0) is not.
O. **de Méré's four rolls** [ENUM] (addendum). Aᵢ = roll i shows 6
   over 1296: S = 864, 216, 24, 1 (= 4·216, 6·36, 4·6, 1); union 671;
   671/1296 = 0.517747…; complement 1 − (5/6)⁴ = 671/1296 (625 = 5⁴
   no-six outcomes). Ladder 864, 648, 672, 671 → 2/3, 1/2, 14/27
   (0.5185…), 671/1296; bracket 1/2 ≤ 671/1296 ≤ 14/27 ≤ 2/3. Source:
   Weisstein, "de Méré's Problem" (MathWorld) — de Méré and Pascal,
   no Fermat, no year (flag O-1: keep "1654" off screen).
P. **The nine derangements of 1234** [ENUM] (addendum): 2143, 2341,
   2413, 3142, 3412, 3421, 4123, 4312, 4321; the 15 with a fixed
   point: 1234, 1243, 1324, 1342, 1423, 1432, 2134, 2314, 2431, 3124,
   3214, 3241, 4132, 4213, 4231.
Q. **Toggle pairing** [ENUM] (addendum). S ↔ S △ {1} on nonempty
   subsets of {1..k}, k = 1..6: every pair flips parity, exactly one
   survivor {1}, 2·pairs + 1 = 2ᵏ − 1. k = 3: {2}↔{12}, {3}↔{13},
   {23}↔{123}; k = 4: seven pairs ({2}↔{12}, {3}↔{13}, {4}↔{14},
   {23}↔{123}, {24}↔{124}, {34}↔{134}, {234}↔{1234}). Benjamin–Quinn
   Σ_{j=0}^{m} (−1)^j C(k,j) = (−1)^m C(k−1,m): k = 4 → 1, −3, 3, −1, 0.
   Flag Q-1: that is the j-from-0 convention; anchor G's from-1
   partial sums are 1 minus these (4, −2, 2, 1) — never both under one
   label.
R. **Two roads / rare events** [ENUM] (addendum). (1−1/4)⁴ = 81/256 =
   0.316406 vs 3/8 = 0.375; (1−1/8)⁸ = 0.343609 vs 2119/5760 =
   0.367882. Four events at 1/100: bound 4/100 = 0.04; independent
   exact 1 − (99/100)⁴ = 0.03940399 (flag R-1: "exact" assumes
   independence; the bound holds regardless).

### Sources (verifier pass — for the topic README, `- [ ]`, authors as credited)

- Sheldon Ross, *A First Course in Probability*, 10th ed. (Pearson, 2019) — PDF
  mirror,
  <https://www.cs.utexas.edu/~abdonm/SDS%20321/a_first_course_in_probability.pdf>
  — Ch. 2 §2.4 Prop. 4.3 (two events), Prop. 4.4 (the inclusion–exclusion
  identity) with Remarks 1–3 (counting argument, compact form, the Bonferroni
  ladder, Boole's inequality); Example 5m the matching problem, e⁻¹ ≈ .3679.
- William Feller, *An Introduction to Probability Theory and Its Applications*,
  vol. 1 (Wiley, 1950) — archive.org,
  <https://archive.org/details/dli.ernet.5666> — Ch. IV §1 Theorem (1.5) P₁ = S₁
  − S₂ + ⋯ ± S_N; §4 the matching table; IV.6 problem (3) Bonferroni's
  inequalities; V.3 Example (e) and the Bernstein credit.
- John Venn, *Symbolic Logic* (Macmillan, 1881) — archive.org full text,
  <https://archive.org/details/symboliclogic00venniala> — ch. V pp. 105–107:
  "four circles cannot be so drawn as to intersect one another in the way
  required"; the four-ellipse diagram with 16 partitions.
- Branko Grünbaum, "Venn Diagrams and Independent Families of Sets",
  *Mathematics Magazine* 48(1) (1975) 12–23,
  <https://www.tandfonline.com/doi/abs/10.1080/0025570X.1975.11976431> — the
  five-ellipse Venn diagram and the general theory (citation only).
- Abraham de Moivre, *The Doctrine of Chances* (London, 1718) — archive.org full
  text,
  <https://archive.org/details/bim_eighteenth-century_the-doctrine-of-chances_moivre-abraham-de_1718>
  — Problem XXV, letters "taken promiscuously": the matching problem in the
  first edition.
- J J O'Connor and E F Robertson, "Montmort's Problême du Treize" (MacTutor),
  <https://mathshistory.st-andrews.ac.uk/Extras/Montmort_Treize/> — posed 1708,
  solved 1713, the Nicolaus Bernoulli correspondence.
- J J O'Connor and E F Robertson, Pierre Rémond de Montmort biography
  (MacTutor), <https://mathshistory.st-andrews.ac.uk/Biographies/Montmort/> —
  the *Essay d'analyse* editions.
- Lajos Takács, "The problem of coincidences", *Archive for History of Exact
  Sciences* 21(3) (1980) 229–244,
  <https://link.springer.com/article/10.1007/BF00327875> — the standard history
  of the matching problem (citation only, paywalled).
- András Prékopa, "Inclusion-exclusion formula" (Encyclopedia of Mathematics),
  <https://encyclopediaofmath.org/wiki/Inclusion-exclusion_formula> —
  "frequently attributed to H. Poincaré … already known to A. De Moivre".
- M. Hazewinkel, "Montmort matching problem" (Encyclopedia of Mathematics),
  <https://encyclopediaofmath.org/wiki/Montmort_matching_problem> — jeu du
  treize / rencontre; 1 − e⁻¹.
- Ana Patrícia Martins and Teresa Sousa, "Formulations of the
  inclusion–exclusion principle from Legendre to Poincaré, with emphasis on
  Daniel Augusto da Silva", *BJHM* 37(3) (2022) 212–229,
  <https://www.tandfonline.com/doi/full/10.1080/26375451.2022.2082158> — the
  19th-century attributions (citation only).
- Alexander Bogomolny, "Mutually (Jointly) Independent Events" (Cut the Knot),
  <https://www.cut-the-knot.org/Probability/MutuallyIndependentEvents.shtml> —
  both Bernstein 1946 examples (triple ∅ and triple 1/4), with the Russian
  citation.
- Deborah Bennett, "Origins of the Venn Diagram" (2015),
  <https://logic-teaching.github.io/pred/texts/Bennett%202015%20-%20Origins%20of%20the%20Venn%20Diagram.pdf>
  — Venn 1880 quotes; four ellipses = 16 compartments.
- Satyadev Nandakumar, "Venn Diagrams and Circles" (IIT Kanpur),
  <https://www.cse.iitk.ac.in/users/satyadev/venn.html> — the Euler-formula
  count V = 12, E = 24, F = 14 for four circles.
- Eric W. Weisstein, "de Méré's Problem" (MathWorld),
  <https://mathworld.wolfram.com/deMeresProblem.html> — 1 − (5/6)⁴ ≈ 0.5177 vs 1
  − (35/36)²⁴ ≈ 0.4914; de Méré and Pascal.
- Wikipedia, Inclusion–exclusion principle,
  <https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle> —
  general formula, the counting and indicator proofs, attribution paragraph (de
  Moivre 1718, Da Silva 1854, Sylvester 1883), the derangement limit.
- Wikipedia, Boole's inequality,
  <https://en.wikipedia.org/wiki/Boole%27s_inequality> — the Bonferroni
  inequalities in S_k notation; Bonferroni 1936 citation.
- Wikipedia, Derangement, <https://en.wikipedia.org/wiki/Derangement> — D(n) =
  1, 0, 1, 2, 9, 44, 265, 1854, 14833; Montmort 1708/1713.
- Wikipedia, Venn diagram, <https://en.wikipedia.org/wiki/Venn_diagram> — the
  1880 citation (vol. 10 no. 59); "only 14 regions as opposed to 2⁴ = 16";
  Venn's ellipses; Grünbaum's five.
