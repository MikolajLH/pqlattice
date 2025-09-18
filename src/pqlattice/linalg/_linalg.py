import numpy as np

from ..typing import Matrix, SquareMatrix, Vector, validate_aliases
from ._utils import row_add, row_scale, row_swap


@validate_aliases
def hnf(a: Matrix) -> tuple[Matrix, SquareMatrix]:
    """
    TODO: write docstring

    Parameters
    ----------
    a : Matrix
        _description_

    Returns
    -------
    tuple[Matrix, SquareMatrix]
        _description_
    """
    H = np.array(a, dtype=object)
    m, n = H.shape
    U = np.eye(m, dtype=object)  # The transformation matrix
    pivot_row = 0
    pivot_col = 0

    while pivot_row < m and pivot_col < n:
        # pivot selection
        if np.all(H[pivot_row:, pivot_col] == 0):
            pivot_col += 1
            continue

        candidates = [(abs(H[i, pivot_col]), i) for i in range(pivot_row, m) if H[i, pivot_col] != 0]
        _, best_row = min(candidates)

        row_swap(H, pivot_row, best_row)
        row_swap(U, pivot_row, best_row)

        # clear below pivot
        for i in range(pivot_row + 1, m):
            while H[i, pivot_col] != 0:
                factor = H[i, pivot_col] // H[pivot_row, pivot_col]

                row_add(H, i, pivot_row, -factor)
                row_add(U, i, pivot_row, -factor)

                if H[i, pivot_col] != 0:
                    row_swap(H, pivot_row, i)
                    row_swap(U, pivot_row, i)

        if H[pivot_row, pivot_col] < 0:
            row_scale(H, pivot_row, -1)
            row_scale(U, pivot_row, -1)

        pivot_val = H[pivot_row, pivot_col]

        # Reduce rows above pivot
        for i in range(pivot_row):
            factor = H[i, pivot_col] // pivot_val
            row_add(H, i, pivot_row, -factor)
            row_add(U, i, pivot_row, -factor)

        pivot_row += 1
        pivot_col += 1

    return H, U


@validate_aliases
def left_kernel(a: Matrix):
    """
    TODO: write docstring

    Parameters
    ----------
    A : Matrix
        _description_
    """
    return right_kernel(a.T)


@validate_aliases
def right_kernel(a: Matrix) -> Matrix:
    """
    TODO: write docstring

    Parameters
    ----------
    A : Matrix
        _description_
    """
    H, U = hnf(a.T)
    kernel_basis: list[Vector] = []

    m, _ = H.shape
    for i in range(m):
        if np.all(H[i] == 0):
            kernel_basis.append(U[i])

    return np.array(kernel_basis, dtype=object)


@validate_aliases
def left_nullity(a: Matrix) -> int:
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
def det(a: SquareMatrix):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrix
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def minor(a: SquareMatrix, i: int, j: int):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrix
        _description_
    i : int
        _description_
    j : int
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def cofactor(a: SquareMatrix, i: int, j: int):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrix
        _description_
    i : int
        _description_
    j : int
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def cofactor_matrix(a: SquareMatrix):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrix
        _description_
    """
    # TODO: implement
    pass
