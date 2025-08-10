import math
import random

import pytest

from pqlattice.integer.integer import eea


def make_randint_gen(a: int, b: int, n: int):
    for _ in range(n):
        yield random.randint(a, b)


class Testeea:
    # TODO: this mark.parametrize is kind of ugly, consider changing it
    @pytest.mark.parametrize(
        "a, b",
        zip(make_randint_gen(-(2**63), 2**63 - 1, 100), make_randint_gen(-(2**63), 2**63 - 1, 100), strict=False),
    )
    def test_random(self, a: int, b: int):
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
