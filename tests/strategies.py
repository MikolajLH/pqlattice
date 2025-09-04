from collections.abc import Callable

import hypothesis.strategies as st
from tests import oracle


@st.composite
def primes(draw: Callable[[st.SearchStrategy[int]], int], min_value: int = 2, max_bits: int = 128):
    i = draw(st.integers(min_value=min_value - 1, max_value=2**max_bits))
    return oracle.next_prime(i)
