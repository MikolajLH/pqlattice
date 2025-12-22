from ..typing import Matrix, SquareMatrix, Vector, validate_aliases


@validate_aliases
def q_ary_lattice_basis(A: Matrix, modulus: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def dual_q_ary_lattice_basis(A: Matrix, modulus: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def bai_galbraith(A: Matrix, b: Vector, q: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def kannan(lattice_basis: SquareMatrix, target_vector: Vector, M: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def subset_sum(sequence: Vector, S: int) -> SquareMatrix:
    raise NotImplementedError()


@validate_aliases
def ntru() -> SquareMatrix:
    raise NotImplementedError()
