import pytest
from hypothesis import settings
from sagemath import sage_client
from tests import oracle

settings.register_profile("default", deadline=None)
settings.load_profile("default")


def pytest_addoption(parser):
    parser.addoption("--sage", action="store_true", default=False, help="Enable tests that use SageMath")
    parser.addoption("--fast-backend", action="store_true", default=False, help="Use fast backend for algorithms")


@pytest.fixture(scope="session", autouse=True)
def set_fast_backend(request):
    should_set_fast_backend = request.config.getoption("--fast-backend")
    if should_set_fast_backend:
        import pqlattice as pq

        try:
            pq.settings.set_backend("fast")
        except RuntimeError:
            pytest.fail("Coulnd't set fast backend")

    yield


@pytest.fixture(scope="session", autouse=True)
def initialize_sage_oracle(request):
    should_run_sage = request.config.getoption("--sage")

    if should_run_sage:
        try:
            oracle.Sage._engine = sage_client.connect()
        except ConnectionRefusedError:
            pytest.fail("Could not connect to Sage server")

    yield
    oracle.Sage._engine = None
