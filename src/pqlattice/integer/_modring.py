from typing import overload

from ..typing import Array
from ._integer import eea


@overload
def mod(a: int, modulus: int) -> int: ...


@overload
def mod(a: Array, modulus: int) -> Array: ...


def mod(a: int | Array, modulus: int) -> int | Array:
    """_summary_

    Parameters
    ----------
    a : int | Array
        _description_
    modulus : int
        _description_

    Returns
    -------
    int | Array
        _description_
    """
    return a % abs(modulus)


@overload
def cmodl(a: int, modulus: int) -> int: ...


@overload
def cmodl(a: Array, modulus: int) -> Array: ...


def cmodl(a: int | Array, modulus: int) -> int | Array:
    """_summary_

    Parameters
    ----------
    a : int | Array
        _description_
    modulus : int
        _description_

    Returns
    -------
    int | Array
        _description_
    """
    return mod(a, modulus) - modulus // 2


@overload
def cmodr(a: int, modulus: int) -> int: ...


@overload
def cmodr(a: Array, modulus: int) -> Array: ...


def cmodr(a: int | Array, modulus: int) -> int | Array:
    """_summary_

    Parameters
    ----------
    a : int | Array
        _description_
    modulus : int
        _description_

    Returns
    -------
    int | Array
        _description_
    """
    return mod(a, modulus) - int(modulus / 2 - 0.1)


@overload
def modinv(a: int, modulus: int) -> int: ...


@overload
def modinv(a: Array, modulus: int) -> Array: ...


def modinv(a: int | Array, modulus: int) -> int | Array:
    """_summary_

    Parameters
    ----------
    a : int | Array
        _description_
    modulus : int
        _description_

    Returns
    -------
    int | Array
        _description_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    """
    if isinstance(a, int):
        if mod(a, modulus) == 0:
            raise ValueError(f"{a} mod {modulus} is zero; Modular inverse does not exist")
        gcd, a_inv, _ = eea(a, modulus)
        if gcd != 1:
            raise ValueError(f"Modular inverse of {a} mod {modulus} does not exist; gcd is equal to {gcd}")
    else:
        if (mod(a, modulus) == 0).all():
            raise ValueError(f"{a} mod {modulus} is zero; Modular inverse does not exist")
        gcd, a_inv, _ = eea(a, modulus)
        if (gcd != 1).any():
            raise ValueError(f"Modular inverse of {a} mod {modulus} does not exist; gcd is equal to {gcd}")

    return mod(a_inv, modulus)


@overload
def modpow(a: Array, r: int, modulus: int) -> Array: ...


@overload
def modpow(a: int, r: int, modulus: int) -> int: ...


def modpow(a: int | Array, r: int, modulus: int) -> int | Array:
    """_summary_

    Parameters
    ----------
    a : int | Array
        _description_
    r : int
        _description_
    modulus : int
        _description_

    Returns
    -------
    int | Array
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
