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


@hypothesis.given(iqp_gap.poly_st(3))
@hypothesis.settings(deadline=400)
def test_gap(f):
    N = f.parent().ngens
    qr = qiskit.QuantumRegister(N)
    qc = qiskit.QuantumCircuit(qr)
    qc.append(iqp_gap.qiskit.gap(f), qr)
    qc.save_statevector()
    simulator = qiskit.providers.aer.Aer.get_backend("aer_simulator")
    qc = qiskit.transpile(qc, simulator)
    sv = simulator.run(qc).result().data().get("statevector")
    result = sv.probabilities()[0]
    analytical_result = (iqp_gap.gap(f) / 2**N) ** 2
    np.testing.assert_almost_equal(result, analytical_result)
