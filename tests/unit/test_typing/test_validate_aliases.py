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


def test_validate_aliases_with_wrong_types():
    with pytest.raises(TypeError):
        check_vector(np.ndarray((12,), dtype=bool))
        check_vector_int(np.ndarray((17,), dtype=float))
        check_vector_float(3.14)  # type: ignore

        check_matrix(None)  # type: ignore
        check_matrix_int(True)  # type: ignore
        check_matrix_float(np.ndarray((1, 12), dtype=np.int64))  # type: ignore

        check_square_matrix(False)  # type: ignore
        check_square_matrix_int(2.78)  # type: ignore
        check_square_matrix_float(np.ndarray((4, 4), dtype=int))  # type: ignore


# def test_validate_aliases_with_wrong_shapes():
#     with pytest.raises(TypeError):
#         check_vector(np.ndarray())
#         check_vector_int(42)
#         check_vector_float(3.14)

#         check_matrix(None)
#         check_matrix_int(True)
#         check_matrix_float(b"xxx")

#         check_square_matrix(False)
#         check_square_matrix_int(2.78)
#         check_square_matrix_float(7)
#         pass
