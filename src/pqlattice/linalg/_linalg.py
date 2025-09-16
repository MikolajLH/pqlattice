import numpy as np

from ..typing import MatrixInt, SquareMatrixInt, validate_aliases
from ._utils import row_add, row_scale, row_swap


@validate_aliases
def hnf(a: MatrixInt) -> tuple[MatrixInt, SquareMatrixInt]:
    """
    TODO: write docstring

    Parameters
    ----------
    a : MatrixInt
        _description_

    Returns
    -------
    tuple[MatrixInt, SquareMatrixInt]
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
def left_kernel(a: MatrixInt):
    """
    TODO: write docstring

    Parameters
    ----------
    A : MatrixInt
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def right_kernel(a: MatrixInt):
    """
    TODO: write docstring

    Parameters
    ----------
    A : MatrixInt
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def nullity(a: MatrixInt):
    """
    TODO: write docstring

    Parameters
    ----------
    A : MatrixInt
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def det(a: SquareMatrixInt):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrixInt
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def minor(a: SquareMatrixInt, i: int, j: int):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrixInt
        _description_
    i : int
        _description_
    j : int
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def cofactor(a: SquareMatrixInt, i: int, j: int):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrixInt
        _description_
    i : int
        _description_
    j : int
        _description_
    """
    # TODO: implement
    pass


@validate_aliases
def cofactor_matrix(a: SquareMatrixInt):
    """
    TODO: write docstring

    Parameters
    ----------
    A : SquareMatrixInt
        _description_
    """
    # TODO: implement
    pass
