import numpy as np

from .._utils import as_integer
from ..linalg import hnf
from ..typing import Matrix, SquareMatrix, Vector, validate_aliases


def lwe_basis(A: Matrix, q: int) -> SquareMatrix:
    # lattice: L = { x | Ax = 0 mod q }
    m, _ = A.shape
    Im = q * as_integer(np.identity(m))
    G = np.vstack((A.T, Im))
    H, _ = hnf(G)

    return H[:m]


def sis_basis(A: Matrix, q: int) -> SquareMatrix:
    # lattice: L = { y | y = xA mod q }
    B_p = lwe_basis(A, q)
    B_inv = np.linalg.inv(B_p.astype(float))
    B_dual = np.round(q * B_inv.T).astype(int)
    return B_dual


@validate_aliases
def bai_galbraith(A: Matrix, b: Vector, q: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def kannan(A: Matrix, b: Vector, q: int, M: int = 1) -> SquareMatrix:
    # m, n = A.shape
    # Im = q *as_integer(np.identity(m))
    # In = as_integer(np.identity(n))

    raise NotImplementedError()


@validate_aliases
def subset_sum(sequence: Vector, S: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def ntru() -> SquareMatrix:
    raise NotImplementedError()
