# Plan 007: `probability/` — random variables & distributions

Branch: `feat/probability-random-variables`, cut from updated `main`
(349fc20, the plan-006 merge).
Started: 2026-08-11.

Chosen as the roadmap's second stop (after `calculus/`, before the
softmax/likelihood bridge): this series closes the graph's **oldest**
open promise — `counting-rules` → binomial, standing since the repo's
first topic — plus `independence` → random variables, and it is the
remaining gate on the softmax bridge (`calculus/` delivered the e-half).
It also unblocks the law of large numbers (the swamping seed), entropy
(expectation is the missing half of `ShrinkCounts`' surprisal), and the
conditional series' deferred continuous priors.

The centerpiece is device-ready, recorded twice by audits: group
`ChainsOfTrials`' 16 quartered-square cells by head count and the
binomial pmf (1, 4, 6, 4, 1)/16 = C(4,k)/16 falls out of a picture the
viewer already owns — the quartered square's fifth series, fused with
`CombinationRule`'s C(n,r).

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Research: pedagogy + source verification (agents in flight) | Scene design written below |
| 1 | Plan committed, module stub in `probability/` | `make check` |
| 2 | Scenes at `--quality draft`; renders verified (count, names, ffprobe, frames incl. transition windows and every beat's steady state) | Draft renders verified by eye |
| 3 | Concepts table, references `- [ ]`, wiki graph + log updated | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `make clean-drafts` + 1080p60 render |

No welcome-gif re-render this time unless the topic row changes —
`probability/` is already hand-listed; adding a "random variables"
entry to its row is a design call made in Phase 3.

## Checklist

- [x] Phase 0: research reports received (pedagogy + source-verifier
  main report + on-request addendum, all pinned below), scene design
  finalized below; the addendum's A3 flag resolved by grep (the
  independence module's biased die is "double weight on 6" over 7 —
  matches 27/7)
- [ ] Phase 1: plan + module stub, `make check` green
- [ ] Phase 2: all scenes render at draft; verified per CLAUDE.md checklist
- [ ] Phase 3: README + wiki complete, `make test` green
- [ ] Phase 4: local review + audit clean
- [ ] Phase 5: PR, drafts cleaned, 1080p60 render verified

## Research questions the reports must settle

- RV-as-function-first (the die as a function, not a set) vs
  distribution-first — which ordering fits a viewer trained on the
  unit square?
- The expectation visual: center of mass vs fair price vs long-run
  average — noting long-run average forward-references LLN, which may
  stay a promise.
- Does variance belong in this series, or is spread deferred?
- Does LLN get a quantified scene (the swamping beat, made numeric) or
  remain promised?
- How the binomial-from-the-square reveal is best staged, and what the
  Galton board adds (with its history verified, not assumed).
- Exact numbers for every candidate beat: the (1,4,6,4,1)/16 grouping,
  a biased binomial for contrast, dice expectations, E = np both
  routes, the Pascal–Fermat/Huygens/Bernoulli/de Moivre dates, and the
  plan-006 seed (1+1/n)^n = Σ C(n,k)/nᵏ.

## Verified technical anchors (from the source-verifier report)

Method tags per plan 006's convention. All probability/counting
arithmetic ran in exact `Fraction`s; no floats touched any exact value.

- **Four fair flips** [computed-exact, two routes]: 16 outcomes,
  grouped by head count → (1, 4, 6, 4, 1); enumeration and C(4,k)
  agree. On screen keep the /16 forms (1/16, 4/16, 6/16, 4/16, 1/16)
  when the 16-cell square is visible; sum = 1 exactly.
- **Binomial pmf** [quoted, OpenStax Introductory Business Statistics
  2e §4.2 / formula review]: P(x) = C(n,x) pˣ q^(n−x); conditions
  [quoted, OpenStax Introductory Statistics 2e §4.3]: fixed n, two
  outcomes, constant p, independent identical trials. Biased case
  n=4, p=1/3 [computed-exact, two routes — formula and weighted
  enumeration of all 16 sequences]: 16/81, 32/81, 24/81, 8/81, 1/81;
  sum = 81/81.
- **Expectation** [quoted, Grinstead & Snell Def. 6.1]: E(X) =
  Σ x·m(x). Fair die E = 7/2 = 3.5 exactly. Two fair dice
  [computed-exact, both routes]: distribution (1,2,3,4,5,6,5,4,3,2,1)/36,
  E = 7 by enumeration AND by linearity (3.5 + 3.5).
- **E[binomial] = np** [computed-exact, two routes each]: n=4 p=1/2 →
  2; n=4 p=1/3 → 4/3; definition-sum and indicator-linearity agree.
  Linearity [quoted, G&S Thm. 6.2] with the verbatim no-independence
  remark: "mutual independence of the summands was not needed as a
  hypothesis" — the caption-grade citation.
- **Balance point** [computed-exact]: Σ (x − E)·P(x) = 0 exactly (as
  Fractions) for the die, the two-dice sum, and binomial(4, 1/3).
- **E need not be attainable**: die 3.5 vs faces 1..6; five flips
  E = 5/2 [computed-exact, both routes]. The prose sentence is
  standard commentary, not a quoted theorem [reasoned].
- **Variance** [quoted, G&S §6.2: V(X) = E((X−μ)²), shortcut
  E(X²) − μ², binomial npq]: n=4 p=1/2 → 1 and n=4 p=1/3 → 8/9, each
  by THREE routes [computed-exact]. Die 35/12; two-dice sum 35/6
  (additivity visible). Variance is presentable definition-first
  ("expected squared distance from the balance point") with no
  algebra — both fetched treatments do so [reasoned].
- **History** [quoted MacTutor/Wikipedia/G&S]: Pascal–Fermat, five
  letters, summer 1654, problem of points — the origin of
  *probability*; expectation as an explicit concept is Huygens 1657
  (De Ratiociniis in Ludo Aleae, the first printed probability work —
  phrase captions accordingly). Jacob Bernoulli died 1705; Ars
  Conjectandi published 1713 by nephew Nicolaus I — the weak LLN
  proved by ~1689, in print 1713: keep the two years distinct. de
  Moivre's normal approximation: private pamphlet 1733 (day disputed
  — never print it), folded into Doctrine of Chances 1738. Galton:
  quincunx demonstrated at the Royal Institution 1874 (built 1873,
  secondary-sourced); Natural Inheritance 1889; the two-stage version
  was described in an 1877 letter and NOT built — never animate it
  as a machine that existed.
