import json
import os
import tracemalloc

import pytest

import pqlattice as pq


def pytest_addoption(parser):
    parser.addoption("--max-dim", action="store", default=10, type=int, help="Maximum lattice dimension to benchmark")


def pytest_generate_tests(metafunc):
    if "dim_param" in metafunc.fixturenames:
        max_dim = metafunc.config.getoption("--max-dim")

        dims = list(range(5, max_dim + 1))

        metafunc.parametrize("dim_param", dims)


@pytest.fixture
def hard_lattice(request, dim_param):
    _ = request
    n = dim_param
    det_bound = min(2**15, 2**n)
    return pq.random.randlattice(n, det_upper_bound=det_bound)


memory_result = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    tracemalloc.start()

    yield

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak / 1024 / 1024

    memory_result[item.name] = peak_mb


def pytest_sessionfinish(session, exitstatus):
    if not memory_result:
        _ = session
        _ = exitstatus
        return

    output_file = "memory_raport.json"

    with open(output_file, "w") as f:
        json.dump(memory_result, f, indent=4)

    print(f"\n[MEMORY] Raport saved to {os.path.abspath(output_file)}")
