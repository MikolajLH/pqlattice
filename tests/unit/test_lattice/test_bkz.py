from typing import NamedTuple

import pytest
from hypothesis import given, settings
from tests import oracle
from tests.strategies import lattices, sage_lattices

from pqlattice._utils import as_integer
from pqlattice.lattice._bkz import bkz
from pqlattice.linalg._utils import norm2
from pqlattice.typing import SquareMatrix


class TestBKZ:
    class Case(NamedTuple):
        # input:
        L: list[list[int]]

    KNOWN_CASES = [
        Case(
            L=[
                [1099511627776, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [88303093011, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [255824600484, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [457522822267, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [516192839528, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [96516603839, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [-28686044121, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [-75358705517, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [504645769259, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [-508797991892, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [278236629654, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [254989519529, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [-422253263494, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            ]
        )
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_bzk_known_cases(self, case: Case):
        B = as_integer(case.L)
        v_norm2 = norm2(bkz(B)[0])

        sage_v_norm2 = norm2(oracle.Sage.bkz(B)[0])

        assert v_norm2 == sage_v_norm2

    @given(lattice_basis=lattices())
    def test_bkz_with_sage_oracle(self, lattice_basis: SquareMatrix):
        B = bkz(lattice_basis)
        v_norm2 = norm2(bkz(B)[0])

        sage_v_norm2 = norm2(oracle.Sage.bkz(lattice_basis)[0])

        assert v_norm2 == sage_v_norm2

    @settings(max_examples=10)
    @given(lattice_basis=sage_lattices())
    def test_bkz_with_sage_oracle_and_sage_lattices(self, lattice_basis: SquareMatrix):
        B = bkz(lattice_basis)
        v_norm2 = norm2(bkz(B)[0])

        sage_v_norm2 = norm2(oracle.Sage.bkz(lattice_basis)[0])

        assert v_norm2 == sage_v_norm2
