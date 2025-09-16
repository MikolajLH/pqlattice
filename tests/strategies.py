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
