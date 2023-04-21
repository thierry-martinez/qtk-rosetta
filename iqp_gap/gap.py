"""
Classical implementation in Python of the gap function for a
polynomial.
"""

import itertools
import hypothesis
import sympy


def gap(poly):
    """
    Return the gap of the polynomial `poly`,
    i.e. #{ v | poly(v) = 0 } - #{ v | poly(v) = 1 },
    with a classical implementation in Python.

    >>> import sympy
    >>> _, x, y, z = sympy.polys.rings.ring('x, y, z', sympy.GF(2))
    >>> gap(x * y * z + x * z + y * z + x)
    2
    """
    return sum(
        (-1) ** int(poly(*valuation))
        for valuation in itertools.product((0, 1), repeat=poly.parent().ngens)
    )


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


@hypothesis.strategies.composite
def poly_st(draw, max_degree):
    """
    Hypothesis strategy to generate polynomials
    """
    N = draw(hypothesis.strategies.integers(min_value=1, max_value=8))
    _, *x = sympy.polys.rings.ring(",".join([f"x{i}" for i in range(N)]), sympy.GF(2))
    return draw(
        hypothesis.strategies.lists(
            hypothesis.strategies.lists(
                hypothesis.strategies.sampled_from(x), min_size=1, max_size=max_degree
            )
            .map(sympy.prod)
            .filter(lambda n: n != 1),
            min_size=1,
        ).map(sum)
    )
