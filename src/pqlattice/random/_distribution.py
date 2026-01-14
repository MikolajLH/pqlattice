import math
import random
from abc import ABC, abstractmethod
from typing import Any, override

from .._utils import as_integer
from ..typing import Matrix, Vector


class Distribution(ABC):
    def __init__(self, seed: int | None = None):
        self._pyrng = random.Random(seed)

    def set_seed(self, seed: int | None) -> None:
        if seed is not None:
            self._pyrng.seed(seed)

    @abstractmethod
    def sample_int(self, seed: int | None) -> int: ...

    @abstractmethod
    def sample_vector(self, n: int, seed: int | None = None) -> Vector: ...

    @abstractmethod
    def sample_matrix(self, rows: int, cols: int | None = None, seed: int | None = None) -> Matrix: ...

    @abstractmethod
    def set_params(self, *args: Any) -> None: ...

    @abstractmethod
    def get_params(self) -> dict[str, Any]: ...


class Uniform(Distribution):
    def __init__(self, range_beg: int, range_end: int, seed: int | None = None):
        """
        Creates a uniform sampler from range [range_beg; range_end].

        Parameters
        ----------
        range_beg : int
            begin of sampling range. Inclusive
        range_end : int
            end of sampling range. Inclusive
        seed : int | None, optional
            seed for random number generator, by default None
        """
        super().__init__(seed)
        self._range_beg = range_beg
        self._range_end = range_end

    @override
    def sample_int(self, seed: int | None = None) -> int:
        """
        Get uniform random int from range `[self.beg_range, self.end_range]`

        Parameters
        ----------
        seed : int | None, optional
            set the new seed, if None does nothing, by default None

        Returns
        -------
        int
            random integer from range [self.beg_range, self.end_range]
        """
        self.set_seed(seed)
        return self._pyrng.randint(self._range_beg, self._range_end)

    @override
    def sample_vector(self, n: int, seed: int | None = None) -> Vector:
        """
        Get a vector of random uniform ints.
        Each element of the vector is sampled from range `[self.beg_range, self.end_range]`.

        Parameters
        ----------
        n : int
            dimension of the vector
        seed : int | None, optional
            set the new seed, if None does nothing, by default None

        Returns
        -------
        Vector
            vector `v` with shape `(n,)` and random elements from range `[self.beg_range, self.end_range]`
        """
        self.set_seed(seed)
        return as_integer([self.sample_int() for _ in range(n)])

    @override
    def sample_matrix(self, rows: int, cols: int | None = None, seed: int | None = None) -> Matrix:
        """
        Get a matrix of random uniform ints.
        Each element of the matrix is sampled from range `[self.beg_range, self.end_range]`.

        Parameters
        ----------
        rows : int
            number of rows
        cols : int | None, optional
            number of cols, if None equal to number of rows , by default None
        seed : int | None, optional
             set the new seed, if None does nothing, by default None

        Returns
        -------
        Matrix
            matrix `m` with shape `(rows, cols)` and random elements from range `[self.beg_range, self.end_range]`
        """
        self.set_seed(seed)
        if cols is None:
            cols = rows
        return as_integer([[self.sample_int() for _ in range(cols)] for _ in range(rows)])

    @override
    def set_params(self, range_beg: int | None = None, range_end: int | None = None) -> None:  # type: ignore
        """
        Set the parameters of the distribution

        Parameters
        ----------
        range_beg : int | None, optional
            if None does nothing, by default None
        range_end : int | None, optional
            if None does nothing, by default None
        """
        if range_beg is None:
            range_beg = self._range_beg
        if range_end is None:
            range_end = self._range_end

        self._range_beg = range_beg
        self._range_end = range_end

    @override
    def get_params(self) -> dict[str, int]:
        """
        returns dictionary of parameters of the distribution

        Returns
        -------
        dict[str, int]
            dict `d = {"range_beg": self._range_beg, "range_end": self._range_end}`
        """
        return {"range_beg": self._range_beg, "range_end": self._range_end}


class DiscreteGaussian(Distribution):
    def __init__(self, sigma: float, center: int | float = 0, tail_cut: float = 6.0, seed: int | None = None):
        """
        Creates DiscreteGaussian sampler that uses rejection sampling method.
        Samples `x` are accepted with probability `exp(-((x - center) ** 2) / (2 * sigma ** 2)).

        Parameters
        ----------
        sigma : float
            standard deviation of the distribution
        center : int | float, optional
            mean of the distribution, by default 0
        tail_cut : float, optional
            samples outside the range `[center - sigma * tail_cut, center + sigma * tail_cut]` are considered to have probability zero, by default 6.0
        seed : int | None, optional
            seed for random number generator, by default None
        """
        super().__init__(seed)
        self.center = center
        self.sigma = sigma
        self.tail_cut = tail_cut

        self._table: dict[int, float] = {}
        self._recompute_table()

    def _recompute_table(self) -> None:
        self.bound = int(math.ceil(self.tail_cut * self.sigma))
        self._table: dict[int, float] = {}
        for x in range(-self.bound, self.bound + 1):
            self._table[x] = math.exp(-(x**2) / (2 * self.sigma**2))

    @override
    def sample_int(self, seed: int | None = None) -> int:
        """
        Get random int according to the gaussian probability.

        Parameters
        ----------
        seed : int | None, optional
            set the new seed, if None does nothing, by default None

        Returns
        -------
        int
            random integer sampled from discrete gaussian distribution
        """
        self.set_seed(seed)

        if isinstance(self.center, int):
            return self._sample_centered_fast() + self.center

        return self._sample_dynamic_rejection(self.center)

    @override
    def sample_vector(self, n: int, seed: int | None = None) -> Vector:
        """
        Get a vector of integers sampled from discrete gaussian distribution.

        Parameters
        ----------
        n : int
             dimension of the vector
        seed : int | None, optional
            set the new seed, if None does nothing, by default None

        Returns
        -------
        Vector
            vector `v` with shape `(n,)` and random elements from discrete gaussian distribution.
        """
        self.set_seed(seed)
        return as_integer([self.sample_int() for _ in range(n)])

    @override
    def sample_matrix(self, rows: int, cols: int | None = None, seed: int | None = None) -> Matrix:
        """
        Get a matrix of integers sampled from discrete gaussian distribution.

        Parameters
        ----------
        rows : int
            number of rows
        cols : int | None, optional
            number of cols, if None equal to number of rows , by default None
        seed : int | None, optional
            set the new seed, if None does nothing, by default None

        Returns
        -------
        Matrix
            matrix `m` with shape `(rows, cols)` and random elements from discrete gaussian distribution.
        """
        self.set_seed(seed)
        if cols is None:
            cols = rows
        return as_integer([[self.sample_int() for _ in range(cols)] for _ in range(rows)])

    @override
    def set_params(self, sigma: float | None = None, center: float | int | None = None, tail_cut: float | None = None) -> None:  # type: ignore
        """
        Set the parameters of the distribution

        Parameters
        ----------
        sigma : float | None, optional
            if None does nothing, by default None
        center : float | int | None, optional
            if None does nothing, by default None
        tail_cut : float | None, optional
            if None does nothing, by default None
        """
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
        """
        returns dictionary of parameters of the distribution

        Returns
        -------
        dict[str, float]
            dict `d = {"sigma": self.sigma, "center": self.center, "tail_cut": self.tail_cut, "bound": self.bound}`
        """
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
