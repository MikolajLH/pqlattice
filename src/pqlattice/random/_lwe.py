import numpy as np

from ..integer._modring import cmodl, mod
from ..typing import Matrix, Vector
from ._distribution import DiscreteGaussian, Uniform


class LWE:
    def __init__(self, n: int, q: int, sigma: float, secret_distribution: str, seed: int):
        """
        Creates LWE sampler with DiscreteGuassianDistribution centered at 0 as noise sampler

        Parameters
        ----------
        n : int
            length of secret vector
        q : int
            modulus
        sigma : float
            sigma value for DiscreteGaussianDistribution
        seed : int
            seed for random number generator
        """
        self.n = n
        self.q = q
        self.U = Uniform(0, q - 1, seed=seed)
        self.D = DiscreteGaussian(sigma, seed=seed)

        secret = self.U.sample_vector(n)
        if secret_distribution == "uniform":
            self._secret = secret
        elif secret_distribution == "binary":
            self._secret = mod(secret, 2)
        elif secret_distribution == "ternary":
            self._secret = cmodl(secret, 3)
        else:
            raise ValueError(f"Unknown distribution {secret_distribution}, expected uniform|binary|ternary")

    @property
    def secret(self) -> Vector:
        """
        Retrieve underlying secret

        Returns
        -------
        Vector
            s: n-vector
        """
        return self._secret

    def set_secret(self, secret: Vector) -> None:
        """
        Set the underlying secret

        Parameters
        ----------
        secret : Vector
            secret vector to set

        Raises
        ------
        ValueError
            when lenght of the provided vector is not correct with the parameter of the LWE sampler
        """
        if secret.shape[0] != self.n:
            raise ValueError(f"expected {self.n} dimension of secret, got {secret.shape[0]}")

        self._secret = secret

    def sample_matrix(self, m: int) -> tuple[Matrix, Vector]:
        """
        Generates a full matrix system (A, b) with 'm' samples.

        Parameters
        ----------
        m : int
            how many samples should the resulting matrix have

        Returns
        -------
        tuple[Matrix, Vector]:

            A (Matrix): m x n matrix (Uniform mod q)
            b (Vector): m-vector (As + e mod q)
        """
        A = self.U.sample_matrix(m, self.n)
        e = self.D.sample_vector(m)

        b = mod(A @ self.secret + e, self.q)

        return A, b

    def next_sample(self) -> tuple[Vector, int]:
        """
        Generates a single sample pair (a, b).

        Returns
        -------
        tuple[Vector, int]
            a (Vector): n-vector (Uniform mod q)
            b (int): as + e mod q
        """
        a = self.U.sample_vector(self.n)
        e = self.D.sample_int()

        _as: int = np.dot(a, self.secret)
        b = mod(_as + e, self.q)

        return a, b
