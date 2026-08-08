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

def test_hardened_single_instance_api_is_exposed():
    assert callable(TimePulse.acquire_single_instance_mutex)
    assert callable(TimePulse.release_single_instance_mutex)

def test_popup_actions_include_snooze_when_enabled():
    assert TimePulse.get_alarm_popup_actions(True) == ("Snooze (3m)", "Lock Now")


def test_popup_actions_omit_snooze_when_disabled():
    assert TimePulse.get_alarm_popup_actions(False) == ("Lock Now",)
