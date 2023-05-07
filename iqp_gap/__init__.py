"""
IQP circuits for estimating the gap of degree-3 polynomials

Reference: https://arxiv.org/pdf/1504.07999.pdf
    Average-case complexity versus approximate simulation of commuting
    quantum computations
    Michael J. Bremner,1 Ashley Montanaro,2 and Dan J. Shepherd
"""

from .gap import gap, polynomial_of_monomial, poly_st
