import random
from abc import ABC, abstractmethod
from typing import override

from .._utils import as_integer
from ..typing import Matrix, Vector


class Distribution(ABC):
    @abstractmethod
    def randint(self, seed: int | None) -> int: ...

    @abstractmethod
    def randvector(self, n: int, seed: int | None) -> Vector: ...

    @abstractmethod
    def randmatrix(self, m: int, n: int | None, seed: int | None) -> Matrix: ...


class Uniform(Distribution):
    def __init__(self, range_beg: int, range_end: int, seed: int | None = None):
        self._pyrng = random.Random(seed)
        self._range_beg = range_beg
        self._range_end = range_end

    @override
    def randint(self, seed: int | None = None) -> int:
        self.set_seed(seed)
        return self._pyrng.randint(self._range_beg, self._range_end + 1)

    @override
    def randvector(self, n: int, seed: int | None = None) -> Vector:
        self.set_seed(seed)
        return as_integer([self.randint() for _ in range(n)])

    @override
    def randmatrix(self, m: int, n: int | None = None, seed: int | None = None) -> Matrix:
        self.set_seed(seed)
        if n is None:
            n = m
        return as_integer([[self.randint() for _ in range(m)] for _ in range(n)])

    def set_seed(self, seed: int | None) -> None:
        if seed is not None:
            self._pyrng.seed(seed)

    def set_range(self, range_beg: int | None = None, range_end: int | None = None) -> None:
        if range_beg is None:
            range_beg = self._range_beg
        if range_end is None:
            range_end = self._range_end

        self._range_beg = range_beg
        self._range_end = range_end

    def get_range(self) -> tuple[int, int]:
        return (self._range_beg, self._range_end)


class DiscreteGaussian(Distribution):
    pass


class RoundedGaussian(Distribution):
    pass  # ?
