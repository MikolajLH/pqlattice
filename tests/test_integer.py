import math
import random

import pytest

from pqlattice.integer.integer import eea


def make_randint_gen(a: int, b: int, n: int):
    for _ in range(n):
        yield random.randint(a, b)


@pytest.mark.parametrize(
    "a, b", zip(make_randint_gen(-(2**63), 2**63 - 1, 100), make_randint_gen(-(2**63), 2**63 - 1, 100), strict=False)
)
def test_eea(a: int, b: int):
    gcd, s, t = eea(a, b)
    assert gcd == math.gcd(a, b) and a * s + b * t == gcd
