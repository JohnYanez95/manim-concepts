"""Answer anchors for the derivative-toolkit problem set (plan 012 R3).

Forward quotients are computed in exact fractions wherever the chapter's
tables are exact (plan 009 anchor A: the entries of the x^2 table are
literally 2 + h); the softmax/LSE closer is checked by finite
differences against the analytic gradient. Run: prints
`problem_id: answer`.
"""

from fractions import Fraction
from math import exp, isclose, log


def softmax(z: list[float]) -> list[float]:
    exps = [exp(v - max(z)) for v in z]
    total = sum(exps)
    return [v / total for v in exps]


def lse(z: list[float]) -> float:
    top = max(z)
    return top + log(sum(exp(v - top) for v in z))


def p1_forward_quotients() -> str:
    """((1+h)^2 - 1)/h = 2 + h exactly; the symmetric quotient is exactly 2."""
    values = []
    for h in (Fraction(1), Fraction(1, 10), Fraction(1, 100)):
        q = ((1 + h) ** 2 - 1) / h
        assert q == 2 + h  # settling = the step fading out of the answer
        values.append(float(q))
        sym = ((1 + h) ** 2 - (1 - h) ** 2) / (2 * h)
        assert sym == 2  # the quadratic's exact symmetric quotient — the aside
    assert values == [3.0, 2.1, 2.01]
    return "3, 2.1, 2.01 -> 2 (entries are 2 + h exactly)"


def p2_chain_rule() -> str:
    """(2x)^2 at x = 1: inner 2 x outer 4 = 8; quotients 8.4, 8.04 refute 4."""
    inner, outer_at_u2 = 2, 2 * 2
    assert inner * outer_at_u2 == 8
    quotients = []
    for h in (Fraction(1, 10), Fraction(1, 100)):
        q = (4 * (1 + h) ** 2 - 4) / h
        assert q == 8 + 4 * h
        quotients.append(float(q))
    assert quotients == [8.4, 8.04]
    assert all(q > 4 + 1 for q in quotients)  # nowhere near the mistaken 4
    return "8 (quotients 8.4, 8.04); outer rate lives at u = 2, not x = 1"


def p3_ln_derivative() -> str:
    """ln' = 1/x via the undo trick; quotients at x = 2 settle on 1/2."""
    rounded = [round((log(2 + h) - log(2)) / h, 4) for h in (1e-1, 1e-2, 1e-3)]
    assert rounded == [0.4879, 0.4988, 0.4999]  # plan 009 anchor D
    # The undo route lands exactly: x * (ln x)' = 1 at any x > 0.
    assert isclose(2 * 0.5, 1.0)
    return "0.4879, 0.4988, 0.4999 -> 1/2 = 1/x at x = 2"


def p4_score_function() -> str:
    """Score 3/p - 1/(1-p): +4, +20/21, -5/4; zero at 3/4; general k/n."""

    def score(p: Fraction) -> Fraction:
        return 3 / p - 1 / (1 - p)

    assert score(Fraction(1, 2)) == 4
    assert score(Fraction(7, 10)) == Fraction(20, 21)
    assert round(float(score(Fraction(7, 10))), 4) == 0.9524
    assert score(Fraction(3, 4)) == 0
    assert score(Fraction(8, 10)) == Fraction(-5, 4)
    # The general zero: k(1-p) = (n-k)p at p = k/n, for several (k, n).
    for k, n in ((3, 4), (7, 10), (1, 6)):
        p_hat = Fraction(k, n)
        assert k * (1 - p_hat) == (n - k) * p_hat
    return "score +4, +0.9524, 0, -1.25; zero solves to p = 3/4 = k/n"


def p5_smoothmax_shares() -> str:
    """grad NLL = p - one-hot at z = (2,1,0); the saturation walk (never -1.0000)."""
    z = [2.0, 1.0, 0.0]
    p = softmax(z)
    # dLSE/dz_i = softmax_i, checked by symmetric finite differences.
    for i in range(3):
        bumped = list(z)
        bumped[i] += 1e-6
        dipped = list(z)
        dipped[i] -= 1e-6
        fd = (lse(bumped) - lse(dipped)) / 2e-6
        assert isclose(fd, p[i], rel_tol=0, abs_tol=1e-9)
    grad = [p[0] - 1, p[1], p[2]]
    assert [round(g, 4) for g in grad] == [-0.3348, 0.2447, 0.0900]
    assert isclose(sum(grad), 0.0, rel_tol=0, abs_tol=1e-12)
    # The nudge beat: z_1 -> 2.01 moves LSE by e^2's share of the total.
    assert round(lse([2.01, 1.0, 0.0]) - lse(z), 5) == 0.00666
    # Saturation: slope p_c - 1 on z = (2, 1, t), truth in the third slot.
    walk = [round(softmax([2.0, 1.0, t])[2] - 1, 4) for t in (0.0, -2.0, -5.0)]
    assert walk == [-0.9100, -0.9868, -0.9993]
    assert all(w > -1 for w in walk)  # -1 is a limit, never reached
    return "(-0.3348, 0.2447, 0.0900) = p - one-hot; walk -0.9100, -0.9868, -0.9993"


ANSWERS = {
    "derivative-toolkit.1": p1_forward_quotients,
    "derivative-toolkit.2": p2_chain_rule,
    "derivative-toolkit.3": p3_ln_derivative,
    "derivative-toolkit.4": p4_score_function,
    "derivative-toolkit.5": p5_smoothmax_shares,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
