"""Run the unit tests in different suites.

Usage:
    python run_tests.py               -> list all suites
    python run_tests.py <suite>       -> run one suite
    python run_tests.py smoke         (example)

Only needs: pytest, pytest-xdist, pytest-order  (see requirements.txt)
"""
import subprocess
import sys

PYTEST = [sys.executable, "-m", "pytest"]

# suite name -> pytest arguments
SUITES = {
    "all":      ["-v"],                                        # everything, in the defined order
    "smoke":    ["-m", "smoke", "-v"],                         # quick checks only
    "negative": ["-m", "negative", "-v"],                      # invalid input / errors
    "boundary": ["-m", "boundary", "-v"],                      # boundary value tests
    "csv":      ["-m", "csv_data", "-v"],                      # data-driven tests (CSV)
    "utils":    ["-m", "utils", "-v"],                         # module groups
    "storage":  ["-m", "storage", "-v"],
    "services": ["-m", "services", "-v"],
    "cli":      ["-m", "cli", "-v"],
    "parallel": ["-n", "4", "--dist", "loadfile", "-v"],       # everything in 4 parallel workers
}

# run the module groups one after another, in this fixed order
GROUP_SEQUENCE = ["utils", "storage", "services", "cli"]


def run(args):
    print("\n>>> pytest " + " ".join(args))
    return subprocess.call(PYTEST + args)


def main():
    if len(sys.argv) < 2:
        print("Available suites:")
        for name, args in SUITES.items():
            print(f"  {name:<10} pytest {' '.join(args)}")
        print(f"  {'sequence':<10} runs {' -> '.join(GROUP_SEQUENCE)} one after another")
        return 0

    name = sys.argv[1]
    if name == "sequence":
        for group in GROUP_SEQUENCE:
            code = run(SUITES[group])
            if code != 0:
                print(f"Stopped: group '{group}' failed.")
                return code
        return 0
    if name not in SUITES:
        print(f"Unknown suite '{name}'. Run without arguments to see the list.")
        return 2
    return run(SUITES[name])


if __name__ == "__main__":
    sys.exit(main())
