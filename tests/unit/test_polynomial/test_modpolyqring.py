from hypothesis import given
from hypothesis import strategies as st
from tests.strategies import polynomials, primes

from pqlattice.polynomial._modpolyqring import construct_ring
from pqlattice.typing import Vector


class TestModIntPolyQuotientRing:
    @given(r=st.sampled_from(["+", "-"]), N=primes(2, 20), q=primes(2, 20), a=polynomials(), b=polynomials())
    def test_properties(self, r: str, N: int, q: int, a: Vector, b: Vector):
        R = construct_ring(r, N, q)
        assert all(R.sub(a, a) == 0)
        assert all(R.sub(b, b) == 0)
