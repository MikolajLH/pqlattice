from tests import oracle

from pqlattice.integer._primes import SMALL_PRIMES


class TestSmallPrimes:
    def test_small_primes_with_oracle(self):
        primes = [i for i in range(256) if oracle.is_prime(i)]
        assert primes == list(SMALL_PRIMES)
