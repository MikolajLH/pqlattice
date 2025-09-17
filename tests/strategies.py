from collections.abc import Callable
from typing import cast

import hypothesis.strategies as st
import numpy as np
import numpy.typing as npt
from hypothesis.extra import numpy as hnp
from tests import oracle

type DrawFn[T] = Callable[[st.SearchStrategy[T]], T]


@st.composite
def primes(draw: DrawFn[int], min_value: int = 2, max_bits: int = 128) -> int:
    """
    TODO: write docstring

    Parameters
    ----------
    draw : DrawFn[int]
        _description_
    min_value : int, optional
        _description_, by default 2
    max_bits : int, optional
        _description_, by default 128

    Returns
    -------
    int
        _description_
    """
    i = draw(st.integers(min_value=min_value - 1, max_value=2**max_bits))
    return oracle.next_prime(i)


@st.composite
def polynomials(draw: DrawFn[int | npt.NDArray[np.integer]], min_deg: int = 0, max_deg: int = 20, min_coeff: int = -(10**5), max_coeff: int = 10**5):
    """
    TODO: write docstring

    Parameters
    ----------
    draw : DrawFn[int | np.ndarray]
        _description_
    min_deg : int, optional
        _description_, by default 0
    max_deg : int, optional
        _description_, by default 20
    min_coeff : int, optional
        _description_, by default -10**5
    max_coeff : int, optional
        _description_, by default 10**5

    Returns
    -------
    _type_
        _description_
    """
    degree = cast(int, draw(st.integers(min_deg, max_deg)))
    lead_coeff = cast(int, draw(st.integers(min_coeff, max_coeff).filter(lambda x: x != 0)))

    if degree == 0:
        return np.array([lead_coeff], dtype=int)

    other_coeffs = cast(npt.NDArray[np.integer], draw(hnp.arrays(dtype=int, shape=degree, elements=st.integers(min_coeff, max_coeff))))

    return np.concatenate([other_coeffs, [lead_coeff]])


@st.composite
def int_matrices(draw: DrawFn[int | npt.NDArray[np.integer]], min_rows: int = 1, max_rows: int = 10, min_cols: int = 1, max_cols: int = 10, min_value: int = -50, max_value: int = 50):
    rows = cast(int, draw(st.integers(min_rows, max_rows)))
    cols = cast(int, draw(st.integers(min_cols, max_cols)))

    matrix = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, (rows, cols), elements=st.integers(min_value, max_value))))

    return matrix


@st.composite
def unimodular_int_matrices(draw: DrawFn[int | npt.NDArray[np.integer]], min_n: int = 1, max_n: int = 10):
    n = cast(int, draw(st.integers(min_n, max_n)))
    min_v = -10
    max_v = 10
    part_L = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, (n, n), elements=st.integers(min_v, max_v))))
    part_R = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, (n, n), elements=st.integers(min_v, max_v))))

    diag_L = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, n, elements=st.sampled_from([-1, 1]))))

    diag_R = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, n, elements=st.sampled_from([-1, 1]))))

    L = part_L + np.diag(diag_L)
    R = part_R + np.diag(diag_R)

    return L @ R


@st.composite
def int_vectors(draw: DrawFn[npt.NDArray[np.integer]], n: int, min_value: int = -100, max_value: int = 100):
    return draw(hnp.arrays(int, n, elements=st.integers(min_value, max_value)))


@st.composite
def low_rank_matrices(draw: DrawFn[npt.NDArray[np.integer] | int], min_rows: int = 2, max_rows: int = 10, min_cols: int = 2, max_cols: int = 10, min_value: int = -50, max_value: int = 50):
    rows = cast(int, draw(st.integers(min_rows, max_rows)))
    cols = cast(int, draw(st.integers(min_cols, max_cols)))

    max_rank = min(rows, cols)
    if max_rank <= 1:
        return np.zeros((rows, cols), dtype=int)

    r = cast(int, draw(st.integers(1, max_rank - 1)))

    U = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, (rows, r), elements=st.integers(min_value, max_value))))
    V = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, (r, cols), elements=st.integers(min_value, max_value))))

    return U @ V


@st.composite
def full_rank_matrices(draw: DrawFn[npt.NDArray[np.integer] | int | bool], min_rows: int = 2, max_rows: int = 10, min_cols: int = 2, max_cols: int = 10, min_value: int = -50, max_value: int = 50, square: bool = False):
    rows = cast(int, draw(st.integers(min_rows, max_rows)))
    cols = cast(int, draw(st.integers(min_cols, max_cols)))

    if square:
        cols = rows

    rank = min(rows, cols)

    A = np.zeros((rows, cols), dtype=int)
    diagonals = cast(npt.NDArray[np.integer], draw(hnp.arrays(int, rank, elements=st.integers(min_value, max_value).filter(lambda x: x != 0))))
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
