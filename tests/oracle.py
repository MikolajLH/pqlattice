# pyright: reportAttributeAccessIssue=false
import gmpy2


def is_prime(n: int) -> bool:
    return gmpy2.is_prime(n)  # type: ignore


def next_prime(n: int) -> int:
    return int(gmpy2.next_prime(n))  # type: ignore
