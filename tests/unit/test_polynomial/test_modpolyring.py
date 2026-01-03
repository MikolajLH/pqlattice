from hypothesis import given
from tests.strategies import polynomials, primes

from pqlattice.polynomial._modpolyring import ModIntPolyRing
from pqlattice.typing import Vector


class TestModIntPolyRing:
    @given(a=polynomials(), b=polynomials(), q=primes(2, 20))
    def test_properties(self, a: Vector, b: Vector, q: int):
        R = ModIntPolyRing(q)
        assert all(R.sub(a, a) == 0)
        assert all(R.sub(b, b) == 0)
