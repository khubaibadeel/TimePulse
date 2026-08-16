import json
from pathlib import Path

import TimePulse


def configure_temp_storage(monkeypatch, tmp_path: Path):
    data_file = tmp_path / "alarms.json"
    history_dir = tmp_path / "TimePulse History"
    monkeypatch.setattr(TimePulse, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(TimePulse, "DATA_FILE", str(data_file))
    monkeypatch.setattr(TimePulse, "HISTORY_DIR", str(history_dir))
    monkeypatch.setattr(TimePulse, "HISTORY_FILE", str(history_dir / "alarm_history.txt"))
    return data_file


def test_save_and_load_round_trip(monkeypatch, tmp_path):
    data_file = configure_temp_storage(monkeypatch, tmp_path)
    data = {
        "password": None,
        "allow_snooze": True,
        "alarms": [
            {
                "id": "test-alarm",
                "label": "Future alarm",
                "datetime": "2999-01-01T08:00:00",
                "time": "08:00",
                "repeat": "none",
                "enabled": True,
            }
        ],
    }

    assert TimePulse.save_data(data)
    assert data_file.exists()
    assert TimePulse.load_data() == {**data, "protect_edit_delete": True}



def test_missing_snooze_setting_defaults_to_true(monkeypatch, tmp_path):
    data_file = configure_temp_storage(monkeypatch, tmp_path)
    data_file.write_text(
        json.dumps({"password": None, "alarms": []}),
        encoding="utf-8",
    )

    loaded = TimePulse.load_data()

    assert loaded["allow_snooze"] is True
    assert loaded["password"] is None
    assert loaded["alarms"] == []


def test_load_returns_normalized_data_when_migration_save_fails(monkeypatch, tmp_path):
    data_file = configure_temp_storage(monkeypatch, tmp_path)
    data_file.write_text(
        json.dumps(
            {
                "password": "existing-password",
                "alarms": [
                    {
                        "id": "test-alarm",
                        "datetime": "2999-01-01T08:00:00",
                        "time": "08:00",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(TimePulse, "save_data", lambda data: False)

    loaded = TimePulse.load_data()

    assert loaded["password"] == "existing-password"
    assert loaded["allow_snooze"] is True
    assert loaded["alarms"][0]["id"] == "test-alarm"


def test_normalize_preserves_unknown_top_level_fields():
    normalized = TimePulse._normalize_data(
        {
            "password": None,
            "alarms": [],
            "allow_snooze": True,
            "future_setting": "keep-me",
        }
    )

    assert normalized["future_setting"] == "keep-me"


def test_snooze_setting_persists_false(monkeypatch, tmp_path):
    configure_temp_storage(monkeypatch, tmp_path)
    data = {"password": None, "allow_snooze": False, "alarms": []}

    assert TimePulse.save_data(data)
    assert TimePulse.load_data()["allow_snooze"] is False


def test_snooze_setting_persists_true(monkeypatch, tmp_path):
    configure_temp_storage(monkeypatch, tmp_path)
    data = {"password": None, "allow_snooze": True, "alarms": []}

    assert TimePulse.save_data(data)
    assert TimePulse.load_data()["allow_snooze"] is True
def test_corrupt_data_is_backed_up(monkeypatch, tmp_path):
    data_file = configure_temp_storage(monkeypatch, tmp_path)
    data_file.write_text("{not valid json", encoding="utf-8")

    assert TimePulse.load_data() == {
        "password": None,
        "allow_snooze": True,
        "protect_edit_delete": True,
        "alarms": [],
    }
    backups = list(tmp_path.glob("alarms.json.*.bak"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "{not valid json"
