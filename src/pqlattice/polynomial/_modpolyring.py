from ..integer._modring import mod, modinv
from ..typing import Vector, validate_aliases
from . import _poly as poly


class ModIntPolyRing:
    def __init__(self, modulus: int):
        """
        Construct the polynomial ring over coefficients from integer quotient ring with given modulus.

        Parameters
        ----------
        modulus : int
            integer quotient ring modulus

        Raises
        ------
        ValueError
            If the modulus is less than 2
        """
        if modulus <= 1:
            raise ValueError("Modulus has to be greater than 1")

        self.modulus = modulus

    @validate_aliases
    def reduce(self, polynomial: Vector) -> Vector:
        """
        Reduces the polynomials coefficients according to the ring, that is modulo `self.modulus`

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        Vector
            polynomial with coefficients from range `[0, self.modulus)`
        """
        return poly.trim(mod(polynomial, self.modulus))

    @validate_aliases
    def is_zero(self, polynomial: Vector) -> bool:
        """
        Checks if the polynomial is the zero polynomial in the ring.

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        bool
            True if it is zero polynomial, False otherwise
        """
        return poly.is_zero_poly(self.reduce(polynomial))

    @validate_aliases
    def deg(self, polynomial: Vector) -> int:
        """
        Returns degree of the given polynomial

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        int
            degree
        """
        return poly.deg(self.reduce(polynomial))

    @validate_aliases
    def add(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """
        Adds two polynomials

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        Vector
            polynomial
        """
        return self.reduce(poly.add(polynomial_a, polynomial_b))

    @validate_aliases
    def sub(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """
        Subtract one polynomial from the other

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        Vector
            polynomial
        """
        return self.reduce(poly.sub(polynomial_a, polynomial_b))

    @validate_aliases
    def mul(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """
        multiplies two polynomials

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        Vector
            polynomial
        """
        return self.reduce(poly.mul(polynomial_a, polynomial_b))

    @validate_aliases
    def euclidean_div(self, polynomial_a: Vector, polynomial_b: Vector) -> tuple[Vector, Vector]:
        """
        Performs the euclidean division for the polynomials

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        tuple[Vector, Vector]
            `tuple[q, r]` such that `polynomial_a == q * polynomial_b + r`

        Raises
        ------
        ZeroDivisionError
            If the `polynomial_b` is the zero polynomial
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
        """
        Returns remainder of the euclidean division

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        Vector
            polynomial
        """
        _, r = self.euclidean_div(polynomial_a, polynomial_b)
        return r

    def to_monic(self, polynomial: Vector) -> Vector:
        """
        Transformt the given polynomial to its monic form, that is multiplies the polynomial by the modular inverse of the leading coefficient.

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        Vector
            polynomial with leading coefficient equal to one.
        """
        leading_coeff: int = polynomial[self.deg(polynomial)]
        return self.reduce(modinv(leading_coeff, self.modulus) * polynomial)

    def gcd(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """
        Computes the polynomial that is the greates common divisor of the given polynomials

        Parameters
        ----------
        polynomial_a : Vector

        polynomial_b : Vector


        Returns
        -------
        Vector
            polynomial
        """
        r0 = self.reduce(polynomial_a)
        r1 = self.reduce(polynomial_b)
        if poly.deg(r1) > poly.deg(r0):
            r0, r1 = r1, r0

        while not self.is_zero(r1):
            r0, r1 = r1, self.rem(r0, r1)

        return r0

    def eea(self, polynomial_a: Vector, polynomial_b: Vector) -> tuple[Vector, Vector, Vector]:
        """
        Extended Euclidean algorithm for the polynomials.

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        tuple[Vector, Vector, Vector]
            `tuple[s, t, gcd]` such that `polynomial_a * s + polynomial_b * t == gcd`
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
        """
        Checks if two polynomials are coprime, that is if their `gcd == 1`

        Parameters
        ----------
        polynomial_a : Vector
        polynomial_b : Vector

        Returns
        -------
        bool
            True if coprime, False otherwise
        """
        return all(self.to_monic(self.gcd(polynomial_a, polynomial_b)) == poly.monomial(1, 0))
