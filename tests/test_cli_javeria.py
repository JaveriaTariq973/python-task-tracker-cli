"""Javeria (24F-3036) - unit tests for app/cli.py
Function: print_task
"""
import pytest

from app.cli import print_task
from app.task_services import add_task

pytestmark = pytest.mark.cli


def _task(**overrides):
    task = {
        "id": 1,
        "description": "Buy milk",
        "status": "todo",
        "createdAt": "2026-01-01T00:00:00",
        "updatedAt": "2026-01-02T00:00:00",
    }
    task.update(overrides)
    return task


@pytest.mark.smoke
def test_print_task_exact_format(capsys):
    print_task(_task())
    assert capsys.readouterr().out == (
        "[1] Buy milk | status: todo | "
        "createdAt: 2026-01-01T00:00:00 | updatedAt: 2026-01-02T00:00:00\n"
    )


def test_print_task_contains_all_fields(capsys):
    print_task(_task(id=7, description="Read", status="done"))
    out = capsys.readouterr().out
    for piece in ["[7]", "Read", "status: done", "createdAt:", "updatedAt:"]:
        assert piece in out


def test_print_task_prints_a_single_line(capsys):
    print_task(_task())
    assert len(capsys.readouterr().out.splitlines()) == 1


@pytest.mark.parametrize("status", ["todo", "in-progress", "done"])
def test_print_task_shows_each_status(capsys, status):
    print_task(_task(status=status))
    assert f"status: {status}" in capsys.readouterr().out


@pytest.mark.boundary
def test_print_task_empty_description(capsys):
    print_task(_task(description=""))
    assert capsys.readouterr().out.startswith("[1]  | status: todo")


@pytest.mark.boundary
def test_print_task_large_id(capsys):
    print_task(_task(id=123456789))
    assert capsys.readouterr().out.startswith("[123456789]")


def test_print_task_unicode_description(capsys):
    print_task(_task(description="ñandú"))
    assert "ñandú" in capsys.readouterr().out


@pytest.mark.negative
def test_print_task_missing_key_raises_key_error():
    with pytest.raises(KeyError):
        print_task({"id": 1, "description": "incomplete"})


# ---------------------------------------------------------------- module-level
def test_module_print_task_of_a_really_added_task(capsys):
    task = add_task("From service")
    print_task(task)
    out = capsys.readouterr().out
    assert out.startswith("[1] From service | status: todo")


def test_module_print_task_returns_none(capsys):
    assert print_task(_task()) is None
