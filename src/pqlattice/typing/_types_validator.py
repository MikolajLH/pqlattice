import logging
from collections.abc import Callable
from inspect import signature
from typing import Any, TypeAliasType, TypeGuard

import numpy as np
from numpy.typing import NDArray

from ._types import (
    Float,
    Int,
    Matrix,
    MatrixFloat,
    MatrixInt,
    SquareMatrix,
    SquareMatrixFloat,
    SquareMatrixInt,
    Vector,
    VectorFloat,
    VectorInt,
)

logger = logging.getLogger(__name__)


def _is_nparray(obj: Any) -> TypeGuard[NDArray[Any]]:
    return isinstance(obj, np.ndarray)


def _is_Vector(obj: Any) -> TypeGuard[Vector]:
    return _is_nparray(obj) and len(obj.shape) == 1 and (obj.dtype == Float or obj.dtype == Int)


def _is_Matrix(obj: Any) -> TypeGuard[Matrix]:
    return _is_nparray(obj) and len(obj.shape) == 2 and (obj.dtype == Float or obj.dtype == Int)


def _is_SquareMatrix(obj: Any) -> TypeGuard[SquareMatrix]:
    return _is_Matrix(obj) and obj.shape[0] == obj.shape[1] and (obj.dtype == Float or obj.dtype == Int)


def _is_VectorInt(obj: Any) -> TypeGuard[VectorInt]:
    return _is_Vector(obj) and obj.dtype == Int


def _is_MatrixInt(obj: Any) -> TypeGuard[MatrixInt]:
    return _is_Matrix(obj) and obj.dtype == Int


def _is_SquareMatrixInt(obj: Any) -> TypeGuard[SquareMatrixInt]:
    return _is_SquareMatrix(obj) and obj.dtype == Int


def _is_VectorFloat(obj: Any) -> TypeGuard[VectorFloat]:
    return _is_Vector(obj) and obj.dtype == Float


def _is_MatrixFloat(obj: Any) -> TypeGuard[MatrixFloat]:
    return _is_Matrix(obj) and obj.dtype == Float


def _is_SquareMatrixFloat(obj: Any) -> TypeGuard[SquareMatrixFloat]:
    return _is_SquareMatrix(obj) and obj.dtype == Float


def get_predicate_for_alias[T: TypeAliasType](type_name: T) -> Callable[[T], bool] | None:
    # Bare
    if type_name == Vector:
        return _is_Vector

    if type_name == Matrix:
        return _is_Matrix

    if type_name == SquareMatrix:
        return _is_SquareMatrix

    # Ints
    if type_name == VectorInt:
        return _is_VectorInt

    if type_name == MatrixInt:
        return _is_MatrixInt

    if type_name == SquareMatrixInt:
        return _is_SquareMatrixInt

    # Floats
    if type_name == VectorFloat:
        return _is_VectorFloat

    if type_name == MatrixFloat:
        return _is_MatrixFloat

    if type_name == SquareMatrixFloat:
        return _is_SquareMatrixFloat

    return None


def _peel_type_alias(tp: Any) -> Any:
    while isinstance(tp, TypeAliasType):
        tp = tp.__value__
    return tp


def validate_aliases[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwds: P.kwargs) -> T:
        # TODO: Is it possible to add memoization?
        sig = signature(func)
        bounded_args = sig.bind(*args, **kwds)
        bounded_args.apply_defaults()
        for arg_name, arg_value in bounded_args.arguments.items():
            if expected_type := func.__annotations__.get(arg_name):  # There is a type annotation for the argument
                # msg = f"func <{func.__name__}>, arg <{arg_name}>  val <{arg_value}> type <{type(arg_value)}> expected <{expected_type}>"
                # logger.info(msg)
                pred = get_predicate_for_alias(expected_type)
                if pred is not None:  # type annotations has a predicate to be checked
                    if not pred(arg_value):  # predicate is not fullfilled
                        raise TypeError(
                            f"func <{func.__name__}>, arg <{arg_name}> val <{arg_value}> arg's type <{type(arg_value)}> predicate for <{expected_type}> failed"
                        )
                    else:  # predicate is fullfilled
                        continue
                else:  # no predicate defined for given type hint
                    true_tp = _peel_type_alias(expected_type)
                    msg = f"func <{func.__name__}>, arg <{arg_name}> val <{arg_value}>, arg's type <{type(arg_value)}>, hint <{expected_type}>, true hint <{true_tp}>"
                    logger.warning(msg)
            else:  # No type annotation for argument
                msg = f"No annotation in function <{func.__name__}>, for argument <{arg_name}> with value <{arg_value}>"
                logger.warning(msg)

        return func(*args, **kwds)

    return wrapper
