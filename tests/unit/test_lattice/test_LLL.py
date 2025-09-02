import pytest

from pqlattice.lattice import LLL, is_LLL_reduced
from pqlattice.typing import SquareMatrix

from ...conftest import load_lattice_basis

CASE_DIM_5 = load_lattice_basis(["5x5.json"])  # type: ignore


@pytest.mark.parametrize("basis", CASE_DIM_5)  # type: ignore
def test_LLL_10(basis: SquareMatrix):
    delta = 0.75
    B = LLL(basis, delta)
    assert is_LLL_reduced(B, delta)
