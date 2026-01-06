from collections.abc import Iterable
from fractions import Fraction
from typing import Any

import numpy as np

from .typing import Array


def as_integer(a: Iterable[Any]) -> Array:
    """_summary_

    Parameters
    ----------
    a : Iterable[Any]
        _description_

    Returns
    -------
    Array
        _description_
    """
    return (np.vectorize(int)(np.array(a, dtype=object))).astype(object)


def as_rational(a: Iterable[Any]) -> Array:
    """_summary_

    Parameters
    ----------
    a : Iterable[Any]
        _description_

    Returns
    -------
    Array
        _description_
    """
    return (np.vectorize(Fraction)(np.array(a, dtype=object))).astype(object)
