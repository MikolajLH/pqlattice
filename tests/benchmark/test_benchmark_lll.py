import pqlattice as pq


def test_lll_scaling(benchmark, hard_lattice):
    benchmark.pedantic(pq.lattice.lll, args=(hard_lattice,), rounds=1, iterations=1, warmup_rounds=0)
