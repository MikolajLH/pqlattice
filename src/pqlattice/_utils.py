from fractions import Fraction
from typing import Any

import numpy as np
from numpy.typing import ArrayLike

from .typing import Array, Matrix, Vector, is_integer, is_Matrix, is_rational, is_Vector, validate_aliases


def as_integer(obj: ArrayLike) -> Array:
    """
    Helper function that converts given obj to numpy's array of python's ints allowing arbitrary large elements

    Parameters
    ----------
    obj : ArrayLike
        object to be converted to numpy's array

    Returns
    -------
    Array
        numpy's array with dtype=object and elements converted to int

    Examples
    --------
    >>> import pqlattice as pq
    >>> pq.as_integer([3**100, 2**100, 5**50])
    array([515377520732011331036461129765621272702107522001,
       1267650600228229401496703205376,
       88817841970012523233890533447265625], dtype=object)
    """
    return (np.vectorize(int)(np.array(obj, dtype=object))).astype(object)


def as_rational(obj: ArrayLike) -> Array:
    """
    Helper function that converts given obj to numpy's array of python's fractions.Fraction allowing arbitrary big rational elements

    Parameters
    ----------
    obj : ArrayLike
        object to be converted to numpy's array

    Returns
    -------
    Array
        numpy's array with dtype=object and elements converted to fractions.Fraction

    Examples
    --------
    >>> import pqlattice as pq
    >>> pq.as_rational([3**100, 2**100, 5**50])
    array([Fraction(515377520732011331036461129765621272702107522001, 1),
       Fraction(1267650600228229401496703205376, 1),
       Fraction(88817841970012523233890533447265625, 1)], dtype=object)
    """
    return (np.vectorize(Fraction)(np.array(obj, dtype=object))).astype(object)


def zeros_vec(n: int) -> Vector:
    return as_integer(np.zeros((n,)))


def zeros_mat(rows: int, cols: int | None = None) -> Matrix:
    if cols is None:
        cols = rows
    return as_integer(np.zeros((rows, cols)))


@validate_aliases
def show(a: Array, max_rows: int = 10, max_cols: int = 10, val_width: int = 15):
    """
    Helper function that prints the numpy's array in a human redable format

    Parameters
    ----------
    a : Array
        The array to print
    max_rows : int, optional
        Max number of rows to display before truncating, by default 10
    max_cols : int, optional
        Max number of columns to display before truncating, by default 10
    val_width : int, optional
        Max characters per cell, by default 15. If a string representation of element is longer, it is truncated e.g 1234...5678

    Examples
    --------
    >>> import pqlattice as pq
    >>> M = pq.random.distribution.Uniform(0, 2**50, seed=0).sample_matrix(7, 5)
    >>> pq.show(M)
    Matrix of integers with shape: 7 x 5
    ====================================
                    [0]              [1]              [2]              [3]              [4]
    [0]  867496826243021   91162487198805  109421..4040930  806253307773444  491889324856851
    [1]  313616384600182  314680579360371  213540430176889  330931104930059  222394738660569
    [2]  166055160201467  743539086037546  796665326308852  712012953150114  460445890320316
    [3]  996855368208390  140240390954947  210028256050344  750154124310314  141827853726696
    [4]  499232256057935  320872572303314  205400145011268  110177..2031755  678794279728913
    [5]  655478801553847  281048514639229  749289460799082  457570956347073  647748016542327
    [6]  206336435080453  713924001980837  545175556185458  414036094290124   74247901643189
    """

    def format_val(val: Any) -> str:
        s = str(val)
        if len(s) > val_width:
            mid = (val_width - 2) // 2
            remainder = (val_width - 2) % 2
            return f"{s[:mid]}..{s[-(mid + remainder) :]}"
        return s

    element_type: str = f"{a.dtype}"
    if is_integer(a):
        element_type = "integers"
    if is_rational(a):
        element_type = "rationals"

    info_header = f"numpy array of {element_type} with shape: {a.shape}"

    is_v = False
    if is_Matrix(a):
        rows, cols = a.shape
        info_header = f"Matrix of {element_type} with shape: {rows} x {cols}"
    elif is_Vector(a):
        dim = a.shape[0]
        info_header = f"Vector of {element_type} with shape: {dim}"
        is_v = True
        rows, cols = 1, dim
    else:
        print(info_header)
        print("=" * len(info_header))
        print(f"{a}")
        return

    print(info_header)
    print("=" * len(info_header))

    ellipsis_col_idx: int | None = None
    ellipsis_row_idx: int | None = None
    if rows <= max_rows:
        row_indices = list(range(rows))
        show_row_ellipsis = False
    else:
        # Top half and bottom half
        r_cut = max_rows // 2
        row_indices = list(range(r_cut)) + list(range(rows - r_cut, rows))
        show_row_ellipsis = True
        ellipsis_row_idx = r_cut

    if cols <= max_cols:
        col_indices = list(range(cols))
        show_col_ellipsis = False
    else:
        c_cut = max_cols // 2
        col_indices = list(range(c_cut)) + list(range(cols - c_cut, cols))
        show_col_ellipsis = True
        ellipsis_col_idx = c_cut

    header = [""]
    for i, c_idx in enumerate(col_indices):
        if show_col_ellipsis and i == ellipsis_col_idx:
            header.append("...")
        header.append(f"[{c_idx}]")

    table_data = [header]

    for i, r_idx in enumerate(row_indices):
        if show_row_ellipsis and i == ellipsis_row_idx:
            ellipsis_row = ["..."] + ["..."] * (len(header) - 1)
            table_data.append(ellipsis_row)

        row_str = [f"[{r_idx}]"]

        for j, c_idx in enumerate(col_indices):
            if show_col_ellipsis and j == ellipsis_col_idx:
                row_str.append("...")

            val = a[c_idx] if is_v else a[r_idx, c_idx]
            row_str.append(format_val(val))

        table_data.append(row_str)

    num_display_cols = len(table_data[0])
    col_widths = [0] * num_display_cols

    for row in table_data:
        for idx, cell in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(cell))

    for row in table_data:
        formatted_row: list[str] = []
        for idx, cell in enumerate(row):
            formatted_row.append(cell.rjust(col_widths[idx]))
        print("  ".join(formatted_row))
