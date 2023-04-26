#include <assert.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "circuit.h"

struct polynomial **read_instances(char *src_path)
{
  FILE *src_file = fopen(src_path, "r");
  if (src_file == NULL) {
    perror(src_path);
    exit(EXIT_FAILURE);
  }
  char *line_ptr = NULL;
  size_t line_len = 0;
  int length = -1;
  int variables = -1;
  size_t capacity = 8192;
  struct polynomial **polynomials =
    (struct polynomial **) malloc(sizeof(struct polynomial *) * capacity);
  assert(polynomials != NULL);
  size_t nb_polynomials = 0;
  while (getline(&line_ptr, &line_len, src_file) != -1) {
    char *c = line_ptr;
    while (*c == ' ') {
      c++;
    }
    if (*c == '#') {
      sscanf(c, "# length: %d, variables: %d", &length, &variables);
    }
    else if (*c != '\n' && *c != 0) {
      assert(length >= 0 && variables >= 0);
      struct polynomial *polynomial = alloc_polynomial(length, variables, NULL);
      struct monomial *monomial = polynomial->monomials;
      while (true) {
        unsigned short degree = 0;
        while (true) {
          int var_len;
          while (*c == ' ') {
            c++;
          }
          assert(*c == 'x');
          sscanf(c, "x%d%n", &monomial->x[degree], &var_len);
          degree++;
          c += var_len;
          while (*c == ' ') {
            c++;
          }
          if (*c != '*') {
            break;
          }
          c++;
        }
        monomial->degree = degree;
        if (*c != '+') {
          break;
        }
        c++;
        monomial++;
      }
      assert(*c == '\n');
      if (nb_polynomials + 1 >= capacity) {
        capacity *= 2;
        polynomials =
          (struct polynomial **) realloc(polynomials,
                                         sizeof(struct polynomial *) *
                                         capacity);
        assert(polynomials != NULL);
      }
      polynomials[nb_polynomials] = polynomial;
      nb_polynomials++;
    }
  }
  polynomials[nb_polynomials] = NULL;
  fclose(src_file);
  return polynomials;
}

enum {
  NB_TIMES = 4,
  NS_PER_SECOND = 1000000000
};

struct command_line {
  char *src_path;
  char *tgt_path;
  unsigned int variables;
};

void usage(FILE * f)
{
  fprintf(f, "Usage: benchmark [--variables=N] <source> <target>\n");
}

void parse_command_line(char *argv[], struct command_line *command_line)
{
  char **arg_cursor = argv;
  int position = 0;
  bool may_have_options = true;
  const char *option_variables = "--variables=";
  size_t len_option_variables = strlen(option_variables);
  arg_cursor++;
  while (*arg_cursor != NULL) {
    char *arg = *arg_cursor;
    arg_cursor++;
    if (may_have_options && strncmp(arg, "--", 2) == 0) {
      if (strcmp(arg, "--") == 0) {
        may_have_options = false;
      }
      else if (strncmp(arg, option_variables, len_option_variables) == 0
               && command_line->variables == 0) {
        char *end;
        long int variables = strtol(arg + len_option_variables, &end, 10);
        if (variables == LONG_MIN || variables == LONG_MAX) {
          perror("variables");
          exit(EXIT_FAILURE);
        }
        else if (end == arg + len_option_variables || end[0] != '\0'
                 || variables <= 0) {
          fprintf(stderr, "invalid number for --variables\n");
          usage(stderr);
          exit(EXIT_FAILURE);
        }
        else {
          command_line->variables = variables;
        }
      }
      else {
        fprintf(stderr, "unexpected option: %s\n", arg);
        usage(stderr);
        exit(EXIT_FAILURE);
      }
    }
    else {
      switch (position) {
        case 0:
          command_line->src_path = arg;
          break;
        case 1:
          command_line->tgt_path = arg;
          break;
        default:
          fprintf(stderr, "unexpected positional argument: %s\n", arg);
          usage(stderr);
          exit(EXIT_FAILURE);
      }
      position++;
    }
  }
  if (position != 2) {
    fprintf(stderr, "only %d positional argument given\n", position);
    usage(stderr);
    exit(EXIT_FAILURE);
  }
}

int main(int argc, char *argv[])
{
  struct command_line command_line;
  command_line.variables = 0;
  parse_command_line(argv, &command_line);
  struct polynomial **polynomials = read_instances(command_line.src_path);
  FILE *tgt_file = fopen(command_line.tgt_path, "w");
  if (tgt_file == NULL) {
    perror(command_line.tgt_path);
    return EXIT_FAILURE;
  }
  QuESTEnv env = createQuESTEnv();
  struct polynomial **cursor;
  for (cursor = polynomials; *cursor != NULL; cursor++) {
    struct polynomial *polynomial = *cursor;
    if (command_line.variables != 0
        && polynomial->variables > command_line.variables) {
      fprintf(tgt_file, "skipped\n");
    }
    else {
      struct timespec start, finish;
      int success;
      success = clock_gettime(CLOCK_REALTIME, &start);
      assert(success == 0);
      qreal result = evaluate_gap(polynomial, env);
      int i;
      for (i = 1; i < NB_TIMES; i++) {
        qreal other_result = evaluate_gap(polynomial, env);
        assert(abs(result - other_result) < 0.00001);
      }
      success = clock_gettime(CLOCK_REALTIME, &finish);
      assert(success == 0);
      long timing =
        ((finish.tv_sec - start.tv_sec) * NS_PER_SECOND + finish.tv_nsec -
         start.tv_nsec) / NB_TIMES;
      fprintf(tgt_file, "%f %ld\n", result, timing);
      free(polynomial);
    }
  }
  free(polynomials);
  fclose(tgt_file);
  return EXIT_SUCCESS;
}
