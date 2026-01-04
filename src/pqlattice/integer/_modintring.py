from typing import overload

from ..typing import Array
from ._modring import cmodl, cmodr, mod, modinv, modpow


class ModIntRing:
    def __init__(self, modulus: int):
        """_summary_

        Parameters
        ----------
        modulus : int
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        if abs(modulus) < 2:
            raise ValueError(f"absolute value of modulus has to greater than one, given modulus: {modulus}")

        self._modulus = abs(modulus)

    @property
    def q(self) -> int:
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._modulus

    def is_zero(self, a: int) -> bool:
        """_summary_

        Parameters
        ----------
        a : int
            _description_

        Returns
        -------
        bool
            _description_
        """
        return self.mod(a) == 0

    @overload
    def mod(self, a: int) -> int: ...

    @overload
    def mod(self, a: Array) -> Array: ...

    def mod(self, a: int | Array) -> int | Array:
        """_summary_

        Parameters
        ----------
        a : int | Array
            _description_

        Returns
        -------
        int | Array
            _description_
        """
        return mod(a, self.q)

    @overload
    def pow(self, a: int, r: int) -> int: ...

    @overload
    def pow(self, a: Array, r: int) -> Array: ...

    def pow(self, a: int | Array, r: int) -> int | Array:
        """_summary_

        Parameters
        ----------
        a : int | Array
            _description_
        r : int
            _description_

        Returns
        -------
        int | Array
            _description_
        """
        return self.mod(modpow(a, r, self.q))

    @overload
    def inv(self, a: int) -> int: ...

    @overload
    def inv(self, a: Array) -> Array: ...

    def inv(self, a: int | Array) -> int | Array:
        """_summary_

        Parameters
        ----------
        a : int | Array
            _description_

        Returns
        -------
        int | Array
            _description_
        """
        return self.mod(modinv(a, self.q))

    @overload
    def neg(self, a: int) -> int: ...

    @overload
    def neg(self, a: Array) -> Array: ...

    def neg(self, a: int | Array) -> int | Array:
        """_summary_

        Parameters
        ----------
        a : int | Array
            _description_

        Returns
        -------
        int | Array
            _description_
        """
        return self.mod(-a)

    def add(self, a: int, b: int) -> int:
        """_summary_

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        int
            _description_
        """
        return self.mod(a + b)

    def mul(self, a: int, b: int) -> int:
        """_summary_

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        int
            _description_
        """
        return self.mod(a * b)

    def div(self, a: int, b: int) -> int:
        """_summary_

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        int
            _description_
        """
        return self.mul(a, self.inv(b))

    def sub(self, a: int, b: int) -> int:
        """_summary_

        Parameters
        ----------
        a : int
            _description_
        b : int
            _description_

        Returns
        -------
        int
            _description_
        """
        return self.mod(a - b)

    @overload
    def cmodl(self, a: int) -> int: ...

    @overload
    def cmodl(self, a: Array) -> Array: ...

    def cmodl(self, a: int | Array) -> int | Array:
        """_summary_

        Parameters
        ----------
        a : int | Array
            _description_

        Returns
        -------
        int | Array
            _description_
        """
        return cmodl(a, self.q)

    @overload
    def cmodr(self, a: int) -> int: ...

    @overload
    def cmodr(self, a: Array) -> Array: ...

    def cmodr(self, a: int | Array) -> int | Array:
        """_summary_

        Parameters
        ----------
        a : int | Array
            _description_

        Returns
        -------
        int | Array
            _description_
        """
        return cmodr(a, self.q)
