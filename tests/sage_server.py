from multiprocessing.managers import BaseManager
from typing import override

from sage_interface import DEFAULT_AUTHKEY, DEFAULT_PORT, SageEngineInterface

# from sage.all import Matrix, ZZ, QQ


class SageEngine(SageEngineInterface):
    @override
    def ok(self) -> bool:
        return True

    @override
    def hello_world(self) -> str:
        print("Hello in Server")
        return "Hello to Client"


_: SageEngineInterface = SageEngine()  # Check if all abstarct methods are implemented


class SageManager(BaseManager):
    pass


SageManager.register("get_engine", callable=lambda: SageEngine())


def main():
    manager = SageManager(address=("", DEFAULT_PORT), authkey=DEFAULT_AUTHKEY)
    print(f"Sage Server listening on {DEFAULT_PORT}...")
    manager.get_server().serve_forever()


if __name__ == "__main__":
    main()
