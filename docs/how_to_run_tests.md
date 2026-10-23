# How to run the unit tests (Task 4)

## 1. Setup (once)
```
git clone <group-repo-url>
cd python-task-tracker-cli
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt  # pytest, pytest-xdist, pytest-order
```

## 2. Folder layout
```
app/                      application code (cli, storage, task_services, utils)
tests/                    all unit tests (+ conftest.py with shared fixtures and execution order)
test_data/                CSV files used by the data-driven tests (Task 3)
docs/                     test design notes, Excel test cases, setup video
pytest.ini                pytest configuration (markers = groups)
run_tests.py              helper to run suites
```

## 3. Test groups (markers)
| Group | Type | What it contains |
|---|---|---|
| `utils`, `storage`, `services`, `cli` | module groups | tests of one module each |
| `smoke` | type group | quick happy-path checks |
| `negative` | type group | invalid input / error handling |
| `boundary` | type group | boundary value analysis |
| `csv_data` | type group | data-driven tests reading `test_data/*.csv` |

Run one group:
```
pytest -m smoke
pytest -m "services and negative"        # combine groups
pytest -m "not csv_data"                  # everything except one group
```

## 4. Suites (helper script)
```
python run_tests.py              # list suites
python run_tests.py all          # all tests in the defined order
python run_tests.py smoke
python run_tests.py negative
python run_tests.py boundary
python run_tests.py csv
python run_tests.py services     # also: utils, storage, cli
python run_tests.py parallel     # 4 workers
python run_tests.py sequence     # utils -> storage -> services -> cli, one after another
```

## 5. Parallel execution (pytest-xdist)
```
pytest -n 4 --dist loadfile      # 4 workers, a file always stays on one worker
pytest -n auto --dist loadfile   # one worker per CPU core
```
Every test uses its own temporary `tasks.json` (fixture `isolated_tasks_file`), so tests never
interfere with each other and are safe to run in parallel.
Note: the strict execution order below is guaranteed for normal (serial) runs.
With `-n` the tests are shared between workers, so only the order inside a worker is kept.

## 6. Execution order (pytest-order)
Defined in `tests/conftest.py` (`pytest_collection_modifyitems`):
1. **Groups run bottom-up:** `utils` -> `storage` -> `services` -> `cli`
   (a module runs only after the modules it depends on).
2. **Inside each group** the `smoke` tests run first, then the remaining tests in file order.

See the order without running anything:
```
pytest --collect-only -q
```

## 7. Parameterization
Tests are data-driven with `@pytest.mark.parametrize`:
- inline data (for example valid and invalid statuses in `test_task_services_*.py`)
- external data from CSV files (`tests/test_csv_driven_*.py` reading `test_data/*.csv`),
  every CSV row is one test case with its own id (`TC-J-01`, `TC-M-05`, ...)

Run one CSV case: `pytest -k "TC-J-07" -v`

## 8. Useful options
```
pytest -v                 # show every test name
pytest -x                 # stop at first failure
pytest -k "add_task"      # run tests whose name contains add_task
pytest --lf               # re-run only the tests that failed last time
```
