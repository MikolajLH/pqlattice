from . import _modring as mr  # type: ignore


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

    def mod(self, a: int):
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

    def pow(self, a: int, r: int):
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

    def inv(self, a: int):
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

    def add(self, a: int, b: int):
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

    def mul(self, a: int, b: int):
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

    def div(self, a: int, b: int):
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

    def sub(self, a: int, b: int):
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

    def pmod(self, a: int):
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

    def cmodl(self, a: int):
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

    def cmodr(self, a: int):
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
