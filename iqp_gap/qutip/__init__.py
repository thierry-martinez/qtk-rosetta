"""
IQP circuits for estimating the gap of degree-3 polynomials with qutip

Reference: https://arxiv.org/pdf/1504.07999.pdf
    Average-case complexity versus approximate simulation of commuting
    quantum computations
    Michael J. Bremner,1 Ashley Montanaro,2 and Dan J. Shepherd
"""

from .circuit import gap, evaluate_gap
