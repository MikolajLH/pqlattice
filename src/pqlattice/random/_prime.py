import math
import random

from ..integer._primality import is_prime


def _randprime(a: int, b: int, seed: int | None = None) -> int:
    def log(n: int, base: float = math.e) -> float:
        return (n.bit_length() - 1) / math.log2(base)

    approx_number_of_primes_to_a = 0 if a == 0 else int(a / log(a))
    approx_number_of_primes_to_b = 0 if b == 0 else int(b / log(b))
    approx_number_of_primes = approx_number_of_primes_to_b - approx_number_of_primes_to_a
    prime_proba = approx_number_of_primes / (b - a)
    number_of_samples = int(math.log(0.001) / math.log(1 - prime_proba)) + 1

    random.seed(seed)
    for _ in range(number_of_samples):
        prime_candidate = random.randint(a, b)
        if is_prime(prime_candidate):
            return prime_candidate

    raise ValueError(f"Couldn't find a prime number in interval [{a}, {b})")


def randprime(kbits: int, seed: int | None = None) -> int:
    a = 2 ** (kbits - 1)
    b = 2**kbits
    return _randprime(a, b, seed=seed)
