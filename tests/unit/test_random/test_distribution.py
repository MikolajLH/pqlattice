from hypothesis import assume, given, settings
from hypothesis import strategies as st

from pqlattice.random._distribution import DiscreteGaussian, Uniform
from pqlattice.typing import is_Matrix, is_SquareMatrix, is_Vector


class TestUniform:
    @given(a=st.integers(), b=st.integers(), seed=st.integers())
    def test_sample_in_range(self, a: int, b: int, seed: int):
        assume(a != b)
        D = Uniform(min(a, b), max(a, b), seed)

        n = D.sample_int()

        assert min(a, b) <= n <= max(a, b)

    @given(n=st.integers(1, 100), m=st.integers(1, 100), a=st.integers(), b=st.integers(), seed=st.integers())
    def test_sample_shape(self, n: int, m: int, a: int, b: int, seed: int):
        D = Uniform(min(a, b), max(a, b), seed)
        k = D.sample_int()
        assert isinstance(k, int)

        v = D.sample_vector(n)
        assert is_Vector(v)

        M = D.sample_matrix(n, m)
        assert is_Matrix(M)

        S = D.sample_matrix(n)
        assert is_SquareMatrix(S)


class TestDiscreteGaussian:
    @settings(max_examples=5)
    @given(seed=st.integers())
    def test_gaussian_distribution(self, seed: int):
        sigma = 3.0
        D = DiscreteGaussian(sigma, seed=seed)

        samples = [D.sample_int() for _ in range(100000)]
        mean = sum(samples) / len(samples)
        var = sum(x**2 for x in samples) / len(samples) - mean**2

        assert abs(mean) < 0.1
        assert abs(var - sigma**2) < 0.5

    @given(n=st.integers(1, 100), m=st.integers(1, 100), seed=st.integers())
    def test_sample_shape(self, n: int, m: int, seed: int):
        sigma = 3.0
        D = DiscreteGaussian(sigma, seed=seed)

        k = D.sample_int()
        assert isinstance(k, int)

        v = D.sample_vector(n)
        assert is_Vector(v)

        M = D.sample_matrix(n, m)
        assert is_Matrix(M)

        S = D.sample_matrix(n)
        assert is_SquareMatrix(S)
