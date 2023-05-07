#ifndef _IQP_GAP_H_
#define _IQP_GAP_H_

#include <stddef.h>
#include <assert.h>
#include <QuEST.h>

#include "gap.h"

void iqp_gap(Qureg qureg, struct polynomial *polynomial);

qreal evaluate_gap(struct polynomial *polynomial, QuESTEnv env);

#endif
