import math
import random

from .._utils import as_integer
from ..typing import Matrix, Vector


class Uniform:
    def __init__(self, range_beg: int, range_end: int, seed: int | None = None):
        self._pyrng = random.Random(seed)
        self._range_beg = range_beg
        self._range_end = range_end

    def sample_int(self, seed: int | None = None) -> int:
        self.set_seed(seed)
        return self._pyrng.randint(self._range_beg, self._range_end)

    def sample_vector(self, n: int, seed: int | None = None) -> Vector:
        self.set_seed(seed)
        return as_integer([self.sample_int() for _ in range(n)])

    def sample_matrix(self, m: int, n: int | None = None, seed: int | None = None) -> Matrix:
        self.set_seed(seed)
        if n is None:
            n = m
        return as_integer([[self.sample_int() for _ in range(m)] for _ in range(n)])

    def set_seed(self, seed: int | None) -> None:
        if seed is not None:
            self._pyrng.seed(seed)

    def set_params(self, range_beg: int | None = None, range_end: int | None = None) -> None:
        if range_beg is None:
            range_beg = self._range_beg
        if range_end is None:
            range_end = self._range_end

        self._range_beg = range_beg
        self._range_end = range_end

    def get_params(self) -> dict[str, int]:
        return {"range_beg": self._range_beg, "range_end": self._range_end}


class DiscreteGaussian:
    def __init__(self, sigma: float, center: int | float = 0, tail_cut: float = 6.0, seed: int | None = None):
        self.center = center
        self.sigma = sigma
        self.tail_cut = tail_cut
        self._pyrng = random.Random(seed)

        self._table: dict[int, float] = {}
        self._recompute_table()

    def _recompute_table(self) -> None:
        self.bound = int(math.ceil(self.tail_cut * self.sigma))
        self._table: dict[int, float] = {}
        for x in range(-self.bound, self.bound + 1):
            self._table[x] = math.exp(-(x**2) / (2 * self.sigma**2))

    def set_seed(self, seed: int | None) -> None:
        if seed is not None:
            self._pyrng.seed(seed)

    def sample_int(self, seed: int | None = None) -> int:
        self.set_seed(seed)

        if isinstance(self.center, int):
            return self._sample_centered_fast() + self.center

        return self._sample_dynamic_rejection(self.center)

    def sample_vector(self, n: int, seed: int | None = None) -> Vector:
        self.set_seed(seed)
        return as_integer([self.sample_int() for _ in range(n)])

    def sample_matrix(self, rows: int, cols: int | None = None, seed: int | None = None) -> Matrix:
        self.set_seed(seed)
        if cols is None:
            cols = rows
        return as_integer([[self.sample_int() for _ in range(cols)] for _ in range(rows)])

    def set_params(self, sigma: float | None = None, center: float | int | None = None, tail_cut: float | None = None) -> None:
        if sigma is None:
            sigma = self.sigma
        if center is None:
            center = self.center
        if tail_cut is None:
            tail_cut = self.tail_cut

        self.sigma = sigma
        self.tail_cut = tail_cut
        self.center = center
        self._recompute_table()

    def get_params(self) -> dict[str, float]:
        return {"sigma": self.sigma, "center": self.center, "tail_cut": self.tail_cut, "bound": self.bound}

    def _sample_centered_fast(self) -> int:
        max_iters = 1000
        for _ in range(max_iters):
            x = random.randint(-self.bound, self.bound)
            prob = self._table.get(x, 0.0)
            if random.random() < prob:
                return x

        raise RuntimeError("Failed to generate sample")

    def _sample_dynamic_rejection(self, c: float) -> int:
        start = int(math.floor(c - self.bound))
        end = int(math.ceil(c + self.bound))

        max_iters = 1000
        for _ in range(max_iters):
            x = random.randint(start, end)
            dist_sq = (x - c) ** 2
            prob = math.exp(-dist_sq / (2 * self.sigma**2))

            if random.random() < prob:
                return x

        raise RuntimeError("Failed to generate sample")
