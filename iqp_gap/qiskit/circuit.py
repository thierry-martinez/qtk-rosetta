"""
IQP circuits for estimating the gap of degree-3 polynomials with Qiskit

Reference: https://arxiv.org/pdf/1504.07999.pdf
    Average-case complexity versus approximate simulation of commuting
    quantum computations
    Michael J. Bremner,1 Ashley Montanaro,2 and Dan J. Shepherd
"""

import qiskit
import iqp_gap
import qiskit.providers.aer


def gap(poly):
    """
    IQP circuits for estimating the gap of degree-3 polynomials

    Reference: https://arxiv.org/pdf/1504.07999.pdf

    >>> import sympy
    >>> import numpy as np
    >>> import qiskit.quantum_info
    >>> _, x, y, z, t = sympy.polys.rings.ring('x, y, z, t', sympy.GF(2))
    >>> qc = gap(x * y * z + x * z + y * z + x)
    >>> np.testing.assert_almost_equal( \
            qiskit.quantum_info.operators.Operator(qc).data[0][0], \
            4 / 2 ** 4 \
        )
    >>> gap(x + 1)
    Traceback (most recent call last):
      ...
    Exception: Unsupported monomial: 1
    >>> gap(x * y * z * t)
    Traceback (most recent call last):
      ...
    Exception: Unsupported monomial: x*y*z*t
    """
    polyring = poly.parent()
    N = polyring.ngens
    qc = qiskit.QuantumCircuit(N)
    for i in range(N):
        qc.h(i)
    for monom in poly.itermonoms():
        variables = [i for (i, n) in enumerate(monom) if n]
        match variables:
            case [xi]:
                qc.z(xi)
            case [xi, xj]:
                qc.cz(xi, xj)
            case [xi, xj, xk]:
                qc.ccz(xi, xj, xk)
            case _:
                raise Exception(
                    f"""Unsupported monomial: {
                        iqp_gap.polynomial_of_monomial(monom, polyring)
                    }"""
                )
    for i in range(N):
        qc.h(i)
    # return qiskit.quantum_info.operators.Operator(qc.to_gate(label="iqp"))
    return qc


def evaluate_gap(poly):
    """
    Estimate the gap of degree-3 polynomials using IQP circuits
    """
    N = poly.parent().ngens
    qr = qiskit.QuantumRegister(N)
    qc = qiskit.QuantumCircuit(qr)
    qc.append(iqp_gap.qiskit.gap(poly), qr)
    qc.save_statevector()
    simulator = qiskit.providers.aer.Aer.get_backend("aer_simulator")
    qc = qiskit.transpile(qc, simulator)
    sv = simulator.run(qc).result().data().get("statevector")
    return sv.probabilities()[0]
