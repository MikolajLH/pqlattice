import numpy as np
from numpy.typing import ArrayLike

from .._utils import as_integer
from ..typing import Vector, validate_aliases


@validate_aliases
def make_poly(data: ArrayLike) -> Vector:
    """
    Helper function, creates polynomial from the array like.

    Parameters
    ----------
    data : ArrayLike

    Returns
    -------
    Vector
        polynomial

    Raises
    ------
    ValueError
        if the data has wrong shape
    """
    arr = as_integer(data)

    if arr.ndim != 1:
        raise ValueError(f"Expected 1D iterable, got {arr.ndim}D")

    return arr


@validate_aliases
def is_zero_poly(p: Vector) -> bool:
    """
    Checks if the poly is zero poly - all coefficients are equal to zero.

    Parameters
    ----------
    p : Vector
        polynomial

    Returns
    -------
    bool
        True if all coefficients are equal to zero, False otherwise

    Raises
    ------
    ValueError
        If the given Vector is empty
    """
    if len(p) == 0:
        raise ValueError("Empty coefficient array is not a proper polynomial")

    return np.count_nonzero(p) == 0


@validate_aliases
def deg(p: Vector) -> int:
    """
    Returns degree of the given polynomial.
    Assumes -1 for the zero polynomial.

    Parameters
    ----------
    p : Vector

    Returns
    -------
    int
        degree

    Raises
    ------
    ValueError
        If the vector is empty
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
    """
    Pad's polynomial's coefficient's array with zero entries for powers higher than polynomial's degree,
    so that length of resulting array is equal to max_deg + 1.

    Parameters
    ----------
    p : Vector
    max_deg : int
        Degree that `p` is to be expanded to

    Returns
    -------
    Vector
        polynomial

    Raises
    ------
    ValueError
        If max deg is less than the degree of the given polynomial
    """
    if is_zero_poly(p):
        return zero_poly(max_deg)

    d = deg(p)
    if max_deg < d:
        raise ValueError("max_deg has to be greater or equal to the degree of a given polynomial p")

    return as_integer(np.pad(trim(p), (0, max_deg - d)))


@validate_aliases
def trim(p: Vector) -> Vector:
    """
    Trims zero coefficients of powers higher than polynomial's degree,
    so that resulting coefficient's arrray has length of `deg(p) + 1`.

    Parameters
    ----------
    p : Vector

    Returns
    -------
    Vector
        polynomial
    """
    if is_zero_poly(p):
        return as_integer([0])

    return p[: deg(p) + 1].copy()


@validate_aliases
def add(p: Vector, q: Vector) -> Vector:
    """
    Adds two polynomials together.

    Parameters
    ----------
    p : Vector
    q : Vector

    Returns
    -------
    Vector
        polynomial
    """
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) + pad(q, max_deg))


@validate_aliases
def sub(p: Vector, q: Vector) -> Vector:
    """
    Subtract one polynomial from the other

    Parameters
    ----------
    p : Vector
    q : Vector

    Returns
    -------
    Vector
        polynomial
    """
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) - pad(q, max_deg))


@validate_aliases
def mul(p: Vector, q: Vector) -> Vector:
    """
    Multiplies two polynomials.

    Parameters
    ----------
    p : Vector
    q : Vector

    Returns
    -------
    Vector
        polynomial
    """
    return trim(np.polymul(p[::-1], q[::-1])[::-1])


@validate_aliases
def monomial(coeff: int, degree: int) -> Vector:
    """
    For given degree `d` and coefficient `c`, constructs a monomial `cX + ** (d - 1)`

    Parameters
    ----------
    coeff : int
    degree : int

    Returns
    -------
    Vector
        polynomial

    Raises
    ------
    ValueError
        if degree is negative
    """
    if degree < 0:
        raise ValueError("degree has to be non negative")

    p = as_integer([0] * (degree + 1))
    p[degree] = coeff
    return p


@validate_aliases
def zero_poly(max_deg: int = 0) -> Vector:
    """
    constructs zero polynomial, expanded to the given parameter max_deg

    Parameters
    ----------
    max_deg : int, optional
        by default 0

    Returns
    -------
    Vector
        Vector of length `max_deg + 1` filled with zeros

    Raises
    ------
    ValueError
        If the `max_deg` is negative
    """
    if max_deg < 0:
        raise ValueError("degree has to be non negative")

    return as_integer([0] * (max_deg + 1))
