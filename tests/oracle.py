# pyright: reportAttributeAccessIssue=false
import math

import gmpy2
import pytest
from sagemath.sage_interface import SageEngineInterface, TMatrix, TVector


def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)


def is_prime(n: int) -> bool:
    return bool(gmpy2.is_prime(n))  # type: ignore


def next_prime(n: int) -> int:
    return int(gmpy2.next_prime(n))  # type: ignore


class Sage:
    _engine: SageEngineInterface | None = None

    @classmethod
    def _get_engine(cls) -> SageEngineInterface:
        if cls._engine is None:
            pytest.skip("Skipping: Test requires SageMath (--sage flag not set)")
        return cls._engine

    @classmethod
    def _check_version(cls) -> None:
        v_major, v_minor = cls._get_engine().sage_version()
        version = float(f"{v_major}.{v_minor}")
        if version < 10.8:
            pytest.skip(f"Need Sage 10.8+, got {version}")

    # -- Public API

    @classmethod
    def gen_lattice(cls, type: str = "modular", n: int = 4, m: int = 8, q: int = 11, seed: int | None = None, quotient: TVector | None = None, dual: bool = False) -> TMatrix:
        return cls._get_engine().gen_lattice(type, n, m, q, seed, quotient, dual)

    @classmethod
    def lll(cls, lattice_basis: TMatrix, delta: float = 0.99, transformation: bool = False) -> TMatrix | tuple[TMatrix, TMatrix]:
        return cls._get_engine().lll(lattice_basis, delta, transformation)

    @classmethod
    def bkz(cls, lattice_basis: TMatrix, delta: float = 0.99, block_size: int = 10) -> TMatrix:
        return cls._get_engine().bkz(lattice_basis, delta, block_size)

    @classmethod
    def hkz(cls, lattice_basis: TMatrix) -> TMatrix:
        return cls._get_engine().hkz(lattice_basis)

    @classmethod
    def shortest_vector(cls, lattice_basis: TMatrix) -> TVector:
        return cls._get_engine().shortest_vector(lattice_basis)

    @classmethod
    def closest_vector(cls, lattice_basis: TMatrix, target_vector: TVector) -> TVector:
        return cls._get_engine().closest_vector(lattice_basis, target_vector)

    @classmethod
    def babai(cls, algorithm: str, lattice_basis: TMatrix, target_vector: TVector, delta: float = 0.99) -> TVector:
        return cls._get_engine().babai(algorithm, lattice_basis, target_vector, delta)

    @classmethod
    def discriminant(cls, lattice_basis: TMatrix) -> int:
        return cls._get_engine().discriminant(lattice_basis)

    @classmethod
    def gaussian_heuristic(cls, lattice_basis: TMatrix) -> float:
        cls._check_version()
        return cls._get_engine().gaussian_heuristic(lattice_basis)

    @classmethod
    def hadamard_ratio(cls, lattice_basis: TMatrix) -> float:
        cls._check_version()
        return cls._get_engine().hadamard_ratio(lattice_basis)

    @classmethod
    def is_unimodular(cls, lattice_basis: TMatrix) -> bool:
        return cls._get_engine().is_unimodular(lattice_basis)

    @classmethod
    def volume(cls, lattice_basis: TMatrix) -> float:
        return cls._get_engine().volume(lattice_basis)

    @classmethod
    def hnf(cls, matrix: TMatrix, transformation: bool = False) -> TMatrix | tuple[TMatrix, TMatrix]:
        return cls._get_engine().hnf(matrix, transformation)

    @classmethod
    def is_lll_reduced(cls, lattice_basis: TMatrix, delta: float = 0.99) -> bool:
        return cls._get_engine().is_lll_reduced(lattice_basis, delta)

    @classmethod
    def gso(cls, matrix: TMatrix, orthonormal: bool = False) -> tuple[TMatrix, TMatrix]:
        return cls._get_engine().gso(matrix, orthonormal)

    @classmethod
    def left_kernel(cls, matrix: TMatrix) -> TMatrix:
        return cls._get_engine().left_kernel(matrix)

    @classmethod
    def left_nullity(cls, matrix: TMatrix) -> int:
        return cls._get_engine().left_nullity(matrix)

    @classmethod
    def right_kernel(cls, matrix: TMatrix) -> TMatrix:
        return cls._get_engine().right_kernel(matrix)

    @classmethod
    def right_nullity(cls, matrix: TMatrix) -> int:
        return cls._get_engine().right_nullity(matrix)

    @classmethod
    def rank(cls, matrix: TMatrix) -> int:
        return cls._get_engine().rank(matrix)

    @classmethod
    def det(cls, matrix: TMatrix) -> int:
        return cls._get_engine().det(matrix)
