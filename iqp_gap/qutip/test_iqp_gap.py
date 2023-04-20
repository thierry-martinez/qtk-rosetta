"""IQP circuits for estimating the gap of degree-3 polynomials"""
"""Reference: https://arxiv.org/pdf/1504.07999.pdf """

import itertools
import qutip
import sympy
import iqp_gap
import iqp_gap.qutip
import numpy as np
import hypothesis

MAX_DEG = 2


@hypothesis.strategies.composite
def poly_st(draw):
    N = draw(hypothesis.strategies.integers(min_value=1, max_value=8))
    _, *x = sympy.polys.rings.ring(",".join([f"x{i}" for i in range(N)]), sympy.GF(2))
    return draw(
        hypothesis.strategies.lists(
            hypothesis.strategies.lists(
                hypothesis.strategies.sampled_from(x), min_size=1, max_size=MAX_DEG
            )
            .map(sympy.prod)
            .filter(lambda n: n != 1),
            min_size=1,
        ).map(sum)
    )


@hypothesis.given(poly_st())
@hypothesis.settings(deadline=400)
def test_gap(f):
    N = f.parent().ngens
    qc = iqp_gap.qutip.gap(f)
    initial_state = qutip.tensor(*(qutip.basis(2, 0) for _ in range(N)))
    initial_density_matrix = initial_state * initial_state.dag()
    result_density_matrix = qc.run(initial_density_matrix)
    result = result_density_matrix
    while True:
        try:
            result = result[0]
        except IndexError:
            break
    analytical_result = (iqp_gap.gap(f) / 2**N) ** 2
    np.testing.assert_almost_equal(result, analytical_result)
