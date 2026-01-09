import logging
import random
from collections.abc import Callable
from typing import Any, cast

import hypothesis.strategies as st
import numpy as np
from hypothesis.extra import numpy as hnp
from sagemath.sage_interface import TArray
from tests import oracle

type DrawFn[T] = Callable[[st.SearchStrategy[T]], T]

logger = logging.getLogger(__name__)


@st.composite
def primes(draw: DrawFn[int], min_value: int = 2, max_bits: int = 128) -> int:
    i = draw(st.integers(min_value=min_value - 1, max_value=2**max_bits))
    return oracle.next_prime(i)


@st.composite
def polynomials(draw: DrawFn[int | TArray], min_deg: int = 0, max_deg: int = 20, min_coeff: int = -(10**5), max_coeff: int = 10**5):
    degree = cast(int, draw(st.integers(min_deg, max_deg)))
    lead_coeff = cast(int, draw(st.integers(min_coeff, max_coeff).filter(lambda x: x != 0)))

    if degree == 0:
        return np.array([lead_coeff], dtype=object)

    other_coeffs = cast(TArray, draw(hnp.arrays(dtype=object, shape=degree, elements=st.integers(min_coeff, max_coeff))))

    return np.concatenate([other_coeffs, [lead_coeff]])


@st.composite
def matrices(draw: DrawFn[int | TArray], min_rows: int = 1, max_rows: int = 10, min_cols: int = 1, max_cols: int = 10, min_value: int = -50, max_value: int = 50):
    rows = cast(int, draw(st.integers(min_rows, max_rows)))
    cols = cast(int, draw(st.integers(min_cols, max_cols)))

    matrix = cast(TArray, draw(hnp.arrays(object, (rows, cols), elements=st.integers(min_value, max_value))))

    return matrix


@st.composite
def vectors(draw: DrawFn[TArray], n: int, min_value: int = -100, max_value: int = 100):
    return draw(hnp.arrays(object, n, elements=st.integers(min_value, max_value)))


@st.composite
def low_rank_matrices(draw: DrawFn[TArray | int], min_rows: int = 2, max_rows: int = 10, min_cols: int = 2, max_cols: int = 10, min_value: int = -50, max_value: int = 50):
    rows = cast(int, draw(st.integers(min_rows, max_rows)))
    cols = cast(int, draw(st.integers(min_cols, max_cols)))

    max_rank = min(rows, cols)
    if max_rank <= 1:
        return np.zeros((rows, cols), dtype=object)

    r = cast(int, draw(st.integers(1, max_rank - 1)))

    U = cast(TArray, draw(hnp.arrays(object, (rows, r), elements=st.integers(min_value, max_value))))
    V = cast(TArray, draw(hnp.arrays(object, (r, cols), elements=st.integers(min_value, max_value))))

    return U @ V


@st.composite
def full_rank_matrices(draw: DrawFn[TArray | int | bool], min_rows: int = 2, max_rows: int = 10, min_cols: int = 2, max_cols: int = 10, min_value: int = -50, max_value: int = 50, square: bool = False):
    rows = cast(int, draw(st.integers(min_rows, max_rows)))
    cols = cast(int, draw(st.integers(min_cols, max_cols)))

    if square:
        cols = rows

    rank = min(rows, cols)

    A = np.zeros((rows, cols), dtype=object)
    diagonals = cast(TArray, draw(hnp.arrays(object, rank, elements=st.integers(min_value, max_value).filter(lambda x: x != 0))))
    A[np.diag_indices(rank)] = diagonals

    if rank == 1:
        return A

    num_scrambles = cast(int, draw(st.integers(min_value=rows + cols, max_value=(rows + cols) * 2)))

    for _ in range(num_scrambles):
        row_op = cast(bool, draw(st.booleans()))
        if row_op:
            i = cast(int, draw(st.integers(0, rows - 1)))
            j = cast(int, draw(st.integers(0, rows - 1)))
            if i == j:
                continue
            factor = cast(int, draw(st.integers(-10, 10)))
            A[i] += factor * A[j]
        else:
            i = cast(int, draw(st.integers(0, cols - 1)))
            j = cast(int, draw(st.integers(0, cols - 1)))
            if i == j:
                continue
            factor = cast(int, draw(st.integers(-10, 10)))
            A[:, i] += factor * A[:, j]

    return A


@st.composite
def lattices(draw: DrawFn[Any], n_range: tuple[int, int] = (2, 20), volume_ub: int | None = None):
    def _gen_unimodular(n: int, rounds: int, rng: random.Random) -> TArray:
        U = np.eye(n, dtype=object)
        for _ in range(rounds):
            i, j = rng.sample(range(n), 2)
            coeff = rng.sample([-1, 1], 1)

            U[i] += coeff * U[j]

        return U

    n: int = draw(st.integers(*n_range))
    det_ub: int = 2**n if volume_ub is None else volume_ub
    diagonals = [draw(st.integers(1, det_ub)) for _ in range(n)]

    H = np.zeros((n, n), dtype=object)
    for i in range(n):
        H[i, i] = diagonals[i]
        modulus = H[i, i]
        for j in range(i, n):
            H[i, j] = draw(st.integers(0, modulus - 1))

    seed = draw(st.integers())
    rng = random.Random(seed)
    U = _gen_unimodular(n, n * 5, rng)

    return U @ H


@st.composite
def sage_lattices(draw: DrawFn[Any], types: list[str] | None = None, n_range: tuple[int, int] = (1, 6), m_range: tuple[int, int] = (4, 12), q_range: tuple[int, int] = (2, 17), allow_dual: bool = True):
    if types is None:
        types = ["modular", "random"]

    type: str = draw(st.sampled_from(types))
    n: int = 1 if type == "random" else draw(st.integers(*n_range))
    m: int = draw(st.integers(*m_range).filter(lambda x: x > n))
    q: int = draw(st.integers(*q_range))
    dual: bool = False if not allow_dual else draw(st.booleans())
    # logger.warning(f"{type=} {n=} {m=} {q=} {dual=}")

    return oracle.Sage.gen_lattice(type, n, m, q, dual=dual)
