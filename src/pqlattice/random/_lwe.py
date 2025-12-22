from typing import overload

from ..typing import Matrix, Vector


class LWE:
    def __init__(self):
        raise NotImplementedError()

    @overload
    def __call__(self, n: int) -> Matrix: ...

    @overload
    def __call__(self, n: None) -> Vector: ...

    def __call__(self, n: int | None = None) -> Matrix | Vector:
        raise NotImplementedError()
