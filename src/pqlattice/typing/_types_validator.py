import logging
from collections.abc import Callable
from inspect import signature
from typing import Any, TypeAliasType, TypeGuard

import numpy as np
from numpy.typing import NDArray

from ._types import Matrix, SquareMatrix, Vector

logger = logging.getLogger(__name__)


def _is_nparray(obj: Any) -> TypeGuard[NDArray[Any]]:
    return isinstance(obj, np.ndarray)


def is_Vector(obj: Any) -> TypeGuard[Vector]:
    return _is_nparray(obj) and len(obj.shape) == 1


def is_Matrix(obj: Any) -> TypeGuard[Matrix]:
    return _is_nparray(obj) and len(obj.shape) == 2


def is_SquareMatrix(obj: Any) -> TypeGuard[SquareMatrix]:
    return is_Matrix(obj) and obj.shape[0] == obj.shape[1]


def _get_predicate_for_alias[T: TypeAliasType](type_name: T) -> Callable[[T], bool] | None:
    # Bare
    if type_name == Vector:
        return is_Vector

    if type_name == Matrix:
        return is_Matrix

    if type_name == SquareMatrix:
        return is_SquareMatrix

    return None


def validate_aliases[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwds: P.kwargs) -> T:
        sig = signature(func)
        bounded_args = sig.bind(*args, **kwds)
        bounded_args.apply_defaults()
        for arg_name, arg_value in bounded_args.arguments.items():
            if expected_type := func.__annotations__.get(arg_name):  # There is a type annotation for the argument
                pred = _get_predicate_for_alias(expected_type)
                if pred is not None and not pred(arg_value):  # type annotations has a predicate to be checked and predicate is not fullfilled
                    raise TypeError(f"func <{func.__name__}>, arg <{arg_name}> val <{arg_value}> arg's type <{type(arg_value)}> predicate for <{expected_type}> failed")

        return func(*args, **kwds)

    return wrapper
