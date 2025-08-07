import numpy as np
from numpy.typing import NDArray

type Vector = NDArray[np.float64 | np.int64]
type Matrix = NDArray[np.float64 | np.int64]
type SquareMatrix = NDArray[np.float64 | np.int64]

type VectorFloat = NDArray[np.float64]
type MatrixFloat = NDArray[np.float64]
type SquareMatrixFloat = NDArray[np.float64]

type VectorInt = NDArray[np.int64]
type MatrixInt = NDArray[np.int64]
type SquareMatrixInt = NDArray[np.int64]

# TODO: Consider using typing.Annotated to define types of values from quotient rings (integer or polynomial)
