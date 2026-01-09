# for compatibility with sage modules to silence Unknown type errors
# ruff: noqa: F405
# ruff: noqa: F403
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
import multiprocessing as mp
import re
from concurrent.futures import ProcessPoolExecutor
from multiprocessing.managers import BaseManager
from typing import Any, override

import numpy as np
from sage.all import *
from sage.modules.free_module_integer import IntegerLattice
from sage.version import version
from sage_interface import DEFAULT_AUTHKEY, DEFAULT_PORT, SageEngineInterface, TMatrix, TVector


def to_numpy(sage_obj: Any) -> TMatrix | TVector:
    arr = sage_obj.numpy(dtype=object)
    if arr.size == 0:
        return arr
    return (np.vectorize(int)(arr.flat).reshape(arr.shape)).astype(object)


def _gen_lattice_task(type: str, n: int, m: int, q: int, seed: int | None, quotient: TVector | None, dual: bool) -> TMatrix:
    n = Integer(n)
    m = Integer(m)
    q = Integer(q)
    seed = None if seed is None else Integer(seed)
    quotient = None  # if quotient is None else Polynomial()
    print(f"{n=} {m=} {q=}")
    try:
        sage_res = sage.crypto.gen_lattice(type, n, m, q, seed, quotient, dual)
        print(f"{sage_res}")
        return to_numpy(sage_res)
    except Exception as e:
        print(f"{e}")

    return None  # type: ignore


def _gso_task(mat: TMatrix, orthonormal: bool) -> tuple[TMatrix, TMatrix]:
    m = Matrix(RDF, mat.tolist())
    r, u = m.gram_schmidt(orthonormal=orthonormal)
    return r.numpy(dtype=float), u.numpy(dtype=float)


def _lll_task(mat: TMatrix, delta: float, transformation: bool) -> TMatrix | tuple[TMatrix, TMatrix]:
    m = Matrix(ZZ, mat.tolist())
    if not transformation:
        r = m.LLL(delta=delta, transformation=transformation)
        return to_numpy(r)
    else:
        r, u = m.LLL(delta=delta, transformation=transformation)
        return to_numpy(r), to_numpy(u)


def _is_lll_reduced_task(mat: TMatrix, delta: float) -> bool:
    m = Matrix(ZZ, mat.tolist())
    return bool(m.is_LLL_reduced(delta=delta))


def _bkz_task(mat: TMatrix, delta: float, block_size: int) -> TMatrix:
    m = IntegerLattice(mat.tolist())
    return to_numpy(m.BKZ(delta=delta, block_size=block_size))


def _hkz_task(mat: TMatrix) -> TMatrix:
    m = IntegerLattice(mat.tolist())
    return to_numpy(m.HKZ())


def _svp_task(mat: TMatrix) -> TVector:
    m = IntegerLattice(mat.tolist())
    v = m.shortest_vector()
    return to_numpy(v)


def _cvp_task(mat: TMatrix, t: TVector) -> TVector:
    m = IntegerLattice(mat.tolist())
    return to_numpy(m.closest_vector(vector(RDF, t)))


def _babai_task(mat: TMatrix, t: TVector, alg: str, d: float) -> TVector:
    m = IntegerLattice(mat.tolist())
    return to_numpy(m.approximate_closest_vector(vector(RDF, t), delta=d, algorithm=alg))


def _hnf_task(mat: TMatrix, transformation: bool) -> TMatrix | tuple[TMatrix, TMatrix]:
    m = Matrix(ZZ, mat.tolist())
    if not transformation:
        r = m.echelon_form(transformation=transformation)
        return to_numpy(r)
    else:
        r, u = m.echelon_form(transformation=transformation)
        return to_numpy(r), to_numpy(u)


def _left_kernel_task(mat: TMatrix) -> TMatrix:
    m = Matrix(ZZ, mat.tolist())
    r = m.left_kernel_matrix()
    return to_numpy(r)


def _left_nullity_task(mat: TMatrix) -> int:
    m = Matrix(ZZ, mat.tolist())
    r = m.left_nullity()
    return int(r)


