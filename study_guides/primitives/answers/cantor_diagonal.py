"""Answer anchors for the Cantor's-diagonal problem set (plan 017, ADR 008).

Every answer is computed exactly — Fractions and integer long division for
digits, never floats — the same route plan 017's verifier used for the
on-screen anchors, and every rule the solutions teach is asserted against
the computation. Run: prints `problem_id: answer`.
"""

from fractions import Fraction
from math import gcd


def _digits(x: Fraction, n: int) -> list[int]:
    """The first n digits after the point of x in [0, 1), truncated."""
    out = []
    for _ in range(n):
        x *= 10
        d = int(x)
        out.append(d)
        x -= d
    return out


def _rule(diagonal: list[int]) -> list[int]:
    """The series' rule: 1 unless the diagonal digit is 1, then 2."""
    return [2 if a == 1 else 1 for a in diagonal]


def _value(digits: list[int], tail_nines: bool = False) -> Fraction:
    """0.d₁d₂…dₖ followed by zeros, or by nines if ``tail_nines``."""
    v = sum(Fraction(d, 10 ** (k + 1)) for k, d in enumerate(digits))
    return v + (Fraction(1, 10 ** len(digits)) if tail_nines else 0)


LIST = [Fraction(2, 7), Fraction(1, 9), Fraction(5, 9), Fraction(1, 11), Fraction(3, 8)]


def p1_five_rows() -> str:
    """Five rationals listed; read the diagonal, apply the rule."""
    diagonal = [_digits(x, n + 1)[n] for n, x in enumerate(LIST)]
    assert diagonal == [2, 1, 5, 9, 0]
    y = _rule(diagonal)
    assert y == [1, 2, 1, 1, 1]
    for n, x in enumerate(LIST):
        assert _digits(x, n + 1)[n] != y[n]
    return "diagonal 2, 1, 5, 9, 0; y = 0.12111..."


def p2_rerun() -> str:
    """Prepend y and run the rule again: y' differs from y at digit 1."""
    y = _rule([2, 1, 5, 9, 0])
    rows = [y] + [_digits(x, 6) for x in LIST]
    diagonal = [rows[n][n] for n in range(6)]
    assert diagonal == [1, 8, 1, 5, 0, 0]
    y2 = _rule(diagonal)
    assert y2 == [2, 1, 2, 1, 1, 1]
    assert y2[0] == 3 - y[0]
    for n in range(6):
        assert rows[n][n] != y2[n]
    return "new diagonal 1, 8, 1, 5, 0, 0; y' = 0.212111...; y'_1 = 3 - y_1"


def p3_plus_one_fails() -> str:
    """'Add 1' on (0.0999..., 0.999..., 0.999...) lands on x_1 itself."""
    x1 = _value([0], tail_nines=True)  # 0.0999... = 1/10
    xn = _value([], tail_nines=True)  # 0.999... = 1
    assert x1 == Fraction(1, 10) and xn == 1
    diagonal = [0, 9, 9]
    y = [(d + 1) % 10 for d in diagonal]
    assert y == [1, 0, 0] and _value(y) == x1
    return "y = 0.1000... = 1/10 = x_1; fix: digits from {1, 2}"


def p4_range() -> str:
    """0.111... = 1/9, 0.222... = 2/9; every {1,2}-digit y lies between."""
    ones = Fraction(1, 10) / (1 - Fraction(1, 10))
    twos = Fraction(2, 10) / (1 - Fraction(1, 10))
    assert ones == Fraction(1, 9) and twos == Fraction(2, 9)
    for bits in range(2**8):
        digits = [1 + (bits >> k & 1) for k in range(8)]
        v = _value(digits)
        assert Fraction(11111111, 10**8) <= v <= Fraction(22222222, 10**8)
    return "1/9 and 2/9; 1/9 <= y <= 2/9, strictly inside [0, 1]"


