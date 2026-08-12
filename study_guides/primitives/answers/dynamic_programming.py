"""Answer anchors for the dynamic-programming problem set (plan 012 R3).

Every answer is computed, not asserted — call counts by instrumented
recursion, path counts by brute enumeration — so the reorganisation the
chapter teaches is checked against the exponential count it replaces.
Run: prints `problem_id: answer`.
"""

from functools import cache
from itertools import product
from math import comb

EPS = "e"  # blank, ASCII-safe


def collapse(path: str) -> str:
    """Merge adjacent repeats, THEN drop blanks — the alignment chapter's map."""
    merged = [ch for i, ch in enumerate(path) if i == 0 or path[i - 1] != ch]
    return "".join(ch for ch in merged if ch != EPS)


def p1_fibonacci_calls() -> str:
    """Naive fib(10) call count vs memoized distinct-subproblem count."""
    calls = 0

    def naive(n: int) -> int:
        nonlocal calls
        calls += 1
        return n if n < 2 else naive(n - 1) + naive(n - 2)

    seen: set[int] = set()

    @cache
    def memo(n: int) -> int:
        seen.add(n)
        return n if n < 2 else memo(n - 1) + memo(n - 2)

    assert naive(10) == memo(10) == 55
    subproblems = len(seen)
    assert subproblems == 11
    # Closed form for the call tree: 2*fib(n+1) - 1 invocations.
    assert calls == 2 * memo(11) - 1 == 177
    return f"naive {calls} calls, memoized {subproblems} subproblems"


def p2_lattice_by_addition() -> int:
    """Routes to each node = sum over incoming edges; corner = C(6,2)."""
    rights, ups = 4, 2
    routes = [[0] * (rights + 1) for _ in range(ups + 1)]
    routes[0][0] = 1
    for y in range(ups + 1):
        for x in range(rights + 1):
            if x:
                routes[y][x] += routes[y][x - 1]
            if y:
                routes[y][x] += routes[y - 1][x]
    corner = routes[ups][rights]
    brute = sum(1 for w in product("RU", repeat=6) if w.count("U") == 2)
    assert corner == brute == comb(6, 2) == 15
    return corner


def unit_trellis_columns(states: str, frames: int) -> list[list[int]]:
    """Unit-weight forward recurrence (stay / advance / legal skip)."""
    n = len(states)
    col = [0] * n
    col[0] = 1
    if n > 1:
        col[1] = 1
    columns = [col]
    for _ in range(frames - 1):
        prev, col = col, [0] * n
        for s in range(n):
            total = prev[s]
            if s >= 1:
                total += prev[s - 1]
            skip_ok = s >= 2 and states[s] != EPS and states[s] != states[s - 2]
            if skip_ok:
                total += prev[s - 2]
            col[s] = total
        columns.append(col)
    return columns


def p3_trellis_one_more_column() -> str:
    """Extend the mini-trellis (states eps A eps) from T=3 to T=4."""
    cols = unit_trellis_columns(EPS + "A" + EPS, 4)
    # The chapter's worked columns, then the new one.
    assert cols[0] == [1, 1, 0]
    assert cols[1] == [1, 2, 1]
    assert cols[2] == [1, 3, 3]
    assert cols[3] == [1, 4, 6]
    accepted = cols[3][1] + cols[3][2]
    brute = sum(1 for p in product("A" + EPS, repeat=4) if collapse("".join(p)) == "A")
    assert accepted == brute == 10
    # And the T=3 close of the worked example: 3 + 3 = 6.
    assert cols[2][1] + cols[2][2] == 6
    return f"column (1, 4, 6), accepted {accepted}"


def p4_work_accounting() -> str:
    """Trellis cells vs raw repeat-free path count at T=100, U=50."""
    frames, letters = 100, 50
    cells = frames * (2 * letters + 1)
    paths = comb(frames + letters, frames - letters)
    assert cells == 10100
    assert 2.0e40 < paths < 2.1e40  # the alignment chapter's 2 x 10^40
    return f"{cells} cells vs about {paths:.1e} paths"


ANSWERS = {
    "dynamic-programming.1": p1_fibonacci_calls,
    "dynamic-programming.2": p2_lattice_by_addition,
    "dynamic-programming.3": p3_trellis_one_more_column,
    "dynamic-programming.4": p4_work_accounting,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
