from collections.abc import Iterable

import numpy as np

from ..typing import Vector, validate_aliases


@validate_aliases
def make_poly(data: Iterable[int | float]) -> Vector:
    arr = np.array(data, dtype=object)

    if arr.ndim != 1:
        raise ValueError(f"Expected 1D iterable, got {arr.ndim}D")

    return arr


@validate_aliases
def is_zero_poly(p: Vector) -> bool:
    if len(p) == 0:
        raise ValueError("Empty coefficient array is not a proper polynomial")

    return np.count_nonzero(p) == 0


@validate_aliases
def deg(p: Vector) -> int:
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
    if is_zero_poly(p):
        return zero_poly(max_deg)

    d = deg(p)
    if max_deg < d:
        raise ValueError("max_deg has to be greater or equal to the degree of a given polynomial p")

    return np.pad(trim(p), (0, max_deg - d))


@validate_aliases
def trim(p: Vector) -> Vector:
    if is_zero_poly(p):
        return np.zeros(1, dtype=object)

    return p[: deg(p) + 1].copy()


@validate_aliases
def add(p: Vector, q: Vector) -> Vector:
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) + pad(q, max_deg))


@validate_aliases
def sub(p: Vector, q: Vector) -> Vector:
    max_deg = max(deg(p), deg(q), 0)
    return trim(pad(p, max_deg) - pad(q, max_deg))


@validate_aliases
def mul(p: Vector, q: Vector) -> Vector:
    return trim(np.polymul(p[::-1], q[::-1])[::-1])


@validate_aliases
def monomial(coeff: int, degree: int) -> Vector:
    if degree < 0:
        raise ValueError("degree has to be non negative")

    p = np.zeros(degree + 1, dtype=object)
    p[degree] = coeff
    return p


@validate_aliases
def zero_poly(max_deg: int = 0) -> Vector:
    if max_deg < 0:
        raise ValueError("degree has to be non negative")

    return np.zeros(max_deg + 1, dtype=object)
