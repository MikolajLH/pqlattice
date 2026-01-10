import os
from typing import NamedTuple

from hypothesis import Verbosity


class HypothesisProfile(NamedTuple):
    name: str
    max_examples: int
    slow_max_examples: int
    verbosity: Verbosity


PROFILE_DEFAULT = HypothesisProfile(name="default", max_examples=200, slow_max_examples=5, verbosity=Verbosity.verbose)

PROFILE_LONG = HypothesisProfile(name="long", max_examples=500, slow_max_examples=20, verbosity=Verbosity.verbose)

PROFILE_FAST = HypothesisProfile(name="fast", max_examples=20, slow_max_examples=1, verbosity=Verbosity.normal)


def get_profile() -> HypothesisProfile:
    name = os.getenv("HYPOTHESIS_PROFILE", "default")
    if name == "default":
        return PROFILE_DEFAULT
    elif name == "long":
        return PROFILE_LONG
    elif name == "fast":
        return PROFILE_FAST
    else:
        print(f"WARNING: unknown hypothesis profile {name}, defaulting to default profile")
        return PROFILE_DEFAULT
