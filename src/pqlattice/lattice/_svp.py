from fractions import Fraction

from .._utils import as_integer, as_rational
from ..typing import SquareMatrix, Vector, validate_aliases
from ._gso import gso
from ._lll import lll


@validate_aliases
def schnorr_euchner_svp(mu: SquareMatrix, B: Vector) -> Vector:
    n = len(B)
    best_norm: Fraction = B[0]
    best_coeffs: Vector = as_integer([1] + [0] * (n - 1))

    r: Vector = as_rational([0] * (n + 1))
    c: Vector = as_rational([0] * n)
    x: Vector = as_integer([0] * n)
    v: Vector = as_rational([0] * n)

    last_move = [0] * n
    k = n - 1

    r[n] = Fraction(0)
    v[n - 1] = Fraction(0)
    c[n - 1] = Fraction(0)
    x[n - 1] = 0
    last_move[n - 1] = 0

    while True:
        y: Fraction = x[k] - c[k]
        current_norm: Fraction = r[k + 1] + (y * y * B[k])
        # print(f"{k=}: {current_norm=:.5f}, {best_norm=:.5f}")
        if current_norm < best_norm:
            if k == 0:
                if current_norm > 0:
                    best_norm = current_norm
                    best_coeffs = x.copy()

                k += 1
                last_move[k] += 1

                step_sign = -1 if (last_move[k] % 2 == 0) else 1
                step_mag = (last_move[k] + 1) // 2
                x[k] = round(c[k]) + (step_sign * step_mag)

            else:
                k -= 1
                center_val = Fraction(0)
                for j in range(k + 1, n):
                    center_val += mu[j][k] * x[j]

                c[k] = -center_val
                x[k] = round(c[k])
                last_move[k] = 0
                r[k + 1] = current_norm
        else:
            k += 1
            if k == n:
                break

            last_move[k] += 1
            step_sign = -1 if (last_move[k] % 2 == 0) else 1
            step_mag = (last_move[k] + 1) // 2

            x[k] = round(c[k]) + (step_sign * step_mag)

    return best_coeffs


@validate_aliases
def shortest_vector(lattice_basis: SquareMatrix) -> Vector:
    """_summary_

    Parameters
    ----------
    lattice_basis : SquareMatrix
        _description_

    Returns
    -------
    Vector
        _description_
    """
    B = lll(lattice_basis)
    B_star, U = gso(B)
    B_norms2 = as_rational([sum(x * x for x in v) for v in B_star])
    mu = U.T
    coeffs = schnorr_euchner_svp(mu, B_norms2)
    return coeffs @ B
