from typing import overload

from ..typing import Array
from ._integer import eea


@overload
def mod(a: int, modulus: int) -> int: ...


@overload
def mod(a: Array, modulus: int) -> Array: ...


def mod(a: int | Array, modulus: int) -> int | Array:
    """
    TODO: write docstring
    https://en.wikipedia.org/wiki/Euclidean_division
    https://en.wikipedia.org/wiki/Modulo
    https://doc.sagemath.org/html/en/reference/finite_rings/sage/rings/finite_rings/integer_mod.html#sage.rings.finite_rings.integer_mod.Mod

    Parameters
    ----------
    a : int
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_
    """
    return a % abs(modulus)


@overload
def cmodl(a: int, modulus: int) -> int: ...


@overload
def cmodl(a: Array, modulus: int) -> Array: ...


def cmodl(a: int | Array, modulus: int) -> int | Array:
    """
    TODO: write docstring

    Parameters
    ----------
    a : int
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_
    """
    return mod(a, modulus) - modulus // 2


@overload
def cmodr(a: int, modulus: int) -> int: ...


@overload
def cmodr(a: Array, modulus: int) -> Array: ...


def cmodr(a: int | Array, modulus: int) -> int | Array:
    """
    TODO: write docstring

    Parameters
    ----------
    a : int
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_
    """
    return mod(a, modulus) - int(modulus / 2 - 0.1)


@overload
def modinv(a: int, modulus: int) -> int: ...


@overload
def modinv(a: Array, modulus: int) -> Array: ...


def modinv(a: int | Array, modulus: int) -> int | Array:
    """
    TODO: write docstring

    Parameters
    ----------
    a : int
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    """

    if mod(a, modulus) == 0:
        raise ValueError(f"{a} mod {modulus} is zero; Modular inverse does not exist")
    gcd, a_inv, _ = eea(a, modulus)
    if gcd != 1:
        raise ValueError(f"Modular inverse of {a} mod {modulus} does not exist; gcd is equal to {gcd}")

    return mod(a_inv, modulus)


@overload
def modpow(a: Array, r: int, modulus: int) -> Array: ...


@overload
def modpow(a: int, r: int, modulus: int) -> int: ...


def modpow(a: int | Array, r: int, modulus: int) -> int | Array:
    """
    TODO: write docstring

    Parameters
    ----------
    a : int
        _description_
    r : int
        _description_
    modulus : int
        _description_

    Returns
    -------
    int
        _description_
    """

    if r < 0:
        return modpow(modinv(a, modulus), -r, modulus)

    y, z = 1, a
    while r != 0:
        if r % 2 == 1:
            y = mod(y * z, modulus)
        r //= 2
        z = mod(z * z, modulus)
    return y


# def pmodinv(a: int, p: int) -> int:
#     """
#     Calculates the multiplicative inverse of *a* modulo *p*
#     use Euler-Fermat Theorem,
#     asume p is prime number

#     Parameters
#     ----------
#     a : `int`
#         _description_
#     p : `int`
#         _description_

#     Returns
#     -------
#     int
#         number z such that (z * a) mod p == 1
#     """
#     phi = p - 1
#     return modpow(a, phi - 1, p)
