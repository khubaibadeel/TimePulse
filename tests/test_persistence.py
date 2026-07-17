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
    assert TimePulse.load_data() == data


def test_corrupt_data_is_backed_up(monkeypatch, tmp_path):
    data_file = configure_temp_storage(monkeypatch, tmp_path)
    data_file.write_text("{not valid json", encoding="utf-8")

    assert TimePulse.load_data() == {"password": None, "alarms": []}
    backups = list(tmp_path.glob("alarms.json.*.bak"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "{not valid json"
