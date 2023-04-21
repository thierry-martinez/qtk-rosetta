"""IQP circuits for estimating the gap of degree-3 polynomials"""
"""Reference: https://arxiv.org/pdf/1504.07999.pdf """

import itertools
import qutip
import sympy
import iqp_gap
import iqp_gap.qutip
import numpy as np
import hypothesis

# We set MAX_DEG to 2 because qutip does not support CCZ gates yet
MAX_DEG = 2


@hypothesis.given(iqp_gap.poly_st(MAX_DEG))
@hypothesis.settings(deadline=400)
def test_gap(f):
    N = f.parent().ngens
    qc = iqp_gap.qutip.gap(f)
    initial_state = qutip.tensor(*(qutip.basis(2, 0) for _ in range(N)))
    result_state = qc.run(initial_state)
    result = np.abs(result_state[0][0][0])
    analytical_result = np.abs(iqp_gap.gap(f) / 2**N)
    np.testing.assert_almost_equal(result, analytical_result)
