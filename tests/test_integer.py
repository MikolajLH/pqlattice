import math

from pqlattice.integer.integer import eea


def test_eea():
    # TODO: use actual pytest features, parameterize instead of using hard coded values
    a, b = 240, 46
    gcd, s, t = eea(a, b)
    assert gcd == math.gcd(a, b)
    assert a * s + b * t == gcd