- **The plan-006 seed** [computed-exact]: (1+1/n)ⁿ = Σ C(n,k)/nᵏ (the
  binomial theorem); verified exactly at n=4 (625/256) and n=12
  (13¹²/12¹²). NOTE: plan 006's printed 2.613035290225 is *rounded*
  at the 12th place (full: 2.613035290224678…) — round explicitly if
  reprinted; don't mix truncation and rounding.
- **Weak LLN** [quoted, G&S Thm. 8.2 — named, never proved, per repo
  convention]. The swamping number [computed-exact, symmetry
  cross-check]: 100 fair flips, P(|heads − 50| ≥ 10) =
  0.0569 (≈5.7%); complement ≈94.3%. The strict-inequality version
  is a DIFFERENT number (0.0352) — pin the caption to ≥. Chebyshev
  gives 1/4 for the same event: the exact tail beats it ~4.4×.

### Addendum (design numbers, verified on request)

- **Swamping tables** [computed-exact, band sum + symmetry fold agree
  exactly on every row]: P(|H/n − 1/2| ≤ 0.05): n=20 → 0.496555;
  n=100 → 0.728747; n=1000 → 0.998608. P(|H − n/2| ≤ 5): n=100 →
  0.728747 (the SAME band 45..55 — the tables genuinely pivot on the
  shared row); n=1000 → 0.272028; n=10000 → 0.087590 (trailing zero
  significant; at 3 sf it is 0.0876, never a truncated 0.0875).
- **Binomial(4, 1/4)** [computed-exact, formula + weighted
  enumeration]: (81, 108, 54, 12, 1)/256, sum 1, E = 1 both routes;
  one-head cell = 27/256 with exactly C(4,1) = 4 such cells. Force
  the /256 and /16 display forms manually — `Fraction` auto-reduces.
- **Biased die** (weights (1,1,1,1,1,2)/7): E = 27/7 = 3.8571…, two
  routes ((21+6)/7); also not attainable — a second "E is not a
  face". Weights confirmed against the independence module at scene
  time (flag A3).
- **X vs Y = tails** [computed-exact, exhaustive]: X + Y = 4 on every
  one of the 16 outcomes (pointwise, not just distributional); pmf_Y
  = pmf_X exactly (palindromic).
- **Ungrouped = grouped** [computed-exact]: stamps sum to 32
  (0+4+12+12+4); 32/16 = 2 = Σ k·P(k) = np — every number a small
  integer.
