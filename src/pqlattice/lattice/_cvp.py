import numpy as np

from .._utils import as_integer, as_rational
from ..typing import SquareMatrix, Vector, validate_aliases
from ._gso import gso, project_coeffs
from ._lll import lll


@validate_aliases
def schnorr_euchner_cvp(mu: SquareMatrix, B: Vector, target_coeffs: Vector) -> Vector:
    raise NotImplementedError()


@validate_aliases
def closest_vector(lattice_basis: SquareMatrix, target_vector: Vector) -> Vector:
    raise NotImplementedError()


@validate_aliases
def babai_nearest_plane(lattice_basis: SquareMatrix, target_vector: Vector) -> Vector:
    n, _ = lattice_basis.shape
    B = lll(lattice_basis)
    b = as_rational(target_vector)
    for j in range(n - 1, -1, -1):
        B_star, _ = gso(B)
        cj = round(project_coeffs(B_star[j], b))
        b -= cj * B[j]

    return as_integer(as_rational(target_vector) - b)


@validate_aliases
def babai_closest_vector(lattice_basis: SquareMatrix, target_vector: Vector) -> Vector:
    return as_integer(np.rint(target_vector @ np.linalg.inv(lattice_basis.astype(float))))
