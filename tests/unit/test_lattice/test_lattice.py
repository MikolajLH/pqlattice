from typing import NamedTuple

import numpy as np
import pytest
from hypothesis import given
from tests import oracle
from tests.strategies import full_rank_matrices, sage_lattices

from pqlattice.lattice._lattice import discriminant, gaussian_heuristic, glr_2dim, hadamard_ratio, rank, volume
from pqlattice.typing import SquareMatrix


class TestGlr2Dim:
    class Case(NamedTuple):
        # input:
        v1: tuple[int, int]
        v2: tuple[int, int]

        # output:
        w1: tuple[int, int]
        w2: tuple[int, int]

    KNOWN_CASES = [
        # Hoffstein - An Introduction to Mathematical Cryptography 2014; page 438.
        Case(v1=(66586820, 65354729), v2=(6513996, 6393464), w1=(2280, -1001), w2=(-1324, -2376))
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_glr_2dim_known_cases(self, case: Case):
        lattice_basis = np.array([case.v1, case.v2], dtype=object)
        expected = np.array([case.w1, case.w2], dtype=object)

        result = glr_2dim(lattice_basis)

        np.testing.assert_equal(result, expected)


class TestLatticeProperties:
    @given(lattice_basis=full_rank_matrices(square=True))
    def test_rank_with_oracle(self, lattice_basis: SquareMatrix):
        result = rank(lattice_basis)
        sage_result = oracle.Sage.rank(lattice_basis)

        assert result == sage_result

    @given(lattice_basis=full_rank_matrices(square=True))
    def test_volume_with_oracle(self, lattice_basis: SquareMatrix):
        result = volume(lattice_basis)
        sage_result = oracle.Sage.volume(lattice_basis)

        assert result == sage_result

    @given(lattice_basis=full_rank_matrices(square=True))
    def test_discriminant_with_oracle(self, lattice_basis: SquareMatrix):
        result = discriminant(lattice_basis)
        sage_result = oracle.Sage.discriminant(lattice_basis)

        assert result == sage_result

    @given(lattice_basis=full_rank_matrices(square=True))
    def test_gaussian_heuristic_with_oracle(self, lattice_basis: SquareMatrix):
        result = gaussian_heuristic(lattice_basis)
        sage_result = oracle.Sage.gaussian_heuristic(lattice_basis)

        assert result == pytest.approx(sage_result)  # type: ignore

    @given(lattice_basis=full_rank_matrices(square=True))
    def test_hadamard_ratio_with_oracle(self, lattice_basis: SquareMatrix):
        result = hadamard_ratio(lattice_basis)
        sage_result = oracle.Sage.hadamard_ratio(lattice_basis)
        assert result == pytest.approx(sage_result)  # type: ignore


class TestLatticePropertiesWithSageLattices:
    @given(lattice_basis=sage_lattices())
    def test_rank_with_oracle(self, lattice_basis: SquareMatrix):
        result = rank(lattice_basis)
        sage_result = oracle.Sage.rank(lattice_basis)

        assert result == sage_result

    @given(lattice_basis=sage_lattices())
    def test_volume_with_oracle(self, lattice_basis: SquareMatrix):
        result = volume(lattice_basis)
        sage_result = oracle.Sage.volume(lattice_basis)

        assert result == sage_result

    @given(lattice_basis=sage_lattices())
    def test_discriminant_with_oracle(self, lattice_basis: SquareMatrix):
        result = discriminant(lattice_basis)
        sage_result = oracle.Sage.discriminant(lattice_basis)

        assert result == sage_result

    @given(lattice_basis=sage_lattices())
    def test_gaussian_heuristic_with_oracle(self, lattice_basis: SquareMatrix):
        result = gaussian_heuristic(lattice_basis)
        sage_result = oracle.Sage.gaussian_heuristic(lattice_basis)

        assert result == pytest.approx(sage_result)  # type: ignore

    @given(lattice_basis=sage_lattices())
    def test_hadamard_ratio_with_oracle(self, lattice_basis: SquareMatrix):
        result = hadamard_ratio(lattice_basis)
        sage_result = oracle.Sage.hadamard_ratio(lattice_basis)
        assert result == pytest.approx(sage_result)  # type: ignore