def p5_two_rows() -> str:
    """Points with two expansions and a terminating one of at most 2 digits."""
    doubles = {Fraction(k, 100) for k in range(1, 100)}
    tenths = {Fraction(k, 10) for k in range(1, 10)}
    assert tenths <= doubles and len(doubles) == 99 and len(doubles - tenths) == 90
    assert _value([4], tail_nines=True) == Fraction(1, 2) == _value([5])
    return "99 points (9 with one digit, 90 needing two); 0.4999... = 0.5000..."


def _stamp(p: int, q: int) -> int:
    s = p + q
    return (s - 2) * (s - 1) // 2 + p


def _walk(limit: int):
    cells = [(p, q) for p in range(1, 40) for q in range(1, 40) if p + q <= 40]
    return sorted(cells, key=lambda c: _stamp(*c))[:limit]


def p6_zigzag() -> str:
    """Stamp 20 on the grid; the kept position of 3/5."""
    walk = _walk(60)
    assert walk[19] == (5, 2) and _stamp(5, 2) == 20
    kept = [c for c in walk if gcd(*c) == 1]
    assert kept[:11] == [
        (1, 1),
        (1, 2),
        (2, 1),
        (1, 3),
        (3, 1),
        (1, 4),
        (2, 3),
        (3, 2),
        (4, 1),
        (1, 5),
        (5, 1),
    ]
    position = kept.index((3, 5)) + 1
    assert position == 19 and _stamp(3, 5) == 24
    return "stamp 20 is 5/2; 3/5 (stamp 24) is kept fraction 19"


def p7_integers() -> str:
    """The pairing n -> n/2 (even), -(n-1)/2 (odd)."""

    def g(n: int) -> int:
        return n // 2 if n % 2 == 0 else -(n - 1) // 2

    assert [g(n) for n in range(1, 11)] == [0, 1, -1, 2, -2, 3, -3, 4, -4, 5]
    assert g(75) == -37 and g(100) == 50
    assert len({g(n) for n in range(1, 2001)}) == 2000
    return "-37 sits at position 75; position 100 holds 50"


def p8_cantor_theorem() -> str:
    """S = {1..5} with five listed subsets: the flipped diagonal."""
    f = {1: {2, 3}, 2: {1, 2, 5}, 3: set(), 4: {1, 2, 3, 4, 5}, 5: {4}}
    d = {s for s in range(1, 6) if s not in f[s]}
    assert d == {1, 3, 5} and all(d != f[m] for m in f)
    assert 2**5 == 32 and len({frozenset(v) for v in f.values()}) <= 5
    return "D = {1, 3, 5}, on no row; 32 subsets, at most 5 hit"


def p9_overflow_and_cover() -> str:
    """p = 0.03 overflows at N = 34; the halving cover at eps = 1/100."""
    p = Fraction(3, 100)
    n = min(n for n in range(1, 1000) if n * p > 1)
    assert n == 34 and n * p == Fraction(102, 100)
    eps = Fraction(1, 100)
    partials = [eps * (1 - Fraction(1, 2**k)) for k in range(1, 5)]
    assert partials == [Fraction(1, 200), Fraction(3, 400), Fraction(7, 800), Fraction(15, 1600)]
    assert sum(eps / 2**k for k in range(1, 60)) < eps
    return "N = 34 (1.02 > 1); partial sums 1/200, 3/400, 7/800, 15/1600, total under 1/100"


ANSWERS = {
    "cantor-diagonal.1": p1_five_rows,
    "cantor-diagonal.2": p2_rerun,
    "cantor-diagonal.3": p3_plus_one_fails,
    "cantor-diagonal.4": p4_range,
    "cantor-diagonal.5": p5_two_rows,
    "cantor-diagonal.6": p6_zigzag,
    "cantor-diagonal.7": p7_integers,
    "cantor-diagonal.8": p8_cantor_theorem,
    "cantor-diagonal.9": p9_overflow_and_cover,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
