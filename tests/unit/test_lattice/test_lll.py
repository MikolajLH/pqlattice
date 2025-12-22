# from typing import cast
from hypothesis import given, settings
from tests import oracle
from tests.strategies import lattices, sage_lattices

from pqlattice.lattice._lll import lll  # , is_lll_reduced
from pqlattice.typing import SquareMatrix

# class TestIsLLLreduced:
#     @given(lattice_basis=lattices())
#     def test_is_lll_reduced_with_sage_oracle(self, lattice_basis: SquareMatrix):
#         delta = 0.99

#         is_reduced_before = is_lll_reduced(lattice_basis, delta)
#         is_reduced_before_expected = oracle.Sage.is_lll_reduced(lattice_basis, delta)

#         assert is_reduced_before == is_reduced_before_expected

#         L = cast(SquareMatrix, oracle.Sage.lll(lattice_basis))

#         assert is_lll_reduced(L, delta)


#     @settings(max_examples=10)
#     @given(lattice_basis=sage_lattices())
#     def test_is_lll_reduced_with_sage_oracle_and_sage_lattices(self, lattice_basis: SquareMatrix):
#         delta = 0.99

#         is_reduced_before = is_lll_reduced(lattice_basis, delta)
#         is_reduced_before_expected = oracle.Sage.is_lll_reduced(lattice_basis, delta)

#         assert is_reduced_before == is_reduced_before_expected

#         L = cast(SquareMatrix, oracle.Sage.lll(lattice_basis))

#         assert is_lll_reduced(L, delta)


class TestLLL:
    @given(lattice_basis=lattices())
    def test_lll_with_sage_oracle(self, lattice_basis: SquareMatrix):
        delta = 0.99
        L = lll(lattice_basis, delta)
        assert oracle.Sage.is_lll_reduced(L, delta)

    @settings(max_examples=10)
    @given(lattice_basis=sage_lattices())
    def test_lll_with_sage_oracle_and_sage_lattices(self, lattice_basis: SquareMatrix):
        delta = 0.99
        L = lll(lattice_basis, delta)
        assert oracle.Sage.is_lll_reduced(L, delta)
