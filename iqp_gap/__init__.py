"""
IQP circuits for estimating the gap of degree-3 polynomials

Reference: https://arxiv.org/pdf/1504.07999.pdf
    Average-case complexity versus approximate simulation of commuting
    quantum computations
    Michael J. Bremner,1 Ashley Montanaro,2 and Dan J. Shepherd
"""

from .gap import gap


def polynomial_of_monomial(monomial, polyring):
    """
    Return a polynomial from the coefficient tuple `monomial`.

    >>> import sympy
    >>> P, x, y, z = sympy.polys.rings.ring('x, y, z', sympy.polys.domains.RR)
    >>> polynomial_of_monomial((1, 1, 0), P)
    x*y
    """
    poly = polyring.zero
    poly[monomial] = 1
    return poly
