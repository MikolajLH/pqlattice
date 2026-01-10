from typing import Any, override

from .._utils import as_integer
from ..typing import Array, Matrix, SquareMatrix, Vector
from ._protocol import BackendInterface

try:
    import fpylll

    HAS_FPYLLL = True
except ImportError:
    HAS_FPYLLL = False

try:
    import flint

    HAS_FLINT = True
except ImportError:
    HAS_FLINT = False


class FastBackend(BackendInterface):
    def __init__(self) -> None:
        if not (HAS_FPYLLL and HAS_FLINT):
            raise RuntimeError("Fast backend is unavailable - dependencies missing")

    def _to_fpylll(self, a: Array) -> Any:
        return fpylll.IntegerMatrix.from_matrix(a.tolist())

    def _from_fpylll(self, mat: Any) -> Array:
        data = [list(row) for row in mat]
        return as_integer(data)

    def _to_flint(self, a: Array) -> Any:
        return flint.fmpz_mat(a.tolist())

    def _from_flint(self, mat: Any) -> Array:
        return as_integer(mat.table())

    @override
    def lll(self, lattice_basis: SquareMatrix, delta: float) -> SquareMatrix:
        mat = self._to_fpylll(lattice_basis)
        fpylll.LLL.reduction(mat, delta=delta)
        return self._from_fpylll(mat)

    @override
    def bkz(self, lattice_basis: SquareMatrix, block_size: int, delta: float) -> SquareMatrix:
        mat = self._to_fpylll(lattice_basis)
        # fpylll.BKZ.reduction(mat, delta=delta)
        mat_bkz = fpylll.BKZ.reduction(mat, fpylll.BKZ.Param(block_size=block_size))
        return self._from_fpylll(mat_bkz)

    @override
    def hkz(self, lattice_basis: SquareMatrix, delta: float) -> SquareMatrix:
        return self.bkz(lattice_basis, len(lattice_basis), delta)

    @override
    def shortest_vector(self, lattice_basis: SquareMatrix) -> Vector:
        mat = self._to_fpylll(lattice_basis)
        fpylll.LLL.reduction(mat)
        sv = fpylll.SVP.shortest_vector(mat, pruning=False, preprocess=False)
        return as_integer(sv)

    @override
    def closest_vector(self, lattice_basis: SquareMatrix, target_vector: Vector) -> Vector:
        A = self._from_fpylll(lattice_basis)
        t = target_vector.tolist()
        v0 = fpylll.CVP.closest_vector(A, t)
        return as_integer(v0)

    @override
    def hnf(self, matrix: Matrix) -> tuple[Matrix, SquareMatrix]:
        mat = self._to_flint(matrix)
        H, U = mat.hnf(transform=True)
        return self._from_flint(H), self._from_flint(U)
