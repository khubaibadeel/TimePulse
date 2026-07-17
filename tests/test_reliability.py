import copy
from datetime import datetime, timedelta

import pytest

import TimePulse


def test_normalize_rejects_non_list_alarms():
    with pytest.raises(ValueError):
        TimePulse._normalize_data({"password": None, "alarms": {}})


def test_normalize_repairs_duplicate_ids():
    future = (datetime.now() + timedelta(days=1)).replace(microsecond=0).isoformat()
    data = {
        "password": None,
        "alarms": [
            {"id": "same", "datetime": future, "time": "08:00"},
            {"id": "same", "datetime": future, "time": "09:00"},
        ],
    }
    normalized = TimePulse._normalize_data(copy.deepcopy(data))
    ids = [alarm["id"] for alarm in normalized["alarms"]]
    assert len(ids) == len(set(ids))


def test_normalize_rejects_invalid_datetime():
    with pytest.raises(ValueError):
        TimePulse._normalize_data({
            "password": None,
            "alarms": [{"id": "bad", "datetime": "not-a-date", "time": "08:00"}],
        })


def test_single_instance_is_noop_off_windows(monkeypatch):
    monkeypatch.setattr(TimePulse.os, "name", "posix")
    assert TimePulse.acquire_single_instance() is True
