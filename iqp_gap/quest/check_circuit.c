#include <assert.h>
#include <check.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <QuEST.h>

#include "gap.h"
#include "circuit.h"

START_TEST(test_gap)
{
  struct monomial x = { 1, { 0, 0, 0 } };
  {
    struct polynomial *p = alloc_polynomial(1, 1, &x);
    ck_assert_int_eq(gap(p), 0);
    free(p);
  }
  {
    struct monomial m[4] = { x, x, x, x };
    struct polynomial *p = alloc_polynomial(4, 1, m);
    ck_assert_int_eq(gap(p), 2);
    free(p);
  }
}

END_TEST START_TEST(test_iqp_gap)
{
  QuESTEnv env = createQuESTEnv();
  srand(time(NULL));
  int i;
  for (i = 0; i < 64; i++) {
    struct polynomial *polynomial = random_polynomial(16, 16, 3);
    qreal result = evaluate_gap(polynomial, env);
    double analytical_result =
      pow(((double) gap(polynomial)) / (1 << polynomial->variables), 2);
    ck_assert_float_eq_tol(result, analytical_result, 0.0001);
    free(polynomial);
  }
}

END_TEST Suite *iqp_gap_suite(void)
{
  Suite *s;
  TCase *tc_core;
  s = suite_create("iqp_gap");
  tc_core = tcase_create("Core");
  tcase_set_timeout(tc_core, 3600);
  tcase_add_test(tc_core, test_gap);
  tcase_add_test(tc_core, test_iqp_gap);
  suite_add_tcase(s, tc_core);
  return s;
}

int main(int argc, char *argv[])
{
  int number_failed;
  Suite *s;
  SRunner *sr;

  s = iqp_gap_suite();
  sr = srunner_create(s);

  srunner_run_all(sr, CK_NORMAL);
  number_failed = srunner_ntests_failed(sr);
  srunner_free(sr);
  return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}
