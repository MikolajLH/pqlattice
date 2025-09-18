from typing import overload

from ..typing import Array
from . import _modring as mr


class ModIntRing:
    """
    TODO: write docstring
    """

    def __init__(self, modulus: int):
        """
        TODO: write docstring

        Parameters
        ----------
        modulus : int
            _description_
        """
        if abs(modulus) < 2:
            raise ValueError(f"absolute value of modulus has to greater than one, given modulus: {modulus}")

        self._modulus = abs(modulus)

    @property
    def q(self):
        """
        TODO: write docstring

        Returns
        -------
        _type_
            _description_
        """
        return self._modulus

    def is_zero(self, a: int) -> bool:
        return self.pmod(a) == 0

    @overload
    def mod(self, a: int) -> int: ...

    @overload
    def mod(self, a: Array) -> Array: ...

    def mod(self, a: int | Array) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return mr.mod(a, self.q)

    @overload
    def pow(self, a: int, r: int) -> int: ...

    @overload
    def pow(self, a: Array, r: int) -> Array: ...

    def pow(self, a: int | Array, r: int) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_
        r : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.mod(mr.modpow(a, r, self.q))

    @overload
    def inv(self, a: int) -> int: ...

    @overload
    def inv(self, a: Array) -> Array: ...

    def inv(self, a: int | Array) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.mod(mr.modinv(a, self.q))

    @overload
    def neg(self, a: int) -> int: ...

    @overload
    def neg(self, a: Array) -> Array: ...

    def neg(self, a: int | Array) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_
        """
        return self.mod(-a)

    def add(self, a: int, b: int) -> int:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.mod(a + b)

    def mul(self, a: int, b: int) -> int:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.mod(a * b)

    def div(self, a: int, b: int) -> int:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.mul(a, self.inv(b))

    def sub(self, a: int, b: int) -> int:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.mod(a - b)

    @overload
    def pmod(self, a: int) -> int: ...

    @overload
    def pmod(self, a: Array) -> Array: ...

    def pmod(self, a: int | Array) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return mr.mod(a, self.q)

    @overload
    def cmodl(self, a: int) -> int: ...

    @overload
    def cmodl(self, a: Array) -> Array: ...

    def cmodl(self, a: int | Array) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return mr.cmodl(a, self.q)

    @overload
    def cmodr(self, a: int) -> int: ...

    @overload
    def cmodr(self, a: Array) -> Array: ...

    def cmodr(self, a: int | Array) -> int | Array:
        """
        TODO: write docstring

        Parameters
        ----------
        a : int
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return mr.cmodr(a, self.q)
