from multiprocessing.managers import BaseManager
from typing import cast

from .sage_interface import DEFAULT_AUTHKEY, DEFAULT_PORT, SageEngineInterface


def connect(port: int = DEFAULT_PORT, authkey: bytes = DEFAULT_AUTHKEY) -> SageEngineInterface:
    class SageManager(BaseManager):
        pass

    SageManager.register("get_engine")
    manager = SageManager(address=("localhost", port), authkey=authkey)

    manager.connect()
    proxy = manager.get_engine()  # type: ignore
    print("Connected to Sage server")
    return cast(SageEngineInterface, proxy)
