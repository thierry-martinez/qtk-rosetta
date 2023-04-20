"""
Classical implementation in Python of the gap function for a
polynomial.
"""

import itertools


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
