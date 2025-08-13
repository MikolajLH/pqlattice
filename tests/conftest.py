import functools
import random

import pytest

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


def repeat_test(n: int):  # type: ignore
    def decorator(func):  # type: ignore
        @pytest.mark.parametrize("_repeat_i", range(n))
        @functools.wraps(func)  # type: ignore
        def wrapper(*args, **kwargs):  # type: ignore
            return func(*args, **kwargs)  # type: ignore

        return wrapper  # type: ignore

    return decorator  # type: ignore


@pytest.fixture
def gen_int8():
    def _make():
        return random.randint(-(2**7), 2**7 - 1)

    return _make


@pytest.fixture
def gen_int16():
    def _make():
        return random.randint(-(2**15), 2**15 - 1)

    return _make


@pytest.fixture
def gen_int32():
    def _make():
        return random.randint(-(2**31), 2**31 - 1)

    return _make


@pytest.fixture
def gen_int64():
    def _make():
        return random.randint(-(2**63), 2**63 - 1)

    return _make
