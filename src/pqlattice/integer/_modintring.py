from typing import overload

from ..typing import Array
from ._modring import cmodl, cmodr, mod, modinv, modpow


class ModIntRing:
    def __init__(self, modulus: int):
        if abs(modulus) < 2:
            raise ValueError(f"absolute value of modulus has to greater than one, given modulus: {modulus}")

        self._modulus = abs(modulus)

    @property
    def q(self):
        return self._modulus

    def is_zero(self, a: int) -> bool:
        return self.mod(a) == 0

    @overload
    def mod(self, a: int) -> int: ...

    @overload
    def mod(self, a: Array) -> Array: ...

    def mod(self, a: int | Array) -> int | Array:
        return mod(a, self.q)

    @overload
    def pow(self, a: int, r: int) -> int: ...

    @overload
    def pow(self, a: Array, r: int) -> Array: ...

    def pow(self, a: int | Array, r: int) -> int | Array:
        return self.mod(modpow(a, r, self.q))

    @overload
    def inv(self, a: int) -> int: ...

    @overload
    def inv(self, a: Array) -> Array: ...

    def inv(self, a: int | Array) -> int | Array:
        return self.mod(modinv(a, self.q))

    @overload
    def neg(self, a: int) -> int: ...

    @overload
    def neg(self, a: Array) -> Array: ...

    def neg(self, a: int | Array) -> int | Array:
        return self.mod(-a)

    def add(self, a: int, b: int) -> int:
        return self.mod(a + b)

    def mul(self, a: int, b: int) -> int:
        return self.mod(a * b)

    def div(self, a: int, b: int) -> int:
        return self.mul(a, self.inv(b))

    def sub(self, a: int, b: int) -> int:
        return self.mod(a - b)

    @overload
    def cmodl(self, a: int) -> int: ...

    @overload
    def cmodl(self, a: Array) -> Array: ...

    def cmodl(self, a: int | Array) -> int | Array:
        return cmodl(a, self.q)

    @overload
    def cmodr(self, a: int) -> int: ...

    @overload
    def cmodr(self, a: Array) -> Array: ...

    def cmodr(self, a: int | Array) -> int | Array:
        return cmodr(a, self.q)
