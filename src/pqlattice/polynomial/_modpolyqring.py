from ..integer._modring import modinv
from ..typing import Vector, validate_aliases
from ._modpolyring import ModIntPolyRing
from ._poly import zero_poly


class ModIntPolyQuotientRing:
    @validate_aliases
    def __init__(self, poly_modulus: Vector, int_modulus: int) -> None:
        self.poly_modulus = poly_modulus
        self.int_modulus = int_modulus
        self.Zm = ModIntPolyRing(int_modulus)

    @property
    def quotient(self):
        return self.poly_modulus

    @validate_aliases
    def reduce(self, polynomial: Vector) -> Vector:
        return self.Zm.rem(polynomial, self.poly_modulus)

    @validate_aliases
    def add(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        return self.reduce(self.Zm.add(polynomial_a, polynomial_b))

    @validate_aliases
    def sub(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        return self.reduce(self.Zm.sub(polynomial_a, polynomial_b))

    @validate_aliases
    def mul(self, polynomial_a: Vector, polynomial_b: Vector) -> Vector:
        return self.reduce(self.Zm.mul(polynomial_a, polynomial_b))

    @validate_aliases
    def inv(self, polynomial: Vector) -> Vector:
        if not self.Zm.coprime(polynomial, self.poly_modulus):
            raise ValueError("Inverse does not exists")

        gcd, u, _ = self.Zm.eea(polynomial, self.poly_modulus)

        c = modinv(gcd, self.int_modulus)

        return self.reduce(u * c)


def construct_ring(p: str, N: int, q: int) -> ModIntPolyQuotientRing:
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
