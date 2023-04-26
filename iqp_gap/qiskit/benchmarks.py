import iqp_gap.benchmarks
import iqp_gap.qiskit

if __name__ == "__main__":
    iqp_gap.benchmarks.benchmark_cmdline(iqp_gap.qiskit.evaluate_gap)
