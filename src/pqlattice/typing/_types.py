from fractions import Fraction
from typing import Any

from numpy.typing import NDArray

type Array = NDArray[Any]

type Vector = NDArray[Any]
type Matrix = NDArray[Any]
type SquareMatrix = NDArray[Any]


def is_rational(a: Array) -> bool:
    return isinstance(a.flat[0], Fraction)


def is_integer(a: Array) -> bool:
    return isinstance(a.flat[0], int)
