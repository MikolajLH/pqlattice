import random

from hypothesis import given
from hypothesis import strategies as st
from tests import oracle

from pqlattice.random._lattice import _gen_unimodular, randlattice  # type: ignore


class TestRandLattice:
    @given(n=st.integers(4, 100), seed=st.integers())
    def test_randlattice_unimodular_with_oracle(self, n: int, seed: int):
        U = _gen_unimodular(n, 20, random.Random(seed))

        assert oracle.Sage.is_unimodular(U), f"{U=}"

    @given(n=st.integers(4, 100), seed=st.integers())
    def test_randlattice_with_oracle(self, n: int, seed: int):
        B = randlattice(n, seed=seed)

        assert oracle.Sage.rank(B) == n, f"{B=}"
