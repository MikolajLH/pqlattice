from fractions import Fraction
from typing import Any

from numpy.typing import NDArray

type Array = NDArray[Any]

type Vector = NDArray[Any]
type Matrix = NDArray[Any]
type SquareMatrix = NDArray[Any]


def is_rational(a: Array) -> bool:
    """
    Check if elements of the numpy's array are of type `fractions.Fraction`

    Parameters
    ----------
    a : Array
        numpy's array

    Returns
    -------
    bool
        True if elements have type `fractions.Fraction`, False otherwise
    """
    return isinstance(a.flat[0], Fraction)


def is_integer(a: Array) -> bool:
    """
    Check if elements of the numpy's array are of type `int`

    Parameters
    ----------
    a : Array
        numpy's array

    Returns
    -------
    bool
        True if elements have type `int, False otherwise
    """
    return isinstance(a.flat[0], int)
