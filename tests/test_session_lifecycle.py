from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import TimePulse


def test_session_lock_only_stops_transient_audio():
    audio = SimpleNamespace(stop_all=Mock())
    tray = SimpleNamespace(stop=Mock())
    app = SimpleNamespace(
        _shutting_down=False,
        audio_manager=audio,
        tray=tray,
        _shutdown_cleanup=Mock(),
    )

    TimePulse.AlarmApp._on_session_lock(app)

    audio.stop_all.assert_called_once_with()
    tray.stop.assert_not_called()
    app._shutdown_cleanup.assert_not_called()


def test_session_unlock_repairs_only_non_native_services():
    app = SimpleNamespace(
        _shutting_down=False,
        _session_notifications_registered=True,
        _ensure_alarm_checker_running=Mock(),
        _setup_session_notifications=Mock(),
        _ensure_tray_available=Mock(),
        tray=SimpleNamespace(stop=Mock(), run=Mock()),
        _shutdown_cleanup=Mock(),
    )

    TimePulse.AlarmApp._on_session_unlock(app)

    app._ensure_alarm_checker_running.assert_called_once_with()
    app._setup_session_notifications.assert_not_called()
    app._ensure_tray_available.assert_not_called()
    app.tray.stop.assert_not_called()
    app.tray.run.assert_not_called()
    app._shutdown_cleanup.assert_not_called()


def test_session_unlock_reregisters_missing_hook_without_touching_tray():
    app = SimpleNamespace(
        _shutting_down=False,
        _session_notifications_registered=False,
        _ensure_alarm_checker_running=Mock(),
        _setup_session_notifications=Mock(),
        _setup_tray=Mock(),
    )

    TimePulse.AlarmApp._on_session_unlock(app)

    app._ensure_alarm_checker_running.assert_called_once_with()
    app._setup_session_notifications.assert_called_once_with()
    app._setup_tray.assert_not_called()


def test_unlock_does_not_duplicate_an_existing_alarm_checker_timer():
    app = SimpleNamespace(
        _shutting_down=False,
        _alarm_check_after_id="after#1",
        _alarm_check_running=True,
        _schedule_alarm_check=Mock(),
        _start_alarm_checker=Mock(),
    )

    assert TimePulse.AlarmApp._ensure_alarm_checker_running(app) is True
    app._schedule_alarm_check.assert_not_called()
    app._start_alarm_checker.assert_not_called()


def test_unlock_restarts_a_stale_running_alarm_checker():
    app = SimpleNamespace(
        _shutting_down=False,
        _alarm_check_after_id=None,
        _alarm_check_running=True,
        _start_alarm_checker=Mock(),
    )
    app._schedule_alarm_check = Mock(
        side_effect=lambda: setattr(app, "_alarm_check_after_id", "after#2")
    )

    assert TimePulse.AlarmApp._ensure_alarm_checker_running(app) is True
    app._schedule_alarm_check.assert_called_once_with()
    app._start_alarm_checker.assert_not_called()


def test_explicit_exit_stops_the_tray_before_destroying_root():
    app = SimpleNamespace(
        _shutting_down=False,
        _shutdown_cleanup=Mock(),
        _stop_tray_for_shutdown=Mock(),
        destroy=Mock(),
    )

    TimePulse.AlarmApp._quit_app_main_thread(app)

    app._shutdown_cleanup.assert_called_once_with()
    app._stop_tray_for_shutdown.assert_called_once_with()
    app.destroy.assert_called_once_with()


def test_tray_shutdown_stops_the_single_tray_loop():
    tray = SimpleNamespace(stop=Mock())
    app = SimpleNamespace(tray=tray, _tray_thread=None, _tray_ready=True)

    TimePulse.AlarmApp._stop_tray_for_shutdown(app)

    tray.stop.assert_called_once_with()
    assert app.tray is None
    assert app._tray_ready is False


def test_only_initial_setup_contains_a_tray_run_path():
    source = (Path(__file__).resolve().parents[1] / "TimePulse.py").read_text(encoding="utf-8")

    assert source.count("tray.run(setup=tray_setup)") == 1
    assert "_ensure_tray_available" not in source