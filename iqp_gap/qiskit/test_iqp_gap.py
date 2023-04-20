"""IQP circuits for estimating the gap of degree-3 polynomials"""
"""Reference: https://arxiv.org/pdf/1504.07999.pdf """

import itertools
import qiskit
import qiskit.providers.aer
import sympy
import iqp_gap
import iqp_gap.qiskit
import numpy as np
import hypothesis


@hypothesis.strategies.composite
def poly_deg_3_st(draw):
    N = draw(hypothesis.strategies.integers(min_value=1, max_value=8))
    _, *x = sympy.polys.rings.ring(",".join([f"x{i}" for i in range(N)]), sympy.GF(2))
    return draw(
        hypothesis.strategies.lists(
            hypothesis.strategies.lists(
                hypothesis.strategies.sampled_from(x), min_size=1, max_size=3
            )
            .map(sympy.prod)
            .filter(lambda n: n != 1),
            min_size=1,
        ).map(sum)
    )


@hypothesis.given(poly_deg_3_st())
@hypothesis.settings(deadline=400)
def test_gap(f):
    N = f.parent().ngens
    qr = qiskit.QuantumRegister(N)
    qc = qiskit.QuantumCircuit(qr)
    qc.append(iqp_gap.qiskit.gap(f), qr)
    qc.save_density_matrix()
    dm_backend = qiskit.providers.aer.Aer.get_backend("aer_simulator")
    qc = qiskit.transpile(qc, dm_backend)
    dm = dm_backend.run(qc).result().data().get("density_matrix")
    result = np.array(dm)[0, 0]
    analytical_result = (iqp_gap.gap(f) / 2**N) ** 2
    np.testing.assert_almost_equal(result, analytical_result)