def _right_kernel_task(mat: TMatrix) -> TMatrix:
    m = Matrix(ZZ, mat.tolist())
    r = m.right_kernel_matrix()
    return to_numpy(r)


def _right_nullity_task(mat: TMatrix) -> int:
    m = Matrix(ZZ, mat.tolist())
    r = m.right_nullity()
    return int(r)


def _rank_task(mat: TMatrix) -> int:
    m = Matrix(ZZ, mat.tolist())
    r = m.rank()
    return int(r)


def _det_task(mat: TMatrix) -> int:
    m = Matrix(ZZ, mat.tolist())
    r = m.det()
    return int(r)


def _discriminant_task(mat: TMatrix) -> int:
    m = IntegerLattice(mat.tolist(), lll_reduce=False)
    d = m.discriminant()
    return int(d)


def _gaussian_heuristic_task(mat: TMatrix) -> float:
    m = IntegerLattice(mat.tolist(), lll_reduce=False)
    d = m.gaussian_heuristic().n()
    return float(d)


def _hadamard_ratio_task(mat: TMatrix) -> float:
    m = IntegerLattice(mat.tolist(), lll_reduce=False)
    d = m.hadamard_ratio(use_reduced_basis=False).n()
    return float(d)


def _is_unimodular_task(mat: TMatrix) -> bool:
    m = IntegerLattice(mat.tolist(), lll_reduce=False)
    d = m.is_unimodular()
    return bool(d)


def _volume_task(mat: TMatrix) -> int:
    m = IntegerLattice(mat.tolist(), lll_reduce=False)
    d = m.volume()
    return int(d)


