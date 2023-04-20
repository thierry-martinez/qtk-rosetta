"""
IQP circuits for estimating the gap of degree-3 polynomials with Qutip
(CCZ gates are not supported yet in Qutip)

Reference: https://arxiv.org/pdf/1504.07999.pdf
    Average-case complexity versus approximate simulation of commuting
    quantum computations
    Michael J. Bremner,1 Ashley Montanaro,2 and Dan J. Shepherd
"""

import qutip


def polynomial_of_monomial(monomial, polyring):
    """
    Return a polynomial from the coefficient tuple `monomial`.

    (The following examples can be checked with `pytest --doctest-modules`.)

    >>> import sympy
    >>> P, x, y, z = sympy.polys.rings.ring('x, y, z', sympy.polys.domains.RR)
    >>> polynomial_of_monomial((1, 1, 0), P)
    x*y
    """
    poly = polyring.zero
    poly[monomial] = 1
    return poly


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
    >>> initial_density_matrix = initial_state * initial_state.dag()
    >>> np.testing.assert_almost_equal( \
            qc.run(initial_density_matrix)[0][0][0], \
            (8 / 2 ** 4) ** 2 \
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
                qc.add_gate("CCZ", targets=[xi], controls=[xj, xk])
            case _:
                raise Exception(
                    f"""Unsupported monomial: {
                        polynomial_of_monomial(monom, polyring)
                    }"""
                )
    for i in range(N):
        qc.add_gate("SNOT", targets=[i])
    return qc
