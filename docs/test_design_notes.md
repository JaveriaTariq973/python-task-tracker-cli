# Test Design Notes - Assignment 3 (Unit Test Automation)

Project: python-task-tracker-cli (Python, standard library only)
Group: Javeria Tariq (24F-3036), Manal (24F-3041)
Tools: pytest, pytest-xdist (parallel), pytest-order (ordering)

Techniques used
- **ECP** (Equivalence Class Partitioning): divide inputs into valid and invalid classes, test one representative per class.
- **BVA** (Boundary Value Analysis): test at and around the edges (empty, 1 item, first/last, 0, -1, max+1).

Modules under test
1. `app/task_services.py` - business logic (7 functions)
2. `app/storage.py` - JSON file read/write (3 functions)
3. `app/cli.py` - command parsing and printing (3 functions)
(`app/utils.py` has one function, `get_current_timestamp`, tested by Manal.)

Isolation: every test uses a temporary `tasks.json` (fixture `isolated_tasks_file` in `tests/conftest.py`), so the real file is never touched.

---------------------------------------------------------------------

## PART A - Javeria (24F-3036)

### Module 1: task_services.py

**generate_next_id(tasks)**
| Technique | Input | Expected |
|---|---|---|
| BVA | `[]` (empty) | 1 |
| BVA | one task id 1 | 2 |
| ECP valid | ids 1,2,3 | 4 |
| ECP valid | ids 1,5,3 (gaps, unordered) | 6 (max + 1) |
| BVA | id 99 | 100 |
| ECP invalid | task without `id` key | KeyError |

**add_task(description)**
| Technique | Input | Expected |
|---|---|---|
| ECP valid | "Buy milk" | dict with id, status `todo`, createdAt == updatedAt |
| BVA | first task | id 1 |
| ECP valid | 3 adds in a row | ids 1,2,3 and saved to file |
| BVA | empty string "" | accepted (no validation - see Findings) |
| BVA | 1000 characters | accepted |
| ECP valid | unicode text | saved correctly |
| ECP invalid | corrupted tasks.json | ValueError, file unchanged |

**list_tasks(status=None)**
| Technique | Input | Expected |
|---|---|---|
| BVA | empty file | `[]` |
| ECP valid | no filter | all tasks |
| ECP valid | `todo`, `in-progress`, `done` | only matching tasks |
| BVA | valid status, no match | `[]` |
| ECP invalid | `finished`, `DONE`, `Todo`, "", " done" | ValueError (case-sensitive) |

**find_task_by_id(tasks, task_id)**
| Technique | Input | Expected |
|---|---|---|
| BVA | first / last element | found |
| ECP valid | middle element | found |
| ECP invalid | id 4, 999 (not present) | None |
| BVA | id 0, -1 | None |
| BVA | empty list | None |
| ECP invalid | id as string "1" | None (type must match) |
| ECP | duplicate ids | first one returned |

### Module 2: storage.py

**ensure_tasks_file_exists()**
| Technique | Input state | Expected |
|---|---|---|
| ECP | file missing | created with `[]` |
| ECP | file exists with data | not overwritten |
| ECP | called twice | same result (idempotent) |
| BVA | existing empty file | stays empty |

**load_tasks()**
| Technique | Input state | Expected |
|---|---|---|
| ECP valid | missing file | `[]` and file is created |
| BVA | empty file / whitespace only | `[]` |
| ECP valid | valid JSON list | list of tasks |
| ECP valid | unicode content | read correctly |
| ECP invalid | corrupted JSON (4 samples) | ValueError mentioning tasks.json |
| ECP | valid JSON but not a list (`{}`) | returned as is (Findings) |

### Module 3: cli.py

**print_task(task)**
| Technique | Input | Expected |
|---|---|---|
| ECP valid | normal task | exact one-line format |
| ECP valid | status todo / in-progress / done | status shown |
| BVA | empty description | prints `[1]  | status...` |
| BVA | very large id | printed in full |
| ECP invalid | dict with missing keys | KeyError |

---------------------------------------------------------------------

## PART B - Manal (24F-3041)

### Module 1: task_services.py

**update_task(task_id, new_description)**
| Technique | Input | Expected |
|---|---|---|
| ECP valid | existing id, new text | description + updatedAt change, createdAt/status same |
| ECP invalid | id 99 (not present) | ValueError "No existe" |
| BVA | id 0, -1, last+1 | ValueError |
| BVA | empty new description | accepted (Findings) |
| ECP invalid | empty file | ValueError |

**delete_task(task_id)**
| Technique | Input | Expected |
|---|---|---|
| ECP valid | existing id | removed, others intact, returns None |
| BVA | delete last remaining task | empty list |
| ECP | ids after delete | not renumbered (next id keeps growing) |
| ECP invalid | missing id / empty file / delete twice / "1" as string | ValueError |

**change_task_status(task_id, status)**
| Technique | Input | Expected |
|---|---|---|
| ECP valid | `todo`, `in-progress`, `done` | status changed, updatedAt changed |
| ECP invalid | `finished`, `DONE`, "", "done " | ValueError "inválido" |
| BVA | id 0, -1, last+1, 999 | ValueError "No existe" |
| ECP | invalid status AND invalid id | status error reported first |

### Module 2: storage.py

**save_tasks(tasks)**
| Technique | Input | Expected |
|---|---|---|
| ECP valid | list of tasks | valid JSON, 2-space indent, non-ASCII kept readable |
| BVA | empty list | `[]` |
| BVA | 200 tasks | round trip equals input |
| ECP | save twice | second overwrites first |
| ECP invalid | non-serializable data (set) | TypeError |

### Module 3: cli.py

**print_task_list(tasks)**
| Technique | Input | Expected |
|---|---|---|
| BVA | `[]` / `None` | "No hay tareas para mostrar." |
| BVA | 1 task | 1 line |
| ECP valid | many tasks | 1 line each, given order |

**handle_command(args)**
| Technique | Input | Expected |
|---|---|---|
| BVA | `[]` | "Debes proporcionar un comando." |
| ECP invalid | `foo`, `ADD`, `remove`, "" | "Comando no reconocido" |
| ECP valid | add / list / update / delete / mark-in-progress / mark-done with correct args | success message + file changed |
| BVA | missing argument for each command | usage message ("Uso: ...") |
| ECP invalid | non-existent id (99, -1) | "Error: No existe..." |
| ECP invalid | non-numeric id ("abc", "1.5", "") | "Error: ..." |
| ECP invalid | `list finished` | "Error: Estado inválido" |
| BVA | extra arguments | ignored |

### Utils: utils.py
**get_current_timestamp()** - ECP: returns str in `YYYY-MM-DDTHH:MM:SS`, length 19, parseable. BVA (fake clock): microseconds dropped, 1 Jan 00:00:00, 31 Dec 23:59:59, leap day 29 Feb.

---------------------------------------------------------------------

## Findings (possible defects / weak validation seen while designing tests)
1. `add_task("")` and `update_task(id, "")` accept an empty description (no validation).
2. `load_tasks()` returns any valid JSON (for example `{}`), it does not check that it is a list of tasks.
3. `handle_command` ignores extra arguments (`add "a" "b"` saves only "a").
4. For a non-numeric id (`update abc x`) the user sees Python's raw `int()` error text.
5. Ids are never reused or renumbered after a delete (by design, documented by a test).
