"""Answer anchors for the ctc-decoding problem set (plan 012 R3).

The tiny prefix beam search is implemented for real — two masses per
prefix, ending-in-blank and ending-in-letter — and every beam answer is
asserted against a brute-force posterior over all raw paths, so the
sketch the chapter draws is checked against the sum it approximates.
Run: prints `problem_id: answer`.
"""

from itertools import product

EPS = "e"  # blank, ASCII-safe


def collapse(path: str) -> str:
    merged = [ch for i, ch in enumerate(path) if i == 0 or path[i - 1] != ch]
    return "".join(ch for ch in merged if ch != EPS)


def posterior(frames: list[dict[str, float]]) -> dict[str, float]:
    """Brute-force transcript masses: enumerate every raw path, collapse."""
    mass: dict[str, float] = {}
    symbols = list(frames[0])
    for path in product(symbols, repeat=len(frames)):
        weight = 1.0
        for t, ch in enumerate(path):
            weight *= frames[t][ch]
        key = collapse("".join(path))
        mass[key] = mass.get(key, 0.0) + weight
    return mass


def greedy_decode(frames: list[dict[str, float]]) -> str:
    return collapse("".join(max(f, key=lambda k: f[k]) for f in frames))


def beam_decode(frames: list[dict[str, float]], width: int) -> dict[str, tuple[float, float]]:
    """CTC prefix beam search: each prefix carries (p_blank, p_letter)."""

    def add(
        store: dict[str, tuple[float, float]], prefix: str, blank: float, letter: float
    ) -> None:
        b, nb = store.get(prefix, (0.0, 0.0))
        store[prefix] = (b + blank, nb + letter)

    beams: dict[str, tuple[float, float]] = {"": (1.0, 0.0)}
    for f in frames:
        nxt: dict[str, tuple[float, float]] = {}
        for prefix, (p_b, p_nb) in beams.items():
            add(nxt, prefix, (p_b + p_nb) * f[EPS], 0.0)  # emit blank: prefix unchanged
            for ch, y in f.items():
                if ch == EPS:
                    continue
                if prefix and prefix[-1] == ch:
                    add(nxt, prefix, 0.0, p_nb * y)  # repeat merges into the last letter
                    add(nxt, prefix + ch, 0.0, p_b * y)  # a blank separated: new letter
                else:
                    add(nxt, prefix + ch, 0.0, (p_b + p_nb) * y)
        ranked = sorted(nxt, key=lambda p: sum(nxt[p]), reverse=True)
        beams = {p: nxt[p] for p in ranked[:width]}
    return beams


def p1_greedy_on_three_frames() -> str:
    """Best-path decoding on a 3-frame matrix over {A, B, eps}."""
    frames = [
        {"A": 0.5, "B": 0.2, EPS: 0.3},
        {"A": 0.4, "B": 0.3, EPS: 0.3},
        {"A": 0.2, "B": 0.3, EPS: 0.5},
    ]
    decoded = greedy_decode(frames)
    assert decoded == "A"  # argmax path A A eps
    mass = posterior(frames)
    best = max(mass, key=lambda k: mass[k])
    assert best == "A"  # here one transcript dominates: greedy happens to agree
    assert abs(sum(mass.values()) - 1.0) < 1e-12
    return f"greedy '{decoded}' agrees with the sum's winner (mass {mass[best]:.4f})"


def p2_where_greedy_starts_lying() -> str:
    """T = 2, y_t(eps) = q: greedy says '' for q > 1/2, truth flips at 1/sqrt(2)."""

    def masses(q: float) -> tuple[float, float]:
        m = posterior([{"A": 1 - q, EPS: q}] * 2)
        assert abs(m[""] - q * q) < 1e-12 and abs(m["A"] - (1 - q * q)) < 1e-12
        return m[""], m["A"]

    empty, letter = masses(0.6)  # the alignment chapter's construction
    assert (round(empty, 2), round(letter, 2)) == (0.36, 0.64)
    assert masses(0.7)[0] < masses(0.7)[1]  # greedy still wrong at 0.7
    assert masses(0.75)[0] > masses(0.75)[1]  # honest past 1/sqrt(2) ~ 0.7071
    boundary = 0.5**0.5
    assert abs(boundary**2 - (1 - boundary**2)) < 1e-12
    return f"wrong for 1/2 < q < {boundary:.4f}; at q = 0.6, 0.36 vs 0.64"


def p3_beam_recovers_the_sum() -> str:
    """Width-2 beam on the q = 0.6 construction is exact: 0.36 vs 0.24 + 0.40."""
    frames = [{"A": 0.4, EPS: 0.6}] * 2
    beams = beam_decode(frames, width=2)
    b_empty, nb_empty = beams[""]
    b_a, nb_a = beams["A"]
    assert abs(b_empty - 0.36) < 1e-12 and nb_empty == 0.0
    assert abs(b_a - 0.24) < 1e-12 and abs(nb_a - 0.40) < 1e-12
    mass = posterior(frames)
    for prefix, (b, nb) in beams.items():
        assert abs(b + nb - mass[prefix]) < 1e-12
    return "'' 0.36; 'A' blank 0.24 + letter 0.40 = 0.64 — matches the brute sum"


def p4_why_two_numbers() -> str:
    """Merging the two masses overcounts 'AA' three-fold at uniform T = 3."""
    frames = [{"A": 0.5, EPS: 0.5}] * 3
    correct = beam_decode(frames, width=8)
    mass = posterior(frames)
    assert abs(sum(correct["AA"]) - mass["AA"]) < 1e-12
    assert abs(mass["AA"] - 0.125) < 1e-12  # only the path A eps A survives

    # The broken variant: one mass per prefix, so a repeated letter always
    # counts as a new letter — no way to tell merged from blank-separated.
    naive: dict[str, float] = {"": 1.0}
    for f in frames:
        nxt: dict[str, float] = {}
        for prefix, p in naive.items():
            nxt[prefix] = nxt.get(prefix, 0.0) + p * f[EPS]
            nxt[prefix + "A"] = nxt.get(prefix + "A", 0.0) + p * f["A"]
        naive = nxt
    assert abs(naive["AA"] - 0.375) < 1e-12
    return "correct P(AA) = 0.125; one-number beam claims 0.375 (three-fold overcount)"


ANSWERS = {
    "ctc-decoding.1": p1_greedy_on_three_frames,
    "ctc-decoding.2": p2_where_greedy_starts_lying,
    "ctc-decoding.3": p3_beam_recovers_the_sum,
    "ctc-decoding.4": p4_why_two_numbers,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
