from ..typing import Matrix, validate_aliases


@validate_aliases
def row_swap(m: Matrix, i: int, k: int) -> None:
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
    """
    TODO: write docstring

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
