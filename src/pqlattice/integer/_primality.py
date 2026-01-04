import logging
import random
from collections.abc import Callable

from . import _modring as mr  # type: ignore
from . import _primes as primes

logger = logging.getLogger(__name__)


def fermat_primality_test(p: int, s: int, int_gen: Callable[[int, int], int] | None = None) -> bool:
    if p <= 1:
        return False

    if int_gen is None:
        int_gen = lambda a, b: random.randint(a, b - 1)

    for _ in range(s):
        a = int_gen(2, p - 2)
        if mr.modpow(a, p - 1, p) == 1:
            return False
    return True


def miller_rabin_primality_test(n: int, s: int, int_gen: Callable[[int, int], int] | None = None) -> bool:
    if int_gen is None:
        int_gen = lambda a, b: random.randint(a, b)

    # n - 1 = r * 2 ** u
    u = 0
    r = n - 1
    while r % 2 == 0:
        u += 1
        r //= 2

    # assert n - 1 == r * 2 ** u, f"{n - 1=}, {r=}, {u=}, {2**u=}, {r * 2 ** u=}"

    for _ in range(s):
        a = int_gen(2, n - 2)
        z = mr.modpow(a, r, n)
        for _ in range(u):
            y = mr.mod(z * z, n)
            if y == 1 and z != 1 and z != n - 1:
                # composite
                return False
            z = y
        if z != 1:
            # composite
            return False

    # likely prime
    return True


def is_prime(p: int) -> bool:
    """_summary_

    Parameters
    ----------
    p : int
        _description_

    Returns
    -------
    bool
        _description_
    """
    if p <= 1:
        return False

    for prime in primes.SMALL_PRIMES:
        if p == prime:
            return True

        if p % prime == 0:
            return False

    return miller_rabin_primality_test(p, 20)
