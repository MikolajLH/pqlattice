import contextlib
from collections.abc import Generator
from typing import Literal

from ._backends._fast import FastBackend
from ._backends._native import NativeBackend
from ._backends._protocol import BackendInterface

BackendName = Literal["native", "fast"]


class _Settings:
    def __init__(self) -> None:
        self._active_backend_name: BackendName = "native"
        self._native_backend = NativeBackend()
        self._fast_backend: FastBackend | None = None

    @property
    def backend_name(self) -> BackendName:
        return self._active_backend_name

    @property
    def backend(self) -> BackendInterface:
        if self.backend_name == "native":
            return self._native_backend
        elif self.backend_name == "fast":
            if self._fast_backend is None:
                self._fast_backend = FastBackend()
            return self._fast_backend

        raise RuntimeError(f"No backend {self.backend_name}")

    def set_backend(self, name: BackendName) -> None:
        self._active_backend_name = name


_config = _Settings()


def get_backend_name() -> BackendName:
    return _config.backend_name


def get_backend() -> BackendInterface:
    return _config.backend


def set_backend(name: BackendName) -> None:
    _config.set_backend(name)


@contextlib.contextmanager
def backend(name: BackendName) -> Generator[None, None, None]:
    """
    Context manager to temporarily switch the backend.

    Usage:
        with pq.settings.backend("fpylll"):
            pq.lattice.lll(B)
    """
    previous = _config.backend_name
    try:
        set_backend(name)
        yield
    finally:
        set_backend(previous)
