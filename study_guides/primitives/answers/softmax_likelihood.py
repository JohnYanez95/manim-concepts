"""Answer anchors for the softmax-likelihood problem set (plan 012 R3).

Every answer is computed from definitions — softmax and LSE from their
formulas, the likelihood grid and its integral in exact fractions, the
underflow cliff on real float32 hardware — and asserted against plan
008's verified anchors. Run: prints `problem_id: answer`.
"""

from fractions import Fraction
from math import exp, isclose, log

import numpy as np


def softmax(z: list[float], temperature: float = 1.0) -> list[float]:
    """exp then normalize, with the subtract-max stabilisation the
    invariance licenses (plan 008 anchors B/C)."""
    top = max(z)
    exps = [exp((v - top) / temperature) for v in z]
    total = sum(exps)
    return [v / total for v in exps]


def p1_workhorse() -> str:
    """softmax(2, 1, 0) — plan 008 anchor A; the 4-dp roundings sum to 0.9999."""
    p = softmax([2.0, 1.0, 0.0])
    rounded = [round(v, 4) for v in p]
    assert rounded == [0.6652, 0.2447, 0.0900]
    assert isclose(sum(p), 1.0, rel_tol=0, abs_tol=1e-12)
    assert round(sum(rounded), 4) == 0.9999  # display, not defect
    # The smooth max the loss section reads its gap from (anchor L).
    lse = log(exp(2) + exp(1) + exp(0))
    assert round(lse, 4) == 2.4076
    assert [round(lse - z, 4) for z in (2, 1, 0)] == [0.4076, 1.4076, 2.4076]
    return f"({rounded[0]}, {rounded[1]}, {rounded[2]}), rounded sum 0.9999"


def p2_naive_normalizer() -> str:
    """z/sum(z) fails twice (plan 008 anchor A5); softmax is shift-invariant."""
    naive = [Fraction(v, 3) for v in (2, 1, 0)]
    shifted = [Fraction(v, 6) for v in (3, 2, 1)]
    assert naive == [Fraction(2, 3), Fraction(1, 3), Fraction(0)]  # score-0 class erased
    assert shifted == [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]  # shares moved
    assert naive != shifted
    for a, b in zip(softmax([2, 1, 0]), softmax([3, 2, 1]), strict=True):
        assert isclose(a, b, rel_tol=0, abs_tol=1e-12)  # exactly the same distribution
    return "naive (2/3, 1/3, 0) vs shifted (1/2, 1/3, 1/6); softmax unchanged"


def p3_base_two() -> str:
    """Base-2 softmax on (2, 1, 0) is exactly (4/7, 2/7, 1/7) — plan 008 anchor E."""
    powers = [Fraction(2**z) for z in (2, 1, 0)]
    total = sum(powers)
    shares = [v / total for v in powers]
    assert shares == [Fraction(4, 7), Fraction(2, 7), Fraction(1, 7)]
    # b^z = e^(z ln b): base 2 is base e at temperature T = 1/ln 2.
    for a, b in zip(shares, softmax([2, 1, 0], temperature=1 / log(2)), strict=True):
        assert isclose(float(a), b, rel_tol=0, abs_tol=1e-12)
    # The dial itself (anchor D): sharpen and flatten, winner unchanged.
    assert [round(v, 4) for v in softmax([2, 1, 0], temperature=0.5)] == [0.8668, 0.1173, 0.0159]
    assert [round(v, 4) for v in softmax([2, 1, 0], temperature=2.0)] == [0.5065, 0.3072, 0.1863]
    return "(4/7, 2/7, 1/7), = base e at T = 1/ln 2 = 1.4427"


def p4_likelihood_curve() -> str:
    """L(p) = 4 p^3 (1-p): values, peak at k/n, exact area 1/5 (anchors H, A2, A3)."""

    def curve(p: Fraction) -> Fraction:
        return 4 * p**3 * (1 - p)

    assert curve(Fraction(1, 4)) == Fraction(3, 64)
    assert curve(Fraction(1, 2)) == Fraction(1, 4)
    assert curve(Fraction(3, 4)) == Fraction(27, 64)
    grid = [Fraction(i, 1000) for i in range(1, 1000)]
    assert max(grid, key=curve) == Fraction(3, 4)  # the peak is k/n exactly
    # Exact polynomial integral: F(p) = p^4 - (4/5) p^5 on [0, 1].
    area = (1 - Fraction(4, 5)) - 0
    assert area == Fraction(1, 5) != 1  # a likelihood is not a distribution over p
    return "L = 3/64, 1/4, 27/64; peak at 3/4 = k/n; area 1/5"


def p5_frames_and_the_cliff() -> str:
    """Per-frame product 0.294 exactly, log-sum -1.2242; float32 dies at 46
    factors of 0.1 while the log walks to -105.9189 (anchors A4, J)."""
    path = [Fraction(7, 10), Fraction(6, 10), Fraction(7, 10)]
    prod = Fraction(1)
    for f in path:
        prod *= f
    assert prod == Fraction(147, 500)
    assert float(prod) == 0.294
    assert round(sum(log(float(f)) for f in path), 4) == -1.2242
    with np.errstate(under="ignore"):
        running = np.float32(1.0)
        for _ in range(45):
            running = np.float32(running * np.float32(0.1))
        assert running > 0  # 45 factors: the smallest subnormal survives
        running = np.float32(running * np.float32(0.1))
        assert running == 0.0  # the 46th lands exactly 0.0
    assert round(46 * log(0.1), 4) == -105.9189
    return "product 0.294, logs -1.2242; float32 dead at 46 factors, log at -105.9189"


ANSWERS = {
    "softmax-likelihood.1": p1_workhorse,
    "softmax-likelihood.2": p2_naive_normalizer,
    "softmax-likelihood.3": p3_base_two,
    "softmax-likelihood.4": p4_likelihood_curve,
    "softmax-likelihood.5": p5_frames_and_the_cliff,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
