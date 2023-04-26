#include "circuit.h"

void iqp_gap(Qureg qureg, struct polynomial *polynomial)
{
  size_t i;
  for (i = 0; i < polynomial->variables; i++) {
    hadamard(qureg, i);
  }
  for (i = 0; i < polynomial->length; i++) {
    struct monomial monomial = polynomial->monomials[i];
    switch (monomial.degree) {
      case 1:
        pauliZ(qureg, monomial.x[0]);
        break;
      case 2:
        controlledPhaseFlip(qureg, monomial.x[0], monomial.x[1]);
        break;
      case 3:
        multiControlledPhaseFlip(qureg, monomial.x, 3);
        break;
      default:
        assert(0);              /* Unsupported monomial */
    }
  }
  for (i = 0; i < polynomial->variables; i++) {
    hadamard(qureg, i);
  }
}

qreal evaluate_gap(struct polynomial *polynomial, QuESTEnv env)
{
  Qureg qureg = createQureg(polynomial->variables, env);
  iqp_gap(qureg, polynomial);
  qreal result = getProbAmp(qureg, 0);
  destroyQureg(qureg, env);
  return result;
}
