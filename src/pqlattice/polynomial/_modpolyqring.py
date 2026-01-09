from ..integer._modring import mod, modinv
from ..typing import Vector, validate_aliases
from ._modpolyring import ModIntPolyRing
from ._poly import zero_poly


class ModIntPolyQuotientRing:
    @validate_aliases
    def __init__(self, poly_modulus: Vector, int_modulus: int) -> None:
        """_summary_

        Parameters
        ----------
        poly_modulus : Vector
            _description_
        int_modulus : int
            _description_
        """
        self.poly_modulus = poly_modulus
        self.int_modulus = int_modulus
        self.Zm = ModIntPolyRing(int_modulus)

    @property
    def quotient(self) -> Vector:
        """_summary_

        Returns
        -------
        Vector
            _description_
        """
        return self.poly_modulus

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
        return self.Zm.rem(polynomial, self.poly_modulus)

    @validate_aliases
    def center_lift(self, polynomial: Vector) -> Vector:
        """
        Hoffstein page. 414 - 415

        Parameters
        ----------
        polynomial : Vector
            _description_

        Returns
        -------
        Vector
            _description_
        """
        return mod(polynomial + self.int_modulus // 2, self.int_modulus) - self.int_modulus // 2

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
        return self.reduce(self.Zm.add(polynomial_a, polynomial_b))

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
        return self.reduce(self.Zm.sub(polynomial_a, polynomial_b))

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
        return self.reduce(self.Zm.mul(polynomial_a, polynomial_b))

    @validate_aliases
    def inv(self, polynomial: Vector) -> Vector:
        """_summary_

        Parameters
        ----------
        polynomial : Vector
            _description_

        Returns
        -------
        Vector
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        if not self.Zm.coprime(polynomial, self.poly_modulus):
            raise ValueError("Inverse does not exists")

        gcd, u, _ = self.Zm.eea(polynomial, self.poly_modulus)

        c = modinv(gcd, self.int_modulus)

        return self.reduce(u * c)


def construct_ring(p: str, N: int, q: int) -> ModIntPolyQuotientRing:
    """_summary_

    Parameters
    ----------
    p : str
        _description_
    N : int
        _description_
    q : int
        _description_

    Returns
    -------
    ModIntPolyQuotientRing
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    g = zero_poly(N)
    match p:
        case "-" | "X^N - 1":
            g[[0, N]] = -1, 1
            pass
        case "+" | "X^N + 1":
            g[[0, N]] = 1, 1
            pass
        case "prime" | "X^N - x - 1":
            g[[0, 1, N]] = -1, -1, 1
        case _:
            raise ValueError(f"Unknown symbol: {p}")

    return ModIntPolyQuotientRing(g, q)
