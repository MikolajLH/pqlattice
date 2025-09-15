import math

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from pqlattice.integer._modring import mod, modinv, modpow


class TestMod:
    @given(a=st.integers(), m=st.integers())
    def test_mod_properties(self, a: int, m: int):
        if m == 0:
            with pytest.raises(ZeroDivisionError):
                mod(a, m)
        else:
            r = mod(a, m)
            assert 0 <= r < abs(m)
            assert (a - r) % m == 0


class TestModInv:
    @given(a=st.integers(), modulus=st.integers().filter(lambda n: abs(n) > 1))
    def test_modinv_properties(self, a: int, modulus: int):
        assume(math.gcd(a, modulus) == 1)
        inv = modinv(a, modulus)
        assert mod(inv * a, modulus) == 1

    @given(st.integers(), st.integers())
    @settings(max_examples=10)
    def test_modinv_properties_failing(self, a: int, modulus: int):
        assume(math.gcd(a, modulus) != 1)
        with pytest.raises((ValueError, ZeroDivisionError)):
            modinv(a, modulus)


class TestModPow:
    @given(a=st.integers(), r=st.integers(min_value=-126, max_value=127), modulus=st.integers().filter(lambda n: abs(n) > 1))
    def test_modpow_properties(self, a: int, r: int, modulus: int):
        if r >= 0:
            p = modpow(a, r, modulus)
            t: int = a**r
            q = mod(t, modulus)
            assert p == q
        else:
            if math.gcd(a, modulus) == 1:
                inv = modinv(a, modulus)
                p = modpow(a, r, modulus)
                t: int = inv ** (-r)
                q = mod(t, modulus)
                assert p == q
            else:
                with pytest.raises((ValueError, ZeroDivisionError)):
                    modpow(a, r, modulus)
