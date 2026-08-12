"""Answer anchors for the independence problem set (plan 012 R3).

Every answer is computed by exact enumeration with Fractions — the same
no-floats route plan 002's research pass used — and every formula the
solutions teach is asserted against the enumeration. Run: prints
`problem_id: answer`.
"""

from fractions import Fraction
from itertools import product

DIE = range(1, 7)


def p1_two_dice_rectangle() -> Fraction:
    """A = first die in {5,6}, B = second in {1,2,3} — a 2x3 rectangle."""
    outcomes = list(product(DIE, DIE))
    joint = Fraction(sum(1 for a, b in outcomes if a in {5, 6} and b in {1, 2, 3}), 36)
    p_a = Fraction(sum(1 for a, _ in outcomes if a in {5, 6}), 36)
    p_b = Fraction(sum(1 for _, b in outcomes if b in {1, 2, 3}), 36)
    assert joint == p_a * p_b == Fraction(1, 3) * Fraction(1, 2) == Fraction(1, 6)
    assert joint == Fraction(2 * 3, 36)  # the rectangle: |S| * |T| cells
    return joint


def p2_one_die_two_events() -> str:
    """The jewel: even vs {1,2,3,4} factors; even vs {1,2,3} does not."""
    even = {2, 4, 6}

    def check(b: set[int]) -> tuple[Fraction, Fraction]:
        joint = Fraction(len(even & b), 6)
        return joint, Fraction(len(even), 6) * Fraction(len(b), 6)

    j1, prod1 = check({1, 2, 3, 4})
    j2, prod2 = check({1, 2, 3})
    assert j1 == prod1 == Fraction(1, 3)
    assert j2 == Fraction(1, 6) != prod2 == Fraction(1, 4)
    return "B={1,2,3,4}: 1/3 = 1/3 independent; B={1,2,3}: 1/6 != 1/4 dependent"


def p3_disjoint_not_independent() -> str:
    """A = even, B = {1,3,5}: disjoint with positive probability."""
    even, odd = {2, 4, 6}, {1, 3, 5}
    joint = Fraction(len(even & odd), 6)
    prod = Fraction(len(even), 6) * Fraction(len(odd), 6)
    assert joint == 0 != prod == Fraction(1, 4)
    return "P(A and B) = 0, P(A)P(B) = 1/4 — maximally dependent"


def p4_bernstein() -> str:
    """Two fair coins: pairwise independence without mutual independence."""
    outcomes = list(product("HT", repeat=2))  # each with probability 1/4

    def prob(pred) -> Fraction:
        return Fraction(sum(1 for w in outcomes if pred(w)), 4)

    a = lambda w: w[0] == "H"  # noqa: E731
    b = lambda w: w[1] == "H"  # noqa: E731
    c = lambda w: (w[0] == "H") != (w[1] == "H")  # noqa: E731  exactly one head
    for x, y in ((a, b), (a, c), (b, c)):
        assert prob(lambda w, x=x, y=y: x(w) and y(w)) == prob(x) * prob(y) == Fraction(1, 4)
    triple = prob(lambda w: a(w) and b(w) and c(w))
    assert triple == 0 != prob(a) * prob(b) * prob(c) == Fraction(1, 8)
    return "all three pairs factor (1/4 each); triple: 0 != 1/8"


def p5_aces() -> str:
    """Two cards: replacement restores 1/169, depletion gives 1/221."""
    deck = range(52)
    aces = set(range(4))
    without = [(x, y) for x in deck for y in deck if x != y]
    both_without = Fraction(sum(1 for x, y in without if x in aces and y in aces), len(without))
    second_ace = Fraction(sum(1 for _, y in without if y in aces), len(without))
    with_repl = [(x, y) for x in deck for y in deck]
    both_with = Fraction(sum(1 for x, y in with_repl if x in aces and y in aces), len(with_repl))
    assert both_without == Fraction(4, 52) * Fraction(3, 51) == Fraction(1, 221)
    assert both_with == Fraction(1, 13) ** 2 == Fraction(1, 169)
    assert second_ace == Fraction(1, 13)  # 204/2652 — depletion never reaches an unseen card
    return "without: 1/221; with: 1/169; P(second is ace) = 1/13 either way"


ANSWERS = {
    "independence.1": p1_two_dice_rectangle,
    "independence.2": p2_one_die_two_events,
    "independence.3": p3_disjoint_not_independent,
    "independence.4": p4_bernstein,
    "independence.5": p5_aces,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