- **Foreshadow (one caption max)**: 0.9¹⁰ = 0.3486784401 EXACTLY
  (terminating); 0.99¹⁰⁰ ≈ 0.366032; 1/e = 0.367879 [exact-interval
  and mpmath, agrees with plan 006's anchors]. Convergence from below,
  gaps 0.0192 and 0.0018. The limit statement is analysis — named,
  not derived, same convention as plan 006.

## Pedagogy findings (pinned from the pedagogy-researcher report)

**RV-first, unambiguously.** The camps split between RV-as-function
first (Blitzstein/Stat 110, MIT 18.05) and distribution-first (Seeing
Theory, AP-style, 3b1b's binomial lesson, which never formally defines
an RV). Distribution-first exists for learners with no concrete sample
space — this repo's viewer has owned a drawn one for three series, so
RV-first cashes the square and prevents rather than creates the
canonical confusion (Blitzstein's "sympathetic magic": mistaking a
variable for its distribution — blueprint vs house).

**The series' strongest new device: sort the square.** Stamp each of
`ChainsOfTrials`' 16 equal cells with its head count (the function as
ink that never moves — randomness is only in where the dart lands),
then slide cells into columns grouped by value: the bar chart
(1,4,6,4,1)/16 is watched being born as conserved, rearranged area.
One move carries the series — function made visible, induced weights
made literal, C(4,k) as a visible cell count (the oldest promise
closes the way `CombinationRule` counts), and the working refutation
of the equiprobability bias (Lecoutre 1992: randomness read as
uniformity, documented to survive and even increase with education —
so the counter must be the visible unequal preimages, not assertion).

**Expectation: center of mass, not long-run average.** MIT 18.05
verbatim: "the expected value is the point at which the distribution
would balance." The long-run-average motivator is (a) circular as
teaching (define E by the long run, then "prove" the long run
approaches E) and (b) a forward reference to unbuilt LLN — in this
repo it appears only as the closer's promise. Fair price
(Huygens 1657) is expectation's level 3. The two sums —
Σ_ω X(ω)P(ω) = Σ_x x·p(x) — are silently switched everywhere;
showing them equal once IS the sorting move, and legitimizes the
linearity proof.

**Linearity needs no independence** — proved by the outcome table
(addition distributes over the same outcomes), demonstrated on the
maximally dependent pair X and 4−X, and it is what makes E = np
honest via indicator stamps, no combinatorics.

**Variance: defer** (consensus treats it as a separate unit; nothing
here needs it; a stated-not-earned npq would violate the why-level).
**LLN: one quantified-swamping scene** on exact binomial sums, the
theorem itself named and promised. **Galton board: skip** — real
boards are chaotic deterministic systems, not binomial machines
(balls collide, skip rows); its normal-silhouette payoff needs
deferred densities; the sorted square does its honest job better.

**The unfair-square beat most treatments skip:** with p ≠ 1/2 the
cells are unequal, but every same-count cell has the same area
p^k q^(n−k) (a product doesn't care about factor order) — THAT is why
"coefficient × one-cell probability" is legitimate. Geometry grammar:
the unfair square's cuts stay STRAIGHT (independence), only their
positions move to p.

**Misconceptions designed against:** sympathetic magic (X = heads vs
Y = tails: same pmf, different variables, X+Y = 4 always);
equiprobability bias (five values fed by 1-4-6-4-1 equal cells); "E
must be attainable/most likely" (fulcrum need not sit under a mass —
3.5; mean ≠ mode); linearity-needs-independence; the gambler's
fallacy in LLN clothing (both bands on screen: proportions converge
while counts spread); dropping C(n,k) (one cell vs a column);
binomial-without-replacement (the owned aces boundary); E[h(X)] =
h(E[X]) (guarded caption only if change-of-variables appears).

## Scene design (built from both reports)

Six scenes. Per the narrative rule now in force: levels 1–2 reference
only owned devices; forward pointers (LLN theorem, variance, entropy,
softmax) live exclusively in when-useful beats and the closer. Every
on-screen number traces to the anchors (incl. the pending addendum —
marked [addendum] below; the Phase 0 gate closes when it lands).

1. **`TheStampedSquare`** — *what: the die as a function, not a set.*
   Cold open backward: the die's six faces, then a stamp: X(face) =
   the number shown — the function is ink, fixed before anything is
   rolled; the only random object is the dart/roll. Then the owned
   16-cell square (`ChainsOfTrials`' quartered twice, third repo
   appearance): stamp every cell with its head count — 0 through 4,
   with cell HHTH stamped 3. A dart lands: the label is looked up,
   never generated. When-useful: every measurement attached to a
   random process is this — a fixed rule reading a random outcome.
