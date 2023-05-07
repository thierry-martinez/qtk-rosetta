#ifndef _GAP_H_
#define _GAP_H_

#include <stddef.h>
#include <stdio.h>

struct monomial {
  unsigned short degree;
  int x[3];
};

struct polynomial {
  size_t length;
  size_t variables;
  struct monomial monomials[1];
};

struct polynomial *alloc_polynomial(size_t length, size_t variables,
                                    struct monomial *monomials);

int gap(struct polynomial *polynomial);

struct monomial random_monomial(size_t variables, size_t max_degree);

struct polynomial *random_polynomial(size_t max_length, size_t max_variables,
                                     size_t max_degree);

void output_monomial(FILE * stream, struct monomial monomial);

void output_polynomial(FILE * stream, struct polynomial *polynomial);

#endif
