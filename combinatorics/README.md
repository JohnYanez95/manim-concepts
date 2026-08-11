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
| 2 | `PermutationRule` | $P^n_r = \dfrac{n!}{(n-r)!}$ | Order matters | Slot-filling from a shrinking pool (5, 4, 3), then the factorial identity by cancelling the unwanted tail $2 \times 1$. | Ranking and scheduling — top-$r$ orderings, seatings, any arrangement where swapping two items gives a different answer. |
| 3 | `CombinationRule` | $C^n_r = \dbinom{n}{r} = \dfrac{n!}{r!\,(n-r)!}$ | Order does not matter | The $3!$ orderings of $\{A,C,E\}$ collapse to one set — every combination was overcounted $r!$ times, so divide. | Sampling without replacement, and every binomial coefficient downstream of it: the binomial distribution, Pascal's triangle, $(x+y)^n$. |
| 4 | `PartitionRule` | $N = \dfrac{n!}{n_1!\,n_2!\cdots n_k!}$ | Split into labelled groups | $6!$ row orderings chopped into blocks of 3/2/1, then divide out the within-block orderings that change nothing. | Multinomial coefficients: dividing into teams, arrangements of a word with repeated letters, and counting the alignments a sequence model can take — the counting step behind CTC. |
| 5 | `WhenToUseIt` | — | Which rule a problem needs | Four problem shapes mapped to the rule each one calls for, then the observation that all four are the product rule with unwanted orderings divided out. | Reading an unfamiliar counting problem and knowing which tool it wants — the step between having the formulas and being able to use them. |

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

Unchecked means **unverified** — see
[reference verification](../README.md#reference-verification-is-human-gated).
Every entry below was suggested rather than confirmed, so all of them start
unchecked. Open one, confirm it covers what the entry claims, and tick it
yourself; nothing automated will.

- [ ] [Rule of product](https://en.wikipedia.org/wiki/Rule_of_product) — the
      multiplicative rule and its independence assumption.
- [ ] [Permutation](https://en.wikipedia.org/wiki/Permutation) — the $k$-
      permutation case that `PermutationRule` animates.
- [ ] [Combination](https://en.wikipedia.org/wiki/Combination) — binomial
      coefficients and the overcounting argument.
- [ ] [Multinomial theorem](https://en.wikipedia.org/wiki/Multinomial_theorem)
      — the multinomial coefficient behind `PartitionRule`.
- [ ] [Twelvefold way](https://en.wikipedia.org/wiki/Twelvefold_way) — the
      map of which counting problem is which; useful for deciding what the
      scenes above are *not* covering.

## Ideas not yet built

Rough queue, in roughly the order they build on each other:

- Pascal's triangle as the recurrence $\binom{n}{r} = \binom{n-1}{r-1} +
  \binom{n-1}{r}$, animated as a choice being made about one element.
- Stars and bars, for combinations *with* repetition.
- Inclusion–exclusion on two and three overlapping sets.
- The binomial theorem, as the multiplicative rule applied to $(x+y)^n$.
