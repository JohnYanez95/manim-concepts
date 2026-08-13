"""Answer anchors for the counting-rules problem set (plan 012 R3).

Every answer is computed, not asserted — by brute enumeration wherever the
space permits, so the formula the solution teaches is checked against a
count the script performed. Run: prints `problem_id: answer`.
"""

from itertools import permutations, product
from math import comb, factorial, perm


def p1_label_sequences() -> int:
    """3 symbols over 4 frames — enumerated, checked against 3**4."""
    count = len(list(product("ABE", repeat=4)))
    assert count == 3**4
    return count


def p2_podiums() -> int:
    """Ordered top-3 of 8 — enumerated, checked against P(8,3)."""
    count = len(list(permutations(range(8), 3)))
    assert count == perm(8, 3) == factorial(8) // factorial(5)
    return count


def p3_teams() -> int:
    """Unordered 3-of-8 — enumerated as sets, checked against C(8,3)."""
    count = len({frozenset(t) for t in permutations(range(8), 3)})
    assert count == comb(8, 3) == p2_podiums() // factorial(3)
    return count


def p4_seeded() -> int:
    """Distinct arrangements of SEEDED — enumerated, checked vs 6!/(3!2!1!)."""
    count = len(set(permutations("SEEDED")))
    assert count == factorial(6) // (factorial(3) * factorial(2) * factorial(1))
    return count


def p5_lattice_routes() -> int:
    """Words over {R,U} with 4 R's and 2 U's — enumerated, checked vs C(6,2)."""
    count = sum(1 for w in product("RU", repeat=6) if w.count("U") == 2)
    assert count == comb(6, 2)
    return count


ANSWERS = {
    "counting-rules.1": p1_label_sequences,
    "counting-rules.2": p2_podiums,
    "counting-rules.3": p3_teams,
    "counting-rules.4": p4_seeded,
    "counting-rules.5": p5_lattice_routes,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
