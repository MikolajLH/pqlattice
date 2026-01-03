from typing import NamedTuple

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from tests import oracle

from pqlattice.integer._integer import eea


class TestEea:
    class Case(NamedTuple):
        # input:
        a: int
        b: int
        # output:
        gcd: int
        s: int
        t: int

    KNOWN_CASES = [
        Case(0, 8, gcd=8, s=0, t=1),
        Case(8, 0, gcd=8, s=1, t=0),
        Case(1, 1, gcd=1, s=0, t=1),
        Case(1, 20, gcd=1, s=1, t=0),
        Case(20, 1, gcd=1, s=0, t=1),
        Case(-1, 1, gcd=1, s=0, t=1),
        Case(7, 7, gcd=7, s=0, t=1),
        Case(13, 13, gcd=13, s=0, t=1),
        Case(64, 64, gcd=64, s=0, t=1),
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_eea_known_cases(self, case: Case):
        assert eea(case.a, case.b) == (case.gcd, case.s, case.t)

    @given(a=st.integers(), b=st.integers())
    def test_eea_properties(self, a: int, b: int):
        assume(a != 0 or b != 0)
        gcd, s, t = eea(a, b)
        assert gcd == oracle.gcd(a, b)
        assert a * s + b * t == gcd

    INVALID_CASES = [(0, 0)]

    @pytest.mark.parametrize("a, b", INVALID_CASES)
    def test_eea_invalid_cases(self, a: int, b: int):
        with pytest.raises(ValueError):
            eea(a, b)
