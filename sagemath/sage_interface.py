from typing import Any, Protocol

from numpy.typing import NDArray

type TArray = NDArray[Any]
type TVector = NDArray[Any]
type TMatrix = NDArray[Any]


DEFAULT_PORT = 5050
DEFAULT_AUTHKEY = b"sage"

# https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html
# https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/lattice.html
# https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.echelon_form
# https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.gram_schmidt


class SageEngineInterface(Protocol):
    def sage_version(self) -> tuple[int, int]: ...

    def gen_lattice(self, type: str, n: int, m: int, q: int, seed: int | None, quotient: TVector | None, dual: bool) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/lattice.html
        """
        ...

    def lll(self, lattice_basis: TMatrix, delta: float, transformation: bool) -> TMatrix | tuple[TMatrix, TMatrix]:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_rational_dense.html#sage.matrix.matrix_rational_dense.Matrix_rational_dense.LLL
        """
        ...

    def bkz(self, lattice_basis: TMatrix, delta: float, block_size: int) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_rational_dense.html#sage.matrix.matrix_rational_dense.Matrix_rational_dense.BKZ
        """
        ...

    def hkz(self, lattice_basis: TMatrix) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.HKZ
        """
        ...

    def shortest_vector(self, lattice_basis: TMatrix) -> TVector:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.shortest_vector
        """
        ...

    def closest_vector(self, lattice_basis: TMatrix, target_vector: TVector) -> TVector:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.closest_vector
        """
        ...

    def babai(self, algorithm: str, lattice_basis: TMatrix, target_vector: TVector, delta: float) -> TVector:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.approximate_closest_vector
        """
        ...

    def discriminant(self, lattice_basis: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.discriminant
        """
        ...

    def gaussian_heuristic(self, lattice_basis: TMatrix) -> float:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.gaussian_heuristic
        """
        ...

    def hadamard_ratio(self, lattice_basis: TMatrix) -> float:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.hadamard_ratio
        """
        ...

    def is_unimodular(self, lattice_basis: TMatrix) -> bool:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.is_unimodular
        """
        ...

    def volume(self, lattice_basis: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.volume
        """
        ...

    def hnf(self, matrix: TMatrix, transformation: bool) -> TMatrix | tuple[TMatrix, TMatrix]:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.echelon_form
        """
        ...

    def is_lll_reduced(self, lattice_basis: TMatrix, delta: float) -> bool:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.is_LLL_reduced
        """
        ...

    def gso(self, matrix: TMatrix, orthonormal: bool) -> tuple[TMatrix, TMatrix]:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.gram_schmidt
        """
        ...

    def left_kernel(self, matrix: TMatrix) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.left_kernel_matrix
        """
        ...

    def left_nullity(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.left_nullity
        """
        ...

    def right_kernel(self, matrix: TMatrix) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.right_kernel_matrix
        """
        ...

    def right_nullity(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.right_nullity
        """
        ...

    def rank(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.rank
        """
        ...

    def det(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.det
        """
        ...
