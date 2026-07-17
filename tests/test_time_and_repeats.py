from datetime import datetime

import TimePulse


def test_to_24h_handles_noon_and_midnight():
    assert TimePulse.to_24h("12", "00", "AM") == (0, 0)
    assert TimePulse.to_24h("12", "00", "PM") == (12, 0)
    assert TimePulse.to_24h("01", "05", "PM") == (13, 5)


def test_to_12h_formats_afternoon_time():
    assert TimePulse.to_12h("23:05") == ("11", "05", "PM")
    assert TimePulse.to_12h("00:00") == ("12", "00", "AM")


def test_daily_repeat_returns_next_future_occurrence():
    alarm = {"datetime": "2026-07-17T10:00:00", "repeat": "daily"}
    now = datetime(2026, 7, 18, 9, 0)
    assert TimePulse.next_repeat_datetime(alarm, now) == datetime(2026, 7, 18, 10, 0)


def test_weekly_repeat_skips_elapsed_intervals():
    alarm = {"datetime": "2026-07-01T08:30:00", "repeat": "weekly"}
    now = datetime(2026, 7, 20, 9, 0)
    assert TimePulse.next_repeat_datetime(alarm, now) == datetime(2026, 7, 22, 8, 30)


def test_monthly_repeat_clamps_day_to_month_end():
    alarm = {
        "datetime": "2026-01-31T08:00:00",
        "repeat": "monthly",
        "repeat_day": 31,
    }
    now = datetime(2026, 2, 1, 9, 0)
    assert TimePulse.next_repeat_datetime(alarm, now) == datetime(2026, 2, 28, 8, 0)


def test_non_repeating_alarm_has_no_next_occurrence():
    alarm = {"datetime": "2026-07-17T10:00:00", "repeat": "none"}
    assert TimePulse.next_repeat_datetime(alarm, datetime(2026, 7, 17, 11, 0)) is None
