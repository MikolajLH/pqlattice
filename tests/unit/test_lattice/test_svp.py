from hypothesis import given, settings
from tests import oracle
from tests.hypothesis_config import get_profile
from tests.strategies import lattices, sage_lattices

from pqlattice.lattice._svp import shortest_vector
from pqlattice.linalg._utils import norm2
from pqlattice.typing import SquareMatrix


class TestShortestVector:
    @settings(max_examples=get_profile().slow_max_examples)
    @given(lattice_basis=sage_lattices())
    def test_shortest_vector_with_sage_oracle_and_sage_lattices(self, lattice_basis: SquareMatrix):
        sv = shortest_vector(lattice_basis)
        sage_sv = oracle.Sage.shortest_vector(lattice_basis)

        sv_norm2 = norm2(sv)
        sage_sv_norm2 = norm2(sage_sv)

        assert sv_norm2 == sage_sv_norm2, f"{lattice_basis}"

    @settings(max_examples=get_profile().slow_max_examples)
    @given(lattice_basis=lattices())
    def test_shortest_vector_with_sage_oracle(self, lattice_basis: SquareMatrix):
        sv = shortest_vector(lattice_basis)
        sage_sv = oracle.Sage.shortest_vector(lattice_basis)

        sv_norm2 = norm2(sv)
        sage_sv_norm2 = norm2(sage_sv)

        assert sv_norm2 == sage_sv_norm2, f"{lattice_basis}"
