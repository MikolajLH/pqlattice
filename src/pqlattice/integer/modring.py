from .integer import eea


def modinv(a: int, modulus: int) -> int:
    gcd, a_inv, _ = eea(a, modulus)
    if gcd != 1:
        raise ValueError(f"Modular inverse of {a} mod {modulus} does not exist; gcd is equal to {gcd}")

    return a_inv % modulus
