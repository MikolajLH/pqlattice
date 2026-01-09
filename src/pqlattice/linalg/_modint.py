import numpy as np

from .._utils import as_integer
from ..integer._modintring import ModIntRing
from ..typing import Matrix, SquareMatrix, Vector, validate_aliases
from ._utils import row_add, row_scale, row_swap


@validate_aliases
def mod_ref(A: Matrix, modulus: int) -> tuple[Matrix, SquareMatrix]:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    tuple[Matrix, SquareMatrix]
        _description_
    """
    R = ModIntRing(modulus)
    m, n = A.shape

    M = R.mod(as_integer(A))
    U = as_integer(np.identity(m))

    for j in range(min(m, n)):
        col = M[:, j]
        nonzero = np.nonzero(col[j:])[0]
        if len(nonzero) == 0:
            continue
        pivot_i = nonzero[0] + j

        if pivot_i != j:
            row_swap(M, pivot_i, j)
            row_swap(U, pivot_i, j)

        pivot: int = M[j, j]
        pivot_inv = R.inv(pivot)
        row_scale(M, j, pivot_inv)
        row_scale(U, j, pivot_inv)

        M = R.mod(M)
        U = R.mod(U)

        for i in range(j + 1, m):
            if M[i, j] != 0:
                row_add(U, i, j, -M[i, j])
                row_add(M, i, j, -M[i, j])
                M = R.mod(M)
                U = R.mod(U)

    return R.mod(M), R.mod(U)


@validate_aliases
def mod_rref(A: Matrix, modulus: int) -> tuple[Matrix, SquareMatrix]:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    tuple[Matrix, SquareMatrix]
        _description_
    """
    R = ModIntRing(modulus)
    m, n = A.shape
    M, U = mod_ref(A, modulus)

    h = m - 1
    for j in range(n - 1, -1, -1):
        if M[h, j] != 1:
            if M[h, j] == 0:
                h -= 1
            continue

        for i in range(h - 1, -1, -1):
            coeff = M[i, j]
            row_add(M, i, h, -coeff)
            row_add(U, i, h, -coeff)

        h -= 1

    return R.mod(M), R.mod(U)


@validate_aliases
def mod_left_kernel(A: Matrix, modulus: int) -> Matrix:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    Matrix
        _description_
    """
    return mod_right_kernel(A.T, modulus)


@validate_aliases
def mod_right_kernel(A: Matrix, modulus: int) -> Matrix:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    Matrix
        _description_
    """
    M, U = mod_rref(A.T, modulus)
    kernel_basis: list[Vector] = []

    m, _ = M.shape
    for i in range(m):
        if np.all(M[i] == 0):
            kernel_basis.append(U[i])

    return as_integer(kernel_basis)


def mod_left_image(A: Matrix, modulus: int) -> Matrix:
    raise NotImplementedError()


def mod_right_image(A: Matrix, modulus: int) -> Matrix:
    raise NotImplementedError()


@validate_aliases
def mod_left_nullity(A: Matrix, modulus: int) -> int:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_
    """
    kernel = mod_left_kernel(A, modulus)
    return kernel.shape[0]


@validate_aliases
def mod_right_nullity(A: Matrix, modulus: int) -> int:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_
    """
    kernel = mod_right_kernel(A, modulus)
    return kernel.shape[0]


def mod_matinv(A: SquareMatrix, modulus: int) -> SquareMatrix:
    """_summary_

    Parameters
    ----------
    A : SquareMatrix
        _description_
    modulus : int
        _description_

    Returns
    -------
    SquareMatrix
        _description_
    """
    n = A.shape[0]
    AId = np.hstack((A, as_integer(np.identity(n))))
    R, _ = mod_rref(AId, modulus)
    return as_integer(R[:, n:])
