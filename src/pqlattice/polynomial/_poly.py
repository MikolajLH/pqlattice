import numpy as np

from ..typing import VectorInt, validate_aliases


@validate_aliases
def is_zero_poly(p: VectorInt) -> bool:
    """
    TODO: write docstring

    Parameters
    ----------
    p : VectorInt
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
def deg(p: VectorInt) -> int:
    """
    TODO: write docstring


    Parameters
    ----------
    p : VectorInt
        _description_

    Returns
    -------
    int
        _description_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    """

    if len(p) == 0:
        raise ValueError("Empty coefficient array is not a proper polynomial")
    nonzeros = np.nonzero(p)[0]
    if len(nonzeros) == 0:
        raise ValueError("Degree of zero polynomial is undefined")
    else:
        return nonzeros[-1]


@validate_aliases
def pad(p: VectorInt, max_deg: int) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    p : VectorInt
        _description_
    max_deg : int
        _description_

    Returns
    -------
    VectorInt
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

    return np.pad(trim(p), (0, max_deg - d))


@validate_aliases
def trim(p: VectorInt) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    p : VectorInt
        _description_

    Returns
    -------
    VectorInt
        _description_
    """
    if is_zero_poly(p):
        return np.zeros(1, dtype=int)

    return p[: deg(p) + 1].copy()


@validate_aliases
def add(p: VectorInt, q: VectorInt) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    p : VectorInt
        _description_
    q : VectorInt
        _description_

    Returns
    -------
    VectorInt
        _description_
    """
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) + pad(q, max_deg))


@validate_aliases
def sub(p: VectorInt, q: VectorInt) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    p : VectorInt
        _description_
    q : VectorInt
        _description_

    Returns
    -------
    VectorInt
        _description_
    """
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) - pad(q, max_deg))


@validate_aliases
def mul(p: VectorInt, q: VectorInt) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    p : VectorInt
        _description_
    q : VectorInt
        _description_

    Returns
    -------
    VectorInt
        _description_
    """
    return trim(np.polymul(p[::-1], q[::-1])[::-1])


@validate_aliases
def monomial(coeff: int, degree: int) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    coeff : int
        _description_
    degree : int
        _description_

    Returns
    -------
    VectorInt
        _description_

    Raises
    ------
    ValueError
        _description_
    """

    if degree < 0:
        raise ValueError("degree has to be non negative")

    p = np.zeros(degree + 1, dtype=int)
    p[degree] = coeff
    return p


@validate_aliases
def zero_poly(max_deg: int = 0) -> VectorInt:
    """
    TODO: write docstring

    Parameters
    ----------
    max_deg : int, optional
        _description_, by default 0

    Returns
    -------
    VectorInt
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if max_deg < 0:
        raise ValueError("degree has to be non negative")

    return np.zeros(max_deg + 1, dtype=int)
