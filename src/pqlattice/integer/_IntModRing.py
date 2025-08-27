from . import mod, modinv, modpow


class IntModRing:
    def __init__(self, modulus: int):
        self._modulus = abs(modulus)

    @property
    def q(self):
        return self._modulus

    def mod(self, a: int):
        return mod(a, self.q)

    def pow(self, a: int, r: int):
        return self.mod(modpow(a, r, self.q))

    def inv(self, a: int):
        return self.mod(modinv(a, self.q))

    def add(self, a: int, b: int):
        return self.mod(a + b)

    def mul(self, a: int, b: int):
        return self.mod(a * b)

    def div(self, a: int, b: int):
        return self.mul(a, self.inv(b))

    def sub(self, a: int, b: int):
        return self.mod(a - b)

    def pmod(self, a: int):
        return mod(a, self.q) - (self.q // 2)

    def cmodl(self, a: int):
        return mod(a, self.q) - (self.q // 2) + 1
