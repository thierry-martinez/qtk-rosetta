"""
IQP circuits for estimating the gap of degree-3 polynomials with Qutip
(CCZ gates are not supported yet in Qutip)

Reference: https://arxiv.org/pdf/1504.07999.pdf
    Average-case complexity versus approximate simulation of commuting
    quantum computations
    Michael J. Bremner,1 Ashley Montanaro,2 and Dan J. Shepherd
"""

import iqp_gap
import numpy as np
import qutip
import sympy


def gap(poly):
    """
    IQP circuits for estimating the gap of degree-3 polynomials
    (CCZ gates are not supported yet in Qutip)

    Reference: https://arxiv.org/pdf/1504.07999.pdf

    >>> import sympy
    >>> import numpy as np
    >>> import qutip
    >>> _, x, y, z, t = sympy.polys.rings.ring('x, y, z, t', sympy.GF(2))
    >>> qc = gap(x * y + x * z + y * z + x)
    >>> initial_state = qutip.tensor(*(qutip.basis(2, 0) for _ in range(4)))
    >>> np.testing.assert_almost_equal( \
            np.abs(qc.run(initial_state)[0][0]), \
            8 / 2 ** 4 \
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
    qc = qutip.qip.circuit.QubitCircuit(N)
    for i in range(N):
        qc.add_gate("SNOT", targets=[i])
    for monom in poly.itermonoms():
        variables = [i for (i, n) in enumerate(monom) if n]
        match variables:
            case [xi]:
                qc.add_gate("Z", targets=[xi])
            case [xi, xj]:
                qc.add_gate("CZ", targets=[xi], controls=[xj])
            case [xi, xj, xk]:
                # CCZ gate is not provided by qutip yet
                qc.add_gate("SNOT", targets=[xi])
                qc.add_gate("TOFFOLI", targets=[xi], controls=[xj, xk])
                qc.add_gate("SNOT", targets=[xi])
            case _:
                raise Exception(
                    f"""Unsupported monomial: {
                        iqp_gap.polynomial_of_monomial(monom, polyring)
                    }"""
                )
    for i in range(N):
        qc.add_gate("SNOT", targets=[i])
    return qc


def evaluate_gap(poly):
    """
    Estimate the gap of degree-3 polynomials using IQP circuits
    """
    N = poly.parent().ngens
    qc = iqp_gap.qutip.gap(poly)
    initial_state = qutip.tensor(*(qutip.basis(2, 0) for _ in range(N)))
    result_state = qc.run(initial_state)
    result_complex = result_state[0][0][0]
    return np.abs(result_complex) ** 2
