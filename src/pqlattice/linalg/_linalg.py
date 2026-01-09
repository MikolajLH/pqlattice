from functools import reduce

import numpy as np

from .._utils import as_integer
from ..typing import Matrix, SquareMatrix, Vector, validate_aliases
from ._utils import row_add, row_scale, row_swap


@validate_aliases
def hnf(A: Matrix) -> tuple[Matrix, SquareMatrix]:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    tuple[Matrix, SquareMatrix]
        _description_
    """
    H, U, _ = _hnf(A)
    return H, U


@validate_aliases
def _hnf(a: Matrix) -> tuple[Matrix, SquareMatrix, int]:
    H = np.array(a, dtype=object)
    m, n = H.shape
    U = np.eye(m, dtype=object)
    pivot_row = 0
    pivot_col = 0
    det_U = 1

    while pivot_row < m and pivot_col < n:
        # pivot selection
        if np.all(H[pivot_row:, pivot_col] == 0):
            pivot_col += 1
            continue

        candidates = [(abs(H[i, pivot_col]), i) for i in range(pivot_row, m) if H[i, pivot_col] != 0]
        _, best_row = min(candidates)

        row_swap(H, pivot_row, best_row)
        row_swap(U, pivot_row, best_row)
        det_U *= -1

        # clear below pivot
        for i in range(pivot_row + 1, m):
            while H[i, pivot_col] != 0:
                factor = H[i, pivot_col] // H[pivot_row, pivot_col]

                row_add(H, i, pivot_row, -factor)
                row_add(U, i, pivot_row, -factor)

                if H[i, pivot_col] != 0:
                    row_swap(H, pivot_row, i)
                    row_swap(U, pivot_row, i)
                    det_U *= -1

        if H[pivot_row, pivot_col] < 0:
            row_scale(H, pivot_row, -1)
            row_scale(U, pivot_row, -1)
            det_U *= -1

        pivot_val = H[pivot_row, pivot_col]

        for i in range(pivot_row):
            factor = H[i, pivot_col] // pivot_val
            row_add(H, i, pivot_row, -factor)
            row_add(U, i, pivot_row, -factor)

        pivot_row += 1
        pivot_col += 1

    return H, U, det_U


@validate_aliases
def right_image(A: Matrix) -> Matrix:
    """
    _summary_

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    Matrix
        _description_
    """
    return left_image(A.T).T


@validate_aliases
def left_image(A: Matrix) -> Matrix:
    """
    _summary_

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    Matrix
        _description_
    """
    H, _ = hnf(A)

    m, _ = H.shape
    k = 0
    for i in range(m):
        if np.all(H[i] == 0):
            k = i
            break

    return as_integer(H[:k])


@validate_aliases
def left_kernel(A: Matrix):
    """
    {x : xA = 0}

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    _type_
        _description_
    """
    H, U = hnf(A)
    kernel_basis: list[Vector] = []

    m, _ = H.shape
    for i in range(m):
        if np.all(H[i] == 0):
            kernel_basis.append(U[i])

    return as_integer(kernel_basis)


@validate_aliases
def right_kernel(A: Matrix) -> Matrix:
    """
    {x : Ax = 0}

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    Matrix
        _description_
    """
    return left_kernel(A.T)


@validate_aliases
def left_nullity(a: Matrix) -> int:
    """_summary_

    Parameters
    ----------
    a : Matrix
        _description_

    Returns
    -------
    int
        _description_
    """
    kernel = left_kernel(a)
    return kernel.shape[0]


@validate_aliases
def right_nullity(a: Matrix) -> int:
    """_summary_

    Parameters
    ----------
    a : Matrix
        _description_

    Returns
    -------
    int
        _description_
    """
    kernel = right_kernel(a)
    return kernel.shape[0]


def rank(a: Matrix) -> int:
    """_summary_

    Parameters
    ----------
    a : Matrix
        _description_

    Returns
    -------
    int
        _description_
    """
    m, n = a.shape
    l_rank = m - left_nullity(a)
    r_rank = n - right_nullity(a)
    assert l_rank == r_rank
    return l_rank


@validate_aliases
def det(A: SquareMatrix) -> int:
    """_summary_

    Parameters
    ----------
    A : SquareMatrix
        _description_

    Returns
    -------
    int
        _description_
    """
    H, _, det_U = _hnf(A)

    return reduce(lambda a, b: a * b, np.diagonal(H), 1) * det_U


@validate_aliases
def minor(A: SquareMatrix, i: int, j: int) -> int:
    """_summary_

    Parameters
    ----------
    A : SquareMatrix
        _description_
    i : int
        _description_
    j : int
        _description_

    Returns
    -------
    int
        _description_
    """
    return det(np.delete(np.delete(A, i, axis=0), j, axis=1))


@validate_aliases
def cofactor(A: SquareMatrix, i: int, j: int) -> int:
    """_summary_

    Parameters
    ----------
    A : SquareMatrix
        _description_
    i : int
        _description_
    j : int
        _description_

    Returns
    -------
    int
        _description_
    """
    return minor(A, i, j) * ((-1) ** (i + 1 + j + 1))


@validate_aliases
def cofactor_matrix(A: SquareMatrix) -> SquareMatrix:
    """_summary_

    Parameters
    ----------
    A : SquareMatrix
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    n = A.shape[0]
    C = np.zeros((n, n), dtype=object)
    for i in range(n):
        for j in range(n):
            C[i, j] = cofactor(A, i, j)
    return C
