from .integer import eea


def modinv(a: int, modulus: int) -> int:
    gcd, a_inv, _ = eea(a, modulus)
    if gcd != 1:
        raise ValueError(f"Modular inverse of {a} mod {modulus} does not exist; gcd is equal to {gcd}")

    return a_inv % modulus


def modpow(a: int, r: int, modulus: int) -> int:
    if r < 0:
        return modpow(modinv(a, modulus), -r, modulus)

    y, z = 1, a
    while r != 0:
        if r % 2 == 1:
            y = (y * z) % modulus
        r //= 2
        z = (z * z) % modulus
    return y
