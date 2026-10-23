"""Javeria (24F-3036) - unit tests for app/task_services.py
Functions: generate_next_id, add_task, list_tasks, find_task_by_id
"""
import pytest

from app.task_services import (
    add_task,
    find_task_by_id,
    generate_next_id,
    list_tasks,
)

pytestmark = pytest.mark.services


# ---------------------------------------------------------------- generate_next_id
@pytest.mark.parametrize(
    "tasks, expected",
    [
        ([], 1),                                          # BVA: empty list
        ([{"id": 1}], 2),                                 # BVA: single task
        ([{"id": 1}, {"id": 2}, {"id": 3}], 4),           # ECP: consecutive ids
        ([{"id": 1}, {"id": 5}, {"id": 3}], 6),           # ECP: gaps, unordered
        ([{"id": 99}], 100),                              # BVA: 2-digit -> 3-digit
    ],
)
@pytest.mark.boundary
def test_generate_next_id_values(tasks, expected):
    assert generate_next_id(tasks) == expected


def test_generate_next_id_does_not_modify_input():
    tasks = [{"id": 1}, {"id": 2}]
    generate_next_id(tasks)
    assert tasks == [{"id": 1}, {"id": 2}]


@pytest.mark.negative
def test_generate_next_id_missing_id_key_raises():
    with pytest.raises(KeyError):
        generate_next_id([{"description": "no id here"}])


# ---------------------------------------------------------------- add_task
@pytest.mark.smoke
def test_add_task_returns_correct_fields(fixed_time):
    task = add_task("Buy milk")
    assert task == {
        "id": 1,
        "description": "Buy milk",
        "status": "todo",
        "createdAt": fixed_time,
        "updatedAt": fixed_time,
    }


def test_add_task_first_task_gets_id_1():
    assert add_task("first")["id"] == 1


def test_add_task_ids_increment():
    first = add_task("one")
    second = add_task("two")
    third = add_task("three")
    assert [first["id"], second["id"], third["id"]] == [1, 2, 3]


def test_add_task_is_saved_to_file(read_file):
    add_task("Persist me")
    saved = read_file()
    assert len(saved) == 1
    assert saved[0]["description"] == "Persist me"


def test_add_task_created_and_updated_are_equal():
    task = add_task("same time")
    assert task["createdAt"] == task["updatedAt"]


@pytest.mark.boundary
def test_add_task_empty_description_is_currently_accepted():
    # Finding: the app has NO validation for an empty description.
    task = add_task("")
    assert task["description"] == ""


@pytest.mark.boundary
def test_add_task_very_long_description():
    long_text = "x" * 1000
    assert add_task(long_text)["description"] == long_text


def test_add_task_unicode_description(read_file):
    add_task("Comprar despensa - خریداری")
    assert read_file()[0]["description"] == "Comprar despensa - خریداری"


@pytest.mark.negative
def test_add_task_corrupted_file_raises_and_keeps_file(isolated_tasks_file):
    isolated_tasks_file.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(ValueError):
        add_task("will fail")
    assert isolated_tasks_file.read_text(encoding="utf-8") == "{not valid json"


# ---------------------------------------------------------------- list_tasks
@pytest.fixture
def mixed_tasks(seed, make_task):
    seed([
        make_task(1, "a", "todo"),
        make_task(2, "b", "in-progress"),
        make_task(3, "c", "done"),
        make_task(4, "d", "todo"),
    ])


def test_list_tasks_empty_returns_empty_list():
    assert list_tasks() == []


def test_list_tasks_no_filter_returns_all(mixed_tasks):
    assert [t["id"] for t in list_tasks()] == [1, 2, 3, 4]


@pytest.mark.parametrize(
    "status, expected_ids",
    [("todo", [1, 4]), ("in-progress", [2]), ("done", [3])],
)
def test_list_tasks_filter_by_valid_status(mixed_tasks, status, expected_ids):
    assert [t["id"] for t in list_tasks(status)] == expected_ids


def test_list_tasks_valid_status_with_no_match(seed, make_task):
    seed([make_task(1, "a", "todo")])
    assert list_tasks("done") == []


@pytest.mark.negative
@pytest.mark.parametrize("bad_status", ["finished", "DONE", "Todo", "", " done"])
def test_list_tasks_invalid_status_raises(bad_status):
    with pytest.raises(ValueError, match="inválido"):
        list_tasks(bad_status)


# ---------------------------------------------------------------- find_task_by_id
@pytest.fixture
def three_tasks(make_task):
    return [make_task(1, "a"), make_task(2, "b"), make_task(3, "c")]


@pytest.mark.smoke
def test_find_task_by_id_found_in_middle(three_tasks):
    assert find_task_by_id(three_tasks, 2)["description"] == "b"


@pytest.mark.boundary
def test_find_task_by_id_first_element(three_tasks):
    assert find_task_by_id(three_tasks, 1)["description"] == "a"


@pytest.mark.boundary
def test_find_task_by_id_last_element(three_tasks):
    assert find_task_by_id(three_tasks, 3)["description"] == "c"


@pytest.mark.negative
@pytest.mark.parametrize("missing_id", [4, 0, -1, 999])
def test_find_task_by_id_not_found_returns_none(three_tasks, missing_id):
    assert find_task_by_id(three_tasks, missing_id) is None


def test_find_task_by_id_empty_list_returns_none():
    assert find_task_by_id([], 1) is None


@pytest.mark.negative
def test_find_task_by_id_string_id_does_not_match(three_tasks):
    assert find_task_by_id(three_tasks, "1") is None


def test_find_task_by_id_duplicate_ids_returns_first(make_task):
    tasks = [make_task(1, "first"), make_task(1, "second")]
    assert find_task_by_id(tasks, 1)["description"] == "first"


# ---------------------------------------------------------------- module-level
def test_module_add_then_list_shows_new_tasks():
    add_task("one")
    add_task("two")
    assert [t["description"] for t in list_tasks()] == ["one", "two"]


def test_module_added_tasks_can_be_found_by_id():
    add_task("one")
    add_task("two")
    tasks = list_tasks()
    assert find_task_by_id(tasks, 2)["description"] == "two"
    assert generate_next_id(tasks) == 3
