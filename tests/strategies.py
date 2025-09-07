from collections.abc import Callable
from typing import cast

import hypothesis.strategies as st
import numpy as np
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
def polynomials(draw: DrawFn[int | np.ndarray], min_deg: int = 0, max_deg: int = 20, min_coeff: int = -(10**5), max_coeff: int = 10**5):
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

    other_coeffs = draw(hnp.arrays(dtype=int, shape=degree, elements=st.integers(min_coeff, max_coeff)))

    return np.concatenate([other_coeffs, [lead_coeff]])
