from ..typing import Matrix


def row_swap(m: Matrix, i: int, k: int) -> None:
    """
    TODO: write docsrting

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


def row_scale(m: Matrix, i: int, s: float | int) -> None:
    """
    TODO: write docsrting

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


def row_add(m: Matrix, i: int, k: int, s: float | int) -> None:
    """
    TODO: write docsrting

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


def col_swap(m: Matrix, i: int, k: int) -> None:
    """
    TODO: write docsrting

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


def col_scale(m: Matrix, i: int, s: float | int) -> None:
    """
    TODO: write docsrting

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


def col_add(m: Matrix, i: int, k: int, s: float | int) -> None:
    """
    TODO: write docsrting

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
