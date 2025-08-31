import random
from collections.abc import Callable

from . import _modring as mr  # type: ignore

# All primes less than 256
SMALL_PRIMES = (
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
    223,
    227,
    229,
    233,
    239,
    241,
    251,
)


def fermat_primality_test(p: int, s: int, int_gen: Callable[[int, int], int] | None = None) -> bool:
    """
    TODO: write docstring

    Parameters
    ----------
    p : int
        _description_
    s : int
        _description_
    int_gen : Callable[[int, int], int] | None, optional
        _description_, by default None

    Returns
    -------
    _type_
        _description_
    """
    if p <= 1:
        return False

    if int_gen is None:
        int_gen = lambda a, b: random.randint(a, b - 1)

    for _ in range(s):
        a = int_gen(2, p - 2)
        if mr.modpow(a, p - 1, p) == 1:
            return False
    return True


def miller_rabin_primality_test(p: int, s: int, int_gen: Callable[[int, int], int] | None = None) -> bool:
    """
    TODO: write docstring

    Parameters
    ----------
    p : int
        _description_
    s : int
        _description_
    int_gen : Callable[[int, int], int] | None, optional
        _description_, by default None

    Returns
    -------
    bool
        _description_
    """
    if p <= 1:
        return False

    if int_gen is None:
        int_gen = lambda a, b: random.randint(a, b - 1)

    u = 0
    r = p - 1
    while r % 2 == 0:
        u += 1
        r //= 2

    for _ in range(s):
        a = int_gen(2, p - 2)
        z = mr.modpow(a, r, p)
        if z != 1 and z != p - 1:
            for _ in range(u - 1):
                z = (z * z) % p
                if z == 1:
                    return False
            if z != p - 1:
                return False
        return True
    return True


def is_prime(p: int) -> bool:
    """
    TODO: write docstring

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

    if p in SMALL_PRIMES:
        return True

    for prime in SMALL_PRIMES:
        if p % prime == 0:
            return False

    return miller_rabin_primality_test(p, 20, lambda a, b: random.randint(a, b - 1))
