import random

import numpy as np

from .._utils import as_integer, zeros_mat
from ..typing import SquareMatrix


def _gen_unimodular(n: int, rounds: int, rng: random.Random) -> SquareMatrix:
    U = as_integer(np.eye(n))
    for _ in range(rounds):
        i, j = rng.sample(range(n), 2)
        coeff = rng.sample([-1, 1], 1)

        U[i] += coeff * U[j]

    return U


def randlattice(n: int, det_upper_bound: int | None = None, seed: int | None = None) -> SquareMatrix:
    """
    Generates lattice basis by, first generating random square matrix in Hermite normal form and then by transforming it using random unimodular matrix.

    Parameters
    ----------
    n : int
        lattice's rank
    det_upper_bound : int | None, optional
        upper bound of lattice volume, by default 2 ** n
    seed : int | None, optional
        seed for random number generator

    Returns
    -------
    SquareMatrix
        n x n matrix representing lattice basis
    """
    det_ub: int = 2**n if det_upper_bound is None else det_upper_bound

    rng = random.Random(seed)
    diagonals = [rng.randint(1, det_ub) for _ in range(n)]

    H = zeros_mat(n)
    for i in range(n):
        H[i, i] = diagonals[i]
        modulus = H[i, i]
        for j in range(i, n):
            H[i, j] = rng.randint(0, modulus - 1)

    U = _gen_unimodular(n, n * 5, rng)

    basis = U @ H
    return basis
