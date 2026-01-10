import pqlattice as pq


def test_bkz_scaling(benchmark, hard_lattice):
    benchmark.pedantic(pq.lattice.bkz, args=(hard_lattice,), rounds=1, iterations=1, warmup_rounds=0)
