import math

from ..typing import Matrix, Vector, validate_aliases


@validate_aliases
def row_swap(m: Matrix, i: int, k: int) -> None:
    """
    utility function for `in place` row swap operation

    Parameters
    ----------
    m : Matrix
    i : int
    k : int
    """
    m[[i, k]] = m[[k, i]]


@validate_aliases
def row_scale(m: Matrix, i: int, s: int) -> None:
    """
    utility function for `in place` row scale operation

    Parameters
    ----------
    m : Matrix
    i : int
    s : int
        scaling factor
    """
    m[i] *= s


@validate_aliases
def row_add(m: Matrix, i: int, k: int, s: int) -> None:
    """
    utility function for `in place` row add operation

    Parameters
    ----------
    m : Matrix
    i : int
        target row
    k : int
        source row
    s : int
        scaling factor
    """
    m[i] += s * m[k]


@validate_aliases
def col_swap(m: Matrix, i: int, k: int) -> None:
    """
    utility function for `in place` column swap operation

    Parameters
    ----------
    m : Matrix
    i : int
    k : int
    """
    m[:, [i, k]] = m[:, [k, i]]


@validate_aliases
def col_scale(m: Matrix, i: int, s: int) -> None:
    """
    utility function for `in place` column scale operation

    Parameters
    ----------
    m : Matrix
    i : int
    s : int
        scaling factor
    """
    m[:, i] *= s


@validate_aliases
def col_add(m: Matrix, i: int, k: int, s: int) -> None:
    """
    utility function for `in place` column add operation

    Parameters
    ----------
    m : Matrix
    i : int
        target column
    k : int
        source column
    s : int
        scaling factor
    """
    m[:, i] += s * m[:, k]


def norm2(v: Vector) -> int:
    """
    computes the squared norm of a given vector, that is the dot product of vector with itself

    Parameters
    ----------
    v : Vector

    Returns
    -------
    int
    """
    return int(v @ v.T)


def norm(v: Vector) -> float:
    """
    computes the square root of the dot product of the vector with itself.

    Parameters
    ----------
    v : Vector

    Returns
    -------
    float
    """
    return math.sqrt(norm2(v))


def per_row_norm2(A: Matrix) -> list[int]:
    """
    Computes the list of squared norms of rows of a given matrix.

    Parameters
    ----------
    A : Matrix

    Returns
    -------
    list[int]
    """
    return [norm2(row) for row in A]


def per_row_norm(A: Matrix) -> list[float]:
    """
    Computes the list of norms of rows of a given matrix.

    Parameters
    ----------
    A : Matrix

    Returns
    -------
    list[float]
    """
    return [math.sqrt(n2) for n2 in per_row_norm2(A)]
