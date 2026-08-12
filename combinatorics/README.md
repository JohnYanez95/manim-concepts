# Combinatorics

## Scope

Counting arguments over finite sets: how many arrangements or selections exist,
and why the formula for each has the shape it does. Each scene shows the
objects being counted, counts them by hand, and only then writes down the
expression that summarises what just happened.

Covered: the four elementary counting rules — product, permutation,
combination, partition — and the relationships between them (a combination is
a permutation with the orderings divided out; a partition is the same move
applied blockwise).

Deliberately **not** covered here:

- Probability. Counting outcomes is a prerequisite for it, not part of it —
  anything that divides by a sample space belongs in `probability/`.
- Generating functions and asymptotic counting. Different machinery, and the
  visual argument would be about power series rather than about objects.
- Graph and design combinatorics.

## Concepts

### counting_rules_manim.py

Watch in order. The first two establish how to count arrangements — the product
rule, then the same product written in factorial form. Dividing out an
overcount only starts at the third: `CombinationRule` removes the $r!$
orderings of a chosen set, and `PartitionRule` applies that same move blockwise.
So `PartitionRule` does not land without `CombinationRule` before it.

| # | Scene | Formula | What it says | Why it's true | When it's useful |
| --- | --- | --- | --- | --- | --- |
| 1 | `MultiplicativeRule` | $N = n_1 n_2 \cdots n_k$ | Independent stages multiply | A tree with $3 \times 4 = 12$ leaf paths, re-cast as a grid so the product is literally the area of a rectangle. | Sizing any search space before you try to enumerate it: keyspaces, configuration counts, the branching factor of a lattice. The first question to ask of "can I just list them all?" |
| 2 | `PermutationRule` | $P^n_r = \dfrac{n!}{(n-r)!}$ | Order matters | Slot-filling from a shrinking pool (5, 4, 3), then the factorial identity by cancelling the unwanted tail $2 \times 1$. | Ranking and scheduling — top-$r$ orderings, seatings, any arrangement where swapping two items gives a different answer. The shrinking pool is also sampling *without replacement* — the move that breaks independence in [`probability/`](../probability/README.md). |
| 3 | `CombinationRule` | $C^n_r = \dbinom{n}{r} = \dfrac{n!}{r!\,(n-r)!}$ | Order does not matter | The $3!$ orderings of $\{A,C,E\}$ collapse to one set — every combination was overcounted $r!$ times, so divide. | Sampling without replacement, and every binomial coefficient downstream of it: the binomial distribution — now delivered by [`probability/`](../probability/README.md)'s random-variables series, whose `TheBinomialColumns` counts this scene's C(4,k) as sorted-column cells — plus Pascal's triangle and $(x+y)^n$, still queued. |
| 4 | `PartitionRule` | $N = \dfrac{n!}{n_1!\,n_2!\cdots n_k!}$ | Split into labelled groups | $6!$ row orderings chopped into blocks of 3/2/1, then divide out the within-block orderings that change nothing. | Multinomial coefficients: dividing into teams, arrangements of a word with repeated letters. The related — differently constrained — alignment count behind [CTC](../deep_learning/README.md) builds on the same divide-out move. |
| 5 | `WhenToUseIt` | — | Which rule a problem needs | Four problem shapes mapped to the rule each one calls for, then the closing observation, worded with care: multiply the choices — divide only when orderings mean the same outcome (the product rule itself divides nothing). | Reading an unfamiliar counting problem and knowing which tool it wants — the step between having the formulas and being able to use them. |

Renders are numbered to match, so a directory listing plays in the same order:
`01_MultiplicativeRule.mp4` … `05_WhenToUseIt.mp4`.

Render them:

```bash
uv run python combinatorics/counting_rules_manim.py                     # all five, 1080p60
uv run python combinatorics/counting_rules_manim.py --list
uv run python combinatorics/counting_rules_manim.py -s PermutationRule -q draft
```

See the [root README](../README.md) for the full flag list.

## References

Ticks are human-gated — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below was suggested unverified and started unchecked; all
were then opened, confirmed, and ticked by the maintainer. Future
entries start unchecked until a human does the same.

- [X] [Rule of product](https://en.wikipedia.org/wiki/Rule_of_product) — the
      multiplicative rule and its independence assumption.
- [X] [Permutation](https://en.wikipedia.org/wiki/Permutation) — the $k$-
      permutation case that `PermutationRule` animates.
- [X] [Combination](https://en.wikipedia.org/wiki/Combination) — binomial
      coefficients and the overcounting argument.
- [X] [Multinomial theorem](https://en.wikipedia.org/wiki/Multinomial_theorem)
      — the multinomial coefficient behind `PartitionRule`.
- [X] [Twelvefold way](https://en.wikipedia.org/wiki/Twelvefold_way) — the
      map of which counting problem is which; useful for deciding what the
      scenes above are *not* covering.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- Pascal's triangle as the recurrence $\binom{n}{r} = \binom{n-1}{r-1} +
  \binom{n-1}{r}$, animated as a choice being made about one element.
- Stars and bars, for combinations *with* repetition.
- Inclusion–exclusion on two and three overlapping sets.
- The binomial theorem, as the multiplicative rule applied to $(x+y)^n$.
- A fifth problem shape in `WhenToUseIt` — counting a sequence model's
  alignments, now that `deep_learning/` delivers the payoff. Needs a
  re-render, so batched for the next combinatorics change. The study
  guide has pre-drafted this shape's visual: the walker's-lattice
  problem (guide problem 1.5, C(6,2) = 15 routes) and its glue
  transition are the picture, ready to animate.
