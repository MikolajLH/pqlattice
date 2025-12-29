import math

from ..typing import Matrix, Vector, validate_aliases


@validate_aliases
def row_swap(m: Matrix, i: int, k: int) -> None:
    m[[i, k]] = m[[k, i]]


@validate_aliases
def row_scale(m: Matrix, i: int, s: float | int) -> None:
    m[i] *= s


@validate_aliases
def row_add(m: Matrix, i: int, k: int, s: float | int) -> None:
    m[i] += s * m[k]


@validate_aliases
def col_swap(m: Matrix, i: int, k: int) -> None:
    m[:, [i, k]] = m[:, [k, i]]


@validate_aliases
def col_scale(m: Matrix, i: int, s: float | int) -> None:
    m[:, i] *= s


@validate_aliases
def col_add(m: Matrix, i: int, k: int, s: float | int) -> None:
    m[:, i] += s * m[:, k]


def norm2(v: Vector) -> int:
    return int(v @ v.T)


def norm(v: Vector) -> float:
    return math.sqrt(norm2(v))


def per_row_norm2(A: Matrix) -> list[int]:
    return [norm2(row) for row in A]


def per_row_norm(A: Matrix) -> list[float]:
    return [math.sqrt(n2) for n2 in per_row_norm2(A)]
