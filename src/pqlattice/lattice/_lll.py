from fractions import Fraction

import numpy as np

from .._utils import as_integer
from ..typing import Matrix, SquareMatrix, validate_aliases
from ._gso import gso, project_coeffs


@validate_aliases
def lll(lattice_basis: Matrix, delta: float = 0.99) -> Matrix:
    """_summary_

    Parameters
    ----------
    lattice_basis : Matrix
        _description_
    delta : float, optional
        _description_, by default 0.99

    Returns
    -------
    Matrix
        _description_
    """
    rows, _ = lattice_basis.shape
    B: Matrix = as_integer(lattice_basis)
    while True:
        B_star, _ = gso(B)
        # Reduction Step
        for i in range(1, rows):
            for j in range(i - 1, -1, -1):
                c_ij = round(project_coeffs(B_star[j], B[i]))
                assert isinstance(c_ij, int)
                B[i] = B[i] - c_ij * B[j]
        # Swap step
        exists = False
        for i in range(rows - 1):
            u = project_coeffs(B_star[i], B[i + 1])
            r = u * B_star[i] + B_star[i + 1]
            if delta * np.dot(B_star[i], B_star[i]) > np.dot(r, r):
                B[[i, i + 1]] = B[[i + 1, i]]
                exists = True
                break
        if not exists:
            break
    return B


@validate_aliases
def is_size_reduced(lattice_basis: SquareMatrix) -> bool:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    bool
        _description_
    """
    _, U = gso(lattice_basis)
    return bool(np.all(np.triu(U, 1) <= Fraction(1, 2)))


@validate_aliases
def lovasz_condition(lattice_basis: SquareMatrix, delta: float) -> bool:
    norm2 = lambda a: np.sum(a * a, axis=1)  # type: ignore
    G, U = gso(lattice_basis)
    lhs = delta * norm2(G[:-1])
    rhs = norm2(G[1:] + np.diag(U, 1)[:, np.newaxis] * G[:-1])
    return bool(np.all(lhs <= rhs))


@validate_aliases
def is_lll_reduced(lattice_basis: SquareMatrix, delta: float = 0.99) -> bool:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_
    delta : float, optional
        _description_, by default 0.99

    Returns
    -------
    bool
        _description_
    """
    return is_size_reduced(lattice_basis) and lovasz_condition(lattice_basis, delta)
