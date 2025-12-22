from ..typing import SquareMatrix, validate_aliases
from ._bkz import bkz
from ._lattice import rank


@validate_aliases
def hkz(lattice_basis: SquareMatrix) -> SquareMatrix:
    return bkz(lattice_basis, rank(lattice_basis))
