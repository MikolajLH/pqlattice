import random

import pytest


@pytest.fixture
def gen_int64():
    def _make():
        return random.randint(-(2**63), 2**63 - 1)

    return _make
