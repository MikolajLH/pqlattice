from typing import NamedTuple

import numpy as np
import pytest
from hypothesis import given
from tests import oracle
from tests.strategies import full_rank_matrices, low_rank_matrices, matrices

from pqlattice.linalg._linalg import hnf, left_kernel, left_nullity, rank, right_kernel, right_nullity
from pqlattice.typing import Matrix


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
        A = np.array(case.A, dtype=object)
        expected_H = np.array(case.H, dtype=object)
        H, _ = hnf(A)

        np.testing.assert_equal(H, expected_H)

    @given(m=matrices())
    def test_hnf_with_oracle(self, m: Matrix):
        H, _ = hnf(m)
        sage_H = oracle.Sage.hnf(m)

        np.testing.assert_array_equal(H, sage_H, f"hnf missmatch for \n{m}\nexpected:\n{sage_H}\ngot\n{H}")


class TestKernelAndImage:
    @given(m=matrices())
    def test_left_kernel(self, m: Matrix):
        K = left_kernel(m)
        if len(K) > 0:
            assert np.all(K @ m == 0)

        null = left_nullity(m)

        assert null == oracle.Sage.left_nullity(m)

    @given(m=low_rank_matrices())
    def test_left_kernel_with_low_rank_matrices(self, m: Matrix):
        K = left_kernel(m)
        if len(K) > 0:
            assert np.all(K @ m == 0)

        null = left_nullity(m)

        assert null == oracle.Sage.left_nullity(m)

    @given(m=matrices())
    def test_right_kernel(self, m: Matrix):
        K = right_kernel(m)
        if len(K) > 0:
            assert np.all(K @ m == 0)

        null = right_nullity(m)

        assert null == oracle.Sage.right_nullity(m)

    @given(m=low_rank_matrices())
    def test_right_kernel_with_low_rank_matrices(self, m: Matrix):
        K = right_kernel(m)
        if len(K) > 0:
            assert np.all(K @ m == 0)

        null = right_nullity(m)

        assert null == oracle.Sage.right_nullity(m)


class TestRank:
    @given(m=matrices())
    def test_rank_with_oracle_general(self, m: Matrix):
        sage_rank = oracle.Sage.rank(m)
        r = rank(m)

        assert r == sage_rank

    @given(m=low_rank_matrices())
    def test_rank_with_oracle_low_rank(self, m: Matrix):
        sage_rank = oracle.Sage.rank(m)
        r = rank(m)

        assert r == sage_rank

    @given(m=full_rank_matrices())
    def test_rank_with_oracle_full_rank(self, m: Matrix):
        rows, cols = m.shape
        sage_rank = oracle.Sage.rank(m)
        assert min(rows, cols) == sage_rank
        r = rank(m)
        assert min(rows, cols) == r
        assert r == sage_rank
