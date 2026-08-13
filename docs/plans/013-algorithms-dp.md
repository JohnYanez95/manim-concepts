# Plan 013: `algorithms/` — dynamic programming as its own concept

Branch: `feat/algorithms-dp`, cut from updated `main` (the ADR-008
merge). Started: 2026-08-12.

The graph's oldest standing promise (`ctc-alignment` → *(dynamic
programming as its own concept)*, promised since plan 001), and the
first series built under ADR 008's inverted pipeline: the guide-first
chapter `study_guides/primitives/dynamic-programming.tex` — already
solve-gated and shipped in guide v1 — is the seed material, the book
drafting what the screen now animates. The wiki row carries two
recorded anchors the closer spends: log-space inheritance
(`TheUnderflowCliff`) and the constant column as LOTP
(`PathsThroughACell`).

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research (pedagogy + verifier); design | Scene design written into the plan |
| 1 | New topic dir `algorithms/`, README skeleton, module stub | `make check` |
| 2 | Six scenes at draft; layout linter clean; frames verified by eye | Linter clean + drafts verified |
| 3 | Concepts table, references `- [ ]`, wiki graph + log; ADR-008 step: the DP primitive trued against the built scenes; new series → welcome.gif re-render (12 series, rows 6+6) | `make test` — **John's source checkpoint** |
| 4 | Local CodeRabbit + connection-auditor, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p60 render |

## Checklist

- [x] Phase 0: both reports pinned below; design finalized (six
  scenes; decisions D1–D6)
- [x] Phase 1: topic dir + stub, `make check` green (the ADR-008
  bib-sync test caught the new references on the first run)
