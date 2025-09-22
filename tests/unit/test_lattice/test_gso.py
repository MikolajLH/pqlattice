from functools import reduce

import numpy as np
from hypothesis import given
from tests import oracle
from tests.strategies import lattices

from pqlattice._utils import as_integer
from pqlattice.lattice._gso import gso
from pqlattice.typing import SquareMatrix


class TestGso:
    @given(lattice_basis=lattices())
    def test_gso_orthogonality(self, lattice_basis: SquareMatrix):
        B_star, _ = gso(lattice_basis)
        gram = B_star @ B_star.T
        np.fill_diagonal(gram, 0)

        assert np.all(gram == 0)

    @given(lattice_basis=lattices())
    def test_gso_basis_invariance(self, lattice_basis: SquareMatrix):
        B_star, _ = gso(lattice_basis)
        gso_det2 = reduce(lambda a, b: a * b, (np.dot(b, b) for b in B_star), 1)
        sage_det = oracle.Sage.det(lattice_basis)
        sage_det2 = sage_det * sage_det
        assert gso_det2 == sage_det2

    @given(lattice_basis=lattices())
    def test_gso_reconstructability(self, lattice_basis: SquareMatrix):
        B_star, U = gso(lattice_basis)
        B = as_integer(U.T @ B_star)

        np.testing.assert_equal(B, lattice_basis)
