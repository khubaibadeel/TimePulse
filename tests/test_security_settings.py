import json
import threading

import TimePulse


class SwitchVar:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


def configure_temp_storage(monkeypatch, tmp_path):
    monkeypatch.setattr(TimePulse, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(TimePulse, "DATA_FILE", str(tmp_path / "alarms.json"))


def make_app(data, switch_var):
    app = object.__new__(TimePulse.AlarmApp)
    app.data = data
    app.data_lock = threading.RLock()
    app.snooze_var = switch_var
    app.protect_edit_delete_var = switch_var
    return app


def test_missing_protect_edit_delete_defaults_to_true(monkeypatch, tmp_path):
    configure_temp_storage(monkeypatch, tmp_path)
    (tmp_path / "alarms.json").write_text(
        json.dumps({"password": None, "alarms": []}), encoding="utf-8"
    )

    assert TimePulse.load_data()["protect_edit_delete"] is True


def test_protect_edit_delete_persists_both_values(monkeypatch, tmp_path):
    configure_temp_storage(monkeypatch, tmp_path)
    for value in (False, True):
        assert TimePulse.save_data(
            {"password": None, "allow_snooze": True,
             "protect_edit_delete": value, "alarms": []}
        )
        assert TimePulse.load_data()["protect_edit_delete"] is value


def test_protect_edit_delete_normalization_preserves_unknown_keys():
    data = TimePulse._normalize_data(
        {"password": None, "allow_snooze": True, "alarms": [],
         "future_setting": {"keep": True}}
    )

    assert data["protect_edit_delete"] is True
    assert data["future_setting"] == {"keep": True}


def test_alarm_change_auth_policy():
    assert TimePulse.requires_alarm_change_auth(True) is True
    assert TimePulse.requires_alarm_change_auth(False) is False


def test_edit_and_delete_route_through_auth_when_protected():
    app = make_app({"protect_edit_delete": True}, SwitchVar(False))
    auth_calls = []
    actions = []

    def auth_then(callback, *args, **kwargs):
        auth_calls.append((callback, args, kwargs))
        callback(*args)

    app._auth_then = auth_then
    app._edit_alarm = lambda alarm_id: actions.append(("edit", alarm_id))
    app._delete_alarm = lambda alarm_id: actions.append(("delete", alarm_id))

    TimePulse.AlarmApp._edit_with_auth(app, "alarm-1")
    TimePulse.AlarmApp._delete_with_auth(app, "alarm-1")

    assert len(auth_calls) == 2
    assert actions == [("edit", "alarm-1"), ("delete", "alarm-1")]


def test_edit_and_delete_bypass_auth_when_unprotected():
    app = make_app({"protect_edit_delete": False}, SwitchVar(False))
    actions = []
    app._auth_then = lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError())
    app._edit_alarm = lambda alarm_id: actions.append(("edit", alarm_id))
    app._delete_alarm = lambda alarm_id: actions.append(("delete", alarm_id))

    TimePulse.AlarmApp._edit_with_auth(app, "alarm-1")
    TimePulse.AlarmApp._delete_with_auth(app, "alarm-1")

    assert actions == [("edit", "alarm-1"), ("delete", "alarm-1")]


def test_snooze_change_requires_auth_and_cancel_restores_switch():
    switch = SwitchVar(True)
    app = make_app({"password": "configured", "allow_snooze": False}, switch)
    calls = []
    app._auth_then = lambda callback, *args, **kwargs: calls.append((callback, args, kwargs))

    TimePulse.AlarmApp._toggle_snooze_setting(app)

    assert len(calls) == 1
    assert app.data["allow_snooze"] is False
    calls[0][2]["on_cancel"]()
    assert switch.get() is False
    assert app.data["allow_snooze"] is False


def test_protection_toggle_requires_auth_and_success_persists(monkeypatch):
    switch = SwitchVar(False)
    app = make_app({"password": "configured", "protect_edit_delete": True}, switch)
    saved = []

    monkeypatch.setattr(TimePulse, "save_data", lambda data: saved.append(dict(data)) or True)
    app._auth_then = lambda callback, *args, **kwargs: callback(*args)

    TimePulse.AlarmApp._toggle_protect_edit_delete_setting(app)

    assert app.data["protect_edit_delete"] is False
    assert saved[-1]["protect_edit_delete"] is False


def test_protection_toggle_cancel_and_save_failure_restore_state(monkeypatch):
    switch = SwitchVar(False)
    app = make_app({"password": "configured", "protect_edit_delete": True}, switch)
    calls = []
    app._auth_then = lambda callback, *args, **kwargs: calls.append((callback, args, kwargs))

    TimePulse.AlarmApp._toggle_protect_edit_delete_setting(app)
    calls[0][2]["on_cancel"]()
    assert switch.get() is True
    assert app.data["protect_edit_delete"] is True

    monkeypatch.setattr(TimePulse, "save_data", lambda data: False)
    monkeypatch.setattr(TimePulse.messagebox, "showerror", lambda *args, **kwargs: None)
    calls[0][0](*calls[0][1])
    assert switch.get() is True
    assert app.data["protect_edit_delete"] is True

def test_snooze_save_failure_restores_state(monkeypatch):
    switch = SwitchVar(True)
    app = make_app({"password": "configured", "allow_snooze": False}, switch)
    monkeypatch.setattr(TimePulse, "save_data", lambda data: False)
    monkeypatch.setattr(TimePulse.messagebox, "showerror", lambda *args, **kwargs: None)
    app._auth_then = lambda callback, *args, **kwargs: callback(*args)

    TimePulse.AlarmApp._toggle_snooze_setting(app)

    assert switch.get() is False
    assert app.data["allow_snooze"] is False