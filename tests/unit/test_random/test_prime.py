from hypothesis import given
from hypothesis import strategies as st
from tests import oracle

from pqlattice.random._prime import randprime


class TestRandPrime:
    @given(kbits=st.integers(2, 1024), seed=st.integers())
    def test_randprime_with_oracle(self, kbits: int, seed: int):
        p = randprime(kbits, seed)
        assert oracle.is_prime(p)
        assert p.bit_length() == kbits, f"{p}"
