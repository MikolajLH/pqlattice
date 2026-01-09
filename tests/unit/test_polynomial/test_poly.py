from typing import NamedTuple

import pytest
from hypothesis import given
from tests import strategies as st

from pqlattice.polynomial._poly import deg, is_zero_poly, make_poly
from pqlattice.typing import Vector


class TestIsZeroPoly:
    class Case(NamedTuple):
        # input:
        p: Vector
        # output:
        res: bool

    KNOWN_CASES = [
        Case(make_poly([0, 0, 0, 0, 1]), False),
        Case(make_poly([1, 0, 0, 0, 0]), False),
        Case(make_poly([0]), True),
        Case(make_poly([0, 0, 0, 0, 0, 0, 0, 0, 0]), True),
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_is_zero_poly_known_cases(self, case: Case):
        assert is_zero_poly(case.p) == case.res

    @given(p=st.polynomials())
    def test_is_zero_poly_properties(self, p: Vector):
        assert not is_zero_poly(p)

    # INVALID_CASES = [make_poly([])]

    # @pytest.mark.parametrize("p", INVALID_CASES)
    # def test_is_zero_poly_invalid_cases(self, p: Vector):
    #     with pytest.raises(ValueError):
    #         is_zero_poly(p)


class TestDeg:
    class Case(NamedTuple):
        # input:
        p: Vector
        # output:
        degree: int

    KNOWN_CASES = [
        Case(make_poly([1]), 0),
        Case(make_poly([2]), 0),
        Case(make_poly([3, 4]), 1),
        Case(make_poly([0, 1]), 1),
    ]

    @pytest.mark.parametrize("case", KNOWN_CASES)
    def test_deg_known_cases(self, case: Case):
        assert deg(case.p) == case.degree

    @given(p=st.polynomials())
    def test_deg_properties(self, p: Vector):
        assert deg(p) == len(p) - 1
