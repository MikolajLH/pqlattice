from collections.abc import Callable

import hypothesis.strategies as st
import numpy as np
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
def full_rank_matrices(draw: DrawFn[np.ndarray], n: int, min_value: int = -100, max_value: int = 100):
    """
    TODO: write docstring

    Parameters
    ----------
    draw : DrawFn[np.ndarray]
        _description_
    n : int
        _description_
    min_value : int, optional
        _description_, by default -100
    max_value : int, optional
        _description_, by default 100
    """
    raise NotImplementedError
