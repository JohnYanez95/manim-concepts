"""Answer anchors for the e-and-ln problem set (plan 012 R3).

Exact Fractions wherever the claim is exact (the split-year table); floats
only where the float behaviour or a settling decimal IS the claim, checked
against plan 006's verified rows. Run: prints `problem_id: answer`.
"""

from fractions import Fraction
from math import e, exp, isclose, log, log1p


def p1_split_year() -> str:
    """(1+1/2)^2 and (1+1/4)^4 exactly: increasing, and under the ceiling."""
    half_year = Fraction(3, 2) ** 2
    quarterly = Fraction(5, 4) ** 4
    assert half_year == Fraction(9, 4)
    assert quarterly == Fraction(625, 256)
    assert half_year < quarterly < 3  # climbs, yet under Bernoulli's ceiling
    assert float(half_year) == 2.25
    assert round(float(quarterly), 4) == 2.4414  # plan 006's table row
    return "9/4 = 2.25, 625/256 = 2.4414..., increasing and < 3"


def p2_settling_ratio() -> str:
    """(2^dt - 1)/dt at dt = 0.1, 0.01, 0.001 settles toward ln 2."""
    ratios = [(2**dt - 1) / dt for dt in (0.1, 0.01, 0.001)]
    assert round(ratios[0], 4) == 0.7177  # plan 006's one-sided rows
    assert round(ratios[1], 4) == 0.6956
    assert round(ratios[2], 5) == 0.69339
    gaps = [abs(r - log(2)) for r in ratios]
    assert gaps[0] > gaps[1] > gaps[2]  # each row closer to ln 2
    return "0.7177, 0.6956, 0.69339 -> ln 2 = 0.6931..."


def p3_stride_arithmetic() -> float:
    """Base 32's constant is five base-2 strides: 5 ln 2 = ln 32."""
    assert isclose(log(32), 5 * log(2), rel_tol=1e-12)
    value = round(log(32), 4)
    assert value == 3.4657
    return value


def p4_doubling_time() -> str:
    """Doubling at 2% continuous: ln 2 / 0.02, vs the rule of 72."""
    years = log(2) / 0.02
    assert round(years, 2) == 34.66
    rule72 = 72 / 2
    assert rule72 == 36.0
    return f"ln 2 / 0.02 = {round(years, 2)} years (rule of 72 says {rule72:.0f})"


def p5_repaid_identity() -> str:
    """ln(e^-1000 + e^-1001): naive route dead, identity route fine."""
    assert exp(-1000) == 0.0  # the naive route asks for log(0)
    stable = -1000 + log1p(exp(-1))  # factor out the larger term
    other = -1001 + log1p(e)  # factor out the smaller: ln(1 + e) route
    assert isclose(stable, other, rel_tol=1e-14)
    assert round(stable, 4) == -999.6867
    return f"identity: {round(stable, 4)}; naive: log(0.0), the cliff"


ANSWERS = {
    "e-and-ln.1": p1_split_year,
    "e-and-ln.2": p2_settling_ratio,
    "e-and-ln.3": p3_stride_arithmetic,
    "e-and-ln.4": p4_doubling_time,
    "e-and-ln.5": p5_repaid_identity,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
