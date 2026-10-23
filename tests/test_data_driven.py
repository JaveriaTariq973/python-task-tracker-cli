import csv
from pathlib import Path

import pytest

from app.cli import handle_command
from app.task_services import change_task_status, generate_next_id, list_tasks

pytestmark = pytest.mark.datadriven

DATA_DIR = Path(__file__).parent / "data"


def read_rows(file_name):
    with open(DATA_DIR / file_name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_cases(file_name, *columns):
    return [
        pytest.param(*[row[c] for c in columns], id=row["test_id"])
        for row in read_rows(file_name)
    ]


@pytest.mark.boundary
@pytest.mark.parametrize("ids, expected", load_cases("next_id_cases.csv", "ids", "expected"))
def test_csv_generate_next_id(ids, expected):
    tasks = [{"id": int(i)} for i in ids.split(";")] if ids else []
    assert generate_next_id(tasks) == int(expected)


@pytest.mark.parametrize("status, expected", load_cases("list_status_cases.csv", "status", "expected"))
def test_csv_list_tasks_status_filter(status, expected):
    if expected == "ok":
        assert list_tasks(status) == []
    else:
        with pytest.raises(ValueError, match="inválido"):
            list_tasks(status)


@pytest.mark.parametrize(
    "task_id, status, expected",
    load_cases("change_status_cases.csv", "task_id", "status", "expected"),
)
def test_csv_change_task_status(seed, make_task, task_id, status, expected):
    seed([make_task(1, "first", "todo")])
    if expected == "ok":
        assert change_task_status(int(task_id), status)["status"] == status
    elif expected == "invalid_status":
        with pytest.raises(ValueError, match="inválido"):
            change_task_status(int(task_id), status)
    else:
        with pytest.raises(ValueError, match="No existe"):
            change_task_status(int(task_id), status)


@pytest.mark.parametrize(
    "args, match, expected",
    load_cases("cli_cases.csv", "args", "match", "expected"),
)
def test_csv_cli_commands(capsys, args, match, expected):
    handle_command(args.split("|") if args else [])
    out = capsys.readouterr().out.rstrip("\n")
    if match == "equals":
        assert out == expected
    else:
        assert out.startswith(expected)
