from typing import NamedTuple

import numpy as np
import pytest
from hypothesis import given
from tests import oracle
from tests.strategies import int_matrices

from pqlattice.linalg._linalg import hnf
from pqlattice.typing import MatrixInt


class TestHnf:
    class Case(NamedTuple):
        # input:
        A: list[list[int]]

        # output:
        H: list[list[int]]

    KNOWN_CASES = [
        # https://en.wikipedia.org/wiki/Hermite_normal_form
        Case(
            A=[
                [3, 3, 1, 4],
                [0, 1, 0, 0],
                [0, 0, 19, 16],
                [0, 0, 0, 3],
            ],
            H=[
                [3, 0, 1, 1],
                [0, 1, 0, 0],
                [0, 0, 19, 1],
                [0, 0, 0, 3],
            ],
        ),
        # https://en.wikipedia.org/wiki/Hermite_normal_form
        Case(
            A=[
                [2, 3, 6, 2],
                [5, 6, 1, 6],
                [8, 3, 1, 1],
            ],
            H=[[1, 0, 50, -11], [0, 3, 28, -2], [0, 0, 61, -13]],
        ),
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_hnf_known_cases(self, case: Case):
        A = np.array(case.A, dtype=int)
        expected_H = np.array(case.H, dtype=int)
        H, _ = hnf(A)

        np.testing.assert_equal(H, expected_H)

    @given(m=int_matrices())
    def test_hnf_with_oracle(self, m: MatrixInt):
        H, _ = hnf(m)
        sage_H = oracle.Sage.hnf(m)

        np.testing.assert_array_equal(H, sage_H, f"hnf missmatch for \n{m}\nexpected:\n{sage_H}\ngot\n{H}")
