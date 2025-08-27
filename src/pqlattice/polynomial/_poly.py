from ..typing import Int, VectorInt


def pad(p: VectorInt, max_deg: int) -> VectorInt:
    pass


def trim(p: VectorInt) -> VectorInt:
    pass


def add(p: VectorInt, q: VectorInt) -> VectorInt:
    pass


def sub(p: VectorInt, q: VectorInt) -> VectorInt:
    pass


def mul(p: VectorInt, q: VectorInt) -> VectorInt:
    pass


def monomial(coeff: Int, degree: Int) -> VectorInt:
    pass


def const_poly(coeff: Int, max_deg: Int | None = None) -> VectorInt:
    pass


def zero_poly(max_deg: Int | None = None) -> VectorInt:
    pass


def is_zero_poly(p: VectorInt) -> bool:
    pass
