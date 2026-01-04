import math
from functools import reduce

import numpy as np

from .._utils import as_integer
from ..linalg._linalg import det
from ..linalg._utils import norm2, per_row_norm
from ..typing import SquareMatrix, Vector, validate_aliases


@validate_aliases
def volume(lattice_basis: SquareMatrix) -> int:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    int
        _description_
    """
    return abs(det(lattice_basis))


@validate_aliases
def rank(lattice_basis: SquareMatrix) -> int:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    int
        _description_
    """
    return lattice_basis.shape[0]


@validate_aliases
def discriminant(lattice_basis: SquareMatrix) -> int:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    int
        _description_
    """
    v = volume(lattice_basis)
    return v * v


@validate_aliases
def hadamard_ratio(lattice_basis: SquareMatrix) -> float:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    float
        _description_
    """
    return (volume(lattice_basis) / reduce(lambda a, b: a * b, per_row_norm(lattice_basis))) ** (1 / rank(lattice_basis))


@validate_aliases
def gaussian_heuristic(lattice_basis: SquareMatrix) -> float:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    float
        _description_
    """
    n = rank(lattice_basis)
    return math.sqrt(n / (2 * math.pi * math.e)) * (volume(lattice_basis) ** (1 / n))


@validate_aliases
def glr_2dim(lattice_basis: SquareMatrix) -> SquareMatrix:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    SquareMatrix
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    if lattice_basis.shape != (2, 2):
        raise ValueError("Lattice has to have rank 2 for gaussian reduction")

    w1: Vector = lattice_basis[0]
    w2: Vector = lattice_basis[1]

    v1 = w1.astype(float)
    v2 = w2.astype(float)
    if norm2(v1) > norm2(v2):
        v1, v2 = v2, v1

    while norm2(v2) > norm2(v1):
        m = np.rint(np.dot(v1, v2) / np.dot(v1, v1))
        if m == 0:
            return as_integer([v1, v2])
        v2 = v2 - m * v1
        if norm2(v1) > norm2(v2):
            v1, v2 = v2, v1

    return np.array([v1, v2])
