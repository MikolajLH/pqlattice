from typing import cast, overload

from .._utils import as_integer
from ..typing import Array


@overload
def eea(a: int, b: int) -> tuple[int, int, int]: ...


@overload
def eea(a: Array, b: int) -> tuple[Array, Array, Array]: ...


def eea(a: int | Array, b: int) -> tuple[int, int, int] | tuple[Array, Array, Array]:
    """_summary_

    Parameters
    ----------
    a : int | Array
        _description_
    b : int
        _description_

    Returns
    -------
    tuple[int, int, int] | tuple[Array, Array, Array]
        _description_
    """
    if isinstance(a, int):
        return _eea(a, b)
    else:
        return tuple(as_integer([_eea(cast(int, el), b) for el in a]).T)


def _eea(a: int, b: int) -> tuple[int, int, int]:
    if a == 0 and b == 0:
        raise ValueError("a and b can't be both zero")

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
