"""Answer anchors for the random-variables problem set (plan 012 R3).

Every distribution is enumerated over the stamped sample space AND checked
against the formula it teaches (plan 007's two-routes discipline); all
exact values are Fractions, floats only where a decimal display is the
claim. Run: prints `problem_id: answer`.
"""

from fractions import Fraction
from itertools import product
from math import comb, exp


def p1_three_flips() -> str:
    """Sort the eight three-flip cells by head count: (1, 3, 3, 1)/8."""
    counts = [0] * 4
    for cells in product("HT", repeat=3):
        counts[cells.count("H")] += 1
    assert counts == [1, 3, 3, 1]
    assert counts == [comb(3, k) for k in range(4)]
    assert sum(counts) == 8
    return "(1, 3, 3, 1)/8"


def p2_balance_points() -> str:
    """Fair die 7/2; biased die (double weight on 6) 27/7 — neither a face."""
    fair = Fraction(sum(range(1, 7)), 6)
    assert fair == Fraction(7, 2)
    weights = [1, 1, 1, 1, 1, 2]
    biased = Fraction(sum(f * w for f, w in zip(range(1, 7), weights, strict=True)), sum(weights))
    assert biased == Fraction(27, 7)
    faces = set(range(1, 7))
    assert fair not in faces and biased not in faces
    return "fair 7/2 = 3.5, biased 27/7"


def p3_two_dice() -> str:
    """E of the two-dice sum: by the diagonal distribution AND by linearity."""
    outcomes = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    diag = [sum(1 for a, b in outcomes if a + b == s) for s in range(2, 13)]
    assert diag == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    by_distribution = Fraction(sum(s * c for s, c in zip(range(2, 13), diag, strict=True)), 36)
    by_enumeration = Fraction(sum(a + b for a, b in outcomes), 36)
    by_linearity = Fraction(7, 2) + Fraction(7, 2)
    assert by_distribution == by_enumeration == by_linearity == 7
    return "E = 7 (distribution route and 3.5 + 3.5)"


def p4_binomial_quarter() -> str:
    """Binomial(4, 1/4) by cells-times-area AND weighted enumeration; E = np."""
    p, q = Fraction(1, 4), Fraction(3, 4)
    formula = [comb(4, k) * p**k * q ** (4 - k) for k in range(5)]
    enumerated = [Fraction(0)] * 5
    for cells in product("HT", repeat=4):
        k = cells.count("H")
        enumerated[k] += p**k * q ** (4 - k)
    assert formula == enumerated
    assert [w * 256 for w in formula] == [81, 108, 54, 12, 1]
    assert sum(formula) == 1
    one_head_cell = p * q**3
    assert one_head_cell == Fraction(27, 256) and comb(4, 1) == 4
    expectation = sum(k * w for k, w in enumerate(formula))
    assert expectation == 1 == 4 * p
    return "(81, 108, 54, 12, 1)/256, E = 1 both routes"


def p5_zero_successes() -> str:
    """(1 - 1/n)^n at n = 10, 100 crowds 1/e from below."""
    exact10 = Fraction(9, 10) ** 10
    assert exact10 == Fraction(3486784401, 10**10)  # terminates exactly
    assert float(exact10) == 0.3486784401
    exact100 = Fraction(99, 100) ** 100
    assert round(float(exact100), 6) == 0.366032  # plan 007's addendum row
    one_over_e = exp(-1)
    assert round(one_over_e, 6) == 0.367879
    assert float(exact10) < float(exact100) < one_over_e  # from below, in order
    return "0.3486784401, 0.366032 -> 1/e = 0.367879, always from below"


ANSWERS = {
    "random-variables.1": p1_three_flips,
    "random-variables.2": p2_balance_points,
    "random-variables.3": p3_two_dice,
    "random-variables.4": p4_binomial_quarter,
    "random-variables.5": p5_zero_successes,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
