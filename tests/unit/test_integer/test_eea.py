import math

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from pqlattice.integer._integer import eea

KNOWN_CASES = [
    ((0, 8), (8, 0, 1)),
    ((8, 0), (8, 1, 0)),
    ((1, 1), (1, 0, 1)),
    ((1, 20), (1, 1, 0)),
    ((20, 1), (1, 0, 1)),
    ((-1, 1), (1, 0, 1)),
    ((7, 7), (7, 0, 1)),
    ((13, 13), (13, 0, 1)),
    ((64, 64), (64, 0, 1)),
]


@pytest.mark.parametrize("inp, expected", KNOWN_CASES)
def test_eea_known_cases(inp: tuple[int, int], expected: tuple[int, int, int]):
    assert eea(*inp) == expected


@given(st.integers(), st.integers())
def test_eea_properties(a: int, b: int):
    assume(a != 0 or b != 0)
    gcd, s, t = eea(a, b)
    assert gcd == math.gcd(a, b)
    assert a * s + b * t == gcd


def test_eea_invalid_cases():
    with pytest.raises(ValueError):
        eea(0, 0)
