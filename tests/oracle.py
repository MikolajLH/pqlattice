# pyright: reportAttributeAccessIssue=false
import math

import gmpy2
import pytest
from tests.sage_interface import SageEngineInterface


def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)


def is_prime(n: int) -> bool:
    return bool(gmpy2.is_prime(n))  # type: ignore


def next_prime(n: int) -> int:
    return int(gmpy2.next_prime(n))  # type: ignore


class Sage:
    _engine: SageEngineInterface | None = None

    @classmethod
    def _get_engine(cls) -> SageEngineInterface:
        if cls._engine is None:
            pytest.skip("Skipping: Test requires SageMath (--sage flag no set)")
            # raise RuntimeError("Sage is not connected")
        return cls._engine

    # -- Public API

    @classmethod
    def ok(cls) -> bool:
        return cls._get_engine().ok()

    @classmethod
    def hello_world(cls) -> str:
        return cls._get_engine().hello_world()
