from hypothesis import given
from hypothesis import strategies as st
from tests import oracle
from tests.strategies import primes

from pqlattice.integer._primality import is_prime


class TestFermatPrimalityTest:
    # TODO: implement
    pass


class TestMillerRabinPrimalityTest:
    # TODO: implement
    pass


class TestIsPrime:
    @given(q=primes())
    def test_is_prime_for_known_primes(self, q: int):
        assert is_prime(q)

    @given(q=st.integers())
    def test_is_prime_with_oracle(self, q: int):
        assert is_prime(q) == oracle.is_prime(q)
