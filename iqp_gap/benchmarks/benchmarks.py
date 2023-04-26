import argparse
import re
import statistics
import time
import matplotlib.pyplot as plt
import numpy as np
import sympy
import iqp_gap

NB_VARIABLES_REGEX = re.compile("variables: ([0-9]+)")


def read_instances(src):
    variables = None
    polynomials = []
    while line := src.readline():
        line = line.strip()
        if line == "":
            continue
        if line[0] == "#":
            m = NB_VARIABLES_REGEX.search(line)
            if m:
                nb_variables = int(m.group(1))
                _, *variables = sympy.polys.rings.ring(
                    ",".join([f"x{i}" for i in range(nb_variables)]), sympy.GF(2)
                )
        else:
            assert variables is not None
            monomials = (m.strip() for m in line.split("+"))
            polynomial = sum(
                sympy.prod(variables[int(x[1:].strip())] for x in monomial.split("*"))
                for monomial in monomials
            )
            polynomials.append(polynomial)
    return polynomials


NB_TIMES = 4


def benchmark_instances(tgt, polynomials, variables, f):
    for polynomial in polynomials:
        print(polynomial)
        if variables is not None and polynomial.parent().ngens > variables:
            tgt.write("skipped\n")
        else:
            start = time.perf_counter_ns()
            result = f(polynomial)
            for _ in range(1, NB_TIMES):
                other_result = f(polynomial)
                np.testing.assert_almost_equal(result, other_result)
            timing = int((time.perf_counter_ns() - start) / NB_TIMES)
            tgt.write(f"{result} {timing}\n")


def benchmark(src, tgt, variables, f):
    benchmark_instances(tgt, read_instances(src), variables, f)


def benchmark_files(src_filename, tgt_filename, variables, f):
    with open(src_filename, "r") as src:
        with open(tgt_filename, "w") as tgt:
            benchmark(src, tgt, variables, f)


def benchmark_cmdline(f):
    parser = argparse.ArgumentParser(prog="benchmarks")
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("--variables", help="maximum number of variables", type=int)
    args = parser.parse_args()
    benchmark_files(args.source, args.target, args.variables, f)


def read_results(src):
    results = []
    while line := src.readline():
        line = line.strip()
        if line == "skipped":
            results.append(None)
        else:
            result, timing = line.split(" ")
            results.append((float(result), int(timing)))
    return results


def make_plot(instance_filename, result_filenames, target_filename):
    with open(instance_filename, "r") as src:
        instances = read_instances(src)
    ## The reference implementation is very slow!
    ## We prefer to check that results are consistent between frameworks
    ## when they are available
    # reference_results = [
    #    (iqp_gap.gap(poly) / 2 ** poly.parent().ngens) ** 2 for poly in instances
    # ]
    reference_results = [[None] for _ in instances]
    fig, ax = plt.subplots()
    for toolkit_name, result_filename in result_filenames.items():
        try:
            timing_dict = {}
            with open(result_filename, "r") as src:
                results = read_results(src)
                for poly, reference_result, result_timing in zip(
                    instances, reference_results, results
                ):
                    try:
                        if result_timing is None:
                            continue
                        result, timing = result_timing
                        if reference_result[0] is None:
                            reference_result[0] = result
                        else:
                            np.testing.assert_almost_equal(
                                reference_result[0], result, decimal=5
                            )
                        n = poly.parent().ngens
                        try:
                            timing_list = timing_dict[n]
                        except KeyError:
                            timing_list = []
                            timing_dict[n] = timing_list
                        timing_list.append(timing)
                    except Exception as exc:
                        raise Exception(poly) from exc
        except Exception as exc:
            raise Exception(toolkit_name) from exc
        ax.plot(
            timing_dict.keys(),
            [statistics.mean(timing) / 10**9 for timing in timing_dict.values()],
            label=toolkit_name,
        )
    ax.set(
        xlabel="qubits = number of monomials",
        ylabel="time (s)",
        title="IQP gap computation",
    )
    ax.legend()
    fig.savefig(target_filename)


def make_plot_cmdline():
    parser = argparse.ArgumentParser(prog="benchmarks")
    parser.add_argument("instances")
    parser.add_argument("results", nargs="*")
    parser.add_argument("-o", "--output", help="output filename")
    args = parser.parse_args()
    result_filenames = {
        toolkit_name: result_filename
        for (toolkit_name, result_filename) in (
            item.split(":") for item in args.results
        )
    }
    make_plot(args.instances, result_filenames, args.output)


if __name__ == "__main__":
    make_plot_cmdline()
