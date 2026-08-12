"""Answer anchors for the logarithms problem set (plan 012 R3).

Integer logs are counted from exponents, never read off a float log call
(plan 005's recorded hazard: math.log(243, 3) == 4.999...); floats appear
only where the float behaviour IS the claim (the underflow problem). Run:
prints `problem_id: answer`.
"""

from fractions import Fraction
from math import log2, log10


def int_log(base: int, value: Fraction) -> int:
    """Exact integer logarithm by counted multiplicative steps."""
    count = 0
    x = Fraction(value)
    while x > 1:
        x /= base
        count += 1
    while x < 1:
        x *= base
        count -= 1
    assert x == 1, "value is not an integer power of the base"
    return count


def p1_doublings() -> int:
    """log2(512) counted as doublings, checked against the exponent."""
    count = int_log(2, Fraction(512))
    assert 2**count == 512
    assert count == 9
    return count


def p2_log_of_a_sum() -> float:
    """log10(100 + 1000): the trap's true value, and the base-2 coincidence."""
    true_value = log10(100 + 1000)
    assert round(true_value, 4) == 3.0414
    assert 3 < true_value < 4  # nowhere near the claimed 5
    assert log10(100 * 1000) == 5.0  # the law converts products, not sums
    # The base-2 near-miss holds only because 2 + 2 == 2 * 2.
    assert 2 + 2 == 2 * 2
    assert log2(2 + 2) == 2.0
    return round(true_value, 4)


def p3_shrink_counts() -> str:
    """Negative logs as counted shrinkings: ten halvings, seven tenfoldings."""
    halvings = -int_log(2, Fraction(1, 1024))
    assert Fraction(1, 2) ** 10 == Fraction(1, 1024)
    assert halvings == 10
    ph = -int_log(10, Fraction(1, 10**7))
    assert ph == 7
    return f"-log2(1/1024) = {halvings}; pH of 1e-7 = {ph}"


def p4_evidence_ruler() -> str:
    """H, H, H, T at LR 9: odds by waterfall, position by base-3 ruler."""
    odds = Fraction(9) * 9 * 9 * Fraction(1, 9)
    assert odds == 81
    position = int_log(3, odds)
    assert position == 4  # +2 +2 +2 -2, counted on the ruler
    assert position == 2 + 2 + 2 - 2
    return f"ruler position {position}, odds {odds}:1"


def p5_cliff_and_logadd() -> str:
    """0.1^324 underflows float64; the counter row and the alpha-add survive."""
    product = 1.0
    for _ in range(324):
        product *= 0.1
    assert product == 0.0  # the cliff, by the running-product route
    assert 0.1**324 == 0.0  # and by the power route
    log_sum = 324 * int_log(10, Fraction(1, 10))
    assert log_sum == -324  # exact integer steps, no float log
    # The log-space addition: a = b = 2^-10, shifted term exactly 1.
    assert 2**-10 + 2**-10 == 2**-9
    identity = -10 + log2(1 + 2 ** (-10 - (-10)))
    assert identity == -9.0
    return f"product 0.0, log10 sum {log_sum}, log2(2^-10 + 2^-10) = -9"


ANSWERS = {
    "logarithms.1": p1_doublings,
    "logarithms.2": p2_log_of_a_sum,
    "logarithms.3": p3_shrink_counts,
    "logarithms.4": p4_evidence_ruler,
    "logarithms.5": p5_cliff_and_logadd,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
