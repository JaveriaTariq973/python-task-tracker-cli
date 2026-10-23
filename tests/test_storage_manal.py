"""Manal (24F-3041) - unit tests for app/storage.py
Function: save_tasks
"""
import json

import pytest

from app.storage import ensure_tasks_file_exists, load_tasks, save_tasks

pytestmark = pytest.mark.storage


@pytest.mark.smoke
def test_save_tasks_writes_valid_json(isolated_tasks_file, make_task):
    save_tasks([make_task(1, "a")])
    data = json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
    assert data[0]["description"] == "a"


@pytest.mark.boundary
def test_save_tasks_empty_list_writes_empty_json_array(isolated_tasks_file):
    save_tasks([])
    assert json.loads(isolated_tasks_file.read_text(encoding="utf-8")) == []


def test_save_tasks_creates_file_when_missing(isolated_tasks_file, make_task):
    assert not isolated_tasks_file.exists()
    save_tasks([make_task(1)])
    assert isolated_tasks_file.exists()


def test_save_tasks_overwrites_instead_of_appending(read_file, make_task):
    save_tasks([make_task(1), make_task(2)])
    save_tasks([make_task(3)])
    assert [t["id"] for t in read_file()] == [3]


def test_save_tasks_keeps_non_ascii_characters_readable(isolated_tasks_file, make_task):
    save_tasks([make_task(1, "ñandú خریداری")])
    raw = isolated_tasks_file.read_text(encoding="utf-8")
    assert "ñandú خریداری" in raw          # ensure_ascii=False
    assert "\\u" not in raw


def test_save_tasks_uses_two_space_indent(isolated_tasks_file, make_task):
    save_tasks([make_task(1)])
    raw = isolated_tasks_file.read_text(encoding="utf-8")
    assert '\n    "id": 1' in raw


@pytest.mark.boundary
def test_save_tasks_many_tasks_round_trip(make_task):
    tasks = [make_task(i, f"task {i}") for i in range(1, 201)]
    save_tasks(tasks)
    assert load_tasks() == tasks


def test_save_tasks_returns_none(make_task):
    assert save_tasks([make_task(1)]) is None


@pytest.mark.negative
def test_save_tasks_non_serializable_data_raises():
    with pytest.raises(TypeError):
        save_tasks([{"id": 1, "bad": {1, 2, 3}}])      # a set is not JSON serializable


# ---------------------------------------------------------------- module-level
def test_module_save_then_load_round_trip(make_task):
    tasks = [make_task(1, "a", "done"), make_task(2, "b")]
    save_tasks(tasks)
    assert load_tasks() == tasks


def test_module_ensure_does_not_erase_saved_tasks(make_task):
    save_tasks([make_task(1)])
    ensure_tasks_file_exists()
    assert len(load_tasks()) == 1
