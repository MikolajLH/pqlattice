import math
import random

from ..integer._primality import is_prime


def _randprime(a: int, b: int, seed: int | None = None) -> int:
    def ilog(n: int, base: float = math.e) -> int:
        return int((n.bit_length() - 1) / math.log2(base))

    try:
        approx_number_of_primes_to_a = 0 if a == 0 else a // ilog(a)
        approx_number_of_primes_to_b = 0 if b == 0 else b // ilog(b)
        approx_number_of_primes = approx_number_of_primes_to_b - approx_number_of_primes_to_a
        prime_proba = approx_number_of_primes / (b - a)
        number_of_samples = int(math.log(0.001) / math.log(1 - prime_proba)) + 1
    except ZeroDivisionError:
        number_of_samples = b - a

    if b - a < 1000:
        number_of_samples = b - a

    random.seed(seed)
    for i in range(number_of_samples):
        prime_candidate = random.randint(a, b)
        if is_prime(prime_candidate):
            return prime_candidate
        if is_prime(a + i):
            return a + i

    raise ValueError(f"Couldn't find a prime number in interval [{a}, {b})")


def randprime(kbits: int, seed: int | None = None) -> int:
    """
    Generates random prime number from range [2 ** (kbits - 1); 2 ** (kbist)].
    Uses Miller-Rabin primality test.

    Parameters
    ----------
    kbits : int
        number of bits the prime number should have
    seed : int | None, optional
        seed for random number generator, by default None

    Returns
    -------
    int
        prime number
    """
    a = 2 ** (kbits - 1)
    b = 2**kbits
    return _randprime(a, b, seed=seed)
