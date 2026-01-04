from ..integer._modring import mod, modinv
from ..typing import Vector, validate_aliases
from . import _poly as poly


class ModIntPolyRing:
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
        if modulus <= 1:
            raise ValueError("Modulus has to be greater than 1")

        self.modulus = modulus

    @validate_aliases
    def reduce(self, polynomial: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        return poly.trim(mod(polynomial, self.modulus))

    @validate_aliases
    def is_zero(self, polynomial: Vector) -> bool:
        """_summary_

        Parameters
        ----------
        polynomial : Vector
            _description_

        Returns
        -------
        bool
            _description_
        """
        return poly.is_zero_poly(self.reduce(polynomial))

    @validate_aliases
    def deg(self, polynomial: Vector) -> int:
        """_summary_

        Parameters
        ----------
        polynomial : Vector
            _description_

        Returns
        -------
        int
            _description_
        """
        return poly.deg(self.reduce(polynomial))

    @validate_aliases
    def add(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        return self.reduce(poly.add(polynomial_a, polynomial_b))

    @validate_aliases
    def sub(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        return self.reduce(poly.sub(polynomial_a, polynomial_b))

    @validate_aliases
    def mul(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        return self.reduce(poly.mul(polynomial_a, polynomial_b))

    @validate_aliases
    def euclidean_div(self, polynomial_a: Vector, polynomial_b: Vector) -> tuple[Vector, Vector]:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        tuple[Vector, Vector]
            _description_

        Raises
        ------
        ZeroDivisionError
            _description_
        """
        if self.is_zero(polynomial_b):
            raise ZeroDivisionError("Can't divide by zero polynomial")

        q = poly.zero_poly()
        r = self.reduce(polynomial_a)

        d = self.deg(polynomial_b)
        c: int = polynomial_b[d]
        while (dr := self.deg(r)) >= d:
            s = poly.monomial(r[dr] * modinv(c, self.modulus), dr - d)
            q = self.add(q, s)
            r = self.sub(r, self.mul(s, polynomial_b))

        return q, r

    @validate_aliases
    def rem(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        _, r = self.euclidean_div(polynomial_a, polynomial_b)
        return r

    def to_monic(self, polynomial: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        leading_coeff: int = polynomial[self.deg(polynomial)]
        return self.reduce(modinv(leading_coeff, self.modulus) * polynomial)

    def gcd(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        r0 = self.reduce(polynomial_a)
        r1 = self.reduce(polynomial_b)
        if poly.deg(r1) > poly.deg(r0):
            r0, r1 = r1, r0

        while not self.is_zero(r1):
            r0, r1 = r1, self.rem(r0, r1)

        return r0

    def eea(self, polynomial_a: Vector, polynomial_b: Vector):
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        _type_
            _description_
        """
        f0, f1 = self.reduce(polynomial_a), self.reduce(polynomial_b)
        a0, a1 = poly.monomial(1, 0), poly.zero_poly()
        b0, b1 = poly.zero_poly(), poly.monomial(1, 0)

        while not self.is_zero(f1):
            q, r = self.euclidean_div(f0, f1)

            f0, f1 = f1, r

            a0, a1 = a1, self.sub(a0, self.mul(q, a1))
            b0, b1 = b1, self.sub(b0, self.mul(q, b1))

        return f0, a0, b0

    def coprime(self, polynomial_a: Vector, polynomial_b: Vector) -> bool:
        """_summary_

        Parameters
        ----------
        polynomial_a : Vector
            _description_
        polynomial_b : Vector
            _description_

        Returns
        -------
        bool
            _description_
        """
        return all(self.to_monic(self.gcd(polynomial_a, polynomial_b)) == poly.monomial(1, 0))
