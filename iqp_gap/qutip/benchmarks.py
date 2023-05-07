import iqp_gap.benchmarks
import iqp_gap.qutip

if __name__ == "__main__":
    iqp_gap.benchmarks.benchmark_cmdline(iqp_gap.qutip.evaluate_gap)