2. **`SortTheSquare`** — *the pmf born as rearranged area.* The
   stamped cells slide into columns grouped by value: (1, 4, 6, 4,
   1)/16, conserved area, bars summing visibly to 1. Five values fed
   by sixteen equally likely cells — unequal bars from equal cells
   (the equiprobability bias refuted by mechanism). Then the
   blueprint-vs-house beat: stamp the SAME square with Y = tails —
   the sorted bars are identical, yet X ≠ Y and X + Y = 4 in every
   cell [addendum]. The distribution forgets which cell was which;
   the variable remembers.
3. **`TheBalancePoint`** — *expectation, defined not simulated.*
   E[X] = Σ x·p(x), drawn as a fulcrum under the die's flat pmf:
   balance at 3.5 — not a face; a weighted average need not be
   attainable. The two sums shown equal once: summing stamps over
   cells (32/16) = summing values times weights (= 2 for the flips)
   [addendum] — the sort IS the regrouping. The repo's own biased die
   (double weight on 6): E = 27/7 [addendum] — the balance point
   moves with the measure, echoing "independence belongs to the
   measure". When-useful: Huygens 1657, the fair price of a ticket —
   the number you act on.
4. **`SameOutcomesAdd`** — *linearity, dependence welcome.* The
   outcome-table proof: E[X+Y] sums (x+y)·P over the SAME outcomes;
   addition distributes — no independence anywhere (G&S's verbatim
   remark as the caption). Demonstrated on the maximally dependent
   pair X and 4−X (sum 4, always). Then the owned 6×6 grid
   (`TheProductRule`'s) re-read: the two-dice sum paints diagonals —
   (1,2,3,4,5,6,5,4,3,2,1)/36, and E = 7 arrives twice: by the
   diagonals' weighted sum, and as 3.5 + 3.5. When-useful: linearity
   is the workhorse — it prices any bundle of bets from its parts.
5. **`TheBinomialColumns`** — *the oldest promise closes.* Recall the
   sorted columns; count cells per column: 1, 4, 6, 4, 1 — and
   counting 4-letter HT-words with k heads is exactly
   `CombinationRule`'s C(4,k): the coefficient is a cell count, never
   a memorized factor. Then re-cut the square with the cuts at
   p = 1/4 (STRAIGHT cuts — independence unchanged; only positions
   move): cells now unequal, but every k-head cell has the same area
   pᵏq^(4−k) — the product doesn't care about order — so column k
   weighs C(4,k)·pᵏq^(4−k): the pmf assembles with nothing smuggled
   [addendum: (81, 108, 54, 12, 1)/256, E = 1]. Indicator stamps give
   E = np with zero combinatorics. Conditions named (fixed n, two
   outcomes, constant p, independent trials); the owned aces beat
   marks the boundary (no replacement → no binomial). When-useful:
   the count-of-successes model everywhere trials repeat unchanged.
6. **`ProportionsConverge`** — *swamping, quantified; the promises
   named.* Binomial bars on the FRACTION axis, n = 20 → 100 → 1000:
   P(within ±5% of half) climbs 0.4966 → 0.7287 → 0.9986 [addendum]
   while, paired, P(within ±5 heads) falls 0.7287 → 0.2720 → 0.0876
   (n = 100, 1000, 10000) [addendum] — proportions converge, counts
   spread: the gambler's fallacy dies by two numbers moving in
   opposite directions ("swamps, not compensates", now numeric).
   Closer (the series' only forward pointers, as use-cases): the weak
   LLN named via G&S Thm. 8.2 — the theorem this table computes
   instances of — promised with variance; average surprisal over the
   16 equal cells = 4 bits, one caption (entropy's other half now
   exists); and the per-frame distributions CTC consumes are pmfs
   like these — the softmax bridge is next.

Deliberately not covered (→ README Scope): continuous distributions
and densities (no integrals yet — named as the road not taken),
variance and the LLN proof (promised together), the binomial theorem
and Pascal's triangle (the (1,4,6,4,1) row may nod, never depend —
combinatorics owns them), the Galton board (physical boards are not
binomial machines; skipped by verification, not oversight), and
likelihood/softmax (3b1b's own binomial lesson pivots there — that is
the NEXT series' door).
