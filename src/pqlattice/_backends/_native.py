from typing import override

from ..lattice._bkz import bkz
from ..lattice._hkz import hkz
from ..lattice._lll import lll
from ..lattice._svp import shortest_vector
from ..linalg._linalg import hnf
from ..typing import Matrix, SquareMatrix, Vector
from ._protocol import BackendInterface


class NativeBackend(BackendInterface):
    @override
    def lll(self, lattice_basis: SquareMatrix, delta: float) -> SquareMatrix:
        return lll(lattice_basis, delta)

    @override
    def bkz(self, lattice_basis: SquareMatrix, block_size: int, delta: float) -> SquareMatrix:
        _ = delta
        return bkz(lattice_basis, block_size)

    @override
    def hkz(self, lattice_basis: SquareMatrix, delta: float) -> SquareMatrix:
        _ = delta
        return hkz(lattice_basis)

    @override
    def shortest_vector(self, lattice_basis: SquareMatrix) -> Vector:
        return shortest_vector(lattice_basis)

    @override
    def hnf(self, matrix: Matrix) -> tuple[Matrix, SquareMatrix]:
        return hnf(matrix)
