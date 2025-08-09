def eea(a: int, b: int) -> tuple[int, int, int]:
    """extended euclidean algorithm
    TODO: add doc string
    """
    if a == 0 and b == 0:
        raise ValueError("<PQLE> a and b can't be both zero")

    old_s, s = 1, 0
    old_r, r = a, b
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s

    t = 0 if b == 0 else (old_r - old_s * a) // b
    s = old_s
    gcd = old_r
    if gcd < 0:
        gcd = -gcd
        s = -s
        t = -t

    return gcd, s, t
