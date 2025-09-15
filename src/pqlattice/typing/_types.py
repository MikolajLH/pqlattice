from typing import Any

import numpy as np
from numpy.typing import NDArray

type ArrayInt = NDArray[np.integer[Any]]

type Vector = NDArray[np.floating[Any] | np.integer[Any]]
type Matrix = NDArray[np.floating[Any] | np.integer[Any]]
type SquareMatrix = NDArray[np.floating[Any] | np.integer[Any]]

type VectorFloat = NDArray[np.floating[Any]]
type MatrixFloat = NDArray[np.floating[Any]]
type SquareMatrixFloat = NDArray[np.floating[Any]]

type VectorInt = NDArray[np.integer[Any]]
type MatrixInt = NDArray[np.integer[Any]]
type SquareMatrixInt = NDArray[np.integer[Any]]
