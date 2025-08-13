import random

import pytest

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


@pytest.fixture
def gen_int64():
    def _make():
        return random.randint(-(2**63), 2**63 - 1)

    return _make
