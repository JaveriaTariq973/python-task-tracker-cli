"""Shared fixtures for all unit tests.

Har test ek temporary tasks.json use karta hai, is liye asli tasks.json
kabhi touch nahi hoti aur tests parallel (pytest -n) mein bhi safe hain.
"""
import json

import pytest

from app import storage, task_services

FIXED_TIME = "2026-02-02T10:00:00"
OLD_TIME = "2026-01-01T00:00:00"


@pytest.fixture(autouse=True)
def isolated_tasks_file(tmp_path, monkeypatch):
    """Point storage.TASKS_FILE to a fresh temp file for every test."""
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "TASKS_FILE", path)
    return path


@pytest.fixture
def seed(isolated_tasks_file):
    """seed([...tasks...]) writes tasks straight into the temp tasks.json."""
    def _seed(tasks):
        isolated_tasks_file.write_text(json.dumps(tasks), encoding="utf-8")
    return _seed


@pytest.fixture
def read_file(isolated_tasks_file):
    """read_file() returns the parsed content of the temp tasks.json."""
    def _read():
        return json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
    return _read


@pytest.fixture
def make_task():
    """make_task(id, description, status) builds a task dict."""
    def _make(task_id=1, description="task", status="todo"):
        return {
            "id": task_id,
            "description": description,
            "status": status,
            "createdAt": OLD_TIME,
            "updatedAt": OLD_TIME,
        }
    return _make


@pytest.fixture
def fixed_time(monkeypatch):
    """Make task_services use a predictable timestamp."""
    monkeypatch.setattr(task_services, "get_current_timestamp", lambda: FIXED_TIME)
    return FIXED_TIME
