from . import mod, modinv, modpow


class IntModRing:
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
        return mod(a, self.q)

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
        return self.mod(modpow(a, r, self.q))

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
        return self.mod(modinv(a, self.q))

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
        return mod(a, self.q)

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
        return mod(a, self.q) - (self.q // 2)

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
        return mod(a, self.q) - (self.q // 2) + 1
