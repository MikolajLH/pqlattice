from .. import settings
from ..typing import Matrix, SquareMatrix
from ._linalg import cofactor, cofactor_matrix, det, left_kernel, left_nullity, minor, rank, right_kernel, right_nullity
from ._modint import mod_left_kernel, mod_left_nullity, mod_matinv, mod_ref, mod_right_kernel, mod_right_nullity, mod_rref
from ._utils import norm, norm2, per_row_norm, per_row_norm2, row_add, row_scale, row_swap


def hnf(matrix: SquareMatrix) -> tuple[Matrix, SquareMatrix]:
    return settings.get_backend().hnf(matrix)


__all__ = [
    "hnf",
    "det",
    "left_kernel",
    "right_kernel",
    "left_nullity",
    "right_nullity",
    "rank",
    "minor",
    "cofactor",
    "cofactor_matrix",
    "norm",
    "norm2",
    "per_row_norm",
    "per_row_norm2",
    "row_add",
    "row_scale",
    "row_swap",
    "mod_ref",
    "mod_rref",
    "mod_right_kernel",
    "mod_left_kernel",
    "mod_left_nullity",
    "mod_right_nullity",
    "mod_matinv",
]