- [x] Phase 2: six scenes at draft (6 files, distinct names,
  16–37 s). Linter: eight real findings fixed before render (the
  fib tree spilling into the right margin, ticker rows through the
  canopy — now one bottom-edge line, caption crowding in scenes 3/4,
  the D&C chips' edges touching their labels — gaps widened);
  remaining findings are the explained node-label class (labels
  inside background-filled circles). Frames verified by eye across
  all six. As-built truing: scene 2's tree→DAG merge animation
  simplified at build to the fold + the naming (the chain-DAG lives
  in prose and scene 5's shape table carries the tree-vs-DAG verdict)
- [x] Phase 3: README complete (six rows, all three levels; scope
  with four deliberate exclusions; seventeen references unchecked
  for the maintainer's pass); wiki — node added, **the graph's
  oldest promise flipped delivered** (ctc-alignment →
  dynamic-programming, closed by `TheTrellisWasAMemo` with both
  recorded anchors spent in the closer), new delivered edge to
  counting-rules (the lattice checked against C(6,2) on screen),
  the fold recorded as a new device, tree↔grid's fourth direction,
  the mapping close's fifth series, log entry; **ADR-008 step**: the
  guide's DP primitive trued to series-backed (header + the
  seed-that-sprouted closing; both PDFs rebuilt, figures clean);
  welcome re-rendered at twelve series (rows 6+6, 383 KB).
  `make test` green (235). **At John's source checkpoint**
- [x] Phase 4: local CodeRabbit returned three minors — all
  residuals of the cut merge animation (the plan's scene-2 body, the
  wiki fold bullet now describing the actual visual, the README
  when-useful cell gaining the use condition) — applied. Audit: 17
  findings applied, zero numeric — two NEW promised rows recorded
  (divide & conquer, spoken on screen; edit distance worked, its
  table already pinned), the promise's home cell finally pointed at
  algorithms/, the backward-sweep horizon recorded as row 48's third
  strand, the WARM lineage's fourth removal and the waist ring's
  rename, the Pascal-queue screen precedent, beam search's second
  anchor, the stale root-README/study-INDEX trio fixed,
  "in-degree" softened to the on-screen claim, and "oldest promise"
  disambiguated to "oldest standing" (plan 007's row keeps the
  elder title)
- [x] Phase 5: PR #15 opened; bot review returned three findings,
  all applied (the duplicate-count tags now leave with the tree — a
  real lingering-mobject bug; the lattice's arrow claim trued to the
  build; the retrieval row's missing 001.raw81 added).
  `clean-drafts`, then 1080p60 finals: 6 files, distinct names,
  16–37 s, scene 1's fixed close verified by frame. The plan
  closes; the PR awaits the maintainer's merge — and with it, the
  graph's oldest standing promise is paid on screen

## Decisions (made at design time)

1. **New top-level topic `algorithms/`**, module
   `dynamic_programming_manim.py`. The teaching bodies ground in
   Fibonacci (neutral), the counting lattice, and the CTC trellis —
   two of three grounds are not deep learning, and the cross-topic
   edge `ctc-alignment → dynamic-programming` mirrors
   `counting-rules → ctc-alignment`. Scope boundary in the topic
   README: no optimization-DP zoo (knapsack/rod-cutting/LIS), no
   "optimal substructure" vocabulary (replaced by "the stored answer
   is all the future needs"), no pseudocode, no Bellman-equation/MDP
   branch, no beam search (stays queued in deep_learning).
2. **Recursion-first, counting-first** (Erickson/Demaine camp, with
   Demaine's explicit license that counting recurrences are "almost
   trivially correct"): the recurrence is the concept, the table its
   residue. The series NEVER teaches "DP = filling tables" — scene
   4's reconciliation beat shows memo and loop building the same
   table in the same order.
3. **The Bellman/Wilson naming story is told only as Bellman's
   story** — the verifier established the chronology that contradicts
   it (term in print Aug 1952, PNAS communicated 5 June 1952 by von
   Neumann; Wilson SecDef from Jan 1953; Bellman dates naming to Fall
   1950, under Marshall). One hedged aside, "as Bellman told it".
   The principle of optimality, if shown, uses the **1954 P-550
   plural wording** (verified against RAND's scan), never the
   secondhand 1957 singular.
4. **"Memo functions (Michie, 1968)"**, never "memoization (Michie,
   1968)" — the word does not appear in the verified text.
5. **The two-DP-stories bridge is an explicit beat** (pedagogy
   pitfall 8): Fibonacci is recompute-avoidance; the trellis is a sum
   reorganised (nothing ever computed twice because nothing was ever
   enumerated); the bridge is "one stored answer serves many
   parents — distributivity does the factoring".
6. **Three unrelated 15s** (fib(5)'s 15 call nodes, the lattice's 15
   nodes, the flagship 15 routes) never share a screen uncaptioned;
   the fib tree drawn at n=5 or 6 only — 177 arrives by ticker,
   never by drawing. Call-count convention fixed on screen before
   any ticker (every invocation counts; base cases answer directly).

Off-screen list: unhedged Wilson story; "memoization (Michie 1968)"
verbatim; "Wagner–Fischer invented edit distance" (say "the standard
Wagner–Fischer table (1974)" / "Levenshtein distance"); the 1957
book's principle wording; "O(2^n)" for the naive calls (growth is
Θ(φ^n); the ratio table never reaches 1.6180 by n=12 — show
approach, not arrival); the GE-vs-GM Wilson reconciliation
(unverified); skip edges on the 3-state mini trellis (it has none).

## Scene design

Module: `algorithms/dynamic_programming_manim.py`, six scenes. The
worked objects: fib (tree at n=5/6, ticker to 177 at n=10), the
walker's lattice (4 rights, 2 ups, corner 15), the mini trellis
(ε A ε, columns (1,1,0)→(1,2,1)→(1,3,3), accepted 3+3=6), the AB
trellis re-read (81/15/20 cells), the scale card (10,100 cells vs
2.013×10⁴⁰ paths).

**1. `TheQuestionAskedTwice`** — computed exactly as written, the
recursion answers the same question over and over. The fib(5)/fib(6)
call tree with duplicate labels flashing WARM; the convention pinned
("every call counts; base cases answer directly"); the ticker to 177
calls for 11 questions at n=10, with repeat counts (F8 ×2, F7 ×3,
F6 ×5 — asked at the sequence's own rate) beside the tree. Formula
last: calls(n) = 2·F(n+1) − 1.

**2. `WriteTheAnswersDown`** *(as built: the fold and the naming;
the same-label merge animation was cut — the DAG appears in scene
5's shape table)* — store each answer once and the tree
folds into six memo boxes (eleven at n = 10, by ticker). The
Erickson fold: first computations write down into a memo row (GOOD),
later copies grey WARM into lookups — the tree stays drawn; the fold
is the greying. The move NAMED (dynamic
programming — solve every small version once, store it, let the big
version assemble itself), the Bellman aside in one hedged line, memo
functions credited (Michie 1968). The two conditions stated: the
questions repeat, and the stored number is all the future needs.

**3. `TheLatticeRecounted`** — shared prefixes, counted once. The
walker's lattice by Pascal addition (as built: undirected grid
lines, the fill marching bottom-up, one demonstrated arrow pair
from the left and from below — pitfall 7 satisfied by caption +
demonstration, not per-edge arrowheads), two routes
converging on a node bundled into one sum; corner 15 checked against
the counting series' C(6,2) on screen. Caption bridge: "recounted,
never listed". (This puts the guide's pre-drafted lattice visual on
screen; the combinatorics WhenToUseIt fifth-shape re-render stays a
separately batched change.)

**4. `TheTrellisWasAMemo`** — the forward trellis was dynamic
programming all along; α_t(s) is a stored answer. The mini trellis's
columns land 3+3=6 with the waist cell ringed ("two prefixes end
here — stored once, reused after"); the AB trellis's 81/15/20
re-read; the scale card 10,100 vs 2.013×10⁴⁰ (~36 orders). The
reconciliation beat: memoization and tabulation are one table, two
orders — asked-when-needed vs filled deliberately. The two-stories
bridge (decision 5) closes the scene.

**5. `WhatBreaksIt`** — dynamic programming pays exactly for how much
past the future needs. (a) No overlap: a divide-and-conquer tree
(disjoint halves), a memo nobody reads twice — filing, not speedup;
Demaine's shape table (star/chain/tree/DAG, DP = in-degree > 1) as
one panel. (b) No small state: legality reading two frames back
fattens each cell into a pair — column 101 → 10,201, table ≈ 1.02
million cells, still polynomial but priced; pushed to "remember
everything visited", the state IS the path and the table becomes the
exponential object (the longest-simple-path lesson, priced not
declared).

**6. `TheSignatureInTheWild`** — the WhenToUseIt-format closer. The
two-part signature (an exponential count/sum over arrangements +
a small state with interchangeable futures — both required) mapped
over: edit distance (state: a prefix pair; the Wagner–Fischer table
named), routes on grids (state: the junction), hidden-state models'
forward algorithm (Rabiner — Graves' own sentence names the trellis
"a dynamic programming algorithm"), Pascal's recurrence (the queued
combinatorics idea, foreshadowed only). Horizon pointers, use-case
framing only: the same grid swept backward (a second DP over
suffixes — the gradient series later on the road); the recurrence's
additions inherit log-space (`TheUnderflowCliff`); the constant
column as LOTP over the frame partition (the recorded anchors,
spent).

**Device lineage this series extends:** the tree↔grid recast (third
direction: tree → DAG), the WARM-cancels convention (duplicate
subtrees greyed), the waist bundle (the alignment series' prefix
bundle, renamed), the counting strip's spirit (stored counters), the
WhenToUseIt mapping close (fifth series to use it).

---

## Pinned report: pedagogy researcher (digest — ADR 007)

Consensus order (recursion-first camp: Erickson ch. 3, MIT 6.006
SRTBOT/Demaine, Avik Das, VisuAlgo, Reducible): slow-correct
recursion → recursion tree with visible repetition → memoize (tree
folds; count the drop) → recognize the DAG; tabulation = the same
table filled deliberately → generalize the recipe → boundaries.
Camp split: recursion-first (the recurrence is the concept;
Erickson: "not about filling in tables — smart recursion!") vs
table-first (CLRS rod-cutting; source of the documented cargo cult).
Orthogonal split: optimization-first (nearly everyone) vs
counting-first (rare; Demaine licenses it — counting recurrences
"almost trivially correct"). The repo takes recursion-first +
counting-first; every asset is counting DP, and "optimal
substructure" is omitted (Demaine's footnote: it is a property of
recursion generally).

Devices: the duplicate-label call tree; the memo-trimmed tree
(Erickson fig 3.2 — the single best diagram found: first copies
write down, later copies grey and read up); tree→DAG merge
(same-label nodes slide together; in-degree > 1 IS overlap); the
lattice with route counts marching by Pascal addition; the
mini-trellis waist ("the whole method in one circle"); the
cells-vs-paths scale card; state-fattening for the boundary;
Demaine's shape table.

Misconceptions (Shindler et al. 2022 replication ×15 universities of
Zehra et al. SIGCSE '18; Danielsiek 2012): "DP = tables" (counter:
memo and loop produce the same table in the same order); failing to
SEE overlap — the top hurdle (counter: two routes converging on one
node); applying DP where nothing repeats (counter: tree-shaped
subproblem graph = every memo entry written once, read never);
DP-vs-D&C conflation (same counter — in-degree); memo sizing errors
M8/M9 (counter: the waist argument — futures of εA and AA are
identical because legality reads only where the path stands; store
the count, never the routes); base-case errors (counter: the empty
prefix's 1 appears before the recurrence runs); greedy-default (one
closer line only); the name itself (programming = planning).
Repo-specific trap to dodge: "the trellis avoids recomputing paths"
— nothing was ever computed twice; the bridge beat (decision 5) is
mandatory. Pitfalls: drawable trees only at n=5/6; conventions
pinned before tickers; the three unrelated 15s; lattice arrows must
match fill order; skip-edge fidelity (mini trellis has none).

Topic dir: new `algorithms/` (reasons in decision 1). Scope
boundary as in decision 1.

Sources (all consulted; full URLs in the topic README's references):
Erickson *Algorithms* ch. 3 + home; MIT 6.006 S20 lecture 15 notes
(Demaine, Ku, Solomon) + OCW video page; Shindler et al. 2022;
Zehra et al. SIGCSE '18; Dreyfus 2002; Avik Das's graphical intro;
VisuAlgo recursion page; Reducible's five-steps video (paraphrase
only); Wikipedia "Block walking"; Levin §3.1; Goldstein (TDS);
Baeldung memoization-vs-tabulation; U. Hawaii ICS 311 notes
(longest-simple-path counterexample).

---

## Pinned report: source verifier (digest — ADR 007)

Method: exact integer/Decimal arithmetic, no floats in counting
steps; primary PDFs fetched and read (Bellman 1952 PNAS scan, RAND
P-550, Dreyfus 2002, Graves 2006); the repo's committed answer
script run and reproduced.

**Sec. 0 — reused and reconfirmed** (guide chapter + answer script,
all re-derived independently): fib(10) 177 calls / 11 subproblems /
F(10)=55; lattice corner 15 = C(6,2) (Pascal + brute 2⁶); mini
trellis (1,1,0)→(1,2,1)→(1,3,3), accepted 6 (recurrence + brute 2³);
10,100 cells vs C(150,50) exactly
20,128,660,909,731,932,294,240,234,380,929,315,748,140 (41 digits,
2.013×10⁴⁰ at 4 sf; gap exactly 36 orders by floor-log10); state
squaring 101² = 10,201, table 1,020,100; repo anchors 001.raw81,
001.paths15, 001.astronomical reconfirmed.

**A — call tables** (both routes agree, n = 0..12):
F: 0 1 1 2 3 5 8 13 21 34 55 89 144;
calls: 1 1 3 5 9 15 25 41 67 109 177 287 465. Convention: every
invocation counts; bases answer directly. calls(n) = 2·F(n+1) − 1.
Repeat counts at n=10: F8 ×2, F7 ×3, F6 ×5, F5 ×8, F4 ×13, F3 ×21,
F2 ×34, F1 ×55, F0 ×34; sum = 177 exactly.

**B — the Wilson story, verbatim** (Bellman, *Eye of the Hurricane*
1984 p. 159, via Dreyfus 2002, read in full): "…I felt I had to do
something to shield Wilson and the Air Force from the fact that I
was really doing mathematics… It's impossible to use the word,
dynamic, in a pejorative sense… It was something not even a
Congressman could object to." Bellman places the naming in Fall 1950.

**C — the chronology that contradicts it** (each date sourced):
PNAS 38(8):716–719 (1952), "Communicated by J. von Neumann, June 5,
1952" — read in scan; Charles E. Wilson SecDef 28 Jan 1953 – 8 Oct
1957 (DoD Historical Office); Fall-1950 SecDef was George C.
Marshall (Miller Center/Truman Library, snippet-confirmed ×3).
Dreyfus 2002 itself does NOT flag the conflict — citing it alone
would launder the myth. The "GE Wilson at ODM" reconciliation is
UNVERIFIED — off screen.

**I — principle of optimality, verbatim, primary** (RAND P-550,
30 July 1954, p. 4, read in RAND's own scan; text of the AMS Laramie
address, printed as Bull. AMS 60:503–515): "An optimal policy has
the property that whatever the initial state and initial decisions
are, the remaining decisions must constitute an optimal policy with
regard to the state resulting from the first decisions." (PLURAL
wording; the 1957 book's singular version is unverified secondary —
do not display.) Also usable, same scan: "A sequence of decisions
will be called a policy…" (p. 2); "Not at all! It is sufficient to
furnish a general prescription which determines at any stage the
decision to be made in terms of the current state of the system."
(p. 3 — Bellman stating "the state is all the future needs"); the
"makes even a modern computing machine cringe" line (p. 3). The 1952
paper's closest line: "In many cases, the problem of determining an
optimal sequence of operations may be reduced to that of determining
an optimal first operation." — "principle of optimality" does NOT
appear in 1952.

**J — growth**: φ = 1.6180339887…; calls(n)/φⁿ → 2φ/√5 = 1.44721…;
ratio calls(n)/calls(n−1) at n = 5..12: 1.6667, …, 1.6202; reaches
1.6181 only at n=20 — show approach, not arrival.

**K/L — edit distance**: Wagner & Fischer, JACM 21(1):168–173
(1974), DOI confirmed; the metric is Levenshtein's (1965/66); the DP
found independently several times (none of those verified — no
"first/invented" claims). KITTEN→SITTING full 7×8 table computed by
recurrence AND breadth-first search over real edits; distance 3
(K→S, E→I, +G). Table pinned in the verifier transcript; final row:
6 6 5 4 3 3 2 3.

**M — memo functions**: Michie, "'Memo' Functions and Machine
Learning", Nature 218:19–22 (6 Apr 1968); title spelling verified;
"memoization" absent from the archived full text — coinage claims
limited to "memo functions"; the memo-not-memorization derivation is
secondary-only (light aside at most).

**N — lineage**: Graves 2006, verbatim: "Fortunately the problem can
be solved with a dynamic programming algorithm, similar to the
forward-backward algorithm for HMMs (Rabiner, 1989)." — the flagship
closer quote; already repo-carried.

FLAGS: (1) Wilson anecdote = Bellman's retelling only, scenes
attribute, never assert; (2) 1957 book unfetched — use P-550
wording; Bull. AMS printed pages returned 403, P-550 self-describes
as the address text; (3) "memoization" not verbatim-safe; (4)
edit-distance attribution hedged; (5) Dreyfus doesn't flag the myth;
(6) Marshall/Wilson dates snippet-confirmed ×3 institutions; (7)
ratio pacing (no arrival by n=12); (8) C(T+U,T−U) is repeat-free
transcripts only.

Sources for the topic README (`- [ ]`, human-gated): Dreyfus 2002
(cs.miami.edu PDF + INFORMS canonical); Bellman 1952 PNAS; RAND
P-550; DoD Historical Office (Wilson); Miller Center (Marshall);
Michie 1968 (Nature + poplog archive); Wagner–Fischer JACM 1974;
Graves 2006 (already carried). Plus the pedagogy list above.
