from .. import settings
from ..typing import SquareMatrix, Vector
from . import embeddings
from ._cvp import babai_closest_vector, babai_nearest_plane, closest_vector
from ._gso import gso
from ._lattice import discriminant, gaussian_heuristic, glr_2dim, hadamard_ratio, rank, volume
from ._lll import is_lll_reduced, is_size_reduced


def lll(lattice_basis: SquareMatrix, delta: float = 0.99) -> SquareMatrix:
    return settings.get_backend().lll(lattice_basis, delta)


def bkz(lattice_basis: SquareMatrix, block_size: int = 10, delta: float = 0.99) -> SquareMatrix:
    return settings.get_backend().bkz(lattice_basis, block_size, delta)


def hkz(lattice_basis: SquareMatrix, delta: float = 0.99) -> SquareMatrix:
    return settings.get_backend().hkz(lattice_basis, delta)


def shortest_vector(lattice_basis: SquareMatrix) -> Vector:
    return settings.get_backend().shortest_vector(lattice_basis)


__all__ = [
    "volume",
    "rank",
    "hadamard_ratio",
    "discriminant",
    "gaussian_heuristic",
    "glr_2dim",
    "gso",
    "lll",
    "is_lll_reduced",
    "is_size_reduced",
    "bkz",
    "hkz",
    "shortest_vector",
    "closest_vector",
    "babai_closest_vector",
    "babai_nearest_plane",
    "embeddings",
]
