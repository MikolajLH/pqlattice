from typing import Literal

from ..integer._modring import mod, modinv
from ..typing import Vector, validate_aliases
from ._modpolyring import ModIntPolyRing
from ._poly import zero_poly


class ModIntPolyQuotientRing:
    @validate_aliases
    def __init__(self, poly_modulus: Vector, int_modulus: int) -> None:
        """
        Creates the polynomial quotient ring of coefficient from the integer quotien ring

        Parameters
        ----------
        poly_modulus : Vector
            modulus of the polynomial quotient ring
        int_modulus : int
            modulus of the integer quotient ring
        """
        self.poly_modulus = poly_modulus
        self.int_modulus = int_modulus
        self.Zm = ModIntPolyRing(int_modulus)

    @property
    def quotient(self) -> Vector:
        """
        Get the polynomial modulus of this ring.

        Returns
        -------
        Vector
            `p` the polynomial modulus of this quotient ring
        """
        return self.poly_modulus

    @validate_aliases
    def reduce(self, polynomial: Vector) -> Vector:
        """

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        Vector
            polynomial
        """
        return self.Zm.rem(polynomial, self.poly_modulus)

    @validate_aliases
    def center_lift(self, polynomial: Vector) -> Vector:
        """
        Hoffstein page. 414 - 415

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        Vector
            polynomial
        """
        return mod(polynomial + self.int_modulus // 2, self.int_modulus) - self.int_modulus // 2

    @validate_aliases
    def add(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """
        adds two polynomials

        Parameters
        ----------
        polynomial_a : Vector

        polynomial_b : Vector


        Returns
        -------
        Vector
            polynomial
        """
        return self.reduce(self.Zm.add(polynomial_a, polynomial_b))

    @validate_aliases
    def sub(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        """
        subtract one polynomial from the other

        Parameters
        ----------
        polynomial_a : Vector

        polynomial_b : Vector

        Returns
        -------
        Vector
            polynomial
        """
        return self.reduce(self.Zm.sub(polynomial_a, polynomial_b))

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
        return self.reduce(self.Zm.mul(polynomial_a, polynomial_b))

    @validate_aliases
    def inv(self, polynomial: Vector) -> Vector:
        """
        Tries to find the multiplicative inverse of the given polynomial in the ring.

        Parameters
        ----------
        polynomial : Vector

        Returns
        -------
        Vector
            polynomial

        Raises
        ------
        ValueError
            If the inverse does not exists
        """
        if not self.Zm.coprime(polynomial, self.poly_modulus):
            raise ValueError("Inverse does not exists")

        gcd, u, _ = self.Zm.eea(polynomial, self.poly_modulus)

        c = modinv(gcd, self.int_modulus)

        return self.reduce(u * c)


def construct_ring(p: Literal["-", "+", "prime"], N: int, q: int) -> ModIntPolyQuotientRing:
    """
    Helper function for constructing rings relevant to NTRU-like systems
    The ring type argument corresponds to following quotients:
    - "+" -> quotient is `X ** N + 1`
    - "-" -> quotient is `X ** N - 1`
    - "prime" -> quotient is `X ** N - x - 1`

    Parameters
    ----------
    p : '+'|'-'|'prime'
        type of the ring to be constructed
    N : int
        Degree of the quotient polynomial
    q : int
        modulus of the integer quotient ring

    Returns
    -------
    ModIntPolyQuotientRing
    """
    g = zero_poly(N)
    match p:
        case "-":
            g[[0, N]] = -1, 1
        case "+":
            g[[0, N]] = 1, 1
        case "prime":
            g[[0, 1, N]] = -1, -1, 1
        case _:
            raise ValueError(f"Unknown symbol: {p}")

    return ModIntPolyQuotientRing(g, q)
