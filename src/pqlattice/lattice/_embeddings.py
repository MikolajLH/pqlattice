import numpy as np

from .._utils import as_integer, zeros_mat
from ..linalg import hnf
from ..typing import Matrix, SquareMatrix, Vector, validate_aliases


def lwe_basis(A: Matrix, q: int) -> SquareMatrix:
    """
    _summary_

    Parameters
    ----------
    A : Matrix
        _description_
    q : int
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    # lattice: L = { x | Ax = 0 mod q }
    m, _ = A.shape
    Im = q * as_integer(np.identity(m))
    G = np.vstack((A.T, Im))
    H, _ = hnf(G)

    return H[:m]


def sis_basis(A: Matrix, q: int) -> SquareMatrix:
    """
    _summary_

    Parameters
    ----------
    A : Matrix
        _description_
    q : int
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    # lattice: L = { y | y = xA mod q }
    B_p = lwe_basis(A, q)
    B_inv = np.linalg.inv(B_p.astype(float))
    B_dual = np.round(q * B_inv.T).astype(int)
    return B_dual


@validate_aliases
def kannan(A: Matrix, b: Vector, q: int) -> SquareMatrix:
    """
    _summary_

    Parameters
    ----------
    A : Matrix
        _description_
    b : Vector
        _description_
    q : int
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    return bai_galbraith(A, b, q, 1)


@validate_aliases
def bai_galbraith(A: Matrix, b: Vector, q: int, M: int) -> SquareMatrix:
    """
    _summary_

    Parameters
    ----------
    A : Matrix
        _description_
    b : Vector
        _description_
    q : int
        _description_
    M : int
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    m, n = A.shape

    Im = as_integer(np.identity(m))
    In = as_integer(np.identity(n))

    Zmxn = zeros_mat(m, n)
    Zmx1 = zeros_mat(m, 1)
    Znx1 = zeros_mat(n, 1)
    Z1xn = zeros_mat(1, n)

    bT = b.reshape(1, -1)
    IM = M * (zeros_mat(1, 1) + 1)

    return np.block(
        [
            [q * Im, Zmxn, Zmx1],
            [A.T, In, Znx1],
            [-bT, Z1xn, IM],
        ]
    )


@validate_aliases
def subset_sum(sequence: Vector, S: int) -> SquareMatrix:
    """
    _summary_

    Parameters
    ----------
    sequence : Vector
        _description_
    S : int
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    n = len(sequence)
    A = as_integer(np.identity(n + 1) * 2)
    A[-1] = 1
    A[:-1, -1] = sequence
    A[-1, -1] = S

    return A


@validate_aliases
def ntru() -> SquareMatrix:
    raise NotImplementedError()
