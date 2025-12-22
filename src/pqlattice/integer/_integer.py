from typing import cast, overload

from .._utils import as_integer
from ..typing import Array


@overload
def eea(a: Array, b: int) -> tuple[Array, Array, Array]: ...


@overload
def eea(a: int, b: int) -> tuple[int, int, int]: ...


def eea(a: int | Array, b: int) -> tuple[int, int, int] | tuple[Array, Array, Array]:
    r"""
    Implementation of [extended euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm) for integers.

    Computes the greatest common divisor of a and b and the coefficients of Bézout's identity.

    Parameters
    ----------
    a : int
    b : int

    Returns
    -------
    (gcd, s, t) : tuple[int, int, int]
        Integers such that a * s + b * t = gcd.

    Raises
    ------
    ValueError
        If both a and b are equal to 0

    Notes
    -----
    When a == b, then s = 0 and t = 1, so for any integer x different than 0, eea(x, x) == (x, 0, 1)

    Examples
    --------
    >>> eea(240, 46)
    (2, -9, 47)
    """
    if isinstance(a, int):
        return _eea(a, b)
    else:
        return tuple(as_integer([_eea(cast(int, el), b) for el in a]).T)


def _eea(a: int, b: int) -> tuple[int, int, int]:
    if a == 0 and b == 0:
        raise ValueError("<PQLE> a and b can't be both zero")

    old_s, s = 1, 0
    old_r, r = a, b
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s

    t = 0 if b == 0 else (old_r - old_s * a) // b
    s = old_s
    gcd = old_r
    if gcd < 0:
        gcd = -gcd
        s = -s
        t = -t

    return gcd, s, t
