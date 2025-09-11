from typing import Protocol

DEFAULT_PORT = 5050
DEFAULT_AUTHKEY = b"sage"


class SageEngineInterface(Protocol):
    def ok(self) -> bool: ...

    def hello_world(self) -> str: ...
