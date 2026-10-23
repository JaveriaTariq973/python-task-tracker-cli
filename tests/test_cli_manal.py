"""Manal (24F-3041) - unit tests for app/cli.py
Functions: print_task_list, handle_command
"""
import pytest

from app.cli import handle_command, print_task_list

pytestmark = pytest.mark.cli


def run(args, capsys):
    handle_command(args)
    return capsys.readouterr().out


@pytest.fixture
def two_tasks(seed, make_task):
    seed([make_task(1, "first", "todo"), make_task(2, "second", "done")])


# ---------------------------------------------------------------- print_task_list
@pytest.mark.boundary
def test_print_task_list_empty_list_shows_message(capsys):
    print_task_list([])
    assert capsys.readouterr().out == "No hay tareas para mostrar.\n"


@pytest.mark.boundary
def test_print_task_list_none_shows_message(capsys):
    print_task_list(None)
    assert "No hay tareas" in capsys.readouterr().out


def test_print_task_list_single_task(capsys, make_task):
    print_task_list([make_task(1, "only")])
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 1 and lines[0].startswith("[1] only")


def test_print_task_list_multiple_tasks_one_line_each(capsys, make_task):
    print_task_list([make_task(1, "a"), make_task(2, "b"), make_task(3, "c")])
    assert len(capsys.readouterr().out.splitlines()) == 3


def test_print_task_list_keeps_given_order(capsys, make_task):
    print_task_list([make_task(2, "b"), make_task(1, "a")])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("[2]") and lines[1].startswith("[1]")


def test_print_task_list_no_empty_message_when_tasks_exist(capsys, make_task):
    print_task_list([make_task(1)])
    assert "No hay tareas" not in capsys.readouterr().out


# ---------------------------------------------------------------- handle_command: general
@pytest.mark.negative
def test_handle_command_no_arguments(capsys):
    assert run([], capsys) == "Debes proporcionar un comando.\n"


@pytest.mark.negative
@pytest.mark.parametrize("command", ["foo", "ADD", "remove", ""])
def test_handle_command_unknown_command(capsys, command):
    assert run([command], capsys) == f"Comando no reconocido: {command}\n"


# ---------------------------------------------------------------- handle_command: add
@pytest.mark.smoke
def test_handle_add_success(capsys, read_file):
    out = run(["add", "Buy milk"], capsys)
    assert out == "Tarea agregada correctamente (ID: 1)\n"
    assert read_file()[0]["description"] == "Buy milk"


@pytest.mark.negative
def test_handle_add_missing_description_shows_usage(capsys, isolated_tasks_file):
    out = run(["add"], capsys)
    assert out.startswith("Uso: python main.py add")
    assert not isolated_tasks_file.exists()      # nothing was saved


def test_handle_add_extra_arguments_are_ignored(capsys, read_file):
    run(["add", "first", "ignored"], capsys)
    assert read_file()[0]["description"] == "first"


@pytest.mark.boundary
def test_handle_add_empty_description_is_currently_accepted(capsys):
    assert "agregada correctamente" in run(["add", ""], capsys)


# ---------------------------------------------------------------- handle_command: list
def test_handle_list_empty(capsys):
    assert run(["list"], capsys) == "No hay tareas para mostrar.\n"


def test_handle_list_all(two_tasks, capsys):
    assert len(run(["list"], capsys).splitlines()) == 2


@pytest.mark.parametrize("status, expected_text", [("todo", "first"), ("done", "second")])
def test_handle_list_with_status_filter(two_tasks, capsys, status, expected_text):
    out = run(["list", status], capsys)
    assert expected_text in out and len(out.splitlines()) == 1


@pytest.mark.negative
def test_handle_list_invalid_status_prints_error(capsys):
    assert run(["list", "finished"], capsys).startswith("Error: Estado inválido")


# ---------------------------------------------------------------- handle_command: update
def test_handle_update_success(two_tasks, capsys, read_file):
    assert run(["update", "1", "changed"], capsys) == "Tarea 1 actualizada correctamente.\n"
    assert read_file()[0]["description"] == "changed"


@pytest.mark.negative
@pytest.mark.parametrize("args", [["update"], ["update", "1"]])
def test_handle_update_missing_arguments_shows_usage(capsys, args):
    assert run(args, capsys).startswith("Uso: python main.py update")


@pytest.mark.negative
def test_handle_update_nonexistent_id(two_tasks, capsys):
    assert run(["update", "99", "x"], capsys) == "Error: No existe una tarea con ID 99\n"


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", ["abc", "1.5", ""])
def test_handle_update_non_numeric_id_prints_error(two_tasks, capsys, bad_id):
    assert run(["update", bad_id, "x"], capsys).startswith("Error:")


# ---------------------------------------------------------------- handle_command: delete
def test_handle_delete_success(two_tasks, capsys, read_file):
    assert run(["delete", "1"], capsys) == "Tarea 1 eliminada correctamente.\n"
    assert [t["id"] for t in read_file()] == [2]


@pytest.mark.negative
def test_handle_delete_missing_id_shows_usage(capsys):
    assert run(["delete"], capsys).startswith("Uso: python main.py delete")


@pytest.mark.negative
@pytest.mark.parametrize("bad_id, start", [("99", "Error: No existe"), ("-1", "Error: No existe"), ("abc", "Error:")])
def test_handle_delete_invalid_id_prints_error(two_tasks, capsys, bad_id, start):
    assert run(["delete", bad_id], capsys).startswith(start)


# ---------------------------------------------------------------- handle_command: mark-*
@pytest.mark.parametrize(
    "command, status",
    [("mark-in-progress", "in-progress"), ("mark-done", "done")],
)
def test_handle_mark_commands_success(two_tasks, capsys, read_file, command, status):
    assert run([command, "1"], capsys) == f"Tarea 1 marcada como {status}.\n"
    assert read_file()[0]["status"] == status


@pytest.mark.negative
@pytest.mark.parametrize("command", ["mark-in-progress", "mark-done"])
def test_handle_mark_commands_missing_id_shows_usage(capsys, command):
    assert run([command], capsys).startswith(f"Uso: python main.py {command}")


@pytest.mark.negative
@pytest.mark.parametrize("command", ["mark-in-progress", "mark-done"])
def test_handle_mark_commands_nonexistent_id(two_tasks, capsys, command):
    assert run([command, "50"], capsys) == "Error: No existe una tarea con ID 50\n"


# ---------------------------------------------------------------- module-level
def test_module_full_cli_flow(capsys):
    run(["add", "Task A"], capsys)
    run(["add", "Task B"], capsys)
    run(["mark-done", "1"], capsys)
    assert "Task A" in run(["list", "done"], capsys)
    run(["delete", "2"], capsys)
    assert len(run(["list"], capsys).splitlines()) == 1


def test_module_cli_and_print_task_list_show_same_data(two_tasks, capsys, make_task):
    cli_out = run(["list"], capsys)
    print_task_list([make_task(1, "first", "todo"), make_task(2, "second", "done")])
    assert capsys.readouterr().out == cli_out
