from fractions import Fraction

import numpy as np

from .._utils import as_rational
from ..typing import Matrix, SquareMatrix, Vector, validate_aliases


@validate_aliases
def project_coeffs(q: Vector, b: Vector) -> Fraction:
    if np.dot(q, q) == 0:
        return Fraction(0, 1)

    return np.dot(b, q) / np.dot(q, q)


@validate_aliases
def gso(B: Matrix) -> tuple[Matrix, SquareMatrix]:
    """_summary_

    Parameters
    ----------
    B : Matrix
        _description_

    Returns
    -------
    tuple[Matrix, SquareMatrix]
        _description_
    """
    rows, _ = B.shape

    B_star: Matrix = as_rational(B)
    U: SquareMatrix = as_rational(np.identity(rows))

    for j in range(1, rows):
        b: Vector = B_star[j].copy()
        for i in range(j):
            U[i, j] = project_coeffs(B_star[i], b)
            B_star[j] -= U[i][j] * B_star[i]

    # B = U.T @ B_star
    return B_star, U
