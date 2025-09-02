from collections.abc import Callable

import numpy as np

from ..typing import Matrix, MatrixFloat, SquareMatrix, SquareMatrixFloat, validate_aliases


@validate_aliases
def GSO(B: Matrix) -> tuple[MatrixFloat, SquareMatrixFloat]:
    m, n = B.shape
    assert m == n

    proj_coeff: Callable[[float, float], float] = lambda q, b: np.dot(b, q) / np.dot(q, q)

    B_star = B.astype(float)
    U = np.identity(m)

    for j in range(1, m):
        b = B_star[j].copy()
        for i in range(j):
            U[i, j] = proj_coeff(B_star[i], b)
            B_star[j] -= U[i][j] * B_star[i]

    # B = U.T @ B_star
    return B_star, U  # type: ignore


def LLL(lattice_basis: SquareMatrix, delta: float = 0.75) -> SquareMatrixFloat:
    n = lattice_basis.shape[0]
    B = lattice_basis.astype(float)
    while True:
        Bstar, _ = GSO(B)
        # Reduction Step
        for i in range(1, n):
            for j in range(i - 1, -1, -1):
                cij = round(np.dot(B[i], Bstar[j]) / np.dot(Bstar[j], Bstar[j]))
                B[i] = B[i] - cij * B[j]
        # Swap step
        exists = False
        for i in range(n - 1):
            u = np.dot(B[i + 1], Bstar[i]) / np.dot(Bstar[i], Bstar[i])
            r = u * Bstar[i] + Bstar[i + 1]
            if delta * np.dot(Bstar[i], Bstar[i]) > np.dot(r, r):
                B[[i, i + 1]] = B[[i + 1, i]]
                exists = True
                break
        if not exists:
            break
    return B
