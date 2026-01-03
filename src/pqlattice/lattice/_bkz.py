from .._utils import as_integer, as_rational
from ..typing import Matrix, SquareMatrix, Vector, validate_aliases
from ._gso import gso
from ._lll import lll
from ._svp import schnorr_euchner_svp


@validate_aliases
def update_block(lattice_basis: SquareMatrix, new_vector: Vector, start_index: int, block_size: int) -> SquareMatrix:
    B = as_integer(lattice_basis)
    local_basis = as_integer([new_vector] + B[start_index : start_index + block_size].tolist())
    reduced_local = lll(local_basis)

    zero_vec = reduced_local[0]
    if any(s != 0 for s in zero_vec):
        raise ValueError("block update failed")

    cleaned_basis = as_integer(reduced_local[1:])

    for i in range(block_size):
        B[start_index + i] = cleaned_basis[i]

    return B


@validate_aliases
def bkz(lattice_basis: SquareMatrix, block_size: int = 10) -> SquareMatrix:
    n, m = lattice_basis.shape

    B = lll(lattice_basis)

    is_changed = True
    while is_changed:
        is_changed = False
        for k in range(n - 1):
            h = min(block_size, n - k)
            local_basis: Matrix = B[k : k + h]

            B_star, U = gso(local_basis)
            B_norms2 = as_rational([sum(x * x for x in v) for v in B_star])
            mu = U.T
            coeffs = schnorr_euchner_svp(mu, B_norms2)

            is_trivial = True
            if abs(coeffs[0]) == 1:
                is_trivial = all(c == 0 for c in coeffs[1:])
            elif coeffs[0] == 0:
                is_trivial = False
            else:
                is_trivial = False

            if is_trivial:
                continue

            new_vector = as_integer([0] * m)
            for i in range(h):
                if coeffs[i] == 0:
                    continue
                for d in range(m):
                    new_vector[d] += coeffs[i] * local_basis[i][d]

                B = update_block(B, new_vector, k, h)
                is_changed = True
    return B
