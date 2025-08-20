from pqlattice.types import *
from typing import Any, Callable, TypeVar, TypeAliasType, TypeGuard
from inspect import signature

def _is_nparray(obj: Any) -> TypeGuard[NDArray[Any]]:
    return isinstance(obj, np.ndarray)


def _is_Vector(obj: Any) -> TypeGuard[Vector]:
    return _is_nparray(obj) and len(obj.shape) == 1


def _is_Matrix(obj: Any) -> TypeGuard[Matrix]:
    return _is_nparray(obj) and len(obj.shape) == 2


def _is_SquareMatrix(obj: Any) -> TypeGuard[SquareMatrix]:
    return _is_Matrix(obj) and obj.shape[0] == obj.shape[1]


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



T = TypeVar('T', bound=TypeAliasType)
def get_predicate_for_alias(type_name: T) -> Callable[[T], bool] | None:
    
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



def validate_types[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwds: P.kwargs) -> T:
        sig = signature(func)
        bounded_args = sig.bind(*args, **kwds)
        bounded_args.apply_defaults()
        for arg_name, arg_value in bounded_args.arguments.items():
            if expected_type := func.__annotations__.get(arg_name): # There is a type annotation for the argument
                pred = get_predicate_for_alias(expected_type)
                if pred is not None: # type annotations has a predicate to be checked
                    if not pred(arg_value): # predicate is not fullfilled
                        raise TypeError(f"in function <{func.__name__}> argument <{arg_name}> with value <{arg_value}> of type <{type(arg_value)}> does not fulfill predicate corresponding to expected type {expected_type}")
                    else: # predicate is fullfilled
                        continue
                else: # there is no predicate for given type annotation, I am not sure what to do, raise exception for now. TODO: change or remove
                    raise TypeError(f"In function <{func.__name__}>, argument <{arg_name}> with value <{arg_value}>, No predicate defined for annotation <{expected_type}>")
            else: # No type annotation for argument - raise exception for debugging purposes. TODO: change or remove
                raise NotImplementedError(f"No annotation in function <{func.__name__}>, for argument <{arg_name}> with value <{arg_value}>")
        return func(*args, **kwds)
    return wrapper