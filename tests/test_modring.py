import pytest

import pqlattice.integer.modring as mr


@pytest.mark.parametrize(
    "inp, exp",
    [
        ((1, 2), 1),
        ((3, 2), 1),
        ((11, 2), 1),
        ((1, 3), 1),
        ((4, 3), 1),
        ((2, 3), 2),
        ((1, 5), 1),
        ((6, 5), 1),
        ((2, 5), 3),
        ((3, 5), 2),
        ((4, 5), 4),
    ],
)
def test_modinv(inp: tuple[int, int], exp: int):
    assert mr.modinv(*inp) == exp


@pytest.mark.parametrize(
    "inp, exp",
    [
        ((1, 0, 2), 1),
        ((1, 1, 2), 1),
        ((1, 2, 2), 1),
        ((1, 3, 2), 1),
        ((2, 0, 5), 1),
        ((2, 1, 5), 2),
        ((2, 2, 5), 4),
        ((2, 3, 5), 3),
        ((2, 4, 5), 1),
        ((2, 5, 5), 2),
    ],
)
def test_modpow(inp: tuple[int, int, int], exp: int):
    assert mr.modpow(*inp) == exp
