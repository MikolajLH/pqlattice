from ._integer import eea


def modinv(a: int, modulus: int) -> int:
    """
    TODO: Write Documentation

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
    if a % modulus == 0:
        raise ValueError(f"{a} mod {modulus} is zero; Modular inverse does not exist")
    gcd, a_inv, _ = eea(a, modulus)
    if gcd != 1:
        raise ValueError(f"Modular inverse of {a} mod {modulus} does not exist; gcd is equal to {gcd}")

    return a_inv % modulus


def modpow(a: int, r: int, modulus: int) -> int:
    """
    TODO: Write Documentation

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
            y = (y * z) % modulus
        r //= 2
        z = (z * z) % modulus
    return y
