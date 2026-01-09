import numpy as np
from numpy.typing import ArrayLike

from .._utils import as_integer
from ..typing import Vector, validate_aliases


@validate_aliases
def make_poly(data: ArrayLike) -> Vector:
    """_summary_

    Parameters
    ----------
    data : Iterable[int  |  float]
        _description_

    Returns
    -------
    Vector
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    arr = as_integer(data)

    if arr.ndim != 1:
        raise ValueError(f"Expected 1D iterable, got {arr.ndim}D")

    return arr


@validate_aliases
def is_zero_poly(p: Vector) -> bool:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_

    Returns
    -------
    bool
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if len(p) == 0:
        raise ValueError("Empty coefficient array is not a proper polynomial")

    return np.count_nonzero(p) == 0


@validate_aliases
def deg(p: Vector) -> int:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_

    Returns
    -------
    int
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if len(p) == 0:
        raise ValueError("Empty coefficient array is not a proper polynomial")
    nonzeros = np.nonzero(p)[0]
    if len(nonzeros) == 0:
        return -1
        # raise ValueError("Degree of zero polynomial is undefined")
    else:
        return nonzeros[-1]


@validate_aliases
def pad(p: Vector, max_deg: int) -> Vector:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_
    max_deg : int
        _description_

    Returns
    -------
    Vector
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if is_zero_poly(p):
        return zero_poly(max_deg)

    d = deg(p)
    if max_deg < d:
        raise ValueError("max_deg has to be greater or equal to the degree of a given polynomial p")

    return as_integer(np.pad(trim(p), (0, max_deg - d)))


@validate_aliases
def trim(p: Vector) -> Vector:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_

    Returns
    -------
    Vector
        _description_
    """
    if is_zero_poly(p):
        return as_integer([0])

    return p[: deg(p) + 1].copy()


@validate_aliases
def add(p: Vector, q: Vector) -> Vector:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_
    q : Vector
        _description_

    Returns
    -------
    Vector
        _description_
    """
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) + pad(q, max_deg))


@validate_aliases
def sub(p: Vector, q: Vector) -> Vector:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_
    q : Vector
        _description_

    Returns
    -------
    Vector
        _description_
    """
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) - pad(q, max_deg))


@validate_aliases
def mul(p: Vector, q: Vector) -> Vector:
    """_summary_

    Parameters
    ----------
    p : Vector
        _description_
    q : Vector
        _description_

    Returns
    -------
    Vector
        _description_
    """
    return trim(np.polymul(p[::-1], q[::-1])[::-1])


@validate_aliases
def monomial(coeff: int, degree: int) -> Vector:
    """_summary_

    Parameters
    ----------
    coeff : int
        _description_
    degree : int
        _description_

    Returns
    -------
    Vector
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if degree < 0:
        raise ValueError("degree has to be non negative")

    p = as_integer([0] * (degree + 1))
    p[degree] = coeff
    return p


@validate_aliases
def zero_poly(max_deg: int = 0) -> Vector:
    """_summary_

    Parameters
    ----------
    max_deg : int, optional
        _description_, by default 0

    Returns
    -------
    Vector
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if max_deg < 0:
        raise ValueError("degree has to be non negative")

    return as_integer([0] * (max_deg + 1))
