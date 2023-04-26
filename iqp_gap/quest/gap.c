#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include "gap.h"

struct polynomial *alloc_polynomial(size_t length, size_t variables,
                                    struct monomial *monomials)
{
  size_t sz =
    sizeof(struct polynomial) + sizeof(struct monomial) * (length - 1);
  struct polynomial *result = malloc(sz);
  result->length = length;
  result->variables = variables;
  if (monomials) {
    memcpy(result->monomials, monomials, sizeof(struct monomial) * length);
  }
  return result;
}

int
sum_gap_rec(struct polynomial *polynomial,
            bool valuation[polynomial->variables], int k)
{
  if (k < polynomial->variables) {
    valuation[k] = 0;
    int gap_for_0 = sum_gap_rec(polynomial, valuation, k + 1);
    valuation[k] = 1;
    int gap_for_1 = sum_gap_rec(polynomial, valuation, k + 1);
    return gap_for_0 + gap_for_1;
  }
  else {
    bool sum = 0;
    size_t i;
    for (i = 0; i < polynomial->length; i++) {
      struct monomial monomial = polynomial->monomials[i];
      bool value = 1;
      short d;
      for (d = 0; d < monomial.degree; d++) {
        value = value && valuation[monomial.x[d]];
      }
      sum = sum ^ value;
    }
    if (sum) {
      return -1;
    }
    else {
      return 1;
    }
  }
}

int gap(struct polynomial *polynomial)
{
  bool valuation[polynomial->variables];
  return sum_gap_rec(polynomial, valuation, 0);
}

struct monomial random_monomial(size_t variables, size_t max_degree)
{
  struct monomial result;
  result.degree = 1 + rand() % max_degree;
  if (result.degree > variables) {
    result.degree = variables;
  }
  bool taken[variables];
  size_t i;
  for (i = 0; i < variables; i++) {
    taken[i] = false;
  }
  short d;
  for (d = 0; d < result.degree; d++) {
    size_t rank = rand() % (variables - d);
    size_t p;
    size_t index = 0;
    while (taken[index]) {
      index++;
    }
    for (p = 0; p < rank; p++) {
      index++;
      while (taken[index]) {
        index++;
      }
    }
    taken[index] = true;
    result.x[d] = index;
  }
  return result;
}

struct polynomial *random_polynomial(size_t max_length, size_t max_variables,
                                     size_t max_degree)
{
  size_t length = rand() % max_length;
  size_t variables = 1 + rand() % max_variables;
  size_t i;
  struct polynomial *result = alloc_polynomial(length, variables, NULL);
  for (i = 0; i < length; i++) {
    result->monomials[i] = random_monomial(variables, max_degree);
  }
  return result;
}

void output_monomial(FILE * stream, struct monomial monomial)
{
  int i;
  fprintf(stream, "x%d", monomial.x[0]);
  for (i = 1; i < monomial.degree; i++) {
    fprintf(stream, " * x%d", monomial.x[i]);
  }
}

void output_polynomial(FILE * stream, struct polynomial *polynomial)
{
  if (polynomial->length == 0) {
    fprintf(stream, "0");
    return;
  }
  output_monomial(stream, polynomial->monomials[0]);
  int i;
  for (i = 1; i < polynomial->length; i++) {
    fprintf(stream, " + ");
    output_monomial(stream, polynomial->monomials[i]);
  }
}
