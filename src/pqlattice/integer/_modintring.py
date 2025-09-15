from typing import overload

from ..typing import ArrayInt
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
    def mod(self, a: ArrayInt) -> ArrayInt: ...

    def mod(self, a: int | ArrayInt) -> int | ArrayInt:
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
    def pow(self, a: ArrayInt, r: int) -> ArrayInt: ...

    def pow(self, a: int | ArrayInt, r: int) -> int | ArrayInt:
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
    def inv(self, a: ArrayInt) -> ArrayInt: ...

    def inv(self, a: int | ArrayInt) -> int | ArrayInt:
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
    def neg(self, a: ArrayInt) -> ArrayInt: ...

    def neg(self, a: int | ArrayInt) -> int | ArrayInt:
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
    def pmod(self, a: ArrayInt) -> ArrayInt: ...

    def pmod(self, a: int | ArrayInt) -> int | ArrayInt:
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
    def cmodl(self, a: ArrayInt) -> ArrayInt: ...

    def cmodl(self, a: int | ArrayInt) -> int | ArrayInt:
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
    def cmodr(self, a: ArrayInt) -> ArrayInt: ...

    def cmodr(self, a: int | ArrayInt) -> int | ArrayInt:
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
