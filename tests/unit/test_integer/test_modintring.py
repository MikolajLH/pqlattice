from math import floor, gcd

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from pqlattice.integer._modintring import ModIntRing


@given(modulus=st.integers().filter(lambda x: abs(x) > 1))
def test_constructor(modulus: int):
    ModIntRing(modulus)


@pytest.mark.parametrize("modulus", [-1, 0, 1])
def test_constructor_failing(modulus: int):
    with pytest.raises(ValueError):
        ModIntRing(modulus)


@given(modulus=st.integers().filter(lambda x: 1 < abs(x) < 2**30), a=st.integers())
def test_cmodr(modulus: int, a: int):
    R = ModIntRing(modulus)
    ra = R.cmodr(a)
    m = abs(modulus)

    left_end = -m // 2 if m % 2 == 0 else -floor(m / 2)

    assert -m / 2 <= float(ra) <= m / 2
    if m % 2 == 0:
        assert ra != left_end


@given(modulus=st.integers().filter(lambda x: abs(x) > 1), a=st.integers())
def test_cmodl(modulus: int, a: int):
    R = ModIntRing(modulus)
    ra = R.cmodl(a)
    m = abs(modulus)

    right_end = m // 2 if m % 2 == 0 else floor(m / 2)

    assert -m / 2 <= float(ra) <= m / 2
    if m % 2 == 0:
        assert ra != right_end


@given(modulus=st.integers().filter(lambda x: abs(x) > 1), a=st.integers(), b=st.integers())
def test_ring_ops(modulus: int, a: int, b: int):
    R = ModIntRing(modulus)
    m = abs(modulus)

    add_res = R.add(a, b)
    assert 0 <= add_res < m
    assert (add_res - (a + b)) % modulus == 0

    sub_res = R.sub(a, b)
    assert 0 <= sub_res < m
    assert (sub_res - (a - b)) % modulus == 0

    mul_res = R.mul(a, b)
    assert 0 <= mul_res < m
    assert (mul_res - a * b) % modulus == 0

    if gcd(m, b) == 1:
        div_res = R.div(a, b)
        assert 0 <= mul_res < m
        assert (a - b * div_res) % modulus == 0
    else:
        with pytest.raises((ValueError, ZeroDivisionError)):
            R.div(a, b)


@given(modulus=st.integers().filter(lambda x: abs(x) > 1), a=st.integers(), r=st.integers(min_value=0, max_value=30))
def test_pow_positive(modulus: int, a: int, r: int):
    R = ModIntRing(modulus)
    pow_res = R.pow(a, r)

    m = abs(modulus)
    assert 0 <= pow_res < m
    assert (pow_res - (a**r)) % modulus == 0


@given(modulus=st.integers().filter(lambda x: abs(x) > 1), a=st.integers(), r=st.integers(min_value=-30, max_value=0))
def test_pow_negative(modulus: int, a: int, r: int):
    m = abs(modulus)
    assume(gcd(m, a) == 1)

    R = ModIntRing(modulus)

    pow_res = R.pow(a, r)
    assert 0 <= pow_res < m
    a_inv = R.inv(a)
    assert (a_inv ** abs(r) - pow_res) % modulus == 0


@given(modulus=st.integers().filter(lambda x: abs(x) > 1), a=st.integers(), r=st.integers(min_value=-30, max_value=-1))
def test_pow_negative_failing(modulus: int, a: int, r: int):
    m = abs(modulus)
    assume(gcd(m, a) != 1)
    R = ModIntRing(modulus)

    with pytest.raises((ValueError, ZeroDivisionError)):
        R.pow(a, r)


@given(modulus=st.integers().filter(lambda x: abs(x) > 1), a=st.integers())
def test_inv(modulus: int, a: int):
    assume(gcd(modulus, a) == 1)
    R = ModIntRing(modulus)
    a_inv = R.inv(a)

    assert 0 <= a_inv < abs(modulus)
    assert (a_inv * a - 1) % modulus == 0