class SageEngine(SageEngineInterface):
    def __init__(self):
        ctx = mp.get_context("spawn")
        self.pool = ProcessPoolExecutor(max_workers=1, mp_context=ctx)

    def sage_version(self) -> tuple[int, int]:
        if match := re.search(r"(\d+\.\d+)", version):
            major, minor = match.group(0).split(".")
            return int(major), int(minor)
        else:
            return 0, 0

    @override
    def gen_lattice(self, type: str = "modular", n: int = 4, m: int = 8, q: int = 11, seed: int | None = None, quotient: TVector | None = None, dual: bool = False) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/lattice.html
        """
        print("call gen_lattice")
        future = self.pool.submit(_gen_lattice_task, type, n, m, q, seed, quotient, dual)
        res = future.result()
        return res

    @override
    def gso(self, matrix: TMatrix, orthonormal: bool = False) -> tuple[TMatrix, TMatrix]:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.gram_schmidt
        """
        print("call gso")
        future = self.pool.submit(_gso_task, matrix, orthonormal)
        res = future.result()
        return res

    @override
    def lll(self, lattice_basis: TMatrix, delta: float = 0.99, transformation: bool = False) -> TMatrix | tuple[TMatrix, TMatrix]:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_rational_dense.html#sage.matrix.matrix_rational_dense.Matrix_rational_dense.LLL
        """
        print("call lll")
        future = self.pool.submit(_lll_task, lattice_basis, delta, transformation)
        res = future.result()
        return res

    @override
    def is_lll_reduced(self, lattice_basis: TMatrix, delta: float = 0.99) -> bool:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.is_LLL_reduced
        """
        print("call is_lll_reduced")
        future = self.pool.submit(_is_lll_reduced_task, lattice_basis, delta)
        res = future.result()
        return res

    @override
    def bkz(self, lattice_basis: TMatrix, delta: float = 0.99, block_size: int = 10) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_rational_dense.html#sage.matrix.matrix_rational_dense.Matrix_rational_dense.BKZ
        """
        print("call bkz")
        future = self.pool.submit(_bkz_task, lattice_basis, delta, block_size)
        res = future.result()
        return res

    @override
    def hkz(self, lattice_basis: TMatrix) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.HKZ
        """
        print("call hkz")
        future = self.pool.submit(_hkz_task, lattice_basis)
        res = future.result()
        return res

    @override
    def shortest_vector(self, lattice_basis: TMatrix) -> TVector:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.shortest_vector
        """
        print("call shortest_vector")
        future = self.pool.submit(_svp_task, lattice_basis)
        res = future.result()
        return res

    @override
    def closest_vector(self, lattice_basis: TMatrix, target_vector: TVector) -> TVector:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.closest_vector
        """
        print("call closest_vector")
        future = self.pool.submit(_cvp_task, lattice_basis, target_vector)
        res = future.result()
        return res

    @override
    def babai(self, algorithm: str, lattice_basis: TMatrix, target_vector: TVector, delta: float = 0.99) -> TVector:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.approximate_closest_vector
        """
        print("call babai")
        future = self.pool.submit(_babai_task, lattice_basis, target_vector, algorithm, delta)
        res = future.result()
        return res

    @override
    def hnf(self, matrix: TMatrix, transformation: bool = False) -> TMatrix | tuple[TMatrix, TMatrix]:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.echelon_form
        """
        print("call hnf")
        future = self.pool.submit(_hnf_task, matrix, transformation)
        res = future.result()
        return res

    @override
    def left_kernel(self, matrix: TMatrix) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.left_kernel_matrix
        """
        print("call left_kernel")
        future = self.pool.submit(_left_kernel_task, matrix)
        res = future.result()
        return res

    @override
    def left_nullity(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.left_nullity
        """
        print("call left_nullity")
        future = self.pool.submit(_left_nullity_task, matrix)
        res = future.result()
        return res

    @override
    def right_kernel(self, matrix: TMatrix) -> TMatrix:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.right_kernel_matrix
        """
        print("call right_kernel")
        future = self.pool.submit(_right_kernel_task, matrix)
        res = future.result()
        return res

    @override
    def right_nullity(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.right_nullity
        """
        print("call right_nullity")
        future = self.pool.submit(_right_nullity_task, matrix)
        res = future.result()
        return res

    @override
    def rank(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense.rank
        """
        print("call rank")
        future = self.pool.submit(_rank_task, matrix)
        res = future.result()
        return res

    @override
    def det(self, matrix: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix2.html#sage.matrix.matrix2.Matrix.det
        """
        print("call det")
        future = self.pool.submit(_det_task, matrix)
        res = future.result()
        return res

    @override
    def discriminant(self, lattice_basis: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.discriminant
        """
        print("call discriminant")
        future = self.pool.submit(_discriminant_task, lattice_basis)
        res = future.result()
        return res

    @override
    def gaussian_heuristic(self, lattice_basis: TMatrix) -> float:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.gaussian_heuristic
        """
        print("call gaussian_heuristic")
        future = self.pool.submit(_gaussian_heuristic_task, lattice_basis)
        res = future.result()
        return res

    @override
    def hadamard_ratio(self, lattice_basis: TMatrix) -> float:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.hadamard_ratio
        """
        print("call hadamard_ratio")
        future = self.pool.submit(_hadamard_ratio_task, lattice_basis)
        res = future.result()
        return res

    @override
    def is_unimodular(self, lattice_basis: TMatrix) -> bool:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.is_unimodular
        """
        print("call is_unimodular")
        future = self.pool.submit(_is_unimodular_task, lattice_basis)
        res = future.result()
        return res

    @override
    def volume(self, lattice_basis: TMatrix) -> int:
        """
        https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html#sage.modules.free_module_integer.FreeModule_submodule_with_basis_integer.volume
        """
        print("call volume")
        future = self.pool.submit(_volume_task, lattice_basis)
        res = future.result()
        return res


class SageManager(BaseManager):
    pass


SageManager.register("get_engine", callable=lambda: SageEngine())


def main():
    manager = SageManager(address=("", DEFAULT_PORT), authkey=DEFAULT_AUTHKEY)
    print(f"Sage version: {SageEngine().sage_version()}")
    print(f"Sage server listening on {DEFAULT_PORT}...")
    manager.get_server().serve_forever()


if __name__ == "__main__":
    main()
