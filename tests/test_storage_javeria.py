"""Javeria (24F-3036) - unit tests for app/storage.py
Functions: ensure_tasks_file_exists, load_tasks
"""
import pytest

from app import storage
from app.storage import ensure_tasks_file_exists, load_tasks

pytestmark = pytest.mark.storage


# ---------------------------------------------------------------- ensure_tasks_file_exists
@pytest.mark.smoke
def test_ensure_creates_file_when_missing(isolated_tasks_file):
    assert not isolated_tasks_file.exists()
    ensure_tasks_file_exists()
    assert isolated_tasks_file.exists()


def test_ensure_new_file_contains_empty_list(isolated_tasks_file):
    ensure_tasks_file_exists()
    assert isolated_tasks_file.read_text(encoding="utf-8") == "[]"


def test_ensure_does_not_overwrite_existing_file(isolated_tasks_file):
    isolated_tasks_file.write_text('[{"id": 1}]', encoding="utf-8")
    ensure_tasks_file_exists()
    assert isolated_tasks_file.read_text(encoding="utf-8") == '[{"id": 1}]'


def test_ensure_is_idempotent(isolated_tasks_file):
    ensure_tasks_file_exists()
    ensure_tasks_file_exists()
    assert isolated_tasks_file.read_text(encoding="utf-8") == "[]"


@pytest.mark.boundary
def test_ensure_keeps_existing_empty_file_empty(isolated_tasks_file):
    isolated_tasks_file.write_text("", encoding="utf-8")
    ensure_tasks_file_exists()
    assert isolated_tasks_file.read_text(encoding="utf-8") == ""


def test_ensure_returns_none():
    assert ensure_tasks_file_exists() is None


# ---------------------------------------------------------------- load_tasks
@pytest.mark.smoke
def test_load_tasks_missing_file_returns_empty_and_creates_file(isolated_tasks_file):
    assert load_tasks() == []
    assert isolated_tasks_file.exists()


@pytest.mark.boundary
def test_load_tasks_empty_file_returns_empty_list(isolated_tasks_file):
    isolated_tasks_file.write_text("", encoding="utf-8")
    assert load_tasks() == []


@pytest.mark.boundary
@pytest.mark.parametrize("blank", ["   ", "\n", "\n\n  \t "])
def test_load_tasks_whitespace_only_returns_empty_list(isolated_tasks_file, blank):
    isolated_tasks_file.write_text(blank, encoding="utf-8")
    assert load_tasks() == []


def test_load_tasks_valid_json_returns_tasks(seed, make_task):
    seed([make_task(1, "a"), make_task(2, "b")])
    tasks = load_tasks()
    assert [t["id"] for t in tasks] == [1, 2]


def test_load_tasks_unicode_content(isolated_tasks_file):
    isolated_tasks_file.write_text('[{"id": 1, "description": "ñandú خریداری"}]', encoding="utf-8")
    assert load_tasks()[0]["description"] == "ñandú خریداری"


@pytest.mark.negative
@pytest.mark.parametrize("bad", ["{not json", "[1, 2,", "hello", '[{"id": 1}'])
def test_load_tasks_corrupted_json_raises_value_error(isolated_tasks_file, bad):
    isolated_tasks_file.write_text(bad, encoding="utf-8")
    with pytest.raises(ValueError, match="tasks.json"):
        load_tasks()


def test_load_tasks_valid_json_that_is_not_a_list_is_returned_as_is(isolated_tasks_file):
    # Finding: there is no schema validation, a JSON object is returned unchanged.
    isolated_tasks_file.write_text("{}", encoding="utf-8")
    assert load_tasks() == {}


# ---------------------------------------------------------------- module-level
def test_module_ensure_then_load_gives_empty_list():
    ensure_tasks_file_exists()
    assert load_tasks() == []


def test_module_load_uses_patched_tasks_file_path(isolated_tasks_file):
    assert storage.TASKS_FILE == isolated_tasks_file
    load_tasks()
    assert isolated_tasks_file.exists()
