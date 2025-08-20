import numpy as np
from numpy.typing import NDArray


type Float = np.float32
type Int = np.int64

type Vector = NDArray[Float | Int]
type Matrix = NDArray[Float | Int]
type SquareMatrix = NDArray[Float | Int]

type VectorFloat = NDArray[Float]
type MatrixFloat = NDArray[Float]
type SquareMatrixFloat = NDArray[Float]

type VectorInt = NDArray[Int]
type MatrixInt = NDArray[Int]
type SquareMatrixInt = NDArray[Int]

# TODO: Consider using typing.Annotated to define types of values from quotient rings (integer or polynomial)
