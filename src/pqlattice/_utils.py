from fractions import Fraction

import numpy as np

from .typing import Array, validate_aliases


@validate_aliases
def as_integer(a: Array) -> Array:
    return (np.vectorize(int)(a.astype(object))).astype(object)


@validate_aliases
def as_rational(a: Array) -> Array:
    return (np.vectorize(Fraction)(a.astype(object))).astype(object)
