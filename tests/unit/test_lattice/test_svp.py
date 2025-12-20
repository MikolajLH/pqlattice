from hypothesis import given
from tests import oracle
from tests.strategies import lattices, sage_lattices

from pqlattice.lattice._svp import shortest_vector
from pqlattice.linalg._utils import norm2
from pqlattice.typing import SquareMatrix


class TestShortestVector:
    @given(lattice_basis=sage_lattices())
    def test_shortest_vector_with_sage_oracle_and_sage_lattices(self, lattice_basis: SquareMatrix):
        sv = shortest_vector(lattice_basis)
        sage_sv = oracle.Sage.shortest_vector(lattice_basis)

        sv_norm2 = norm2(sv)
        sage_sv_norm2 = norm2(sage_sv)

        assert sv_norm2 == sage_sv_norm2, f"{lattice_basis}"

    @given(lattice_basis=lattices())
    def test_shortest_vector_with_sage_oracle(self, lattice_basis: SquareMatrix):
        sv = shortest_vector(lattice_basis)
        sage_sv = oracle.Sage.shortest_vector(lattice_basis)

        sv_norm2 = norm2(sv)
        sage_sv_norm2 = norm2(sage_sv)

        assert sv_norm2 == sage_sv_norm2, f"{lattice_basis}"
