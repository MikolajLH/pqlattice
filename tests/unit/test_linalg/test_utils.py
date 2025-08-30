import numpy as np
from hypothesis import assume, given
from hypothesis.extra.numpy import array_shapes, arrays
from hypothesis.strategies import integers, just

from pqlattice.linalg._utils import col_add, col_scale, col_swap, row_add, row_scale, row_swap
from pqlattice.typing import Matrix

ARRAY_ELEMENTS = {
    "min_value": -100_000,
    "max_value": 100_000,
    "allow_nan": False,
    "allow_infinity": False,
}


@given(
    m=arrays(just(int) | just(float), array_shapes(min_dims=2, max_dims=2, max_side=10), elements=ARRAY_ELEMENTS),
    i=integers(min_value=0, max_value=10),
    k=integers(min_value=0, max_value=10),
)
def test_row_swap(m: Matrix, i: int, k: int):
    rows_n = m.shape[0]
    i %= rows_n
    k %= rows_n

    assume(i != k)
    assume(not np.all(m[i] == m[k]))  # discard matrices which have the same values in tested rows
    w = m.copy()

    row_swap(m, i, k)

    assert np.all(m[i] == w[k])
    assert np.all(m[k] == w[i])
    assert not np.all(m[i] == w[i])
    assert not np.all(m[k] == w[k])


@given(
    m=arrays(just(int) | just(float), array_shapes(min_dims=2, max_dims=2, max_side=10), elements=ARRAY_ELEMENTS),
    i=integers(min_value=0, max_value=10),
    k=integers(min_value=0, max_value=10),
    c=integers(min_value=-100_000, max_value=100_000),
)
def test_row_add(m: Matrix, i: int, k: int, c: int):
    rows_n = m.shape[0]
    i %= rows_n
    k %= rows_n
    s = c if np.issubdtype(m.dtype, np.integer) else float(c)
    w = m.copy()

    row_add(m, i, k, s)

    assert np.all(m[i] == w[i] + s * w[k])  # check that target row has correct values
    if i != k:
        assert np.all(m[k] == w[k])  # check that source row has not been changed


@given(
    m=arrays(just(int) | just(float), array_shapes(min_dims=2, max_dims=2, max_side=10), elements=ARRAY_ELEMENTS),
    i=integers(min_value=0, max_value=10),
    c=integers(min_value=-100_000, max_value=100_000),
)
def test_row_scale(m: Matrix, i: int, c: int):
    rows_n = m.shape[0]
    i %= rows_n
    s = c if np.issubdtype(m.dtype, np.integer) else float(c)
    w = m.copy()

    row_scale(m, i, s)

    assert np.all(m[i] == s * w[i])  # check that target row has correct values


# Cols


@given(
    m=arrays(just(int) | just(float), array_shapes(min_dims=2, max_dims=2, max_side=10), elements=ARRAY_ELEMENTS),
    i=integers(min_value=0, max_value=10),
    k=integers(min_value=0, max_value=10),
)
def test_col_swap(m: Matrix, i: int, k: int):
    cols_n = m.shape[1]
    i %= cols_n
    k %= cols_n

    assume(i != k)
    assume(not np.all(m[:, i] == m[:, k]))  # discard matrices which have the same values in tested cols
    w = m.copy()

    col_swap(m, i, k)

    assert np.all(m[:, i] == w[:, k])
    assert np.all(m[:, k] == w[:, i])
    assert not np.all(m[:, i] == w[:, i])
    assert not np.all(m[:, k] == w[:, k])


@given(
    m=arrays(just(int) | just(float), array_shapes(min_dims=2, max_dims=2, max_side=10), elements=ARRAY_ELEMENTS),
    i=integers(min_value=0, max_value=10),
    k=integers(min_value=0, max_value=10),
    c=integers(min_value=-100_000, max_value=100_000),
)
def test_col_add(m: Matrix, i: int, k: int, c: int):
    cols_n = m.shape[1]
    i %= cols_n
    k %= cols_n
    s = c if np.issubdtype(m.dtype, np.integer) else float(c)
    w = m.copy()

    col_add(m, i, k, s)

    assert np.all(m[:, i] == w[:, i] + s * w[:, k])  # check that target col has correct values
    if i != k:
        assert np.all(m[:, k] == w[:, k])  # check that source col has not been changed


@given(
    m=arrays(just(int) | just(float), array_shapes(min_dims=2, max_dims=2, max_side=10), elements=ARRAY_ELEMENTS),
    i=integers(min_value=0, max_value=10),
    c=integers(min_value=-100_000, max_value=100_000),
)
def test_col_scale(m: Matrix, i: int, c: int):
    cols_n = m.shape[1]
    i %= cols_n
    s = c if np.issubdtype(m.dtype, np.integer) else float(c)
    w = m.copy()

    col_scale(m, i, s)

    assert np.all(m[:, i] == s * w[:, i])  # check that target col has correct values
