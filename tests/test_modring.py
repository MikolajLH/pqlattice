from collections.abc import Callable

import pytest

import pqlattice.integer.modring as mr

from .conftest import PRIMES


@pytest.mark.parametrize("modulus", [*PRIMES])
def test_modinv(modulus: int, gen_int64: Callable[[], int]):
    a = gen_int64()
    if a % modulus == 0:
        with pytest.raises(ValueError):
            mr.modinv(a, modulus)
    else:
        inv = mr.modinv(a, modulus)
        mul = (inv * a) % modulus
        assert mul == 1, f"a = {a}; m = {modulus}; inv = {inv}"
