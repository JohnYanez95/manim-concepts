"""Answer anchors for the conditional-probability problem set (plan 012 R3).

Exact Fractions throughout; every conditional probability is computed both
by the definition and by the recount-inside-the-restriction route the
chapter teaches, and the two must agree. Run: prints `problem_id: answer`.
"""

from fractions import Fraction
from itertools import product


def p1_three_coins() -> str:
    """P(HHH) = 1/8 unconditionally, 1/4 given the first coin is heads."""
    outcomes = ["".join(w) for w in product("HT", repeat=3)]
    prior = Fraction(sum(1 for w in outcomes if w == "HHH"), 8)
    restricted = [w for w in outcomes if w[0] == "H"]
    recount = Fraction(sum(1 for w in restricted if w == "HHH"), len(restricted))
    definition = Fraction(sum(1 for w in outcomes if w == "HHH" and w[0] == "H"), 8) / Fraction(
        len(restricted), 8
    )
    assert prior == Fraction(1, 8)
    assert recount == definition == Fraction(1, 4)
    return "1/8 unconditionally; 1/4 given the first is heads"


def p2_aces_licensed() -> str:
    """The multiplication rule prices the aces: (4/52)(3/51) = 1/221."""
    deck = range(52)
    aces = set(range(4))
    pairs = [(x, y) for x in deck for y in deck if x != y]
    joint = Fraction(sum(1 for x, y in pairs if x in aces and y in aces), len(pairs))
    p_first = Fraction(sum(1 for x, _ in pairs if x in aces), len(pairs))
    cond = joint / p_first  # P(second ace | first ace) by the definition
    assert p_first == Fraction(4, 52) and cond == Fraction(3, 51)
    assert joint == p_first * cond == Fraction(1, 221)
    return "P(A1)P(A2|A1) = (4/52)(3/51) = 1/221"


def p3_urn_lotp() -> str:
    """Urn, 5 red 2 blue, two draws without replacement: P(R2) by LOTP."""
    urn = ["R"] * 5 + ["B"] * 2
    pairs = [(i, j) for i in range(7) for j in range(7) if i != j]
    p_r2 = Fraction(sum(1 for i, j in pairs if urn[j] == "R"), len(pairs))
    p_r1 = Fraction(sum(1 for i, _ in pairs if urn[i] == "R"), len(pairs))
    # LOTP over the first draw: P(R2) = P(R1)P(R2|R1) + P(B1)P(R2|B1)
    lotp = Fraction(5, 7) * Fraction(4, 6) + Fraction(2, 7) * Fraction(5, 6)
    assert p_r2 == lotp == p_r1 == Fraction(5, 7)
    return "P(R2) = 5/7 by LOTP and by enumeration; equals P(R1)"


def p4_prevalence_pair() -> str:
    """One test (sens 9/10, FPR 1/10), two prevalences: 1/2 vs 1/12."""

    def posterior(cohort: int, sick: int) -> tuple[int, int, Fraction]:
        sick_pos = sick * 9 // 10
        healthy_pos = (cohort - sick) // 10
        return sick_pos, healthy_pos, Fraction(sick_pos, sick_pos + healthy_pos)

    sp1, hp1, high = posterior(100, 10)  # prevalence 1/10
    sp2, hp2, low = posterior(1000, 10)  # prevalence 1/100
    assert (sp1, hp1) == (9, 9) and high == Fraction(9, 18) == Fraction(1, 2)
    assert (sp2, hp2) == (9, 99) and low == Fraction(9, 108) == Fraction(1, 12)
    # definition route agrees: P(sick|+) = P(sick)P(+|sick) / P(+)
    for prev, expected in ((Fraction(1, 10), high), (Fraction(1, 100), low)):
        p_pos = prev * Fraction(9, 10) + (1 - prev) * Fraction(1, 10)
        assert prev * Fraction(9, 10) / p_pos == expected
    return "prevalence 1/10: 9/18 = 1/2; prevalence 1/100: 9/108 = 1/12"


def p5_conditional_independence() -> str:
    """Two coins (9/10 vs 1/10 heads): dependent marginally, CI given the coin."""
    heads = {"good": Fraction(9, 10), "bad": Fraction(1, 10)}

    def prob(pred) -> Fraction:
        total = Fraction(0)
        for coin in heads:
            for f1, f2 in product("HT", repeat=2):
                w = Fraction(1, 2)
                for f in (f1, f2):
                    w *= heads[coin] if f == "H" else 1 - heads[coin]
                if pred(coin, f1, f2):
                    total += w
        return total

    joint = prob(lambda c, f1, f2: f1 == "H" and f2 == "H")
    p_h1 = prob(lambda c, f1, f2: f1 == "H")
    p_h2 = prob(lambda c, f1, f2: f2 == "H")
    assert p_h1 == p_h2 == Fraction(1, 2)
    assert joint == Fraction(41, 100) != p_h1 * p_h2 == Fraction(1, 4)
    # given the coin, the product form is restored exactly
    for coin, p in heads.items():
        joint_c = prob(lambda c, f1, f2, k=coin: c == k and f1 == "H" and f2 == "H")
        p_coin = Fraction(1, 2)
        assert joint_c / p_coin == p * p
    return "P(H1 and H2) = 41/100 != 1/4; given the coin, it factors"


ANSWERS = {
    "conditional-probability.1": p1_three_coins,
    "conditional-probability.2": p2_aces_licensed,
    "conditional-probability.3": p3_urn_lotp,
    "conditional-probability.4": p4_prevalence_pair,
    "conditional-probability.5": p5_conditional_independence,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
