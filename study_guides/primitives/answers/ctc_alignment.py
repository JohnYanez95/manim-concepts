"""Answer anchors for the ctc-alignment problem set (plan 012 R3).

The collapse map and path counts are enumerated directly — the same
brute-force route plan 001 used — so every answer is a computation, and
formula claims are asserted against the enumeration. Run: prints
`problem_id: answer`.
"""

from itertools import product
from math import comb

EPS = "e"  # blank, ASCII-safe


def collapse(path: str) -> str:
    """Merge adjacent repeats, THEN drop blanks — the order is the point."""
    merged = [ch for i, ch in enumerate(path) if i == 0 or path[i - 1] != ch]
    return "".join(ch for ch in merged if ch != EPS)


def p1_collapses() -> str:
    triple = (collapse("AAeB"), collapse("eABB"), collapse("ABBA"))
    assert triple == ("AB", "AB", "ABA")
    return ", ".join(triple)


def p2_order_matters() -> str:
    """L-eps-L survives merge-then-drop as LL; drop-then-merge kills it."""
    merge_then_drop = collapse("LeL")

    def drop_then_merge(path: str) -> str:
        dropped = path.replace(EPS, "")
        return "".join(ch for i, ch in enumerate(dropped) if i == 0 or dropped[i - 1] != ch)

    assert merge_then_drop == "LL"
    assert drop_then_merge("LeL") == "L"
    return "merge-then-drop: LL; drop-then-merge: L"


def p3_raw_and_collapsing() -> str:
    paths = ["".join(p) for p in product("A" + EPS, repeat=3)]
    hits = [p for p in paths if collapse(p) == "A"]
    assert len(paths) == 8
    assert len(hits) == 6  # matches the trellis's 3 + 3
    return f"raw {len(paths)}, collapsing {len(hits)}"


def p4_t5_paths() -> int:
    """C(T+U, T-U) at T=5, U=2 — checked by enumeration over {A,B,eps}."""
    formula = comb(5 + 2, 5 - 2)
    enumerated = sum(1 for p in product("AB" + EPS, repeat=5) if collapse("".join(p)) == "AB")
    assert formula == enumerated == 35
    return formula


def p5_greedy_fails() -> str:
    """y_t(A)=0.4, y_t(eps)=0.6 at T=2: greedy decodes '', the sum says 'A'."""
    y = {"A": 0.4, EPS: 0.6}
    mass: dict[str, float] = {}
    for path in product("A" + EPS, repeat=2):
        weight = y[path[0]] * y[path[1]]
        mass[collapse("".join(path))] = mass.get(collapse("".join(path)), 0.0) + weight
    greedy = collapse(EPS + EPS)  # blank wins every frame
    best = max(mass, key=lambda k: mass[k])
    assert greedy == "" and best == "A"
    assert abs(mass[""] - 0.36) < 1e-12 and abs(mass["A"] - 0.64) < 1e-12
    return "greedy '', best 'A' (0.36 vs 0.64)"


ANSWERS = {
    "ctc-alignment.1": p1_collapses,
    "ctc-alignment.2": p2_order_matters,
    "ctc-alignment.3": p3_raw_and_collapsing,
    "ctc-alignment.4": p4_t5_paths,
    "ctc-alignment.5": p5_greedy_fails,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
