"""Manal (24F-3041) - unit tests for app/utils.py
Function: get_current_timestamp
"""
import re
from datetime import datetime

import pytest

from app import utils
from app.utils import get_current_timestamp

pytestmark = pytest.mark.utils

ISO_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")


@pytest.mark.smoke
def test_timestamp_returns_string():
    assert isinstance(get_current_timestamp(), str)


def test_timestamp_matches_iso_format_without_microseconds():
    assert ISO_PATTERN.match(get_current_timestamp())


def test_timestamp_has_fixed_length_19():
    assert len(get_current_timestamp()) == 19


def test_timestamp_can_be_parsed_back():
    assert isinstance(datetime.fromisoformat(get_current_timestamp()), datetime)


@pytest.mark.boundary
@pytest.mark.parametrize(
    "fake_now, expected",
    [
        (datetime(2026, 10, 21, 9, 5, 3, 999999), "2026-10-21T09:05:03"),   # micros dropped
        (datetime(2026, 1, 1, 0, 0, 0), "2026-01-01T00:00:00"),            # start of year
        (datetime(2026, 12, 31, 23, 59, 59), "2026-12-31T23:59:59"),       # end of year
        (datetime(2024, 2, 29, 12, 0, 0), "2024-02-29T12:00:00"),          # leap day
    ],
)
def test_timestamp_with_controlled_clock(monkeypatch, fake_now, expected):
    class FakeDatetime:
        @classmethod
        def now(cls):
            return fake_now

    monkeypatch.setattr(utils, "datetime", FakeDatetime)
    assert get_current_timestamp() == expected
