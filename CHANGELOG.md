# Changelog

## v1.0 - Reliability and GitHub readiness

- Enforced single-instance execution on Windows.
- Moved persistent data to the per-user Local AppData directory.
- Added rotating backups, file logging, structural data validation, and visible recovery warnings.
- Added rollback behavior for failed saves.
- Made automatic startup optional and user-controlled.
- Processed simultaneously due alarms independently.
- Persisted dismissal transitions safely around workstation locking.
- Removed forceful normal-process termination.
- Added security policy, contribution guide, issue template, pull-request template, and Dependabot configuration.


All notable changes to TimePulse are documented here.

## v1.0 - 2026-07-17

### Added

- Alarm creation, editing, enabling, disabling, and deletion.
- One-time, daily, weekly, and monthly schedules.
- Quick timers, snoozing, history, tray operation, and theme switching.
- Per-alarm ringtone selection and seven bundled WAV ringtones.
- Optional salted PBKDF2 password protection.
- Windows session-lock audio cancellation and workstation-lock workflow.
- Portable PyInstaller build configuration.
- Automated utility tests and GitHub Actions workflows.
