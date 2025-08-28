import numpy as np
import pytest

from pqlattice.typing import Matrix, MatrixFloat, MatrixInt, SquareMatrix, SquareMatrixFloat, SquareMatrixInt, Vector, VectorFloat, VectorInt, validate_aliases


@validate_aliases
def check_vector(a: Vector):
    pass


@validate_aliases
def check_vector_int(a: VectorInt):
    pass


@validate_aliases
def check_vector_float(a: VectorFloat):
    pass


@validate_aliases
def check_matrix(a: Matrix):
    pass


@validate_aliases
def check_matrix_int(a: MatrixInt):
    pass


@validate_aliases
def check_matrix_float(a: MatrixFloat):
    pass


@validate_aliases
def check_square_matrix(a: SquareMatrix):
    pass


@validate_aliases
def check_square_matrix_int(a: SquareMatrixInt):
    pass


@validate_aliases
def check_square_matrix_float(a: SquareMatrixFloat):
    pass


class TestValidateAliasesWithWrongTypes:
    def test_vector(self):
        with pytest.raises(TypeError):
            check_vector(np.ndarray((12,), dtype=str))

    def test_vector_int(self):
        with pytest.raises(TypeError):
            check_vector_int(np.ndarray((17,), dtype=float))

    def test_vector_float(self):
        with pytest.raises(TypeError):
            check_vector_float(3.14)  # type: ignore

    def test_matrix(self):
        with pytest.raises(TypeError):
            check_matrix(np.ndarray((72, 2), dtype=bool))

    def test_matrix_int(self):
        with pytest.raises(TypeError):
            check_matrix_int(True)  # type: ignore

    def test_matrix_float(self):
        with pytest.raises(TypeError):
            check_matrix_float(np.ndarray((1, 12), dtype=np.int64))

    def test_square_matrix(self):
        with pytest.raises(TypeError):
            check_square_matrix(np.ndarray((12, 12), dtype=None))

    def test_square_matrix_int(self):
        with pytest.raises(TypeError):
            check_square_matrix_int(2.78)  # type: ignore

    def test_square_matrix_float(self):
        with pytest.raises(TypeError):
            check_square_matrix_float(np.ndarray((4, 4), dtype=int))


class TestValidateAliasesWithWrongShapes:
    def test_vector(self):
        with pytest.raises(TypeError):
            check_vector(np.ndarray((2, 4), dtype=int))

    def test_vector_int(self):
        with pytest.raises(TypeError):
            check_vector_int(np.ndarray((9, 1), dtype=int))

    def test_vector_float(self):
        with pytest.raises(TypeError):
            check_vector_float(np.ndarray((1, 4), dtype=float))

    def test_matrix(self):
        with pytest.raises(TypeError):
            check_matrix(np.ndarray((4,), dtype=float))

    def test_matrix_int(self):
        with pytest.raises(TypeError):
            check_matrix_int(np.ndarray(7, dtype=int))

    def test_matrix_float(self):
        with pytest.raises(TypeError):
            check_matrix_float(np.ndarray(13, dtype=float))

    def test_square_matrix(self):
        with pytest.raises(TypeError):
            check_square_matrix(np.ndarray((7, 3), dtype=int))

    def test_square_matrix_int(self):
        with pytest.raises(TypeError):
            check_square_matrix_int(np.ndarray((1, 5), dtype=int))

    def test_square_matrix_float(self):
        with pytest.raises(TypeError):
            check_square_matrix_float(np.ndarray(8, dtype=float))
