<div align="center">
  <img src="assets/TimePulse.png" alt="TimePulse icon" width="96" />

# TimePulse v1.0

A feature-rich Windows desktop alarm manager built with Python and CustomTkinter.

[![Tests](https://github.com/Khubaib295/TimePulse/actions/workflows/tests.yml/badge.svg)](https://github.com/Khubaib295/TimePulse/actions/workflows/tests.yml)
[![Build](https://github.com/Khubaib295/TimePulse/actions/workflows/build.yml/badge.svg)](https://github.com/Khubaib295/TimePulse/actions/workflows/build.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

## Overview

TimePulse provides a modern interface for creating, editing, organizing, and running alarms and quick timers on Windows. It supports per-alarm ringtones, repeat schedules, snoozing, history logging, optional password protection, system-tray operation, and optional automatic startup at sign-in.

## Features

- Create, edit, enable, disable, and delete alarms.
- One-time, daily, weekly, and monthly repeat schedules.
- Quick timers for short countdowns.
- Seven bundled WAV ringtones with per-alarm selection.
- Hover-to-preview ringtone selector with cancellation of overlapping previews.
- Three-minute snooze and automatic alarm-state handling.
- Live clock and next-alarm countdown.
- Alarm history with creation, editing, trigger, snooze, dismissal, and missed-alarm events.
- Optional PBKDF2-HMAC-SHA256 password protection for sensitive actions.
- Light and dark appearance modes.
- Minimize-to-tray support.
- Optional automatic launch through the current user's Windows Startup folder.
- Windows session-lock detection that immediately stops active audio.
- Atomic JSON persistence with backup and corruption-recovery behavior.
- Portable one-file executable packaging through PyInstaller.

## Technology

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Interface | CustomTkinter, Tkinter |
| Tray integration | pystray, Pillow |
| Storage | Local JSON files |
| Audio | Windows MCI through `ctypes`, with `winsound` fallback |
| Windows integration | WTS session notifications, Startup folder, Win32 APIs |
| Packaging | PyInstaller |
| Testing | pytest, GitHub Actions |

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer; Python 3.12 is recommended
- A writable per-user profile directory (`%LOCALAPPDATA%`)

## Run from source

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python TimePulse.py
```

You can also run `setup_development.bat`, followed by `RUN_TIMEPULSE.bat`.

## Publish this repository

Create an empty public GitHub repository named `TimePulse` under `Khubaib295`. Do not initialize it with GitHub's README, license, or `.gitignore`. Then run:

```cmd
PUSH_TO_GITHUB.bat
```

The script initializes Git when necessary, creates the first commit, configures the correct repository URL, and pushes the `main` branch.

## Build the executable

```cmd
python -m pip install -r requirements-dev.txt
pyinstaller --clean TimePulse.spec
```

The resulting executable will be created at:

```text
dist\TimePulse.exe
```

The PyInstaller specification bundles the application icon, CustomTkinter assets, and all WAV files in `ringtones/`.

## Data files

TimePulse stores writable runtime data under `%LOCALAPPDATA%\TimePulse` on Windows:

```text
%LOCALAPPDATA%\TimePulse\alarms.json
%LOCALAPPDATA%\TimePulse\alarms.json.bak
%LOCALAPPDATA%\TimePulse\Alarm History\alarm_history.txt
%LOCALAPPDATA%\TimePulse\TimePulse.log
```

These files are excluded from Git because they can contain personal schedules, labels, and password hashes. Password protection restricts actions inside the application; it does **not** encrypt the JSON file.

## Ringtones

Bundled ringtones are stored in `ringtones/`. The application accepts plain `.wav` filenames only and rejects absolute paths or directory traversal. A user can place an external `ringtones` directory beside `TimePulse.exe`; external files are preferred over bundled copies.

The default ringtone is `Soft_Arrival.wav`.

## Testing

```cmd
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Automated tests cover password hashing, time conversion, repeat scheduling, ringtone filename validation, JSON persistence and recovery, and source syntax. GUI interaction, audio playback, Windows locking, and packaged executable behavior require manual Windows testing. See [docs/TESTING.md](docs/TESTING.md).

## Important behavior

Dismissing an alarm locks the Windows workstation. If no action is taken, TimePulse attempts the lock automatically after 30 seconds. Snoozing postpones the alarm by three minutes without locking the workstation.

TimePulse does not wake a sleeping computer. A one-time alarm that is already stale when the application next starts is marked as missed.

## Project structure

```text
TimePulse/
├── TimePulse.py
├── TimePulse.spec
├── version_info.txt
├── assets/
├── docs/
├── ringtones/
├── tests/
├── requirements.txt
└── requirements-dev.txt
```

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Developed by [Khubaib295](https://github.com/Khubaib295).
