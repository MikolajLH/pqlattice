import pytest

from pqlattice.lattice import LLL, is_LLL_reduced

from ..conftest import load_lattice_sizes


@pytest.mark.parametrize("dim, basis", load_lattice_sizes("5-50.json"))
def test_LLL(benchmark, dim, basis):  # type: ignore
    delta = 0.75
    B = benchmark(LLL, basis, delta)  # type: ignore
    assert is_LLL_reduced(B, delta)  # type: ignore
    assert B.shape == (dim, dim)  # type: ignore
