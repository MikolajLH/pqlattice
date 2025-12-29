from functools import reduce

import numpy as np

from ..typing import Matrix, SquareMatrix, Vector, validate_aliases
from ._utils import row_add, row_scale, row_swap


@validate_aliases
def hnf(A: Matrix) -> tuple[Matrix, SquareMatrix]:
    H, U, _ = _hnf(A)
    return H, U


@validate_aliases
def _hnf(a: Matrix) -> tuple[Matrix, SquareMatrix, int]:
    H = np.array(a, dtype=object)
    m, n = H.shape
    U = np.eye(m, dtype=object)  # The transformation matrix
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

        # Reduce rows above pivot
        for i in range(pivot_row):
            factor = H[i, pivot_col] // pivot_val
            row_add(H, i, pivot_row, -factor)
            row_add(U, i, pivot_row, -factor)

        pivot_row += 1
        pivot_col += 1

    return H, U, det_U


@validate_aliases
def left_kernel(a: Matrix):
    return right_kernel(a.T)


@validate_aliases
def right_kernel(a: Matrix) -> Matrix:
    H, U = hnf(a.T)
    kernel_basis: list[Vector] = []

    m, _ = H.shape
    for i in range(m):
        if np.all(H[i] == 0):
            kernel_basis.append(U[i])

    return np.array(kernel_basis, dtype=object)


@validate_aliases
def left_nullity(a: Matrix) -> int:
    kernel = left_kernel(a)
    return kernel.shape[0]


@validate_aliases
def right_nullity(a: Matrix) -> int:
    kernel = right_kernel(a)
    return kernel.shape[0]


def rank(a: Matrix) -> int:
    m, n = a.shape
    l_rank = m - left_nullity(a)
    r_rank = n - right_nullity(a)
    assert l_rank == r_rank
    return l_rank


@validate_aliases
def det(A: SquareMatrix) -> int:
    H, _, det_U = _hnf(A)

    return reduce(lambda a, b: a * b, np.diagonal(H), 1) * det_U


@validate_aliases
def minor(A: SquareMatrix, i: int, j: int) -> int:
    return det(np.delete(np.delete(A, i, axis=0), j, axis=1))


@validate_aliases
def cofactor(A: SquareMatrix, i: int, j: int) -> int:
    return minor(A, i, j) * ((-1) ** (i + 1 + j + 1))


@validate_aliases
def cofactor_matrix(A: SquareMatrix) -> SquareMatrix:
    n = A.shape[0]
    C = np.zeros((n, n), dtype=object)
    for i in range(n):
        for j in range(n):
            C[i, j] = cofactor(A, i, j)
    return C
