"""Answer anchors for the inclusion–exclusion problem set (plan 016, ADR 008).

Every answer is computed by exact enumeration with Fractions — the same
route plan 016's verifier used for the on-screen anchors — and every formula
the solutions teach is asserted against the enumeration. Run: prints
`problem_id: answer`.
"""

from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, factorial, gcd

DIE = range(1, 7)


def _ie(events: list[set], total: int) -> Fraction:
    """Inclusion–exclusion over any number of events on a finite space."""
    n = len(events)
    acc = Fraction(0)
    for k in range(1, n + 1):
        for subset in combinations(events, k):
            acc += Fraction((-1) ** (k + 1) * len(set.intersection(*subset)), total)
    return acc


def p1_one_die() -> str:
    """A = at most 3, B = a multiple of 3: the overlap {3} counted twice."""
    a, b = {1, 2, 3}, {3, 6}
    union = Fraction(len(a | b), 6)
    assert union == Fraction(3, 6) + Fraction(2, 6) - Fraction(1, 6) == Fraction(2, 3)
    exactly_one = Fraction(len(a ^ b), 6)
    assert exactly_one == Fraction(3, 6) + Fraction(2, 6) - 2 * Fraction(1, 6) == Fraction(1, 2)
    return "P(A or B) = 2/3; exactly one = 1/2"


def p2_three_events_two_dice() -> str:
    """Three events on the 36-cell grid, with the (6, 6) ledger."""
    cells = {(x, y) for x in DIE for y in DIE}
    a = {c for c in cells if c[0] >= 5}
    b = {c for c in cells if c[1] >= 5}
    c = {c for c in cells if sum(c) >= 11}
    sizes = (len(a), len(b), len(c), len(a & b), len(a & c), len(b & c), len(a & b & c))
    assert sizes == (12, 12, 3, 4, 3, 3, 3)
    union = Fraction(len(a | b | c), 36)
    assert (
        union == _ie([a, b, c], 36) == Fraction(12 + 12 + 3 - 4 - 3 - 3 + 3, 36) == Fraction(5, 9)
    )
    star = (6, 6)
    plus = sum(star in s for s in (a, b, c))
    minus = sum(star in (s & t) for s, t in combinations((a, b, c), 2))
    triple = int(star in (a & b & c))
    assert (plus, plus - minus, plus - minus + triple) == (3, 0, 1)
    return "sizes 12,12,3 | 4,3,3 | 3; P = 20/36 = 5/9; (6,6) reads 3, 0, 1"


def p3_five_hats() -> str:
    """Five hats: at least one match, and D(5)."""
    perms = list(permutations(range(5)))
    derangements = sum(1 for p in perms if all(p[i] != i for i in range(5)))
    at_least_one = Fraction(len(perms) - derangements, len(perms))
    series = sum(Fraction((-1) ** (k + 1), factorial(k)) for k in range(1, 6))
    assert derangements == 44 and at_least_one == series == Fraction(19, 30)
    return "P(at least one match) = 19/30; D(5) = 44"


def p4_three_rolls() -> str:
    """At least one six in three rolls: inclusion–exclusion, complement, brackets."""
    rolls = list(product(DIE, repeat=3))
    events = [{r for r in rolls if r[i] == 6} for i in range(3)]
    union = Fraction(len(set.union(*events)), 216)
    terms = [Fraction(3, 6), Fraction(-3, 36), Fraction(1, 216)]
    assert union == sum(terms) == 1 - Fraction(5, 6) ** 3 == Fraction(91, 216)
    s1, s2 = terms[0], terms[0] + terms[1]
    assert s2 == Fraction(5, 12) <= union <= s1 == Fraction(1, 2)
    return "3/6 - 3/36 + 1/216 = 91/216 = 1 - 125/216; brackets 5/12 <= 91/216 <= 1/2"


def p5_bernstein_other_form() -> str:
    """Bernstein's other example: pairwise independent, triple 1/4, union 1."""
    omega = {1, 2, 3, 4}
    a, b, c = {1, 2}, {1, 3}, {1, 4}

    def prob(s: set) -> Fraction:
        return Fraction(len(s), len(omega))

    for x, y in combinations((a, b, c), 2):
        assert prob(x & y) == prob(x) * prob(y) == Fraction(1, 4)
    assert prob(a & b & c) == Fraction(1, 4) != Fraction(1, 8)
    union = prob(a | b | c)
    assert union == _ie([a, b, c], 4) == 1
    shortcut = 1 - (1 - prob(a)) * (1 - prob(b)) * (1 - prob(c))
    assert shortcut == Fraction(7, 8) and shortcut - union == Fraction(-1, 8)
    return "pairs 1/4 each; triple 1/4; union 1; shortcut 7/8, low by 1/8"


def p6_sieve_sixty() -> str:
    """1..60 divisible by 2, 3 or 5 — the counting form of the same rule."""
    numbers = range(1, 61)
    d = [{x for x in numbers if x % m == 0} for m in (2, 3, 5)]
    covered = len(set.union(*d))
    assert covered == 30 + 20 + 12 - 10 - 6 - 4 + 2 == 44
    survivors = sum(1 for x in numbers if gcd(x, 30) == 1)
    assert survivors == 60 - covered == 16
    return "44 covered; 16 survivors"


def p7_toggle_pairing() -> str:
    """The toggle pairing for k = 5, and the alternating binomial sum."""
    k = 5
    subsets = [frozenset(s) for r in range(1, k + 1) for s in combinations(range(1, k + 1), r)]
    paired = [s for s in subsets if s ^ {1}]
    survivors = [s for s in subsets if not (s ^ {1})]
    assert len(paired) == 30 and len(subsets) == 31 and survivors == [frozenset({1})]
    partials, acc = [], 0
    for j in range(1, k + 1):
        acc += (-1) ** (j + 1) * comb(k, j)
        partials.append(acc)
    assert partials == [5, -5, 5, 0, 1]
    # the ledger form of Benjamin–Quinn's partial-sum identity — the one on screen
    assert partials == [1 - (-1) ** m * comb(k - 1, m) for m in range(1, k + 1)]
    assert [1 - (-1) ** m * comb(3, m) for m in range(1, 5)] == [4, -2, 2, 1]
    return "30 subsets in 15 pairs; {1} survives; partial sums 5, -5, 5, 0, 1"


def p8_union_bound() -> str:
    """Five events at 0.02: Boole's bound against the independent exact value."""
    p = Fraction(2, 100)
    bound = 5 * p
    exact = 1 - (1 - p) ** 5
    assert bound == Fraction(1, 10) and exact < bound
    assert f"{float(exact):.6f}" == "0.096079"
    return "bound 0.10; exact if independent 0.096079"


ANSWERS = {
    "inclusion-exclusion.1": p1_one_die,
    "inclusion-exclusion.2": p2_three_events_two_dice,
    "inclusion-exclusion.3": p3_five_hats,
    "inclusion-exclusion.4": p4_three_rolls,
    "inclusion-exclusion.5": p5_bernstein_other_form,
    "inclusion-exclusion.6": p6_sieve_sixty,
    "inclusion-exclusion.7": p7_toggle_pairing,
    "inclusion-exclusion.8": p8_union_bound,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
