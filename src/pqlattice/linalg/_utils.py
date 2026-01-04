import math

from ..typing import Matrix, Vector, validate_aliases


@validate_aliases
def row_swap(m: Matrix, i: int, k: int) -> None:
    """_summary_

    Parameters
    ----------
    m : Matrix
        _description_
    i : int
        _description_
    k : int
        _description_
    """
    m[[i, k]] = m[[k, i]]


@validate_aliases
def row_scale(m: Matrix, i: int, s: float | int) -> None:
    """_summary_

    Parameters
    ----------
    m : Matrix
        _description_
    i : int
        _description_
    s : float | int
        _description_
    """
    m[i] *= s


@validate_aliases
def row_add(m: Matrix, i: int, k: int, s: float | int) -> None:
    """_summary_

    Parameters
    ----------
    m : Matrix
        _description_
    i : int
        _description_
    k : int
        _description_
    s : float | int
        _description_
    """
    m[i] += s * m[k]


@validate_aliases
def col_swap(m: Matrix, i: int, k: int) -> None:
    """_summary_

    Parameters
    ----------
    m : Matrix
        _description_
    i : int
        _description_
    k : int
        _description_
    """
    m[:, [i, k]] = m[:, [k, i]]


@validate_aliases
def col_scale(m: Matrix, i: int, s: float | int) -> None:
    """_summary_

    Parameters
    ----------
    m : Matrix
        _description_
    i : int
        _description_
    s : float | int
        _description_
    """
    m[:, i] *= s


@validate_aliases
def col_add(m: Matrix, i: int, k: int, s: float | int) -> None:
    """_summary_

    Parameters
    ----------
    m : Matrix
        _description_
    i : int
        _description_
    k : int
        _description_
    s : float | int
        _description_
    """
    m[:, i] += s * m[:, k]


def norm2(v: Vector) -> int:
    """_summary_

    Parameters
    ----------
    v : Vector
        _description_

    Returns
    -------
    int
        _description_
    """
    return int(v @ v.T)


def norm(v: Vector) -> float:
    """_summary_

    Parameters
    ----------
    v : Vector
        _description_

    Returns
    -------
    float
        _description_
    """
    return math.sqrt(norm2(v))


def per_row_norm2(A: Matrix) -> list[int]:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    list[int]
        _description_
    """
    return [norm2(row) for row in A]


def per_row_norm(A: Matrix) -> list[float]:
    """_summary_

    Parameters
    ----------
    A : Matrix
        _description_

    Returns
    -------
    list[float]
        _description_
    """
    return [math.sqrt(n2) for n2 in per_row_norm2(A)]
