import numpy as np
import pytest

from pqlattice.typing import Matrix, SquareMatrix, Vector, validate_aliases


@validate_aliases
def check_vector(a: Vector):
    pass


@validate_aliases
def check_matrix(a: Matrix):
    pass


@validate_aliases
def check_square_matrix(a: SquareMatrix):
    pass


class TestValidateAliasesWithWrongShapes:
    def test_vector(self):
        with pytest.raises(TypeError):
            check_vector(np.ndarray((2, 4), dtype=int))
            check_vector(np.ndarray((9, 1), dtype=int))
            check_vector(np.ndarray((1, 4), dtype=float))

    def test_matrix(self):
        with pytest.raises(TypeError):
            check_matrix(np.ndarray((4,), dtype=float))
            check_matrix(np.ndarray(7, dtype=int))
            check_matrix(np.ndarray(13, dtype=float))

    def test_square_matrix(self):
        with pytest.raises(TypeError):
            check_square_matrix(np.ndarray((7, 3), dtype=int))
            check_square_matrix(np.ndarray((1, 5), dtype=int))
            check_square_matrix(np.ndarray(8, dtype=float))
