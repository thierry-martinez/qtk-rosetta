"""IQP circuits for estimating the gap of degree-3 polynomials"""
"""Reference: https://arxiv.org/pdf/1504.07999.pdf """

import itertools
import qiskit
import sympy
import iqp_gap
import iqp_gap.qiskit
import numpy as np
import hypothesis


@hypothesis.given(iqp_gap.poly_st())
@hypothesis.settings(deadline=400)
def test_gap(poly):
    N = poly.parent().ngens
    result = iqp_gap.qiskit.evaluate_gap(poly)
    analytical_result = (iqp_gap.gap(poly) / 2**N) ** 2
    np.testing.assert_almost_equal(result, analytical_result)
