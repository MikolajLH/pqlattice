from typing import NamedTuple

import pytest
from hypothesis import given
from hypothesis import strategies as st
from tests import oracle
from tests.strategies import primes

from pqlattice.integer._primality import fermat_primality_test, is_prime, miller_rabin_primality_test


class TestFermatPrimalityTest:
    class Case(NamedTuple):
        # input:
        p: int
        # output:
        is_p: bool

    KNOWN_CASES = [
        Case(p=-1, is_p=False),
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_fermat_primality_test(self, case: Case):
        res = fermat_primality_test(case.p, 10)
        assert res == case.is_p


class TestMillerRabinPrimalityTest:
    class Case(NamedTuple):
        # input:
        p: int
        # output:
        is_p: bool

    KNOWN_CASES = [
        Case(p=221, is_p=False),
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_miller_rabin_primality_test(self, case: Case):
        res = miller_rabin_primality_test(case.p, 10)
        assert res == case.is_p


class TestIsPrime:
    @given(q=primes())
    def test_is_prime_for_known_primes(self, q: int):
        assert is_prime(q)

    @given(q=st.integers())
    def test_is_prime_with_oracle(self, q: int):
        assert is_prime(q) == oracle.is_prime(q)
