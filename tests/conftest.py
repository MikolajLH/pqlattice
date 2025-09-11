from multiprocessing.managers import BaseManager
from typing import cast

import pytest
from tests import oracle
from tests.sage_interface import DEFAULT_AUTHKEY, DEFAULT_PORT, SageEngineInterface


class SageManager(BaseManager):
    pass


SageManager.register("get_engine")


def pytest_addoption(parser):
    parser.addoption("--sage", action="store_true", default=False, help="Enable tests that use SageMath")


@pytest.fixture(scope="session", autouse=True)
def initialize_sage_oracle(request):
    should_run_sage = request.config.getoption("--sage")

    if should_run_sage:
        manager = SageManager(address=("localhost", DEFAULT_PORT), authkey=DEFAULT_AUTHKEY)
        try:
            manager.connect()
            proxy = manager.get_engine()
            oracle.Sage._engine = cast(SageEngineInterface, proxy)
        except ConnectionRefusedError:
            pytest.fail(f"Could not connect to Sage server on port {DEFAULT_PORT}")

    yield
    oracle.Sage._engine = None
