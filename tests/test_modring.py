from collections.abc import Callable

import pytest

import pqlattice.integer.modring as mr

from .conftest import PRIMES, repeat_test


@pytest.mark.parametrize("modulus", [*PRIMES])
@repeat_test(50)
def test_modinv(_repeat_i: int, modulus: int, gen_int64: Callable[[], int]):
    a = gen_int64()
    if a % modulus == 0:
        with pytest.raises(ValueError):
            mr.modinv(a, modulus)
    else:
        inv = mr.modinv(a, modulus)
        mul = (inv * a) % modulus
        assert mul == 1, f"a = {a}; m = {modulus}; inv = {inv}"


@repeat_test(50)
def test_modpow_positive(_repeat_i: int, gen_int64: Callable[[], int], gen_int8: Callable[[], int], gen_int16: Callable[[], int]):
    a = gen_int64()
    r = abs(gen_int8()) + 1
    modulus = abs(gen_int16()) + 2
    p = mr.modpow(a, r, modulus)
    q = (a**r) % modulus
    assert p == q, f"a = {a}; r = {r}; m = {modulus}"


@pytest.mark.parametrize("modulus", [*PRIMES])
@repeat_test(50)
def test_modpow_field(_repeat_i: int, modulus: int, gen_int64: Callable[[], int], gen_int8: Callable[[], int]):
    a = gen_int64()
    r = gen_int8()
    if a % modulus == 0:
        pass
        # TODO: fix this tests
        # with pytest.raises(ValueError):
        #     mr.modpow(a, r, modulus)
        #     mr.modpow(a, -r, modulus)
    else:
        p = mr.modpow(a, r, modulus)
        q = mr.modpow(a, -r, modulus)
        mul = (p * q) % modulus
        assert mul == 1, f"p = {p}; q = {q}; m = {modulus}; mul = {mul}"
