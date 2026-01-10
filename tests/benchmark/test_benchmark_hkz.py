import pqlattice as pq


def test_hkz_scaling(benchmark, hard_lattice):
    benchmark.pedantic(pq.lattice.hkz, args=(hard_lattice,), rounds=1, iterations=1, warmup_rounds=0)
