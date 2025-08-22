import math
from collections.abc import Callable

import pytest

from pqlattice.integer import eea

from .conftest import repeat_test


class Testeea:
    @repeat_test(50)
    def test_random(self, _repeat_i: int, gen_int64: Callable[[], int]):
        a = gen_int64()
        b = gen_int64()
        gcd, s, t = eea(a, b)
        assert gcd == math.gcd(a, b) and a * s + b * t == gcd

    # TODO: replace hardcoded values that have no meaning (8 and 20) with fixtures that return random value
    @pytest.mark.parametrize(
        "inp, exp",
        [
            ((0, 8), (8, 0, 1)),
            ((8, 0), (8, 1, 0)),
            ((1, 1), (1, 0, 1)),
            ((1, 20), (1, 1, 0)),
            ((20, 1), (1, 0, 1)),
            ((-1, 1), (1, 0, 1)),
            ((7, 7), (7, 0, 1)),
            ((13, 13), (13, 0, 1)),
            ((64, 64), (64, 0, 1)),
        ],
    )
    def test_cases(self, inp: tuple[int, int], exp: tuple[int, int, int]):
        assert eea(*inp) == exp

    def test_invalid(self):
        with pytest.raises(ValueError):
            eea(0, 0)
