"""Manal (24F-3041) - unit tests for app/task_services.py
Functions: update_task, delete_task, change_task_status
"""
import pytest

from app.task_services import (
    add_task,
    change_task_status,
    delete_task,
    list_tasks,
    update_task,
)

pytestmark = pytest.mark.services


@pytest.fixture
def two_tasks(seed, make_task):
    seed([make_task(1, "first", "todo"), make_task(2, "second", "todo")])


# ---------------------------------------------------------------- update_task
@pytest.mark.smoke
def test_update_task_changes_description_and_updated_at(two_tasks, fixed_time):
    task = update_task(1, "new text")
    assert task["description"] == "new text"
    assert task["updatedAt"] == fixed_time


def test_update_task_keeps_created_at_and_status(two_tasks, fixed_time):
    task = update_task(1, "new text")
    assert task["createdAt"] == "2026-01-01T00:00:00"
    assert task["status"] == "todo"


def test_update_task_is_saved_to_file(two_tasks, read_file):
    update_task(2, "saved change")
    assert read_file()[1]["description"] == "saved change"


def test_update_task_does_not_touch_other_tasks(two_tasks, read_file):
    update_task(2, "only me")
    assert read_file()[0]["description"] == "first"


@pytest.mark.negative
def test_update_task_nonexistent_id_raises(two_tasks):
    with pytest.raises(ValueError, match="99"):
        update_task(99, "x")


@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize("bad_id", [0, -1, 3])
def test_update_task_boundary_ids_raise(two_tasks, bad_id):
    with pytest.raises(ValueError, match="No existe"):
        update_task(bad_id, "x")


@pytest.mark.negative
def test_update_task_failure_leaves_file_unchanged(two_tasks, read_file):
    before = read_file()
    with pytest.raises(ValueError):
        update_task(50, "x")
    assert read_file() == before


@pytest.mark.negative
def test_update_task_on_empty_file_raises():
    with pytest.raises(ValueError):
        update_task(1, "x")


@pytest.mark.boundary
def test_update_task_empty_description_is_currently_accepted(two_tasks):
    # Finding: no validation for an empty new description.
    assert update_task(1, "")["description"] == ""


# ---------------------------------------------------------------- delete_task
@pytest.mark.smoke
def test_delete_task_removes_task(two_tasks):
    delete_task(1)
    assert [t["id"] for t in list_tasks()] == [2]


def test_delete_task_returns_none(two_tasks):
    assert delete_task(1) is None


def test_delete_task_keeps_other_tasks_intact(two_tasks, read_file):
    delete_task(1)
    assert read_file()[0]["description"] == "second"


def test_delete_task_does_not_renumber_ids(two_tasks):
    delete_task(1)
    assert add_task("third")["id"] == 3


@pytest.mark.boundary
def test_delete_last_remaining_task_leaves_empty_list(seed, make_task):
    seed([make_task(1)])
    delete_task(1)
    assert list_tasks() == []


@pytest.mark.negative
def test_delete_task_nonexistent_id_raises(two_tasks):
    with pytest.raises(ValueError, match="No existe"):
        delete_task(42)


@pytest.mark.negative
def test_delete_task_on_empty_file_raises():
    with pytest.raises(ValueError):
        delete_task(1)


@pytest.mark.negative
def test_delete_same_task_twice_raises_second_time(two_tasks):
    delete_task(1)
    with pytest.raises(ValueError):
        delete_task(1)


@pytest.mark.negative
def test_delete_task_string_id_does_not_match(two_tasks):
    with pytest.raises(ValueError):
        delete_task("1")


# ---------------------------------------------------------------- change_task_status
@pytest.mark.smoke
@pytest.mark.parametrize("new_status", ["todo", "in-progress", "done"])
def test_change_status_to_each_valid_status(two_tasks, new_status):
    assert change_task_status(1, new_status)["status"] == new_status


def test_change_status_updates_updated_at_only(two_tasks, fixed_time):
    task = change_task_status(1, "done")
    assert task["updatedAt"] == fixed_time
    assert task["createdAt"] == "2026-01-01T00:00:00"


def test_change_status_is_saved_to_file(two_tasks, read_file):
    change_task_status(2, "in-progress")
    assert read_file()[1]["status"] == "in-progress"


def test_change_status_does_not_touch_other_tasks(two_tasks, read_file):
    change_task_status(2, "done")
    assert read_file()[0]["status"] == "todo"


@pytest.mark.negative
@pytest.mark.parametrize("bad_status", ["finished", "DONE", "In-Progress", "", "done "])
def test_change_status_invalid_status_raises(two_tasks, bad_status):
    with pytest.raises(ValueError, match="inválido"):
        change_task_status(1, bad_status)


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", [0, -1, 3, 999])
def test_change_status_nonexistent_id_raises(two_tasks, bad_id):
    with pytest.raises(ValueError, match="No existe"):
        change_task_status(bad_id, "done")


@pytest.mark.negative
def test_change_status_checks_status_before_id(two_tasks):
    # both are invalid -> the status error is reported first
    with pytest.raises(ValueError, match="inválido"):
        change_task_status(999, "wrong")


@pytest.mark.negative
def test_change_status_invalid_status_leaves_file_unchanged(two_tasks, read_file):
    before = read_file()
    with pytest.raises(ValueError):
        change_task_status(1, "wrong")
    assert read_file() == before


# ---------------------------------------------------------------- module-level
def test_module_full_lifecycle_add_update_status_delete():
    task = add_task("Write report")
    update_task(task["id"], "Write final report")
    change_task_status(task["id"], "in-progress")
    assert list_tasks("in-progress")[0]["description"] == "Write final report"
    delete_task(task["id"])
    assert list_tasks() == []


def test_module_status_filter_reflects_changes(two_tasks):
    change_task_status(1, "done")
    assert [t["id"] for t in list_tasks("done")] == [1]
    assert [t["id"] for t in list_tasks("todo")] == [2]
