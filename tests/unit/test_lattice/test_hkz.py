from hypothesis import given, settings
from tests import oracle
from tests.strategies import lattices, sage_lattices

from pqlattice.lattice._hkz import hkz
from pqlattice.linalg._utils import norm2
from pqlattice.typing import SquareMatrix


class TestHKZ:
    @settings(max_examples=5)
    @given(lattice_basis=lattices())
    def test_hkz_with_sage_oracle(self, lattice_basis: SquareMatrix):
        H = hkz(lattice_basis)
        sv = oracle.Sage.shortest_vector(lattice_basis)
        assert norm2(H[0]) == norm2(sv)

    @settings(max_examples=10)
    @given(lattice_basis=sage_lattices())
    def test_hkz_with_sage_oracle_and_sage_lattices(self, lattice_basis: SquareMatrix):
        H = hkz(lattice_basis)
        sv = oracle.Sage.shortest_vector(lattice_basis)
        assert norm2(H[0]) == norm2(sv)
